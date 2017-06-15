# -*- coding:utf-8 -*-

import asyncio, logging
import aiomysql

def log(sql, args=()):
    logging.info('SQL: %s' % sql)

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

# yield from将调用一个子协程（也就是在一个协程中调用另一个协程）并直接获得子协程的返回结果
@asyncio.coroutine
def select(sql, args, size=None):
    log(sql, args)
    global __pool
    with(yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)           # 始终使用sql语句，防止sql注入攻击
        yield from cur.execute(sql.replace('?', '%s'), args or ())  # sql语句的占位符为？，而mysql的为%s，在select函数内自动替换
        if size:    # 如果出入size，就可以通过fetchmany获取指定数量的记录，否则，通过fetchall获取所有记录。
            re = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.colse()
        logging.info('rows returned: %s' %len(rs))
        return rs

