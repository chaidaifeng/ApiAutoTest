# -*- coding:utf-8 -*-
"""
@File: personal_center.py
@Author: cdf
@Description: 用人经理-个人中心
"""


from ApiAutoCore.base.public import des_encrypt
from ..middler.transfer import Transfer
from ..middler.read_data import read_biz_data
from ..middler.login import GetLoginToken


class PersonalCenter:
    """用人经理用例方法"""
    def __init__(self):
        self.Transfer = Transfer()
        self.apiRequest = self.Transfer.apiRequest
        self.UpdateYml = self.Transfer.UpdateYml
        self.logger = self.Transfer.logger
        # 读取设置全部配置文件数据
        self.read_file = self.Transfer.config.all_data
        # 获取用人经理token
        self.header = GetLoginToken().get_manager_token()
        # 读取全部测试数据
        self.data = read_biz_data('personal_center.yml').read_data()
        # 读取到登录数据
        self.login_data = self.read_file[self.read_file['set_env']]['login']

    def get_account_info(self):
        """个人中心-获取公司及个人信息"""
        # 获取用例数据
        all_data = self.data['get_account_info']
        # 用例中参数化数据进行替换
        updata_data = self.UpdateYml.update_yml(all_data)
        self.logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            params=updata_data['data'],
                                            headers=self.header).json()
        self.logger.debug('接口响应：\n' + str(res))
        return res

    def update_pwd(self):
        """个人中心-修改密码"""
        # 获取当前账号密码
        password = des_encrypt(self.login_data['manager_pwd'], self.read_file['des_secret_key'], self.read_file['des_iv'])

        # 获取用例数据
        all_data = self.data['update_pwd']
        # 用例中参数化数据进行替换
        updata_data = self.UpdateYml.update_yml(all_data, newPassword=str(password))
        self.logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        self.logger.debug('接口响应：\n' + str(res))
        return res

    def logout(self):
        """个人中心-退出登录"""
           # 获取用例数据
        all_data = self.data['logout']
        # 用例中参数化数据进行替换
        updata_data = self.UpdateYml.update_yml(all_data)
        self.logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        self.logger.debug('接口响应：\n' + str(res))
        return res

if __name__ == '__main__':
    print(PersonalCenter().update_pwd())
