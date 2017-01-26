import re
import urllib
import urllib.request
from collections import deque

queue = deque("https://www.zhihu.com/")#存放待爬取的网址
visited = set("https://www.zhihu.com/")#存放爬取过的网址。判断是否爬取过

url = "http://news.dbanotes.net"#入口网站
queue.append(url)
count = 1

while queue:
	url = queue.popleft()#删除已经爬取过的队首的网址url
	visited |= {url}#把已经爬取过的页面放入set中，方便下面的判断
	urlop = urllib.request.urlopen(url)
	if 'html' not in urlop.getheader('Content-Type'):
		continue#如果是html再继续爬取
	try:
		data = urlop.read().decode('utf-8')
	except:
		continue
	value = re.findall(r'href="(.+?)"',data)
	for x in value:
		if 'http' in x and x not in visited:
			print("加入队列：" + x)