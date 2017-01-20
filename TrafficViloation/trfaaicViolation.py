#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib
from urllib import urlencode


# ----------------------------------
# 全国车辆违章调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/36
# ----------------------------------

def main():
    # 配置您申请的APPKey
    appkey = "*********************"

    # 1.获取支持城市参数接口
    request1(appkey, "GET")

    # 2.请求违章查询接口
    request2(appkey, "GET")

    # 3.接口剩余请求次数查询
    request3(appkey, "GET")


# 获取支持城市参数接口
def request1(appkey, m="GET"):
    url = "http://v.juhe.cn/wz/citys"
    params = {
        "province": "",  # 默认全部，省份简写，如：ZJ、JS
        "dtype": "",  # 返回数据格式：json或xml或jsonp,默认json
        "format": "",  # 格式选择1或2，默认1
        "callback": "",  # 返回格式选择jsonp时，必须传递
        "key": appkey,  # 你申请的key

    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"], res["reason"])
    else:
        print "request api error"


# 请求违章查询接口
def request2(appkey, m="GET"):
    url = "http://v.juhe.cn/wz/query"
    params = {
        "dtype": "",  # 返回数据格式：json或xml或jsonp,默认json
        "callback": "",  # 返回格式选择jsonp时，必须传递
        "key": appkey,  # 你申请的key
        "city": "",  # 城市代码 *
        "hphm": "",  # 号牌号码 完整7位 ,需要utf8 urlencode*
        "hpzl": "",  # 号牌类型，默认02
        "engineno": "",  # 发动机号 (根据城市接口中的参数填写)
        "classno": "",  # 车架号 (根据城市接口中的参数填写)

    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"], res["reason"])
    else:
        print "request api error"


# 接口剩余请求次数查询
def request3(appkey, m="GET"):
    url = "http://v.juhe.cn/wz/status"
    params = {
        "key": appkey,  # 应用APPKEY(应用详细页查询)
        "dtype": "",  # 返回数据的格式,xml或json，默认json

    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"], res["reason"])
    else:
        print "request api error"


if __name__ == '__main__':
    main()