import re, ast, pickle, pandas, codecs, os
from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

file_path = "logItems.txt"
package_to_explore = "com.tencent.mm-package"
previous_latitude, previous_longitude, previous_altitude, previous_location_tag = 0, 0, 0, 0 
previous_address, previous_location = 0, 0
previous_SSID_number, previous_LinkSpeed, previous_signal, previous_network = 0, 0, 0, 0
previous_bluetooth_state, previous_bluetooth_count = 0, 0
previous_weather, previous_temperature = 0, 0
stored_service = []


def build_info(lines):
    list_information = []
    for line in lines:
        information = re.split('##|@@', line)
        line_dict = {}
        service_name = information[0]+'-'+information[1]
        if service_name in stored_service:
            line_dict["task"] = service_name
            line_dict["time"] = information[2]
            line_dict["location"] = information[3]
            line_dict["network"] = information[4]
            line_dict["bluetooth"] = information[5]
            line_dict["activities"] = information[6]
            line_dict["weather"] = information[7]
            list_information.append(line_dict)
    return list_information


def digest_time(time):
    if time == ' ':
        return 0, 0, 0, 0, 0, 0, 0
    time_info = re.split("-|/|:", time)
    year = (int)(time_info[0])
    month = (int)(time_info[1])
    day = (int)(time_info[2])
    exact_time = (int)(time_info[3])*3600+300*((int)(time_info[4])/5)
    am_pm = any
    if((int)(time_info[3]) > 12):
        am_pm = 1
    else:
        am_pm = 0
        
    week_day = datetime.date(datetime(year, month, day)).weekday()
    hour = (int)(time_info[3])
    return year, month, day, exact_time, am_pm, hour, week_day


def digest_location(raw_location):
    global previous_latitude, previous_longitude, previous_altitude, previous_location_tag, previous_address, previous_location
    diff_latitude, diff_longitude, diff_altitude, diff_tag, diff_location, diff_address = 0, 0, 0, 0, 0, 0
    if raw_location == ' ':
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    location_info = re.split("==", raw_location)
    latitude = round((float)(location_info[1]), 3)
    if previous_latitude != latitude:
        diff_latitude = 1
        previous_latitude = latitude
    longitude = round((float)(location_info[2]), 3)
    if previous_longitude != longitude:
        diff_longitude = 1
        previous_longitude = longitude
    altitude = round((float)(location_info[3]), 3)
    if previous_altitude != altitude:
        diff_altitude = 1
        previous_altitude = altitude
    location = location_info[4]
    if previous_location != location:
        diff_location = 1
        previous_location = location
    if location_table.get(location) is None:
        location_table[location] = len(location_table)+1
        location = location_table[location]
    else:
        location = location_table[location]
    address = location_info[5]
    if previous_address != address:
        diff_address = 1
        previous_address = address
    if address_table.get(address) is None:
        address_table[address] = len(address_table)+1
        address = address_table[address]
    else:
        address = address_table[address]
        
    tag = ast.literal_eval(location_info[6])[0].get("tags").replace(';', '_')
    tag = location_name_dict.get(tag)
    if previous_location_tag != tag:
        diff_tag = 1
        previous_location_tag = tag

    return latitude, diff_latitude, longitude, diff_longitude, altitude, diff_altitude, tag, diff_tag, location, diff_location, address, diff_address


