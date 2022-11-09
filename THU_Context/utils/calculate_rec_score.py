def calculate_rec_score(rule_based_dict, feature_based_dict, current_context_dict):
    """function to calculate the score of recommendation

    Args:
        rule_based_dict (dict): 
            the dictionary of rule-based recommendation in the following format
            {
                <task_name1>: [
                    {
                        "feature_name": <feature_name>,
                        "context": <context>
                    },
                    ...
                ],
                <task_name2>: [
                    {
                        "feature_name": <feature_name>,
                        "context": <context>
                    },
                    ...
                ]
            }
        feature_based_dict (dict): 
            the dictionary of feature-based recommendation in the following format
            {
                <task_name1>: [
                    <feature_name1>,
                    <feature_name2>,
                    ...
                ],
                <task_name2>: [
                    <feature_name1>,
                    <feature_name2>,
                    ...
                ]
            }
        current_context_dict (dict): 
            the dictionary of current context in the following format
            {
                <feature_name1>: <context1>,
                <feature_name2>: <context2>,
                ...
            }     


    Returns:
    a list of tuples in the following format
    [(<task_name>, <score>), ...]
    """
    
    feature_characteristic_dict = {
        "year": (-1, -1),
        "month": (-1, -1),
        "day": (-1, -1),
        "exact_time": (0, 86340),
        "latitude": (-1, -1),
        "diff_latitude": (-1, -1),
        "longitude": (-1, -1),
        "diff_longitude": (-1, -1),
        "altitude": (-1, -1),
        "diff_altitude": (-1, -1),
        "location_tag": (-1, -1),
        "diff_tag": (-1, -1),
        "SSID_number": (-1, -1),
        "diff_SSID": (-1, -1),
        "LinkSpeed": (0, 1000),
        "diff_LinkSpeed": (-1, -1),
        "signal": (0, 3),
        "diff_signal": (-1, -1),
        "bluetooth_state": (-1, -1),
        "diff_bluetooth_state": (-1, -1),
        "network": (-1, -1),
        "diff_network": (-1, -1),
        "bluetooth_devices_connected_count": (-1, -1),
        "diff-bluetooth_devices_connected_count": (-1, -1),
        "activities": (-1, -1),
        "diff_activities": (-1, -1),
        "weather": (-1, -1),
        "diff_weather": (-1, -1),
        "temperature": (-30, 50),
        "diff_temperature": (-1, -1),
        "location": (-1, -1),
        "diff_location": (-1, -1),
        "address": (-1, -1),
        "diff_address": (-1, -1),
        "am_pm": (-1, -1),
        "hour": (0, 23),
        "week_day": (-1, -1)
    }

    # score calculating
    # assuming feature_based_dict and rule_based_dict share the same task_name
    # 2 steps
    # 1. calculate feature similarity score by checking if feature in rule_based_dict is in feature_based_dict
    # if yes, then add 1 to the score_feature_similarity
    # 2. calculate context_accuracy score by compare the context in rule_based_dict with current_context_dict
    # if current feature is (-1, -1) in feature_characteristic_dict, 
    # then if context in rule_based_dict is the same as current_context_dict, add 1 to the score_context_accuracy
    # if current feature is not (-1, -1) in feature_characteristic_dict, 
    # treat the value in feature_characteristic_dict as the range of the feature
    # diff = abs(context in rule_based_dict - current_context_dict)
    # ratio = diff / range
    # add 1-ratio to the score_context_accuracy
    # finally, calculate the score of recommendation by adding score_feature_similarity and score_context_accuracy
    score_feature_similarity = 0
    score_context_accuracy = 0
    task_score_dict = {}
    for task_name in rule_based_dict:
        for rule in rule_based_dict[task_name]:
            if rule["feature_name"] in feature_based_dict[task_name]:
                score_feature_similarity += 1
            if feature_characteristic_dict[rule["feature_name"]] == (-1, -1):
                if rule["context"] == current_context_dict[rule["feature_name"]]:
                    score_context_accuracy += 1
            else:
                diff = abs(rule["context"] - current_context_dict[rule["feature_name"]])
                ratio = diff / (feature_characteristic_dict[rule["feature_name"]][1] - feature_characteristic_dict[rule["feature_name"]][0])
                score_context_accuracy += 1 - ratio
        task_score_dict[task_name] = score_feature_similarity + score_context_accuracy
    
    # change highest score to 1 and lowest score to 0, adjust other value accordingly
    for key in task_score_dict:
        task_score_dict[key] = (task_score_dict[key] - min(task_score_dict.values())) / (max(task_score_dict.values()) - min(task_score_dict.values()))
    # sort the dict by value
    return list(sorted(task_score_dict.items(), key = lambda kv:(kv[1], kv[0])))

