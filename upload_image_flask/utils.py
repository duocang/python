import sys
import os
import oss2 # 阿里云链接
from boto3.session import Session
import boto3
import uuid
import requests

class QssClient(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(QssClient, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        #Client初始化
        ACCESS_ID = 'flask_test'
        SECRET_KEY = 'c626ad4c6c06eb4d66f588b3edab540832d2d31afcaecbf4cd4cbd3c1266ab88'
        url='https://nyc3.digitaloceanspaces.com'
        session = Session(ACCESS_ID, SECRET_KEY)
        self.client = session.client('s3', endpoint_url=url)
        #Client初始化结束
        #列出该用户拥有的桶
        print [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]
        sself.client.create_bucket(Bucket="您的bucket名") #默认是私有的桶
        # auth = #认证的秘钥
        # endpoint = #服务器域名
        # bucket_name =#服务器的盘名
        # self.bucket = oss2.Bucket(auth, endpoint, bucket_name, connect_timeout=30)
        # super(QssClient, self).__init__()

    def upload(self, file_path, dir_name='文件夹名'):
        file_name = str(uuid.uuid1())
        with open(file_path, 'rb') as f:
            remote = '%s/%s.jpg' % (dir_name, str(file_name))
            # result = self.bucket.put_object(remote, f)
            result = self.client.upload_file()
            file_url = result.resp.response.url
            f.close()
        os.remove(file_path)
        return file_url

    def upload_list(self, file_list, dir_name='location'):
        file_url_list = []
        for f in file_list:
            file_url = self.upload(f, dir_name=dir_name)
            file_url_list.append(file_url)
        return file_url_list