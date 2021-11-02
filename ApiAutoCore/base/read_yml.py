# -*- coding: utf-8 -*-
"""
@File:read_yml.py
@Author:cdf
@Version:3.0
@Description:文件读取修改方法
"""
import ruamel.yaml
from ApiAutoCore.base.public import filePath


class readYaml:
    """初始化文件"""
    def __init__(self, *file_name):     # 传参相对路径+文件名
        # 获取传入文件的路径
        self.file_path = filePath(*file_name)
        # print(self.file_path)
        # 读取文件
        with open(filePath(*file_name), "r", encoding="utf-8") as docs:
            try:
                self.all_data = ruamel.yaml.safe_load(docs)
            except ruamel.yaml.YAMLError as exc:
                print(str(exc))
        docs.close()    # 关闭文件

    # 返回文件数据
    def read_data(self):
        return self.all_data

    # 切换环境配置
    def setConfig(self, env):
        self.all_data['set_env'] = env
        with open(filePath(self.file_path), 'w+', encoding='utf8') as outfile:
            ruamel.yaml.dump(self.all_data, outfile, default_flow_style=False, allow_unicode=True, Dumper=ruamel.yaml.RoundTripDumper)
        outfile.close()

    # # 切换环境配置
    # def set_host(self, host):
    #     self.all_data['set_host'] = host
    #     with open(filePath(self.file_path), 'w+', encoding='utf8') as outfile:
    #         ruamel.yaml.dump(self.all_data, outfile, default_flow_style=False, allow_unicode=True, Dumper=ruamel.yaml.RoundTripDumper)
    #     outfile.close()

    # 设置log等级
    def set_log_level(self, level):
        self.all_data['log_level'] = level
        with open(filePath(self.file_path), 'w+', encoding='utf8') as outfile:
            ruamel.yaml.dump(self.all_data, outfile, default_flow_style=False, allow_unicode=True, Dumper=ruamel.yaml.RoundTripDumper)
        outfile.close()

    # 获取环境host
    def configEnv(self):
        env = self.all_data['set_env']
        return env


if __name__ == '__main__':
    print(readYaml('ApiTestManagerPc', 'middler', 'config.yml').configEnv())
