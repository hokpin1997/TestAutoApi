# -*- coding:utf-8 -*-
from utils.otherUtils.read_data import GetYamlData, ensure_path_sep
from utils.requestsUtils.requestControl import RequestControl


config = GetYamlData(ensure_path_sep("common/conf.yaml")).get_yaml_data()
api_test_url = config["host"]["api_test"]


class SetupPage(RequestControl):

    def cancel_account(self, **kwargs):
        return self.post("/user/cancellation", **kwargs)


setupPage = SetupPage(api_test_url)


if __name__ == '__main__':
    pass