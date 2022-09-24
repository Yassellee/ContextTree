from . import process_logitem

class Config:
    def __init__(self):
        self.num_context = 30
        self.dict_raw_data, self.list_task = process_logitem.main()
        self.if_use_raw_data = True