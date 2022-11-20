from Boruta import generate_feature_names


def test_generate_feature_names():
    tasks_to_digest = [
        "美团",
        "云空间",
        "联系人",
        "安卓配置wifi",
        "图库",
        "微信",
        "抖音",
        "面对面建群",
        "百度",
        "相机",
        "软件更新",
        "微信查看消息",
        "知乎",
        "设置",
        "浏览器",
        "新浪新闻",
        "百度地图",
        "拍拍助手",
        "美团搜索",
        "微信查看朋友圈",
        "Bilibili看直播",
        "网易云fm",
        "支付宝",
        "3D地图示例",
        "饿了么美食外卖",
        "QQ",
        "信息",
        "滚动截屏",
        "饿了么",
        "备忘录",
        "网易云音乐",
        "腾讯新闻",
        "哔哩哔哩",
        "手机管家",
        "智慧语音",
        "Bilibili热门视频",
        "淘宝",
        "朋友圈"
    ]
    username = "ljh20"

    generate_feature_names(tasks_to_digest, username)


if __name__ == "__main__":
    test_generate_feature_names()