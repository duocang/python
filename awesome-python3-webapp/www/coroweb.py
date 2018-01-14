# -*- coding: utf-8 -*-

import asyncio, os, inspect, logging, functools
from urllib import parse
from aiohttp import web
from apis import  APIError

'''
get方式的安全性叫post方式要差，包含机密信息的话，建议使用post数据提交方式
在做数据查询时，建议使用get方式，而在做数据添加、修改或删除时，建议使用post方式
'''

def get(path):
    '''
    把一个函数映射为一个RUL处理函数，这样，一个函数通过@get()的装饰就附带了URL信息
    :param path:
    :return: 包装后的函数
    '''

    # Define decorator @get('/path')
    def decorator(func):
        # 被装饰的函数其实已经是一个新的函数（函数名等属性发生变化）。此时会对程序造成一些不便。
        # 所以functools包中提供了一个wraps的decorator来消除这样的副作用。
        # 写decorator时，在实现之前加上functools.wraps，它能保留原有函数的名称和docstring.
        @functools.warps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

def post(path):
    '''
    @post与@get定义类似
    :param path:
    :return:
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator()


'''
使用inspect模块，创建几个函数用以获取URL处理函数与request参数之间的关系
inspect模块：
1. 对是否是模块、框架、函数等进行类型检查
2. 获取源码
3. 获取类或函数的参数信息
4. 解析堆栈

inspect.signature（fn)将返回一个inspect.Signature类型的对象，值为fn这个函数的所有参数
inspect.Signature对象的paramerters属性是一个mappingproxy（映射）类型的对象，值为一个有序字典（Orderdict)。

    这个字典里的key是即为参数名，str类型

    这个字典里的value是一个inspect.Parameter类型的对象，根据我的理解，这个对象里包含的一个参数的各种信息
inspect.Parameter对象的kind属性是一个_ParameterKind枚举类型的对象，值为这个参数的类型（可变参数，关键词参数，etc）
inspect.Parameter对象的default属性：如果这个参数有默认值，即返回这个默认值，如果没有，返回一个inspect._empty类。

'''
def get_required_kw_args(fn):   # 手机没有默认值的命名关键字参数
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        '''
        if the parameter has no default value, this attribute is set to Parameter.empty
        kind: describes how argument values are bound to the parameter. 
            Value must be supplied as a keyword argument. Keyword only parameters are those which 
            appear after a * or *args entry in a Python function definition.
        '''
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)


def get_named_kw_args(fn):  # 获取命名关键字参数
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)

def has_named_kw_args(fn):  # 判断有没有命名关键字参数
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)


def has_var_kw_arg(fn): # 判断有没有关键字参数
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True

def has_request_arg(fn):    # 判断是否含有叫‘request’参数，且该参数是否为最后一个参数
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue    # 跳出当前循环，进入下一个循环
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL    # This corresponds to a *args parameter in a Python function definition.
                      and param.kind != inspect.Parameter.KEYWORD_ONLY  # Keyword only parameters are those which appear after a * or *args entry in a Python function definition.
                      and param.kind != inspect.Parameter.VAR_KEYWORD): # This corresponds to a **kwargs parameter in a Python function definition.
            raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found


'''
定义RequestHandler，正式向request参数获取URL处理函数所需的参数
'''
class RequestHandler(object):
    def __init__(self, app, fn):    # 接受app参数
        self._app = app
        self._func = fn
        self._has_request_arg = has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)

    async def __call__(self, request):  # 协程
        kw = None
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            if request.method == 'POST':    # 判断客户端发来的方法是否为POST
                if not request.content_type:    # 查询有没提交数据的格式（EncType）
                    return web.HTTPBadRequest(text="Missing Content-Type")

                ct = request.content_type.lower()   # 小写
                if ct.startswith('application/json'):  # startswith
                    params = await request.json()    # Read request body decoded as json
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest(text='JSON body must be an object.')
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    # reads POST parameters from request body. If method is not POST, PUT, PATCH, TRACE or DELETE or
                    # content_type is not empty or application/x-www-form-urlencoded or multipart/form-data returns
                    # empty multidict.
                    params = await request.post()
                    kw = dict(**params)
                else:
                    return web.HTTPBadRequest(text='Unsupported Content_Type: %s' %(request.content_type))
        if request.method == 'GET':
            qs = request.query_string   # The query string in the URL
            if qs:
                kw = dict()
                # Parse a query string given as a string argument. Data are returned as a dictionary.
                # The dictionary keys are the unique query variable names and the values are lists
                # of values for each name.
                for k, v in parse.parse_qs(qs, True).items():
                    kw[k] = v[0]

        if kw is None:
            kw = dict(**request.match_info)
        else:
            if not self._has_var_kw_arg and self._named_kw_args:  # 当函数参数没有关键字参数时，移去request除命名关键字参数所有的参数信息
                copy = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            for k, v in request.match_info.items():  # 检查命名关键参数
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v
        if self._has_request_arg:
            kw['request'] = request
        if self._required_kw_args:  # 假如命名关键字参数(没有附加默认值)，request没有提供相应的数值，报错
            for name in self._required_kw_args:
                if name not in kw:
                    return web.HTTPBadRequest(text='Missing argument: %s' % (name))
        logging.info('call with args: %s' % str(kw))
        try:
            r = await self._func(**kw)
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)
'''
上述RequestHandler可以看出最后调用URL函数时，URL函数可能返回一个叫做APIError的错误。其作用就是用来返回诸如账号登录信息的错误。
'''


'''
由于新建的web框架是基于aiohttp框架，所以需要再编写一个add_route函数，用来注册一个URL处理函数，主要起验证函数
是否包含URL的相应方法与路径信息，以及将函数变为协程。
'''
def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s,' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn): #判断是否为协程且生成器,不是使用isinstance
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)'
                 % (method, path, fn.__name__, ','.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn)) # RequestHandler有两个参数

'''
通常add_route()注册会调用多次，为了使用框架的便利性可以编写一个批量注册的函数。
预期效果：只需向这个函数提供需要注册函数的文件路径，新编写的函数会筛选注册文件内所有符合注册条件的函数.
'''
# 直接导入文件，批量注册一个URL处理函数
def add_routes(app, module_name):
    n = module_name.rfind('.')
    if n == -1:
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name], 0), name)#第一个参数为文件路径参数，不能掺夹函数名，类名
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__d', None)
            if path and method: #这里要查询path以及method是否存在而不是等待add_route函数查询，因为那里错误就要报错了
                add_route(app, fn)

# 添加静态文件夹的路径
def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'statics') # 输出当前文件夹中‘static’的路径
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' %('/static/', path))