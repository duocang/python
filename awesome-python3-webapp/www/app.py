# -*- coding: utf-8 -*-
import logging
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web

# 通过下面的方式进行简单配置日志级别
logging.basicConfig(level=logging.INFO)

def index(request):
	return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')


async def init(loop):   # 异步运行的函数
	app = web.Application(loop=loop)
	app.router.add_route("GET", '/', index)
	srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9001) # 该操作需要进行异步操作
	logging.info('server started at http://127.0.0.1:9000...')
	return srv

loop = asyncio.get_event_loop() # 创建asyncio event loop
loop.run_until_complete(init(loop)) # 用asyncio event loop来异步运行init()
loop.run_forever()
