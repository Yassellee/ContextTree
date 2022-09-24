import codecs, re, ast, pickle, pandas, numpy
from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, _tree
from matplotlib import pyplot as plt
from sklearn import tree

file_path = "logitems0919.txt"
package_to_explore = "com.tencent.mm"

def digest_time(time):
    if time == ' ':
        return 0, 0, 0, 0
    time_info = re.split("-|/|:", time)
    year = (int)(time_info[0])
    month = (int)(time_info[1])
    day = (int)(time_info[2])
    exact_time = (int)(time_info[3])*3600+300*((int)(time_info[4])/5)
    return year, month, day, exact_time    


def digest_location(location):
    if location == ' ':
        return 0, 0, 0, 0
    location_info = re.split("==", location)
    latitude = round((float)(location_info[1]), 3)
    longitude = round((float)(location_info[2]), 3)
    altitude = round((float)(location_info[3]), 3)
    tag = ast.literal_eval(location_info[6])[0].get("tags").replace(';', '_')
    tag = location_name_dict.get(tag)

    return latitude, longitude, altitude, tag


def digest_network(network):
    if network == ' ':
        return 0, 0, 0
    network = ast.literal_eval(network)
    SSID_number = network["SSID"]
    LinkSpeed = network["LinkSpeed"]
    signal = network["signal"]

    if SSID_table.get(SSID_number) is None:
        SSID_table[SSID_number] = len(SSID_table)+1
    else:
        SSID_number = SSID_table[SSID_number]

    return SSID_number, LinkSpeed, signal


def digest_bluetooth(bluetooth):
    if bluetooth == ' ':
        return 0
    return ast.literal_eval(bluetooth).get("bluetooth_state:")


def digest_list_information(list_information):
    list_task = []
    year = [] 
    month = []
    day = []
    exact_time = []
    latitude = [] 
    longitude = [] 
    altitude = []
    location_tag = []
    SSID_number = []
    LinkSpeed = [] 
    signal = [] 
    bluetooth_state = []
    for line_dict in list_information:
        list_task.append(line_dict["task"])
        cur_year, cur_month, cur_day, cur_exact_time = digest_time(time=line_dict["time"])
        cur_latitude, cur_longitude, cur_altitude, cur_location_tag = digest_location(location=line_dict["location"])
        cur_SSID_number, cur_LinkSpeed, cur_signal = digest_network(network=line_dict["network"])
        cur_bluetooth_state = digest_bluetooth(bluetooth=line_dict["bluetooth"])
        year.append(cur_year)
        month.append(cur_month)
        day.append(cur_day)
        exact_time.append(cur_exact_time)
        latitude.append(cur_latitude)
        longitude.append(cur_longitude)
        altitude.append(cur_altitude)
        location_tag.append(cur_location_tag)
        SSID_number.append(cur_SSID_number)
        LinkSpeed.append(cur_LinkSpeed)
        signal.append(cur_signal)
        bluetooth_state.append(cur_bluetooth_state)

    ans_dict = {}
    ans_dict["year"] = year
    ans_dict["month"] = month
    ans_dict["day"] = day
    ans_dict["exact_time"] = exact_time
    ans_dict["latitude"] = latitude
    ans_dict["longitude"] = longitude
    ans_dict["altitude"] = altitude
    ans_dict["location_tag"] = location_tag
    ans_dict["SSID_number"] = SSID_number
    ans_dict["LinkSpeed"] = LinkSpeed
    ans_dict["signal"] = signal
    ans_dict["bluetooth_state"] = bluetooth_state

    return pandas.DataFrame(data=ans_dict), list_task


def build_info(types, lines):
    list_information = []
    for line in lines:
        information = re.split('##|@@', line)
        line_dict = {}
        if types == information[1]:
            line_dict["task"] = information[0]
            line_dict["types"] = information[1]
            line_dict["time"] = information[2]
            line_dict["location"] = information[3]
            line_dict["network"] = information[4]
            line_dict["bluetooth"] = information[5]
            list_information.append(line_dict)
    return list_information


