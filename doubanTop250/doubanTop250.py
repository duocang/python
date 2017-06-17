#-*- coding:utf-8 -*-
import urllib.request
import ssl
from lxml import etree
from time import time
import requests

url = 'https://movie.douban.com/top250'
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)

def fetch_page(url):
    response = urllib.request.urlopen(url, context=context)
    return response

def parse(url):
    response = fetch_page(url)
    page = response.read()
    html = etree.HTML(page)

    xpath_movie = '//*[@id="content"]/div/div[1]/ol/li'
    xpath_title = './/span[@class="title"]'         # 当前节点下所有class等于title的span
    xpath_pages = '//*[@id="content"]/div/div[1]/div[2]/a'  #当前页面下所有元素，id=content下的div中。。。

    pages = html.xpath(xpath_pages)     # 获取之后的页面链接
    fetch_list = []
    result = []

    for element_movie in html.xpath(xpath_movie):   # 当前页面的电影
        result.append(element_movie)

    for p in pages:
        fetch_list.append(url + p.get('href'))      # 抓取所有的链接

    for url in fetch_list:          # 在for循环中，依次获取每个页面中的电影，继续添加到result中
        response = fetch_page(url)
        page = response.read()
        html = etree.HTML(page)
        for element_movie in html.xpath(xpath_movie):
            result.append(element_movie)

    for i, movie in enumerate(result, 1):
        title = movie.find(xpath_title).text
        print(i, title)

def main():
    start = time()
    parse(2,url)
    end = time()
    print('Cost {} seconds'.format((end - start) / 5))


if __name__ == '__main__':

    main()


# ssl: SSL stands for Secure Sockets Layer and is designed to
# create secure connection between client and server.

# XPath使用路径表达式在XML文档中选取节点。节点是通过沿着路径或者step来选取的。
# nodename 选取此节点的所有子节点
# / 从根节点选取
# // 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置
# .	选取当前节点。
# .. 选取当前节点的父节点。
# @	选取属性# 。

