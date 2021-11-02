# -*- coding: utf-8 -*-
"""
@File:update_yml.py
@Author:cdf
@Version:1.0
@Description:替换yml变量数据
"""
import re
from ApiAutoCore.base.log import Logger


class UpdateYml:
    # 初始化log信息
    def __init__(self, project_name):
        self.logger = Logger(project_name).get_logger()

    # 正则匹配修改对应数据
    def update_yml(self, data, **keys):     # data为待替换的数据；keys为替换的参数如：name='产品经理',phone='18301001111'
        pattern = r'#(.*?)#'
        try:
            while re.findall(pattern, str(data)):
                # 匹配
                key = re.search(pattern, str(data)).group(1)
                self.logger.info(f'{str(keys)}匹配到的参数：{keys[key]}')
                # 替换，得到测试数据
                data = re.sub(pattern, str(keys[key]), str(data), count=1)
        except Exception as e:
            self.logger.error(f'未找到#{str(keys)}#的替换参数，请检查变量参数是否缺失')
            raise e
        if isinstance(data, str):
            return eval(data)
        else:
            return data


if __name__ == '__main__':
    d = {'id': None, 'customerId': 309993, 'selectedName': None,  'appellation': 2, 'name': '#name#', 'mobile': '#phone#',
            'tel': 22222222223, 'ext': '中文', 'fax': 2131, 'position': 1233, 'email': '23213@123.com', 'wechat': 123213,
            'qq': 1231, 'roleType': 4, 'keyPersonFlag': None, 'year': 1990, 'month': 4, 'day': 6,
            'entryTime': 1627747200000, 'preference': 21313321, 'birthday': '1990-04-06', 'company': 1}

    data2 = {'customerId': 309993, 'selectedName': '#selectedName#', 'name': '#name#'}
    print(UpdateYml('ApiTestManagerPc').update_yml(d, name='a', phone='1512412412'))