def build_data():
    pd_dataframe = None
    list_task = None
    with open("location_name_dict.pkl", 'rb') as f1:
        global location_name_dict
        location_name_dict = pickle.load(f1)
    with open("SSID_table.pkl", 'rb') as f2:
        global SSID_table
        SSID_table = pickle.load(f2)

    with codecs.open(filename=file_path, mode='r', encoding="UTF-8") as file:
        lines = file.readlines()
        list_information = build_info("package", lines)
        pd_dataframe, list_task = digest_list_information(list_information)

    with open("SSID_table.pkl", 'wb') as f3:
        pickle.dump(SSID_table, f3)

    return pd_dataframe, list_task

def Boruta_strategy(processed_data, list_task):
    data = processed_data.values
    original_feature_names = processed_data.columns.values
    labels = []
    for task in list_task:
        if task == package_to_explore:
            labels.append(1)
        else:
            labels.append(0)

    forest = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5)
    forest.fit(data, labels)
    feature_selector = BorutaPy(forest, n_estimators='auto', verbose=2, random_state=1)
    feature_selector.fit(data, labels)
    processed_data = feature_selector.transform(data)

    new_feature_names = []
    for i in range(len(list(original_feature_names))):
        if feature_selector.support_[i] == True:
            new_feature_names.append(list(original_feature_names)[i])

    return processed_data, new_feature_names, labels


def build_feature(processed_data, list_task):
    return Boruta_strategy(processed_data, list_task)

def build_tree(processed_data, new_feature_names, labels):
    decision_tree = DecisionTreeClassifier()
    decision_tree.fit(processed_data, labels)

    fig = plt.figure(figsize=(25,20))
    _ = tree.plot_tree(decision_tree, 
                feature_names=new_feature_names,  
                class_names=[package_to_explore, "NOT_"+package_to_explore],
                filled=True)
    fig.savefig("tree.png")

    return decision_tree


def build_rules(tree, feature_names): 
    class_names = [0, 1]
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    paths = []
    path = []

    def recurse(node, path, paths):
        
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            p1, p2 = list(path), list(path)
            p1 += [f"({name} <= {numpy.round(threshold, 3)})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} > {numpy.round(threshold, 3)})"]
            recurse(tree_.children_right[node], p2, paths)
        else:
            path += [(tree_.value[node], tree_.n_node_samples[node])]
            paths += [path]
            
    recurse(0, path, paths)

    # sort by samples count
    samples_count = [p[-1][1] for p in paths]
    ii = list(numpy.argsort(samples_count))
    paths = [paths[i] for i in reversed(ii)]

    rules = []
    for path in paths:
        rule = "if "
        
        for p in path[:-1]:
            if rule != "if ":
                rule += " and "
            rule += str(p)
        rule += " then "
        if class_names is None:
            rule += "response: "+str(numpy.round(path[-1][0][0][0],3))
        else:
            classes = path[-1][0][0]
            l = numpy.argmax(classes)
            rule += f"class: {class_names[l]} (proba: {numpy.round(100.0*classes[l]/numpy.sum(classes),2)}%)"
        rule += f" | based on {path[-1][1]:,} samples"
        rules += [rule]
        
    return rules


def main():
    pd_dataframe, list_task = build_data()

    processed_data, new_feature_names, labels = build_feature(pd_dataframe, list_task)

    tree = build_tree(processed_data, new_feature_names, labels)

    rules = build_rules(tree, new_feature_names)

    with codecs.open(filename="rules.txt", mode='w', encoding='UTF-8') as rule_file:
        for r in rules:
            rule_file.writelines(r)
            rule_file.writelines('\r\n')
            rule_file.writelines('\r\n')



if __name__ == '__main__':
    main()