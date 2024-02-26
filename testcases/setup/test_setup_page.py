# -*- coding:utf-8 -*-
import allure
import pytest
from operation.setup import cancel_account
from utils.logUtils.log_control import INFO
from utils.otherUtils.read_data import GetTestCase
from utils.otherUtils.allure_tools import allure_step_no

case_ids = ['test_cancel_account']
# 从缓存中读取用例数据
test_data = GetTestCase.case_data(case_ids)


def step_1(step):
    step = f"步骤1 ==>> {step}"
    allure_step_no(step)
    INFO.logger.info(step)


@allure.epic("设置页面")
class TestSetupPage:

    @allure.feature("注销")
    @allure.description("注销账号场景")
    @pytest.mark.parametrize("test_data", test_data["test_cancel_account"],
                             ids=[i['detail'] for i in test_data["test_cancel_account"]])
    def test_cancel_account(self, test_data, work_login_init):
        step_1("获取注销账号token")
        work_login_init(test_data)
        expect_code = test_data["assert_data"]["expect_code"]
        expect_msg = test_data["assert_data"]["expect_msg"]
        resData = cancel_account(test_data)
        assert resData.status_code == 200

        # 业务code
        business_code = resData.response_json["code"]
        assert business_code == expect_code

        # msg 可能为none
        res_msg = resData.response_json.get("message")
        assert expect_msg in res_msg if res_msg is not None else res_msg == expect_msg


if __name__ == '__main__':
    pytest.main(["-q", "-s", "-k", "test_setup_page.py"])
