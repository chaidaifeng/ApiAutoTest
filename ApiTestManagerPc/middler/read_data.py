# -*- coding: utf-8 -*-
"""
@File:read_Data.py
@Author:cdf
@Version:1.0
@Description:data数据读取封装（简化输入）
"""
import os
from ApiAutoCore.base.read_yml import readYaml


def read_biz_data(*file_name):
    """封装读取yaml方法，简化参数输入"""
    path = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
    return readYaml(path.split(os.sep)[-1], 'data', *file_name)


if __name__ == '__main__':
    print(read_biz_data('resume_screening.yml').read_data())


