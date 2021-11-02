# -*- coding: utf-8 -*-
"""
@File:api_request.py
@Author:cdf
@Version:3.0
@Description:request请求封装
"""
import datetime
import requests
from ApiAutoCore.base.read_yml import readYaml
from ApiAutoCore.base.log import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class apiRequest:

    def __init__(self, project_name):
        self.read_data = readYaml(project_name, 'middler', 'config.yml')   # 读取配置文件
        self.config_env = self.read_data.configEnv()    # 获取所属环境配置
        self.base_url = self.read_data.all_data[self.config_env]['host']
        self.logger = Logger(project_name).get_logger()

    """封装https请求，根据实际情况传参"""
    def send_requests(self, method, url, data=None, params=None, headers=None, cookies=None,
                      json=None, files=None, auth=None, timeout=None, proxies=None,
                      verify=False, cert=None):    # 禁用SSL证书验证verify=False
        url = ''.join(self.base_url + url)
        start_time = datetime.datetime.now()
        res = requests.request(method=method, url=url, data=data, params=params, headers=headers,
                               cookies=cookies, json=json, files=files, auth=auth, timeout=timeout,
                               proxies=proxies, verify=verify, cert=cert)
        end_time = datetime.datetime.now()
        self.logger.debug('请求内容：' + str(res.request.body))
        self.logger.debug('请求地址：' + str(res.url))
        # self.logger.debug('接口返回：' + str(res))
        self.logger.debug('请求头：' + str(res.request.headers))
        self.logger.critical('url：' + str(res.url) + '\ntime：' + str(round((end_time - start_time).total_seconds(), 5)))
        # self.logger.critical('url：' + str(res.url) + '\nrequest中的time：' + str(res.elapsed.total_seconds()))

        return res


if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
               'host': 's.pinpin.com',
               # 'Content-Type': 'application/pdf',
               'Cookie': 'hy_data_2020_id=17b2f38622f88e-0bce6541f96ffb-3d385d08-1049088-17b2f38623051d; hy_data_2020_js_sdk=%7B%22distinct_id%22%3A%2217b2f38622f88e-0bce6541f96ffb-3d385d08-1049088-17b2f38623051d%22%2C%22site_id%22%3A1216%2C%22user_company%22%3A1346%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%2217b2f38622f88e-0bce6541f96ffb-3d385d08-1049088-17b2f38623051d%22%7D; LiveWSALA33200344=72358b7af7c946e5b4d4ccbafdaebcf7; NALA33200344fistvisitetime=1628584829944; pvuvMachineId=d5356a2545394322a33461aacf56c898; Hm_lvt_2fe0d8bb16537140e266bfe55a157d37=1628584829,1628647373; LiveWSALA33200344sessionid=5ca757ce56be47ed91929f2da1bee4cc; NALA33200344visitecounts=2; NALA33200344lastvisitetime=1628648826961; NALA33200344visitepages=35; Hm_lpvt_2fe0d8bb16537140e266bfe55a157d37=1628648827; token=b299e16916fb555cf6d93c5253fc8aa8'
               }
    urls = '/pfapi/bside/pinpincloud/exam/listexaminees.json?examStatus=-1&pageSize=20&pageNo=1'
    data = ''
    r = apiRequest('ApiTestManagerPc').send_requests(method='GET', url=urls, headers=headers).json()
    print(r)
