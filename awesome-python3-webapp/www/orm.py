# -*- coding:utf-8 -*-

__author__= "Xuesong Wang"

import asyncio, logging
import aiomysql

def log(sql, args=()):
    logging.info('SQL: %s' % sql)


'''
web框架使用了基于asyncio的aiohttp，这是基于协程的异步模型。
在协程中，不能调用普通的同步io操作，因为所有用户都是由一个线程
服务的，协程的执行速度必须非常快，才可处理大量用户的请求。而耗时
的io操作不能在协程中以同步的方式调用，否则，等待一个io操作时，
无法响应其他用户。
一旦决定使用异步，则系统每一层都必须是异步
'''


'''
创建连接池
每一个http请求都可以从连接池中获取数据库连接
连接池由全局变量__pool存储，使用连接池的好处是不必频繁地打开或关闭数据库
缺省情况下将编码设置为utf8，自动提交事务
'''
async def create_pool(loop, **kw):
    print('create database connection pool...')
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
    ) # 创建连接所需要的参数
    print("connection is done")

async def destory_pool():
    global pool
    if pool is not None :
        pool.close()
        await pool.wait_closed()


# 用于输出元类中创建sql_insert语句中的占位符
# 构造sql语句参数字符串，最后返回的字符串会以','分割多个'?'，如 num==2，则会返回 '?, ?'
def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


'''
单独封装select，其他insert, update, delete一并另行封装，理由如下：
使用Cursor对象执行insert，update，delete语句时，执行结果由rowcount返回影响的行数，就可以拿到执行结果。
使用Cursor对象执行select语句时，通过featchall()可以拿到结果集。结果集是一个list，每一个元素都是一个tuple，对应一行记录。
'''

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

'''
select 
要执行SELECT语句，用select函数执行，需要传入SQL语句和SQL参数
SQL语句的占位符是？，而MySQL的占位符是%s，select（）函数在内部自动替换。
使用带参数的SQL，而非自己拼接SQL字符串，这样可以防止SQL注入攻击。
yield from将调用一个子协程（也就是在一个协程中调用另一个协程）并直接获得子协程的返回结果
'''
async def select(sql, args, size=None):
    log(sql, args)
    #global __pool
    async with __pool.get() as conn:
        # #获取一个cursor，通过aiomysql.DictCursor获取到的cursor在返回结果时会返回一个字典格式
        async with conn.cursor(aiomysql.DictCursor) as cur: # aiomysql.DictCursor  # create dict cursor
        # #把sql语句的'?'替换为'%s',并把args的值填充到相应的位置补充成完整的可执行sql语句并执行mysql中得占位符是'?'
            await cur.execute(sql.replace('?', '%s'), args or ()) # A cursor which returns results as a dictionary.
            ##如果有要求的返回行数，则取要求的行数，如果没有，则全部取出
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs)) # 显示获取的数据长度
        return rs # 返回获取的数据

# 首先定义Field类，它负责保存数据库表的字段名和字段类型

# 用于标识model里每个成员变量的类
# name：名字 column_type：值类型 primary_key:是否primary_key default:默认值
class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
    # 直接打印对象的实现方法
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

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):   # 当前准备创建的类的对象；类的名字类继承的父类集合；类的方法集合
        if name == 'Model':  # 排除Model类本身：
            return type.__new__(cls, name, bases, attrs)
        # 获取table名称
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))

        # 获取所有的Field和主键名
        mappings = dict()
        fields = [] # 保存出主键外的属性
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v

                if v.primary_key:   # 找到主键
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primaryKey = k  # 此列设为列表的主键
                else:
                    fields.append(k)    # 保存除主键外的属性

        if not primaryKey:      # 无主键
            raise RuntimeError('Primary key not found.')

        for k in mappings.keys():
            attrs.pop(k)    # 从类属性中删除Field属性，否则容易造成运行时错误（实例的属性会遮盖类的同名属性）

        escaped_fields = list(map(lambda f: "`%s`" %f, fields)) # 转换为sql语法

        # 创建拱Model类使用的属性
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)

# Model从dict继承，所以具备所有dict的功能，同时又实现了特殊方法__getattr__()和__setattr__()，
# 因此又可以像引用普通字段那样写：
# >> > user['id']
# 123
# >> > user.id
# 123
# 定义ORM映射的基类Model

class Model(dict, metaclass = ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None) # 直接调回内置函数，注意此处没有下划线，Node的用处是在当User没有赋值数据时返回None，用于调用update

    def getValueOrDefault(self, key):
        value = getattr(self, key, None) # 第三个参数None，可以在没有返回值时，返回None，用于save
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        sql = [cls.__select__]
        if where:
            sql.append("where")
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)  # tuple融入list
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql), args)

    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. '
        sql = ['select %s _num_ from `%s`' %(selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    async def find(cls, primarykey):
        sql = '%s where `%s`=?' % (cls.__select__, cls.__primary_key__)
        rs = await select(sql, [primarykey], 1)
        if len(rs) == 0:
            return None
        return rs[0]['__num__']

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        print(args)
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warning('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getValue(self.__primary_key__)] # 此处不能使用list()-->'int' object is not iterable
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warn('faild to remove by primary key: affected rows: %s' % rows)