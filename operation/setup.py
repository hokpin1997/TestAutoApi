# -*- coding:utf-8 -*-
from page.Setup.setupPage import SetupPage
from utils.otherUtils.read_data import GetYamlData, ensure_path_sep


config = GetYamlData(ensure_path_sep("common/conf.yaml")).get_yaml_data()
api_test_url = config["host"]["api_test"]


def cancel_account(test_data):
    is_dependence_login = test_data.get("is_dependence_login")
    req_data = test_data["req_data"]
    phone = req_data.get("phone")
    json_data = {
        "phone": phone
    }
    headers = {
        "Content-Type": "application/json"
    }
    res = SetupPage(api_test_url, test_data).cancel_account(json=json_data, headers=headers, is_dependence_login=is_dependence_login)
    return res
