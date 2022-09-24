import codecs, pickle

ans_dict = {}

with codecs.open(filename="location_name.txt", mode='r', encoding='utf-8') as file:
    lines = file.readlines()
    index = 1
    for line in lines:
        line = line.strip('\n').strip('\r')
        line_info = line.split(',')
        parent_name = line_info[0]
        children_names = line_info[1].split('、')
        for children_name in children_names:
            ans_dict[parent_name+'_'+children_name] = index
            index += 1

with open("location_name_dict.pkl", 'wb') as f:
    pickle.dump(ans_dict, f)

with open("SSID_table.pkl", 'wb') as f2:
    pickle.dump({}, f2)
