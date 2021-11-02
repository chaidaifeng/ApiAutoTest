#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File:log.py
@Author:cdf
@Version:3.0
@Description:logging进行封装
"""


import logging
import time
import os
from logging.handlers import TimedRotatingFileHandler
from ApiAutoCore.base.public import filePath
from ApiAutoCore.base.read_yml import readYaml


class Logger(object):

    def __init__(self, project_name):
        global logPath
        # 从base的config中获取jenkins数据
        logPath = filePath(project_name, 'log')  # 获取log文件的路径
        self.logger = logging.getLogger()
        # 获取日志等级
        level = readYaml(project_name, 'middler', 'config.yml').all_data['log_level']
        if level == 'NOTSET':
            logging.root.setLevel(logging.NOTSET)   # 获取日志等级
            self.consoleOutputLevel = 'ERROR'       # 控制台日志输出级别
            self.fileOutputLevel = 'ERROR'          # 写入日志文件输出级别
        elif level == 'info':
            logging.root.setLevel(logging.INFO)
            self.consoleOutputLevel = 'INFO'
            self.fileOutputLevel = 'INFO'
        elif level == 'debug':
            logging.root.setLevel(logging.DEBUG)
            self.consoleOutputLevel = 'DEBUG'
            self.fileOutputLevel = 'DEBUG'
        elif level == 'waning':
            logging.root.setLevel(logging.WARNING)
            self.consoleOutputLevel = 'WARNING'
            self.fileOutputLevel = 'WARNING'
        elif level == 'error':
            logging.root.setLevel(logging.ERROR)
            self.consoleOutputLevel = 'ERROR'
            self.fileOutputLevel = 'ERROR'
        elif level == 'critical':
            logging.root.setLevel(logging.CRITICAL)
            self.consoleOutputLevel = 'CRITICAL'
            self.fileOutputLevel = 'CRITICAL'
        self.logFileName = time.strftime(f'{str(project_name)}_' + "%Y_%m_%d")+'.log'  # 日志文件的名称：项目名+日期年月日 +'.log'
        self.backupCount = 5  # 最多存放日志的数量

        # 日志输出格式
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s-%(funcName)s-%(lineno)s- \
        %(levelname)s - %(message)s')

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.consoleOutputLevel)
            self.logger.addHandler(console_handler)

            # 每天重新创建一个日志文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(filename=os.path.join(logPath, self.logFileName), when='D',
                                                    interval=1, backupCount=self.backupCount, delay=True,
                                                    encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.fileOutputLevel)
            self.logger.addHandler(file_handler)
        return self.logger


if __name__ == "__main__":
    logger = Logger('ApiTestManagerPc').get_logger()
    # 保存日志文件
    logger.debug("程序调试bug 日志")
    logger.info("程序正常运行 日志 ")
    logger.warning('警告 日志')
    logger.error('程序出错 日志')
    logger.critical('特别严重 日志')
