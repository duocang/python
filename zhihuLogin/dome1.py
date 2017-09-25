# encoding: utf-8
from http import cookiejar
from http.cookiejar import LoadError
from bs4 import BeautifulSoup
import time
import requests

headers = {
"Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except LoadError:
    print("load cookies failed", "还没有cookie信息")

# 获取xsrf
def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
    return xsrf

# 获取验证码
# 验证码是通过/captcha.gif借口返回的，这里我们将验证码图片下载到当前目录，由人工识别，亦可以使用第三方库来自动识别，比如pytesser
def get_captcha():
    """
    验证码保存到本地，手动识别
    """
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('catcha.jpg', 'wb') as f:
        f.write(r.content)
    captcha = input("验证码：")
    return captcha

# 登录
def login(email, password):
    login_url = 'https://www.zhihu.com/login/email'
    data = {
        'email': email,
        'password': password,
        '_xsrf': get_xsrf(),
        "captcha": get_captcha(),
        'remember_me': 'true'
    }
    response = session.post(login_url, data=data, headers=headers)
    login_code = response.json()
    print(login_code)
    print(login_code['msg'])
    for i in session.cookies:
        print(i)
    session.cookies.save()

if __name__ == '__main__':
    email = "wangxuesong29@gmail.com"
    print("email: wangxuesong29@gmail.com")
    password = input("密码：")
    login(email, password)