# -*- coding: utf-8 -*-
"""
@File:conf_test.py
@Author:cdf
@Version:1.0
@Description:自定义pytest关键字
"""


import pytest
# from ApiAutoCore.base.log import logger
# from ApiAutoCore.base.read_yml import readYaml
from ApiTestManagerPc.middler.transfer import Transfer

Transfer = Transfer()
logger = Transfer.logger
read_config = Transfer.config


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", help="env：表示测试环境，默认dev环境"
    )
    logger.debug('添加pytest自定义参数:--env')


@pytest.fixture(autouse=True, scope='session')    # pytest.fixture标签进行获取自定义参数
def set_env(request):
    # 修改配置环境
    set_env = request.config.getoption("--env")
    if set_env:
        read_config.setConfig(set_env)
    logger.info('当前环境：' + str(read_config.read_data()['set_env']))
    yield


if __name__ == '__main__':
    pytest.main(['-s'])

