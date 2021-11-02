# -*- coding: utf-8 -*-
"""
@File:login.py
@Author:cdf
@Version:1.0
@Description:获取登录token
"""

# from ApiAutoCore.base.api_request import apiRequest
# from ApiAutoCore.base.read_yml import readYaml
# from ApiAutoCore.base.log import Logger
from ApiAutoCore.base.public import des_encrypt
from ApiTestManagerPc.middler.transfer import Transfer

# 忽略证书进行https访问接口
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GetLoginToken:
    """获取登录token"""
    # 初始化实例
    def __init__(self):
        self.Transfer = Transfer()
        self.logger = self.Transfer.logger
        self.apiRequest = self.Transfer.apiRequest
        # 系统配置
        self.config = self.Transfer.config.all_data
        self.login_data = self.config[self.config['set_env']]['login']
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
            'host': '',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
                        }
        self.read_file = self.Transfer.config.all_data

    """获取聘聘云token（功能版和智简版token共用）"""
    # 第一步，登录聘聘云获取companyId
    def pinpin_get_company_id(self, host_flag, sys=None):
        url = '/api/auth/login.json'
        """判断功能版和智简版的host，host_flag=1时为功能版，host_flag=2时为智简版"""
        if host_flag == 1:
            host = self.read_file['headers']['pinpin_host']  # 读取config配置的host
        elif host_flag == 2:
            host = self.read_file['headers']['pinpin_ats_host']  # 读取config配置的host
        self.headers['host'] = host
        # 根据传参切换系统账号，默认走聘聘账号
        if sys == 'manager':
            mobile = self.login_data['manager']
            password = self.login_data['manager_pwd']
        else:
            mobile = self.login_data['mobile']
            password = self.login_data['password']

        """明文的密码转换成密文"""
        self.password = des_encrypt(password, self.config['des_secret_key'], self.config['des_iv'])
        self.params = {'mobile': mobile, 'password': self.password}
        self.logger.debug(f"用户名：{mobile} 密码:{self.password}")
        result = self.apiRequest.send_requests(method='post', url=url, data=self.params, headers=self.headers).json()
        # 判断是否正常获取company_id
        try:
            company_id = result['data'][0]['companyId']
        except Exception as e:
            try:
                self.logger.error(result)
                self.logger.error(
                    '未获得正常获取到companyId\t请确认账号信息：' + '\n' +
                    '账号：' + self.read_file['login']['mobile'] +
                    '\t密码：' + self.read_file['login'][
                        'password'] + repr(e))
            except Exception as e:
                self.logger.error(str(result)+repr(e))
        else:
            self.logger.debug('正常获取到companyId：' + str(company_id))

        finally:
            self.logger.debug('接口响应数据：' + repr(result))
        return company_id

    # 第二步，使用companyId登录获取token
    def pinpin_get_token(self, host_flag, sys=None):
        company_id = self.pinpin_get_company_id(host_flag=host_flag, sys=sys)
        """switch.json接口登录获取token"""
        url_switch = '/api/auth/account/switch.json'
        self.params['companyId'] = company_id
        r = self.apiRequest.send_requests(method='post', url=url_switch, data=self.params, headers=self.headers)
        self.headers['Cookie'] = r.headers['Set-Cookie']
        return self.headers

    # 获取用人经理系统token
    def get_manager_token(self):
        return self.pinpin_get_token(host_flag=2, sys='manager')


if __name__ == '__main__':
    # print('pinpin_get_token：', GetLoginToken().pinpin_get_token(host_flag=1))
    print(GetLoginToken().pinpin_get_token(host_flag=1))
    print(GetLoginToken().pinpin_get_token(host_flag=2))
    print(GetLoginToken().get_manager_token())
    # print(GetLoginToken().apollo_get_token())




