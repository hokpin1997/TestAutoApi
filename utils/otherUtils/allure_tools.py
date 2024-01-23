# -*- coding:utf-8 -*-
import json
import allure


def allure_step(step, var):
    """
    :param step: 赋值步骤名称及上传附件
    :param var: 附件内容
    """
    with allure.step(step):
        allure.attach(json.dumps(str(var), ensure_ascii=False, indent=4), step, allure.attachment_type.JSON)


def allure_step_no(step):
    """
    无附件的操作步骤
    :param step: 步骤名称
    :return:
    """
    with allure.step(step):
        pass