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
# 连接池由全局变量__pool存储，
async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )

# 使用连接池的好处就是不必频繁地打开和关闭数据库连接，而是能复用就尽量复用

# yield from将调用一个子协程（也就是在一个协程中调用另一个协程）并直接获得子协程的返回结果
async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur: # aiomysql.DictCursor  # create dict cursor
            await cur.execute(sql.replace('?', '%s'), args or ()) # A cursor which returns results as a dictionary.
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        return rs


# 要执行INSERT、UPDATE、DELETE语句，可以定义一个通用的execute()函数，
# 因为这3种SQL的执行都需要相同的参数，以及返回一个整数表示影响的行数：
async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected
# execute()函数和select()函数所不同的是，cursor对象不返回结果集，而是通过rowcount返回结果数。


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)

class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)

class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)

class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)
