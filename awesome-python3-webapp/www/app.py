# -*- coding: utf-8 -*-

__author__ = 'Xuesong Wang'
'''
async web application
'''

import logging
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web # aiohttp是一个用于web服务的库

# 通过下面的方式进行简单配置日志级别
logging.basicConfig(level=logging.INFO)

def index(request):
	return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html') # index 函数内，添加content_type，否则默认下载


async def init(loop):   # 异步运行的函数
	app = web.Application(loop=loop) # Application is a synonym for web-server. event loop used for processing HTTP requests.
    # 通过router的指定的方法可以把请求的链接和对应的处理函数关联在一起
	app.router.add_route("GET", '/', index) # 主页
	srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9001) # 该操作需要进行异步操作
	logging.info('server started at http://127.0.0.1:9001...')
	return srv

loop = asyncio.get_event_loop() # 创建asyncio event loop
loop.run_until_complete(init(loop)) # 用asyncio event loop来异步运行init()
loop.run_forever()
