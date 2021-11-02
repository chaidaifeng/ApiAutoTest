# -*- coding: utf-8 -*-
"""
@File:run_all.py
@Author:cdf
@Version:1.0
@Description:执行调试用例
"""

import subprocess
import pytest
from ApiAutoCore.base.public import filePath
from ApiTestManagerPc.conftest import read_config

if __name__ == '__main__':
    env = 'test'
    read_config.setConfig(env)
    fileName = 'test_personal_center.py'
    TestCase = filePath('ApiTestManagerPc', 'testCase',  fileName
                        )  # 指定执行测试用例
    # recruitment or job or more or options or process
    markCase = '-m'+'manager'  # 指定执行标记用例
    pytest.main(["-s", "-v", TestCase,  #markCase,
                 "--alluredir", "report/result", "--junit-xml", "report/result.xml", "--clean-alluredir", "--durations=0"])

    # allure生成报表，并启动程序
    subprocess.call('allure generate report/result/ -o report/html --clean', shell=True)
    subprocess.call('allure open -h 127.0.0.1 -p 9999 ./report/html', shell=True)

    # # 查看allure服务进程
    # process = subprocess.call('netstat -ano | findstr "9999"', shell=True)
    # print(process)
    #
    # # 手动杀掉进程
    # pid = '14192'
    # subprocess.call('taskkill -pid %s -f' % pid, shell=True)
