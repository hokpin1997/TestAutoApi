# -*- coding:utf-8 -*-
import allure
import pytest
from utils.logUtils.log_control import INFO
from utils.otherUtils.read_data import GetTestCase
from utils.otherUtils.allure_tools import allure_step_no
from utils.requestsUtils.request_control import RequestControl

case_ids = ['test_password_login_01', "test_password_login_02", "test_password_login_03"]
# 从缓存中读取用例数据
test_data = GetTestCase.case_data(case_ids)


def step_1(step):
    step = f"步骤1 ==>> {step}"
    allure_step_no(step)
    INFO.logger.info(step)


@allure.epic("UIM自动化")
@allure.feature("登录")
class TestPasswordLoginPage:

    @allure.story("密码登录")
    @pytest.mark.parametrize("test_data", test_data,
                             ids=[i['detail'] for i in test_data])
    def test_password_login(self, test_data, case_skip):
        expect_code = test_data["assert_data"]["expect_code"]
        expect_msg = test_data["assert_data"]["expect_msg"]
        resData = RequestControl(test_data).request()
        assert resData.status_code == 200

        # 业务code
        business_code = resData.response_json["code"]
        assert business_code == expect_code

        # msg 可能为none
        res_msg = resData.response_json.get("message")
        assert expect_msg in res_msg if res_msg is not None else res_msg == expect_msg


if __name__ == '__main__':
    pytest.main(["-q", "-s", "-k", "test_password_login.py"])
