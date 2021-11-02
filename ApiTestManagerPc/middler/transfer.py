# -*- coding: utf-8 -*-
"""
@File:transfer.py
@Author:cdf
@Version:1.0
@Description:中转base方法，简化调用方法
"""
from ApiAutoCore.base.read_yml import readYaml
from ApiAutoCore.base.api_request import apiRequest
from ApiAutoCore.base.log import Logger
from ApiAutoCore.base.asert_contrast import Asert
from ApiAutoCore.base.update_yml import UpdateYml


class Transfer:
    """初始化方法"""
    def __init__(self):
        # 读取config配置,初始化方法
        self.config = readYaml('ApiTestManagerPc', 'middler', 'config.yml')
        self.logger = Logger(self.config.all_data['project']).get_logger()
        self.apiRequest = apiRequest(self.config.all_data['project'])
        self.Asert = Asert(self.config.all_data['project'])
        self.UpdateYml = UpdateYml(self.config.all_data['project'])


if __name__ == '__main__':
    print(Transfer().logger.error('111'))
