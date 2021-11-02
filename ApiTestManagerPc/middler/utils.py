# -*- coding:utf-8 -*-
"""
@File: utils.py
@Author: cdf
@Description:业务常用公共方法
"""

import datetime
import random
import pytest
from ApiTestManagerPc.middler.login import GetLoginToken


@pytest.fixture(scope='session', autouse=True)
def token():
    token = dict()
    token['pp_headers'] = GetLoginToken().pinpin_get_token(host_flag=1)
    token['ats_headers'] = GetLoginToken().pinpin_get_token(host_flag=2)
    token['manager_headers'] = GetLoginToken().get_manager_token()
    yield token


# 随机生成信息
def random_info():
    # 姓名
    name = "张三" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 手机号
    phone = "13" + ''.join(str(random.choice(range(10))) for _ in range(9))
    # 公司名称
    company_name = "华为公司" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 职位名称
    job_name = "产品经理" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 邮箱
    email = "13" + ''.join(str(random.choice(range(10))) for _ in range(9)) + "@test.com"
    # 报表名称
    report_name = "新增报表" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 计算字段名称
    name_formula = "计算字段" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 招聘官网名称
    website_name = "招聘官网" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 招聘官网地址
    website_url = "autosc" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 招聘阶段
    stage_name = "阶段" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 招聘流程
    recruit_name = "招聘流程" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 评价模板名称
    appraise_template_name = "新增模板" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 邮件模板名称
    email_template_name = "新增模板" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 简历名称
    resume_name = "新增简历" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 分组名称
    group_name = "新增分组" + ''.join(str(random.choice(range(10))) for _ in range(5))
    # 人才库名称
    library_name = "新增人才库" + ''.join(str(random.choice(range(10))) for _ in range(5))

    return {'name': name, 'phone': phone, 'company_name': company_name, 'job_name': job_name, 'email': email,
            'report_name': report_name, 'name_formula': name_formula,
            'website_name': website_name, 'website_url': website_url, 'stage_name': stage_name,
            'recruit_name': recruit_name, 'appraise_template_name': appraise_template_name,
            'email_template_name': email_template_name, 'resume_name': resume_name, 'group_name': group_name,
            'library_name': library_name}


# 创建当前日期
def create_month():
    month = []
    month.append(str(datetime.datetime.now().year))
    month.append(str(datetime.datetime.now().month))
    month.append(str(datetime.datetime.now().day + 1))
    date1 = ''.join(month)
    date2 = '-'.join(month)
    return {'date1': date1, 'date2': date2}


