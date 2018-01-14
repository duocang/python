
import www.orm
import www.models


import asyncio





loop = asyncio.get_event_loop()
async def test():
    await www.orm.create_pool(loop = loop,host='localhost', port=3306, user='www-data', password='www-data', db='awesome')

    u = www.models.User(name='Test', email='tes8t1@example.com', passwd='1234567890', image='about:blank', id = '1234')

    await u.save()

loop.run_until_complete(test())


#async def test(loop, **kw):
#    print('fasdsda')
#    u = www.models.User(name=kw.get('name'), email=kw.get('email'), passwd=kw.get('passwd'), image=kw.get('image'))
#    await u.save()
#    await www.orm.destory_pool()
#
#data=dict(name='gaf', email='235123345@qq.com', passwd='1312345', image='about:blank')
#loop=asyncio.get_event_loop()
#loop.run_until_complete(test(loop, **data))
#loop.close()