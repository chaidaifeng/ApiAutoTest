# -*- coding:utf-8 -*-
"""
@File: interview_arrangement.py
@Author: cdf
@Description: 用人经理-安排面试
"""

from ApiAutoCore.base.api_request import apiRequest
from ApiAutoCore.base.log import logger
from ApiAutoCore.base.read_yml import readYaml
from ApiAutoCore.base.update_yml import update_yml
from ApiTestManagerPc.middler.read_data import read_biz_data
from ApiTestManagerPc.middler.utils import create_month
from ApiTestManagerPc.middler.login import GetLoginToken
from ApiTestManagerPc.page.personal_center import PersonalCenter
from ApiTestPinPin.page.ats_recruitment_process import RecruitmentProcess


class InterviewArrangement:
    """用人经理用例方法"""
    def __init__(self, header):
        self.apiRequest = apiRequest()
        # 获取用人经理token
        self.header = header
        # 读取全部测试数据
        self.data = read_biz_data('interview_arrangement.yml').read_data()
        # 读取设置全部配置文件数据
        self.read_file = readYaml('ApiAutoCore', 'config', 'config.yml').read_data()
        # 读取到登录数据
        self.login_data = self.read_file[self.read_file['set_env']]['login']
        # 调用其他方法
        self.RecruitmentProcess = RecruitmentProcess(GetLoginToken().pinpin_get_token(host_flag=2))

    def add_resume(self):
        """添加推荐人选到面试"""
        # 创建订单，获取人选id
        resume_info = self.RecruitmentProcess.add_recommend_order()
        logger.debug('创建的订单数据：' + str(resume_info))
        resume_id = resume_info['resumeInfo']['resumeId']

        # 获取订单信息
        recommend_info = self.RecruitmentProcess.get_recommend_info(resume_id)
        logger.debug('订单其他信息：' + str(recommend_info))
        recommend_id = recommend_info[0]['recommendId']
        job_id = recommend_info[0]['jobId']
        job_name = recommend_info[0]['jobName']
        recruit_process_id = recommend_info[0]['recruitProcessId']

        # 获取面试阶段
        recruit_stage = self.RecruitmentProcess.get_process_stage(recruit_process_id)
        recruit_stage_id = recruit_stage['data'][1]['id']
        logger.debug('获取面试阶段id:' + str(recruit_stage_id))

        # 操作订单到面试阶段
        self.RecruitmentProcess.change_recommend_stage(recommend_id, recruit_stage_id)

        # 操作安排面试给用人经理
        self.RecruitmentProcess.save_interview_arrange(resume_info['resumeId'], recommend_id, job_id, job_name)
        return resume_info

    def get_interview_list(self):
        """面试安排-待面试列表"""
        # 获取用例数据
        all_data = self.data['get_interview_list']
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

    def get_template(self, interview_id):
        """获取简历详情中模板信息"""
        # 获取用例数据
        all_data = self.data['get_template']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data, interviewId=str(interview_id))
        logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            params=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def get_appraise_question(self, appraise_template_id):
        """获取简历详情中评价问题"""
        # 获取用例数据
        all_data = self.data['get_appraise_question']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data, appraiseTemplateId=str(appraise_template_id))
        logger.debug(f'参数化更新后的用例数据：{updata_data}')

        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            params=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def interview_pass(self):
        """数据模式-操作通过"""
        # 创建推荐简历
        resume_info = self.add_resume()
        logger.debug('创建的简历：\n' + str(resume_info))
        # 获取评价信息
        interview_info = self.get_interview_list()['data']['list'][-1]
        interview_id = interview_info['id']
        # 获取模板信息
        template_id = self.get_template(interview_id)['data']['interviewAppraiseTemplateId']
        # 获取模板问题
        question_info = self.get_appraise_question(template_id)['data']['questionList']
        question_id = question_info[0]['id']
        question_item_dto_id = question_info[0]['questionItemDtoList'][0]['id']     # 获取通过id
        question_remark_id = question_info[1]['id']

        # 获取用例数据
        all_data = self.data['interview']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data,
                                 interviewId=str(interview_id),
                                 questionId=str(question_id),
                                 questionItemDtoId=str(question_item_dto_id),
                                 questionRemarkId=str(question_remark_id),
                                 )
        logger.debug(f'参数化更新后的用例数据：{updata_data}')
        # 处理字典中列表数据
        updata_data = eval(str(updata_data).replace('[', '"[').replace(']', ']"'))
        logger.debug(f'处理列表转换后数据：' + str(updata_data['data']))
        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def interview_fail(self):
        """数据模式-操作不通过"""
        # 创建推荐简历
        resume_info = self.add_resume()
        logger.debug('创建的简历：\n' + str(resume_info))
        # 获取评价信息
        interview_info = self.get_interview_list()['data']['list'][-1]
        interview_id = interview_info['id']
        # 获取模板信息
        template_id = self.get_template(interview_id)['data']['interviewAppraiseTemplateId']
        # 获取模板问题
        question_info = self.get_appraise_question(template_id)['data']['questionList']
        question_id = question_info[0]['id']
        question_item_dto_id = question_info[0]['questionItemDtoList'][1]['id']     # 获取不通过id
        question_remark_id = question_info[1]['id']

        # 获取用例数据
        all_data = self.data['interview']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data,
                                 interviewId=str(interview_id),
                                 questionId=str(question_id),
                                 questionItemDtoId=str(question_item_dto_id),
                                 questionRemarkId=str(question_remark_id),
                                 )
        logger.debug(f'参数化更新后的用例数据：{updata_data}')
        # 处理字典中列表数据
        updata_data = eval(str(updata_data).replace('[', '"[').replace(']', ']"'))
        logger.debug(f'处理列表转换后数据：' + str(updata_data['data']))
        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def interview_undetermined(self):
        """数据模式-操作待定"""
        # 创建推荐简历
        resume_info = self.add_resume()
        logger.debug('创建的简历：\n' + str(resume_info))
        # 获取评价信息
        interview_info = self.get_interview_list()['data']['list'][-1]
        interview_id = interview_info['id']
        # 获取模板信息
        template_id = self.get_template(interview_id)['data']['interviewAppraiseTemplateId']
        # 获取模板问题
        question_info = self.get_appraise_question(template_id)['data']['questionList']
        question_id = question_info[0]['id']
        question_item_dto_id = question_info[0]['questionItemDtoList'][2]['id']     # 获取不通过id
        question_remark_id = question_info[1]['id']

        # 获取用例数据
        all_data = self.data['interview']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data,
                                 interviewId=str(interview_id),
                                 questionId=str(question_id),
                                 questionItemDtoId=str(question_item_dto_id),
                                 questionRemarkId=str(question_remark_id),
                                 )
        logger.debug(f'参数化更新后的用例数据：{updata_data}')
        # 处理字典中列表数据
        updata_data = eval(str(updata_data).replace('[', '"[').replace(']', ']"'))
        logger.debug(f'处理列表转换后数据：' + str(updata_data['data']))
        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def no_interview(self):
        """数据模式-操作未面试"""
        # 创建推荐简历
        resume_info = self.add_resume()
        logger.debug('创建的简历：\n' + str(resume_info))
        # 获取评价信息
        interview_info = self.get_interview_list()['data']['list'][-1]
        interview_id = interview_info['id']
        # 获取模板信息
        template_id = self.get_template(interview_id)['data']['interviewAppraiseTemplateId']
        # 获取模板问题
        question_info = self.get_appraise_question(template_id)['data']['questionList']
        question_id = question_info[0]['id']
        question_item_dto_id = question_info[0]['questionItemDtoList'][3]['id']     # 获取不通过id
        question_remark_id = question_info[1]['id']

        # 获取用例数据
        all_data = self.data['interview']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data,
                                 interviewId=str(interview_id),
                                 questionId=str(question_id),
                                 questionItemDtoId=str(question_item_dto_id),
                                 questionRemarkId=str(question_remark_id),
                                 )
        logger.debug(f'参数化更新后的用例数据：{updata_data}')
        # 处理字典中列表数据
        updata_data = eval(str(updata_data).replace('[', '"[').replace(']', ']"'))
        logger.debug(f'处理列表转换后数据：' + str(updata_data['data']))
        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def list_no_interview(self):
        """面试安排列表中操作未面试"""
        # 创建推荐简历
        resume_info = self.add_resume()
        logger.debug('创建的简历：\n' + str(resume_info))
        # 获取评价信息
        interview_info = self.get_interview_list()['data']['list'][-1]
        interview_id = interview_info['id']

        # 获取用例数据
        all_data = self.data['list_no_interview']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data,
                                 interviewId=str(interview_id)
                                 )
        logger.debug(f'参数化更新后的用例数据：{updata_data}')
        # 处理字典中列表数据
        updata_data = eval(str(updata_data).replace('[', '"[').replace(']', ']"'))
        logger.debug(f'处理列表转换后数据：' + str(updata_data['data']))
        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res

    def save_interview_date(self):
        """设置面试时间保存"""
        # 获取当前用人经理id
        user_id = PersonalCenter().get_account_info()['data']['id']
        # 生成当前日期
        interview_date = create_month()['date2']

        # 获取用例数据
        all_data = self.data['save_interview_date']
        # 用例中参数化数据进行替换
        updata_data = update_yml(all_data,
                                 interviewerId=str(user_id),
                                 interviewDate=str(interview_date)
                                 )
        logger.debug(f'参数化更新后的用例数据：{updata_data}')
        # 处理字典中列表数据
        updata_data = eval(str(updata_data).replace('[', '"[').replace(']', ']"'))
        logger.debug(f'处理列表转换后数据：' + str(updata_data['data']))
        # 请求用例接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            data=updata_data['data'],
                                            headers=self.header).json()
        logger.debug('接口响应：\n' + str(res))
        return res


if __name__ == '__main__':
    print(InterviewArrangement(GetLoginToken().get_manager_token()).add_resume())
