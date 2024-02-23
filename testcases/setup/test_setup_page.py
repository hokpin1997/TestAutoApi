# -*- coding:utf-8 -*-
import allure
import pytest
from operation.setup import cancel_account
from utils.logUtils.logger import logger
from utils.otherUtils.read_data import GetTestCase
from utils.otherUtils.allure_tools import allure_step_no

case_ids = ['test_cancel_account']
# 从缓存中读取用例数据
test_data = GetTestCase.case_data(case_ids)


def step_1(step):
    step = f"步骤1 ==>> {step}"
    allure_step_no(step)
    logger.info(step)


@allure.epic("设置页面")
class TestSetupPage:

    @allure.feature("设置页")
    @allure.description("注销账号场景")
    @pytest.mark.parametrize("test_data", test_data["test_cancel_account"],
                             ids=[i['detail'] for i in test_data["test_cancel_account"]])
    def test_cancel_account(self, test_data):
        logger.info("*************** 开始执行用例 ***************")
        detail = test_data["detail"]
        logger.info(f"*************** {detail} ***************")
        step_1("注销账号")
        req_data = test_data["req_data"]
        expect_code = test_data["expect_code"]
        expect_msg = test_data["expect_msg"]
        result = cancel_account(req_data)
        assert result.response.status_code == 200
        assert result.code == expect_code
        assert expect_msg in result.msg if result.msg is not None else result.msg == expect_msg
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "-k", "test_setup_page.py"])
