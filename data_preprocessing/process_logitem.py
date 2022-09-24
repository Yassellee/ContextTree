import codecs, re, ast, pickle, pandas

absolute_directory_path = "C:\\Users\\29908\\Desktop\\ContextTree\\data_preprocessing\\"


file_path = "logitems0919.txt"


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


def main():
    pd_dataframe = None
    list_task = None
    with open(absolute_directory_path+"location_name_dict.pkl", 'rb') as f1:
        global location_name_dict
        location_name_dict = pickle.load(f1)
    with open(absolute_directory_path+"SSID_table.pkl", 'rb') as f2:
        global SSID_table
        SSID_table = pickle.load(f2)

    with codecs.open(filename=absolute_directory_path+file_path, mode='r', encoding="UTF-8") as file:
        lines = file.readlines()
        list_information = build_info("package", lines)
        pd_dataframe, list_task = digest_list_information(list_information)

    with open(absolute_directory_path+"SSID_table.pkl", 'wb') as f3:
        pickle.dump(SSID_table, f3)

    return pd_dataframe, list_task

if __name__ == "__main__":
    main()