#-*- coding:utf-8 -*-
import requests
from time import time
import re

url = 'https://movie.douban.com/top250'


def fetch_page(url):
    response = requests.get(url)
    return response


def parse(url):
    response = fetch_page(url)
    page = response.content

    fetch_list = set()
    result = []

    for title in re.findall(rb'<a href=.*\s.*<span class="title">(.*)</span>', page):
        result.append(title)

    for postfix in re.findall(rb'<a href="(\?start=.*?)"', page):
        fetch_list.add(url + postfix.decode())

    for url in fetch_list:
        response = fetch_page(url)
        for title in re.findall(rb'<a href=.*\s.*<span class="title">(.*)</span>', page):
            result.append(title)

    for i, title in enumerate(result, 1):
        title = title.decode()
        print(i, title)

def main():
    start = time()
    parse(url)
    end = time()
    print('Cost {} seconds'.format((end - start)))
if __name__ == '__main__':
    main()