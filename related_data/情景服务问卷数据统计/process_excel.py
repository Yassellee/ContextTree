import xlrd, json, os

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

possible_softwares = {"微信":["微信", "wechat", "紫荆", "粤核酸", "健康宝", "紫晶", "行程码", "雨课堂", "粤康码"], 
                      "B站":["B站", "bilibili", "b站", "哔哩哔哩", "B 站"], 
                      "美团":["美团", "外卖"], 
                      "知乎":["知乎"], 
                      "淘宝":["淘宝", "天猫"], 
                      "支付宝":["支付宝"],
                      "网易云音乐":["网易云"],
                      "QQ音乐":["QQ音乐", "qq音乐", "Q Q 音乐", "q q 音乐", "Q q 音乐"],
                      "小红书":["小红书"],
                      "高德地图":["高德地图", "高德导航", "高德"],
                      "贴吧":["贴吧"],
                      "王者荣耀":["王者"],
                      "抖音":["抖音"],
                      "KEEP":["KEEP", "Keep", "keep"],
                      "虎牙":["虎牙"],
                      "斗鱼":["斗鱼"],
                      "原神":["原神"],
                      "豆瓣":["豆瓣"],
                      "微博":["微博"],
                      "Forest":["Forest", "forest"],
                      "单词软件":["单词", "百词斩", "多邻国", "背词"],
                      "百度相关":["百度"]}
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
            for index_service in range(len(list_service)):
            # for service in list_service:
                if alias in str(list_service[index_service]):
                    if dict_software.get(str(list_service[index_service])) is None:
                        dict_software[str(list_service[index_service])] = []
                    dict_software[str(list_service[index_service])].append(list_context[index_service])
                    dict_software[str(list_service[index_service])] = list(set(dict_software[str(list_service[index_service])]))
                    set_included.add(index_service)
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



