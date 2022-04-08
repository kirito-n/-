import json
import sys
import io
import os
import time
import urllib.request
import http.cookiejar
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
#在config.json文件中填入自己的上网账号和密码
with open('config.json',encoding='utf8') as file:
    config = json.load(file)  
#默认http请求的参数
data = {
        'authType':'',
        'userName':config['username'],
        'password':config['password'],
        'validCode':'zh_CN',
        'validCodeFlag':'false',
        'hasValidateNextUpdatePassword':'true',
        'rememberPwd':'false',
        'browserFlag':'zh',
        'hasCheckCode':'false',
        'checkcode':'',
        'hasRsaToken':'false',
        'rsaToken':'',
        'autoLogin':'false',
        'userMac':'',
        'isBoardPage':'false',
        'disablePortalMac':'false',
        'overdueHour':'0',
        'overdueMinute':'0',
        'isAccountMsgAuth':'',
        'validCodeForAuth':'',
        'isAgreeCheck':'0',
       } 
post_data = urllib.parse.urlencode(data).encode('utf-8')

#伪装成浏览器
headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
#工贸上网验证api地址
login_url = 'http://192.168.99.5/PortalServer/Webauth/webAuthAction!login.action'

req = urllib.request.Request(login_url, headers = headers, data = post_data)
cookie = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

#向认证api发送请求
resp = opener.open(req);
#获取api的返回的数据，方便处理
data = json.loads(resp.read().decode('utf-8'))

#封装一个方法方便调用
def func_req():
    resp = opener.open(req);
    data = json.loads(resp.read())
    print('🐡',flush=True)
#判断返回的token是否为空，为空就是认证失败，为字符串就是认证成功
if data['token']:
    print('连接成功---开始冲浪',flush=True);
    time.sleep(2)
    while data['token']:
        #若成功则每两分钟向认证api发送请求
        time.sleep(120)
        try:
            func_req()
        except:
            print('没有网络---冲浪失败',flush=True);
            break
else:
#账号或者密码错误就会报错需要重新运行  
    print('password or username errors!');