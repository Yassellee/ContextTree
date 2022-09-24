from . import config_preprocessing
import pandas, numpy

local_config = config_preprocessing.Config()

def default_data_builder():
    list_of_name = []
    data_dict = {}

    for i in range(local_config.num_context):
        list_of_name.append("context"+str(i))
    
    for name in list_of_name:
        data_dict[name] = numpy.random.randint(30, size=30)

    data_frame = pandas.DataFrame(data=data_dict)

    return data_frame

def custom_data_builder():
    return local_config.dict_raw_data

def data_frame_builder():
    if local_config.if_use_raw_data:
        return custom_data_builder()
    else:
        return default_data_builder()