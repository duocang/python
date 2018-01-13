# -*- coding: utf-8 -*-

'''
Models for user, bolg, comment.
结核ORM，我们可以把博客中需要使用到的User，blogs以及comments各自的信息，储存到数据库的三个表中，
并通过是使用Model表示出来。
'''

__author__ = 'Xuesong Wang'

import time, uuid

# 统一目录下导入
from .orm import Model, StringField, BooleanField, FloatField, TextField

def next_id():  # 随机生成id
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)

class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')    # 由于是image，所以这里接受字节500
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)

class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)

# 日期和时间用float类型存储在数据库中，而不是datetime类型。
# 这样可以不必关心数据库的时区转换问题，排序非常简单，显示时
# 只需一个float到str的转换。