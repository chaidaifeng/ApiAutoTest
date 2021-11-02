# -*- coding:utf-8 -*-
"""
@File: test_interview_arrangement.py
@Author: cdf
@Description:用人经理-面试安排
"""

import pytest
from ApiAutoCore.base.api_request import apiRequest
from ApiAutoCore.base.asert_contrast import asert_contrast
from ApiAutoCore.base.log import logger
from ApiAutoCore.base.read_yml import readYaml
from ApiAutoCore.base.update_yml import update_yml
from ..middler.read_data import read_biz_data
from ..middler.login import GetLoginToken
from ..page.interview_arrangement import InterviewArrangement
from ..middler.utils import create_month
from ..page.personal_center import PersonalCenter
from ..middler.utils import token


@pytest.mark.manager
class TestInterviewArrangement:
    """准备测试数据"""
    all_data = read_biz_data('interview_arrangement.yml').read_data()['parametrize']
    env_current = readYaml('ApiAutoCore', 'config', 'config.yml').configEnv()

    # 初始化
    def setup_class(self):
        self.Request = apiRequest()
        # 获取用人经理token
        token = GetLoginToken().get_manager_token()
        # 实例化要获取用例的方法
        self.InterviewArrangement = InterviewArrangement(token)
        self.PersonalCenter = PersonalCenter()

    def test_add_resume(self):
        """简历筛选-新增筛选简历"""
        # 接口请求
        res = self.InterviewArrangement.add_resume()
        # 进行断言
        try:
            assert str(res) is not None
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    @pytest.mark.parametrize("data", all_data)
    def test_interview_arrangement(self, token, data):
        """参数化 执行测试"""
        # 接口中获取参数化用例中所需变量参数
        # 获取面试列表简历信息
        resume_info = self.InterviewArrangement.get_interview_list()['data']['list'][-1]
        interview_id = resume_info['id']
        # 当前日历数据
        month = create_month()['date1']
        # 获取当前用人经理id
        user_id = self.PersonalCenter.get_account_info()['data']['id']


        # 用例中参数化数据进行替换
        updata_data = update_yml(str(data),
                                 interviewIds=str(interview_id),
                                 month=str(month),
                                 interviewerId=str(user_id)
                                 )
        logger.info('参数化更新后的用例数据：' + str(updata_data))

        if updata_data['method'] == 'GET':
            # 请求接口
            res = self.Request.send_requests(method=updata_data['method'],
                                             url=updata_data['url'],
                                             params=updata_data['data'],
                                             headers=token['manager_headers']
                                             ).json()
        else:
            # 请求接口
            res = self.Request.send_requests(method=updata_data['method'],
                                             url=updata_data['url'],
                                             data=updata_data['data'],
                                             headers=token['manager_headers']
                                             ).json()
        logger.info(f'接口响应：{res}')

        # 进行断言
        try:
            assert asert_contrast(data['expect']['status'], data['expect']['data'], res['status'], str(res['data']))
            logger.info(f"用例成功：\n{res}")
        except Exception as e:
            logger.error("用例失败：\n" + str(e))
            raise

    """场景用例"""
    def test_interview_pass(self):
        """数据模式-操作通过"""
        # 接口请求
        res = self.InterviewArrangement.interview_pass()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    def test_interview_fail(self):
        """数据模式-操作不通过"""
        # 接口请求
        res = self.InterviewArrangement.interview_fail()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    def test_interview_undetermined(self):
        """数据模式-操作待定"""
        # 接口请求
        res = self.InterviewArrangement.interview_undetermined()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    def test_no_interview(self):
        """数据模式-操作未面试"""
        # 接口请求
        res = self.InterviewArrangement.no_interview()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    def test_list_no_interview(self):
        """面试安排列表中操作未面试"""
        # 接口请求
        res = self.InterviewArrangement.list_no_interview()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    def test_save_interview_date(self):
        """设置面试时间保存"""
        # 接口请求
        res = self.InterviewArrangement.save_interview_date()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise


if __name__ == '__main__':
    pytest.main()



