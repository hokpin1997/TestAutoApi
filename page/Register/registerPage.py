# -*- coding:utf-8 -*-
from utils.otherUtils.read_data import GetYamlData, ensure_path_sep
from utils.requestsUtils.requestControl import RequestControl


config = GetYamlData(ensure_path_sep("common/conf.yaml")).get_yaml_data()
api_test_url = config["host"]["api_test"]


class RegisterPage(RequestControl):

    def phone_register(self, **kwargs):
        return self.post("/user/register", **kwargs)


registerPage = RegisterPage(api_test_url)


if __name__ == '__main__':
    pass