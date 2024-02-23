# -*- coding:utf-8 -*-
import allure
import pytest
from operation.register import phone_register
from utils.logUtils.logger import logger
from utils.otherUtils.read_data import GetTestCase, ensure_path_sep
from utils.otherUtils.allure_tools import allure_step_no, allure_step


case_ids = ['test_register']
# 从缓存中读取用例数据
test_data = GetTestCase.case_data(case_ids)


def step_1(step):
    step = f"步骤1 ==>> {step}"
    allure_step_no(step)
    logger.info(step)


@allure.epic("注册页面")
class TestRegisterPage:

    @allure.feature("注册")
    @allure.description("注册账号场景")
    @pytest.mark.parametrize("test_data", test_data["test_register"],
                             ids=[i['detail'] for i in test_data["test_register"]])
    def test_register(self, test_data):
        logger.info("*************** 开始执行用例 ***************")
        detail = test_data["detail"]
        logger.info(f"*************** {detail} ***************")
        step_1("注册账号")
        req_data = test_data["req_data"]
        expect_code = test_data["expect_code"]
        expect_msg = test_data["expect_msg"]
        result = phone_register(req_data)
        assert result.response.status_code == 200
        assert result.code == expect_code
        assert expect_msg in result.msg if result.msg is not None else result.msg == expect_msg
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "-k", "test_register_page.py"])
