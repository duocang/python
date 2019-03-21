from flask import Flask, jsonify,request
from utils import QssClient
import urllib
import os

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'image_url': 'url from website',
        'ali_url': 'url from ali',
        'done': False
    },
    {
        'id': 2,
        'image_url': 'url from website',
        'ali_url': 'url from ali',
        'done': False
    }
]

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/pics', methods=['POST'])
def create_task():
    if not request.json or not 'image_url' in request.json:
        abort(400)



    urllib.urlretrieve(request.json['image_url'], 'pics\\' + request.json['image_url'].split('/')[-1] ) #先保存图片到本地
    qs = QssClient() #连接服务器
    dir_name = 'location' #设置好服务器保存的文件夹
    full_file_lis = []
    file_path = os.path.join('pics\\', request.json['image_url'].split('/')[-1]) #从本地的保存路径获得图片
    full_file_lis.append(file_path)
    url = qs.upload_list(full_file_lis, dir_name)[0] # 从本地上传图片并获得上传后的地址

    task = {
        'id': tasks[-1]['id'] + 1,
        'image_url': request.json['image_url'],
        'ali_url': url,
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201#返回图片地址的json

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)