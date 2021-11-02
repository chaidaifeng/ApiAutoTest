# -*- coding:utf-8 -*-
"""
@File: mysql_query.py
@Author: jiayf
@Description: 封装数据库查询方法
"""
import mysql.connector
from ApiAutoCore.base.log import logger
from ApiAutoCore.base.read_yml import readYaml


class DBHandler:
    # 初始化
    def __init__(self, host, port, user, password, database, charset='utf8', **kwargs):
        # 建立连接
        self.conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database, charset=charset, **kwargs)
        # 创建路由
        self.cursor = self.conn.cursor()

    # 查询sql
    def query(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            logger.error(e)
            raise e

    # 关闭连接
    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':

    read_data = readYaml('ApiAutoCore', 'config', 'config.yml')  # 读取配置文件

    config_env = read_data.config_env()
    host = read_data.all_data[config_env]['db_host']
    user = read_data.all_data[config_env]['db_user']
    password = read_data.all_data[config_env]['db_password']
    port = 3306
    database = 'awa_customer'
    db = DBHandler(host, port, user, password, database)
    sql = 'select * from customer where id in (3);'

    result = db.query(sql)
    print(result)
    db.close()