def digest_network(network):
    global previous_SSID_number, previous_LinkSpeed, previous_signal, previous_network
    diff_SSID_number, diff_LinkSpeed, diff_signal, diff_network = 0, 0, 0, 0
    if network == ' ':
        return 0, 0, 0, 0, 0, 0, 0, 0
    network = ast.literal_eval(network)
    network_status = any
    if network == {}:
        network_status = 0
        if previous_network != 0:
            diff_network = 1
            previous_network = 0
        else:
            diff_network = 0
            previous_network = 0
        return 0, 0, 0, 0, 0, 0, network_status, diff_network
    else:
        network_status = 1
        if previous_network != 1:
            diff_network = 1
            previous_network = 1
        else:
            diff_network = 0
            previous_network = 1
    SSID_number = network["SSID"]
    LinkSpeed = network["LinkSpeed"]
    signal = network["signal"]

    if SSID_table.get(SSID_number) is None:
        SSID_table[SSID_number] = len(SSID_table)+1
        SSID_number = SSID_table[SSID_number]
    else:
        SSID_number = SSID_table[SSID_number]
    
    if previous_SSID_number != SSID_number:
        diff_SSID_number = 1
        previous_SSID_number = SSID_number
    if previous_LinkSpeed != LinkSpeed:
        diff_LinkSpeed = 1
        previous_LinkSpeed = LinkSpeed
    if previous_signal != signal:
        diff_signal = 1
        previous_signal = signal

    return SSID_number, diff_SSID_number, LinkSpeed, diff_LinkSpeed, signal, diff_signal, network_status, diff_network


def digest_bluetooth(bluetooth):
    global previous_bluetooth_state, previous_bluetooth_count
    diff_bluetooth_state, diff_bluetooth_count = 0, 0
    if bluetooth == ' ':
        return 0, 0, 0, 0
    bluetooth = ast.literal_eval(bluetooth)
    bluetooth_state = bluetooth.get("bluetooth_state:")
    bluetooth_count = len(bluetooth.get("connectedDevices"))

    if previous_bluetooth_state != bluetooth_state:
        diff_bluetooth_state = 1
        previous_bluetooth_state = bluetooth_state
    if previous_bluetooth_count != bluetooth_count:
        diff_bluetooth_count = 1
        previous_bluetooth_count = bluetooth_count

    return bluetooth_state, diff_bluetooth_state, bluetooth_count, diff_bluetooth_count


def digest_activities(activities):
    return 0, 0


def digest_weather(raw_weather):
    global previous_weather, previous_temperature
    diff_weather, diff_temperature = 0, 0
    if raw_weather == ' ':
        return 0, 0, 0, 0
    weather_info = ast.literal_eval(raw_weather)
    weather = weather_info["lives"][0].get("weather")
    temperature = weather_info["lives"][0].get("temperature")
    if previous_weather != weather:
        diff_weather = 1
        previous_weather = weather
    if previous_temperature != temperature:
        diff_temperature = 1
        previous_temperature = temperature
    
    if climate_table.get(weather) is None:
        climate_table[weather] = len(climate_table)+1
        weather = climate_table[weather]
    else:
        weather = climate_table[weather]
    
    return weather, diff_weather, temperature, diff_temperature



