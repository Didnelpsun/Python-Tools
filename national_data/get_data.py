import urllib.request
# 获取cookie
import http.cookiejar
# 对中文转码
from urllib.parse import quote
from main import url


# 根据关键字获取数据
def get_data_list(key_word):
    # 获取cookie
    cookies = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookies)
    opener = urllib.request.build_opener(handler)
    response = opener.open(url)
    cookie = ""
    for item in cookies:
        cookie += item.name + " ; " + item.value

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh',
        'Cookie': cookie
    }

    search_url = "https://data.stats.gov.cn/search.htm?s=" + quote(key_word) + "&m=searchdata&db=&p="

    i = 0
    page_current = 0
    page_count = 2
    data_list = []

    while page_current < page_count:
        # 自增时每一行的域名后面是有一个换行符，所以要去掉
        search_url += str(i).strip('\n')
        # 请求
        request = urllib.request.Request(search_url, headers=headers)
        # 响应
        response = urllib.request.urlopen(request)
        # 获取数据
        data = eval(response.read().decode('utf-8'))
        if i == 0:
            page_count = data["pagecount"]
        page_current = data["pagecurrent"]
        # print(page_current)
        # print(data)
        if len(data["result"]) == 0:
            break
        data_list.extend(data["result"])
        # print(data["result"])
        i += 1
        page_current += 1
    return data_list


# 根据输入获取数据
def get_input_data_list():
    # 获取输入关键字
    key_word = ""
    loop = ''
    while True:
        key_word = input("请输入搜索关键字：")
        if key_word == "":
            print("输入不能为空！")
            continue
        loop = input("是否确定搜索”" + key_word + "“？确认请输入y：")
        if loop == "y":
            break
    return get_data_list(key_word)


# 获取对应数据
# data：数据
# db：所属栏目
# exp：备注
# prank：增长率
# rank：等级
# reg：地区
# report：筛选关键字
# sj：数据时间
# zb：指标
class ClassDataList:
    def __init__(self):
        self.data = []
        self.db = ""
        self.exp = ""
        self.reg = ""
        self.zb = ""

    # def __init__(self, db, exp, reg, zb):
    #     self.data = []
    #     self.db = db
    #     self.exp = exp
    #     self.reg = reg
    #     self.zb = zb


class ClassData:
    def __init__(self, data, prank, rank, report, sj):
        self.data = data
        self.prank = prank
        self.rank = rank
        self.report = report
        self.sj = sj


def get_class_data_list(data_list):
    # 返回的是一个二维数组，第一维是不同指标的数据，每个都是一个ClassDataList对象
    # 第二维是相同指标所有数据，指ClassDataList的data属性包含一个ClassData对象组
    # 准备一个保存指标标签的数组
    label = []
    # 保存数据的数组
    result = []
    for item in data_list:
        # 先判断数据是否为空，若空则直接跳过
        if item["data"].strip('') == "":
            continue
        # 先判断指标数据是否已经存在
        zb = item["zb"]
        index = label.index(zb)
        # 如果存在则将ClassData保存到ClassDataList中
        if index > -1:
            data = ClassData(item["data"], item["prank"], item["rank"], item["report"], item["sj"])
            result[index].data.append(data)
        class_data_list.db = item["db"]
        class_data_list.reg = item["reg"]
        class_data_list.exp = item["exp"]
        class_data_list.zb = item["zb"]
