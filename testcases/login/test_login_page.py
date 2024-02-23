# -*- coding:utf-8 -*-
import allure
import pytest
from operation.login import password_login, verification_code
from utils.logUtils.logger import logger
from utils.otherUtils.read_data import GetTestCase
from utils.otherUtils.allure_tools import allure_step_no

case_ids = ['test_password_login', "test_verification_code"]
# 从缓存中读取用例数据
test_data = GetTestCase.case_data(case_ids)


def step_1(step):
    step = f"步骤1 ==>> {step}"
    allure_step_no(step)
    logger.info(step)


@allure.epic("登录页面")
class TestLoginPage:

    @allure.feature("密码登录")
    @allure.description("密码登录场景")
    @pytest.mark.parametrize("test_data", test_data["test_password_login"],
                             ids=[i['detail'] for i in test_data["test_password_login"]])
    def test_password_login(self, test_data):
        logger.info("*************** 开始执行用例 ***************")
        detail = test_data["detail"]
        logger.info(f"*************** {detail} ***************")
        step_1("密码登录")
        req_data = test_data["req_data"]
        expect_code = test_data["expect_code"]
        expect_msg = test_data["expect_msg"]
        result = password_login(req_data)
        assert result.response.status_code == 200
        assert result.code == expect_code
        assert expect_msg in result.msg if result.msg is not None else result.msg == expect_msg
        logger.info("*************** 结束执行用例 ***************")

    @allure.feature("验证码登录")
    @allure.description("验证码登录场景")
    @pytest.mark.parametrize("test_data", test_data["test_verification_code"],
                             ids=[i['detail'] for i in test_data["test_verification_code"]])
    def test_verification_code(self, test_data):
        logger.info("*************** 开始执行用例 ***************")
        detail = test_data["detail"]
        logger.info(f"*************** {detail} ***************")
        step_1("验证码登录")
        req_data = test_data["req_data"]
        expect_code = test_data["expect_code"]
        expect_msg = test_data["expect_msg"]
        result = verification_code(req_data)
        assert result.response.status_code == 200
        assert result.code == expect_code
        assert expect_msg in result.msg if result.msg is not None else result.msg == expect_msg
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "-k", "test_verification_code"])
