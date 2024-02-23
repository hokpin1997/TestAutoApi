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
        expect_code = test_data["assert_data"]["expect_code"]
        expect_msg = test_data["assert_data"]["expect_msg"]
        resData = phone_register(test_data)
        assert resData.status_code == 200

        # 业务code
        business_code = resData.response_json["code"]
        assert business_code == expect_code

        # msg 可能为none
        res_msg = resData.response_json.get("message")
        assert expect_msg in res_msg if res_msg is not None else res_msg == expect_msg
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "-k", "test_register_page.py"])
