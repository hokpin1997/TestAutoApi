# -*- coding:utf-8 -*-
import allure
import pytest
from operation.login import password_login, verification_code
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
        expect_code = test_data["assert_data"]["expect_code"]
        expect_msg = test_data["assert_data"]["expect_msg"]
        resData = password_login(test_data)
        assert resData.status_code == 200

        # 业务code
        business_code = resData.response_json["code"]
        assert business_code == expect_code

        # msg 可能为none
        res_msg = resData.response_json.get("message")
        assert expect_msg in res_msg if res_msg is not None else res_msg == expect_msg

    @allure.feature("验证码登录")
    @allure.description("验证码登录场景")
    @pytest.mark.parametrize("test_data", test_data["test_verification_code"],
                             ids=[i['detail'] for i in test_data["test_verification_code"]])
    def test_verification_code(self, test_data):
        expect_code = test_data["assert_data"]["expect_code"]
        expect_msg = test_data["assert_data"]["expect_msg"]
        resData = verification_code(test_data)
        assert resData.status_code == 200

        # 业务code
        business_code = resData.response_json["code"]
        assert business_code == expect_code

        # msg 可能为none
        res_msg = resData.response_json.get("message")
        assert expect_msg in res_msg if res_msg is not None else res_msg == expect_msg


if __name__ == '__main__':
    pytest.main(["-q", "-s", "-k", "test_verification_code"])
