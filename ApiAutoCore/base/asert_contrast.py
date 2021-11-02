# -*- coding: utf-8 -*-
"""
@File:asert_contrast.py
@Author:cdf
@Version:1.0
@Description:断言封装
"""

from ApiAutoCore.base.log import Logger


class Asert:

    def __init__(self, project_name):
        self.logger = Logger(project_name).get_logger()

    def asert_contrast(self, code, data, result_code, result_data):
        """验证code和响应数据，可验证一项或两项"""
        # 逾期结果code和data都填写时
        if code and data:
            self.logger.info('进行验证code、data：\n逾期返回：'+str(code) + '\t\t\t实际返回：' + str(result_code))
            self.logger.info('进行验证data、result_data：\n逾期返回：'+str(data) + '\t\t\t实际返回：' + str(result_data))
            try:
                assert code == result_code
                assert data in result_data
                self.logger.info('用例成功')
            except AssertionError as e:
                self.logger.error('用例失败:'+str(e))
                return False
            return True

        # 逾期结果仅有code时
        if code:
            self.logger.info('进行验证code、data：\n逾期返回：'+str(code) + '\t\t\t实际返回：' + str(result_code))
            try:
                assert code == result_code
                self.logger.info('用例成功')
            except AssertionError as e:
                self.logger.error('用例失败:'+str(e))
                return False
            return True

        # 逾期结果仅有data时
        if data:
            self.logger.info('进行验证data、result_data：\n逾期返回：'+str(data) + '\t\t\t实际返回：' + str(result_data))
            try:
                assert data in result_data              # assert data in str(result_data), "包含关系，包含不能是int类型"
                self.logger.info('用例成功')
            except AssertionError as e:
                self.logger.error('用例失败:'+str(e))
                return False
            return True
        else:
            self.logger.error('未设置逾期结果，需设置逾期结果（当前处理为通过）')
            return True


if __name__ == '__main__':
    codes = '200'
    d = '周梅香'
    status_code = '200'
    result_d = "{'name': '周梅香', 'mobile': '13812692824', 'email': 'zhoumeixiang@aimsen.com'," \
               " 'gender': None, 'employeeNo': '100500061'," \
               "/photo/20200508215450/3000000186283153.jpg'}"
    d = Asert('ApiTestManagerPc').asert_contrast(codes, d, status_code, result_d)
    print(d)

