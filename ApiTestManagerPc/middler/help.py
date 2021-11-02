# -*- coding:utf-8 -*-
"""
@File: help.py
@Author: jiayf
@Description: 中间件方法，方便后续测试数据中使用
"""
import random
from datetime import datetime
import time
import string
from ApiAutoCore.base.api_request import apiRequest


class Help:

    # 获取当前日期
    def current_date(self):
        today = datetime.now().strftime('%Y%m%d')
        return today

    # 客户名称
    def customer_name(self):
        customer_name = self.current_date()+'testcustomer' + ''.join(random.sample(string.digits, 1))
        return customer_name

    # 随机生成名称
    def text_name(self):
        text_name = 'test' + ''.join(random.sample(string.ascii_lowercase, 8))
        return text_name

    # 创建手机号
    def create_phone(self):
        phone_num = '1' + ''.join(random.sample(string.digits, 10))
        return phone_num

    # 将yyyymmdd格式的日期，转换为转换据1970-01-01的毫秒数
    def secondsfrom1970(self, date):
        time1 = datetime.strptime(date, "%Y%m%d")
        millisecondsfrom1970 = str(int(time.mktime(time1.timetuple()) *1000))
        return millisecondsfrom1970

    # 文件上传方法
    def upload_files(self, filepath, url, headers, data):
        filename = filepath.split('\\')[-1]
        try:
            while headers['Content-Type']:
                del headers['Content-Type']
                break
        except:
            print(f'"Content-Type"不存在,无需删除')
        files = {'file': (filename, open(filepath, "rb"))}
        result = apiRequest().send_requests(method='post', url=url, data=data, files=files, headers=headers).json()
        id = result['data']['id']
        fileName = result['data']['fileName']
        filePath = result['data']['filePath']
        return {'id': id, 'fileName': fileName, 'filePath': filePath}

    def upload_files_back(self, filepath, url, headers, data):
        filename = filepath.split('\\')[-1]
        try:
            while headers['Content-Type']:
                del headers['Content-Type']
                break
        except:
            print(f'"Content-Type"不存在,无需删除')
        files = {'file': (filename, open(filepath, "rb"))}
        result = apiRequest().send_requests(method='post', url=url, data=data, files=files, headers=headers).json()
        return result


if __name__ == '__main__':
    helpper = Help()

    print(helpper.customer_name())
    ############ 测试日期转换毫秒方法##########
    # today = time.strftime('%Y%m%d')
    # print(helpper.secondsfrom1970(today))

    # ###### 测试”文件上传方法“ ###############
    # filepath = "D:\\HuaYong\\Code\\PPApiTest\\data\\crm\\111.pdf"
    # url = "/api/file/upload.json"
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44', 'host': 'crm.hua-yong.com', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Cookie': 'hy_auth=8A81451395CE4943B71E73181E99BA68; Expires=Sun, 15-Aug-2021 10:35:10 GMT; Path=/, hy_user="eyJ0ZWFtTmFtZSI6bnVsbCwiYnJhbmRzIjpbIjEiLCIyIiwiMyJdLCJyYW5rU2VyeSI6IlQwIiwicmVnaW9uTmFtZSI6bnVsbCwiYnVzaW5lc3NOYW1lIjpudWxsLCJicmFuY2hOYW1lIjpudWxsLCJwaG90byI6IiIsInJlZ2lvbk5vIjpudWxsLCJ0ZWFtTm8iOm51bGwsImJ1c2luZXNzTm8iOm51bGwsInBob25lIjoiMTg2MTgzMDIxODAiLCJuYW1lIjoi5YiY5Lu75rSqIiwiY29tcGFueSI6NCwiam9iTnVtYmVyIjoiMzAwMTAwNTEwIiwiZW1haWwiOiJsaXVyZW5ob25nQGh1YS15b25nLmNvbSIsImJyYW5jaE5vIjpudWxsfQ=="; Version=1; Max-Age=288000; Expires=Sun, 15-Aug-2021 10:35:10 GMT; Path=/'}
    # data = {"company": "1", "source": "3"}
    # print(helpper.upload_files(filepath, url, headers, data))
