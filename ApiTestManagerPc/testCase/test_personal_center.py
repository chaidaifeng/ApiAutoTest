# -*- coding:utf-8 -*-
"""
@File: test_personal_center.py
@Author: cdf
@Description:用人经理-个人中心
"""

import pytest
from ..middler.transfer import Transfer
from ..middler.login import GetLoginToken
from ..middler.read_data import read_biz_data
from ..page.personal_center import PersonalCenter
from ..middler.utils import token


@pytest.mark.manager
class TestPersonalCenter:
    Transfer = Transfer()
    read_file = Transfer.config
    apiRequest = Transfer.apiRequest
    UpdateYml = Transfer.UpdateYml
    Asert = Transfer.Asert
    logger = Transfer.logger
    """准备测试数据"""
    all_data = read_biz_data('personal_center.yml').read_data()['parametrize']
    print(all_data)
    env_current = read_file.configEnv()
    # 实例化要获取用例的方法
    PersonalCenter = PersonalCenter()

    @pytest.mark.parametrize("data", all_data)
    def test_personal_center(self, token, data):
        """参数化用例执行"""
        # 用例中参数化数据进行替换
        updata_data = self.UpdateYml.update_yml(str(data)
                                 )
        self.logger.info('参数化更新后的用例数据：' + str(updata_data))

        # 请求接口
        res = self.apiRequest.send_requests(method=updata_data['method'],
                                            url=updata_data['url'],
                                            params=updata_data['data'],
                                            headers=token['manager_headers']
                                            ).json()
        self.logger.info(f'接口响应：{res}')

        # 进行断言
        try:
            assert self.Asert.asert_contrast(data['expect']['status'], data['expect']['data'], res['status'], str(res['data']))
            self.logger.info(f"用例成功：\n{res}")
        except Exception as e:
            self.logger.error("用例失败：\n" + str(e))
            raise

    """场景用例"""
    def test_update_pwd(self):
        """简历筛选-列表查询"""
        # 接口请求
        res = self.PersonalCenter.update_pwd()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            self.logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            self.logger.error('用例失败：\n' + repr(e))
            raise

    def test_logout(self):
        """个人中心-退出登录"""
        # 因为上一个接口操作了修改密码，需要重新登录
        GetLoginToken().get_manager_token()
        # 接口请求
        res = self.PersonalCenter.logout()
        # 进行断言
        try:
            assert str(res['data']) == 'True'
            self.logger.info(f'用例成功：{str(res)}')
        except Exception as e:
            self.logger.error('用例失败：\n' + repr(e))
            raise


if __name__ == '__main__':
    pytest.main()



