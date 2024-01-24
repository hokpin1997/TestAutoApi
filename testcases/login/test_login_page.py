# -*- coding:utf-8 -*-
import allure
import pytest
from utils.logUtils.logger import logger
from page.Login.login import LoginPage
from utils.otherUtils.read_data import GetYamlData, ensure_path_sep

yaml_data = GetYamlData(ensure_path_sep("data/Login/test_login.yaml")).get_yaml_data()


@allure.step("步骤1 ==>> 密码登录")
def step_1():
    logger.info("步骤1 ==>> 密码登录")


@allure.epic("登录页面")
class TestLoginPage(LoginPage):

    @allure.feature("密码登录")
    @allure.description("该用例是用于密码登录场景")
    @pytest.mark.parametrize("test_data", yaml_data["test_password_login"],
                             ids=[i['detail'] for i in yaml_data["test_password_login"]])
    def test_password_login(self, test_data):
        logger.info("*************** 开始执行用例 ***************")
        step_1()
        req_data = test_data["req_data"]
        except_code = test_data["except_code"]
        except_msg = test_data["except_msg"]
        result = self.password_login(req_data)
        assert result.response.status_code == 200
        assert result.code == except_code
        assert except_msg in result.msg if result.msg is not None else result.msg == except_msg
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_login_page.py"])
