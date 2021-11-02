# -*- coding:utf-8 -*-
"""
@File: test_resume_screening.py
@Author: cdf
@Description:用人经理-筛选
"""

import pytest
from ApiAutoCore.base.api_request import apiRequest
from ApiAutoCore.base.asert_contrast import asert_contrast
from ApiAutoCore.base.log import logger
from ApiAutoCore.base.read_yml import readYaml
from ApiAutoCore.base.update_yml import update_yml
from ..middler.read_data import read_biz_data
from ..middler.login import GetLoginToken
from ..page.resume_screening import ResumeScreening
from ..middler.utils import token


@pytest.mark.manager
class TestResumeScreening:
    """准备测试数据"""
    all_data = read_biz_data('resume_screening.yml').read_data()['parametrize']
    env_current = readYaml('ApiAutoCore', 'config', 'config.yml').configEnv()

    # 初始化
    def setup_class(self):
        self.Request = apiRequest()
        # 获取用人经理token
        token = GetLoginToken().get_manager_token()
        # 实例化要获取用例的方法
        self.ResumeScreening = ResumeScreening(token)

    def test_add_resume(self):
        """面试安排-新增安排面试简历"""
        # 接口请求
        res = self.ResumeScreening.add_resume()
        # 进行断言
        try:
            assert str(res[0]['recommendId']) is not None
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    @pytest.mark.parametrize("data", all_data)
    def test_resume_screening(self, token, data):
        """参数化 执行测试"""
        # 接口中获取参数化用例中所需变量参数
        # 获取筛选列表简历信息
        resume_info = self.ResumeScreening.screening_list()['data']['list'][0]
        resume_id = resume_info['resId']
        recommend_assess_id = resume_info['recommendAssessId']
        recommend_id = resume_info['recommendId']
        # 阶段流程数据
        recruit_info = self.ResumeScreening.recommend_info(recommend_id)['data']
        recruit_process_id = recruit_info['recruitProcessId']
        recruit_stage_id = recruit_info['recruitStageId']

        # 用例中参数化数据进行替换
        updata_data = update_yml(str(data),
                                 resId=str(resume_id),
                                 recommendAssessId=str(recommend_assess_id),
                                 recommendId=str(recommend_id),
                                 recruitProcessId=str(recruit_process_id),
                                 recruitStageId=str(recruit_stage_id)
                                 )
        logger.info('参数化更新后的用例数据：' + str(updata_data))

        # 请求接口
        res = self.Request.send_requests(method=updata_data['method'],
                                         url=updata_data['url'],
                                         params=updata_data['data'],
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
    def test_pass_resume(self):
        """简历筛选-批量筛选通过"""
        # 接口请求
        res = self.ResumeScreening.pass_resume()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    def test_fail_resume(self):
        """简历筛选-批量筛选不通过"""
        # 接口请求
        res = self.ResumeScreening.fail_resume()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    def test_undetermined_resume(self):
        """简历筛选-批量筛选待定"""
        # 接口请求
        res = self.ResumeScreening.undetermined_resume()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    def test_pass_resume_details(self):
        """简历初筛-简历详情-操作通过"""
        # 接口请求
        res = self.ResumeScreening.pass_resume_details()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    def test_fail_resume_details(self):
        """简历初筛-简历详情-操作不通过"""
        # 接口请求
        res = self.ResumeScreening.fail_resume_details()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise

    def test_undetermined_resume_details(self):
        """简历初筛-简历详情-待定"""
        # 接口请求
        res = self.ResumeScreening.undetermined_resume_details()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            logger.error('用例失败：\n' + repr(e))
            raise


if __name__ == '__main__':
    pytest.main()



