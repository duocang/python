# -*- coding:utf-8 -*-

import asyncio, logging
import aiomysql

# web框架使用了基于asyncio的aiohttp，这是基于协程的异步模型。
# 在协程中，不能调用普通的同步io操作，因为所有用户都是由一个线程
# 服务的，协程的执行速度必须非常快，才可处理大量用户的请求。而耗时
# 的io操作不能在协程中以同步的方式调用，否则，等待一个io操作时，
# 无法响应其他用户。

# 一旦决定使用异步，则系统每一层都必须是异步

# 创建连接池
# 每一个http请求都可以从连接池中获取数据库连接
# 使用连接池的好处是不必频繁地打开或关闭数据库
@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(
        hos=kw.get('host', 'localhost'),
        por=kw.get('port', 3306),
        user=kw['root'],
        password=kw['8888'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )

    