def digest_list_information(list_information):
    list_task = []
    year, month, day, exact_time = [], [], [], []
    latitude, diff_latitude, longitude, diff_longitude, altitude, diff_altitude, location_tag, diff_tag = [], [], [], [], [], [], [], []
    SSID_number, diff_SSID, LinkSpeed, diff_LinkSpeed, signal, diff_signal = [], [], [], [], [], []
    location, diff_location, address, diff_address = [], [], [], []
    am_pm, hour, week_day = [], [], []
    bluetooth_state, diff_bluetooth_state = [], []
    network_status, diff_network = [], []
    bluetooth_count, diff_bluetooth_count = [], []
    activities, diff_activities = [], []
    weather, diff_weather, temperature, diff_temperature = [], [], [], []
    last_package = []
    for line_dict in list_information:
        list_task.append(line_dict["task"])
        cur_year, cur_month, cur_day, cur_exact_time, \
        cur_am_pm, cur_hour, cur_week_day = digest_time(time=line_dict["time"])

        cur_latitude, cur_diff_latitude, \
        cur_longitude, cur_diff_longitude, \
        cur_altitude, cur_diff_altitude, \
        cur_location_tag, cur_diff_tag, \
        cur_address, cur_diff_address, \
        cur_location, cur_diff_location  = digest_location(raw_location=line_dict["location"])

        cur_SSID_number, cur_diff_SSID, \
        cur_LinkSpeed, cur_diff_LinkSpeed, \
        cur_signal, cur_diff_signal, \
        cur_network, cur_diff_network = digest_network(network=line_dict["network"])

        cur_bluetooth_state, cur_diff_bluetooth, \
        cur_bluetooth_count, cur_diff_bluetooth_count = digest_bluetooth(bluetooth=line_dict["bluetooth"])

        cur_activities, cur_diff_activities = digest_activities(activities=line_dict["activities"])

        cur_weather, cur_diff_weather, \
        cur_temperature, cur_diff_temperature = digest_weather(raw_weather=line_dict["weather"])

        cur_last_package = line_dict["task"]
        if package_table.get(cur_last_package) is None:
            package_table[cur_last_package] = len(package_table)+1
            cur_last_package = package_table[cur_last_package]
        else:
            cur_last_package = package_table[cur_last_package]
        last_package.append(cur_last_package)
        year.append(cur_year)
        month.append(cur_month)
        day.append(cur_day)
        exact_time.append(cur_exact_time)
        latitude.append(cur_latitude)
        diff_latitude.append(cur_diff_latitude)
        longitude.append(cur_longitude)
        diff_longitude.append(cur_diff_longitude)
        altitude.append(cur_altitude)
        diff_altitude.append(cur_diff_altitude)
        location_tag.append(cur_location_tag)
        diff_tag.append(cur_diff_tag)
        SSID_number.append(cur_SSID_number)
        diff_SSID.append(cur_diff_SSID)
        LinkSpeed.append(cur_LinkSpeed)
        diff_LinkSpeed.append(cur_diff_LinkSpeed)
        signal.append(cur_signal)
        diff_signal.append(cur_diff_signal)
        bluetooth_state.append(cur_bluetooth_state)
        diff_bluetooth_state.append(cur_diff_bluetooth)
        location.append(cur_location)
        diff_location.append(cur_diff_location)
        address.append(cur_address)
        diff_address.append(cur_diff_address)
        am_pm.append(cur_am_pm)
        hour.append(cur_hour)
        week_day.append(cur_week_day)
        network_status.append(cur_network)
        diff_network.append(cur_diff_network)
        bluetooth_count.append(cur_bluetooth_count)
        diff_bluetooth_count.append(cur_diff_bluetooth_count)
        activities.append(cur_activities)
        diff_activities.append(cur_diff_activities)
        weather.append(cur_weather)
        diff_weather.append(cur_diff_weather)
        temperature.append(cur_temperature)
        diff_temperature.append(cur_diff_temperature)

    ans_dict = {}
    ans_dict["year"] = year
    ans_dict["month"] = month
    ans_dict["day"] = day
    ans_dict["exact_time"] = exact_time
    ans_dict["latitude"] = latitude
    ans_dict["diff-latitude"] = diff_latitude
    ans_dict["longitude"] = longitude
    ans_dict["diff-longitude"] = diff_longitude
    ans_dict["altitude"] = altitude
    ans_dict["diff-altitude"] = diff_altitude
    ans_dict["location_tag"] = location_tag
    ans_dict["diff-location_tag"] = diff_tag
    ans_dict["SSID_number"] = SSID_number
    ans_dict["diff-SSID"] = diff_SSID
    ans_dict["LinkSpeed"] = LinkSpeed
    ans_dict["diff-LinkSpeed"] = diff_LinkSpeed
    ans_dict["signal"] = signal
    ans_dict["diff-signal"] = diff_signal
    ans_dict["bluetooth_state"] = bluetooth_state
    ans_dict["diff-bluetooth_state"] = diff_bluetooth_state
    ans_dict["network"] = network_status
    ans_dict["diff-network"] = diff_network
    ans_dict["bluetooth_devices_connected_count"] = bluetooth_count
    ans_dict["diff-bluetooth_devices_connected_count"] = diff_bluetooth_count
    ans_dict["activities"] = activities
    ans_dict["diff-activities"] = diff_activities
    ans_dict["weather"] = weather
    ans_dict["diff-weather"] = diff_weather
    ans_dict["temperature"] = temperature
    ans_dict["diff-temperature"] = diff_temperature
    ans_dict["location"] = location
    ans_dict["diff-location"] = diff_location
    ans_dict["address"] = address
    ans_dict["diff-address"] = diff_address
    ans_dict["am_pm"] = am_pm
    ans_dict["hour"] = hour
    ans_dict["week_day"] = week_day

    return pandas.DataFrame(data=ans_dict), list_task


