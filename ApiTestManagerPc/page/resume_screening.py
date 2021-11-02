# -*- coding:utf-8 -*-
"""
@File: resume_screening.py
@Author: cdf
@Description: 用人经理-简历筛选
"""

from ApiAutoCore.base.api_request import apiRequest
from ApiAutoCore.base.log import logger
from ApiAutoCore.base.read_yml import readYaml
from ApiAutoCore.base.update_yml import update_yml
from ApiTestManagerPc.middler.read_data import read_biz_data
from ApiTestManagerPc.middler.login import GetLoginToken
from ApiTestPinPin.page.ats_recruitment_process import RecruitmentProcess


class ResumeScreening:
    """用人经理用例方法"""
    def __init__(self, header):
        self.apiRequest = apiRequest()
        # 获取用人经理token
        self.header = header
        # 读取全部测试数据
        self.data = read_biz_data('resume_screening.yml').read_data()
        # 读取设置全部配置文件数据
        self.read_file = readYaml('ApiAutoCore', 'config', 'config.yml').read_data()
        # 读取到登录数据
        self.login_data = self.read_file[self.read_file['set_env']]['login']
        # 调用其他方法
        self.RecruitmentProcess = RecruitmentProcess(GetLoginToken().pinpin_get_token(host_flag=2))

    def add_resume(self):
        """添加推荐人选到初筛"""
        # 创建订单，获取人选id
        resume_info = self.RecruitmentProcess.add_recommend_order()
        logger.debug('创建的订单数据：' + str(resume_info))
        # 获取订单信息
        recommend_info = self.RecruitmentProcess.get_recommend_info(resume_info['resumeId'])
        # 操作订单推送给用人经理
        self.RecruitmentProcess.get_recommend_multi(recommend_info[0]['recommendId'])
        return recommend_info

    def screening_list(self):
        """简历筛选-列表查询"""
        # 获取用例数据
        all_data = self.data['screening_list']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data)
        logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            params=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def pass_resume(self):
        """简历筛选-批量筛选通过"""
        # 创建推荐简历
        resume_info = self.add_resume()
        logger.debug('创建的简历：\n' + str(resume_info))
        # 获取评价id
        recommend_assess_id = self.screening_list()['data']['list'][0]['recommendAssessId']

        # 获取用例数据
        all_data = self.data['pass_resume']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data, recommendAssessIds=str(recommend_assess_id))
        logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def fail_resume(self):
        """简历筛选-批量筛选不通过"""
        # 创建推荐简历
        resume_info = self.add_resume()
        logger.debug('创建的简历：\n' + str(resume_info))
        # 获取评价id
        recommend_assess_id = self.screening_list()['data']['list'][0]['recommendAssessId']

        # 获取用例数据
        all_data = self.data['fail_resume']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data, recommendAssessIds=str(recommend_assess_id))
        logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def undetermined_resume(self):
        """简历筛选-批量筛选待定"""
        # 创建推荐简历
        resume_info = self.add_resume()
        logger.debug('创建的简历：\n' + str(resume_info))
        # 获取评价id
        recommend_assess_id = self.screening_list()['data']['list'][0]['recommendAssessId']

        # 获取用例数据
        all_data = self.data['undetermined_resume']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data, recommendAssessIds=str(recommend_assess_id))
        logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def recommend_info(self, recommend_id):
        """简历初筛-简历详情"""
        # 获取用例数据
        all_data = self.data['recommend_info']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data, recommendId=str(recommend_id))
        logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            params=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def pass_resume_details(self):
        """简历初筛-简历详情-操作通过"""
        # # 创建推荐简历
        # resume_info = self.add_resume()
        # logger.debug('创建的简历：\n' + str(resume_info))
        # 获取评价id
        recommend_assess_id = self.screening_list()['data']['list'][0]['recommendAssessId']
        # 获取用例数据
        all_data = self.data['pass_resume_details']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data, recommendAssessId=str(recommend_assess_id))
        logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def fail_resume_details(self):
        """简历初筛-简历详情-操作不通过"""
        # 创建推荐简历
        resume_info = self.add_resume()
        logger.debug('创建的简历：\n' + str(resume_info))
        # 获取评价id
        recommend_assess_id = self.screening_list()['data']['list'][0]['recommendAssessId']

        # 获取用例数据
        all_data = self.data['fail_resume_details']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data, recommendAssessId=str(recommend_assess_id))
        logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def undetermined_resume_details(self):
        """简历初筛-简历详情-待定"""
        # 创建推荐简历
        resume_info = self.add_resume()
        logger.debug('创建的简历：\n' + str(resume_info))
        # 获取评价id
        recommend_assess_id = self.screening_list()['data']['list'][0]['recommendAssessId']

        # 获取用例数据
        all_data = self.data['undetermined_resume_details']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data, recommendAssessId=str(recommend_assess_id))
        logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

if __name__ == '__main__':
    print(ResumeScreening(GetLoginToken().get_manager_token()).add_resume())
