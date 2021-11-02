# -*- coding: utf-8 -*-
"""
@File:__init__.py
@Author:cdf
@Version:1.0
@Description:功能模块配置信息
"""

import random

"""简历配置信息"""

# 人选姓名
resume_name = "autotest"+''.join(str(random.choice(range(10))) for _ in range(9))
# 新建人选手机号
resume_phone = "13"+''.join(str(random.choice(range(10))) for _ in range(9))
# 已有人选手机号
get_resume_phone = "13810523561"
# 人选Email
resume_email = "test@test.com"
# 职位ID
job_id = '80010'

"""职位配置信息"""