def build_data():
    current_path = os.path.abspath(os.path.dirname(__file__))+"/"
    pd_dataframe = None
    list_task = None
    with open(current_path+"location_name_dict.pkl", 'rb') as f1:
        global location_name_dict
        location_name_dict = pickle.load(f1)
    with open(current_path+"SSID_table.pkl", 'rb') as f2:
        global SSID_table
        try:
            SSID_table = pickle.load(f2)
        except:
            SSID_table = {}
    with open(current_path+"address_table.pkl", 'rb') as f3:
        global address_table
        try:
            address_table = pickle.load(f3)
        except:
            address_table = {}
    with open(current_path+"location_table.pkl", 'rb') as f4:
        global location_table
        try:
            location_table = pickle.load(f4)
        except:
            location_table = {}
    with open(current_path+"climate_table.pkl", 'rb') as f5:
        global climate_table
        try:
            climate_table = pickle.load(f5)
        except:
            climate_table = {}
    with open(current_path+"package_table.pkl", 'rb') as f6:
        global package_table
        try:
            package_table = pickle.load(f6)
        except:
            package_table = {}

    with codecs.open(filename=current_path+file_path, mode='r', encoding="UTF-8") as file:
        lines = file.readlines()
        list_information = build_info(lines)
        pd_dataframe, list_task = digest_list_information(list_information)

    with open("SSID_table.pkl", 'wb') as _f2:
        pickle.dump(SSID_table, _f2)
    with open("address_table.pkl", 'wb') as _f3:
        pickle.dump(address_table, _f3)
    with open("location_table.pkl", 'wb') as _f4:
        pickle.dump(location_table, _f4)
    with open("climate_table.pkl", 'wb') as _f5:
        pickle.dump(climate_table, _f5)
    with open("package_table.pkl", 'wb') as _f6:
        pickle.dump(package_table, _f6)

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
    feature_selector = BorutaPy(forest, n_estimators='auto', verbose=2, random_state=1, max_iter=50)
    feature_selector.fit(data, labels)
    processed_data = feature_selector.transform(data)

    new_feature_names = []
    for i in range(len(list(original_feature_names))):
        if feature_selector.support_[i] == True:
            new_feature_names.append(list(original_feature_names)[i])

    return new_feature_names


def build_feature(processed_data, list_task):
    return Boruta_strategy(processed_data, list_task)


def generate_feature_names(tasks_to_digest):
    global stored_service
    real_task = []
    for task in tasks_to_digest:
        real_task.extend([task+"-task", task+"-package"])
    stored_service = real_task

    feature_names_dict = {}

    for task in tasks_to_digest:
        actual_task_list = [task+"-task", task+"-package"]
        for actual_task in actual_task_list:
            global package_to_explore
            package_to_explore = actual_task
            processed_data, list_task = build_data()
            if feature_names_dict.get(task) is not None:
                if list_task != []:
                    feature_names_dict[task].extend(build_feature(processed_data, list_task))
            else:
                if list_task != []:
                    feature_names_dict[task] = build_feature(processed_data, list_task)
                else:
                    feature_names_dict[task] = []
    return feature_names_dict