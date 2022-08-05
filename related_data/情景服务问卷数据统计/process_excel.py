import xlrd, json

"""
Planning to process the raw excel data into the following format

{
    "时间":
    {
        "微信":
        {
            <服务1>: <情景1>,
            ......
        },
        "B站":
        {
            <服务1>: <情景1>,
            ......
        },
        "美团":
        {
            <服务1>: <情景1>,
            ......
        },
        "知乎":
        {
            <服务1>: <情景1>,
            ......
        },
        "淘宝":
        {
            <服务1>: <情景1>,
            ......
        },
        "其他":
        {
            <服务1>: <情景1>,
            ......
        }
    },
    "地点":
    {
        同上
    },
    "前置服务":
    {
        同上
    }
    "条件组合":
    {
        同上
    }
    "外界条件":
    {
        同上
    }
}

"""

possible_softwares = {"微信":["微信", "wechat"], "B站":["B站", "bilibili", "b站"], "美团":["美团"], "知乎":["知乎"], "淘宝":["淘宝", "天猫"]}
contextual_categories = ["时间", "地点", "前置服务", "条件组合", "外界条件"]



def dict_builder(category):
    filename = category+r"-服务组合.xlsx"
    sheet = xlrd.open_workbook(filename).sheet_by_index(0)
    list_context = sheet.col_values(0, start_rowx=1, end_rowx=None)
    list_service = sheet.col_values(1, start_rowx=1, end_rowx=None)
    
    dict_category = {}
    set_included = set()

    for possible_software in possible_softwares:
        dict_software = {}
        for alias in possible_softwares[possible_software]:
            for service in list_service:
                if alias in str(service):
                    if dict_software.get(str(service)) is None:
                        dict_software[str(service)] = []
                    dict_software[str(service)].append(list_context[list_service.index(service)])
                    dict_software[str(service)] = list(set(dict_software[str(service)]))
                    set_included.add(list_service.index(service))
        dict_category[possible_software] = dict_software

    dict_others = {}

    for index_service in range(len(list_service)):
        if index_service not in set_included:
            dict_others[list_service[index_service]] = list_context[index_service]
        
    dict_category["其他"] = dict_others
    
    return dict_category


def main():
    dict_total = {}
    for category in contextual_categories:
        dict_total[category] = dict_builder(category=category)
    
    with open("processed_data.json", 'w', encoding="UTF-8") as file:
        json.dump(dict_total, file, ensure_ascii=False)


if __name__ == "__main__":
    main()



