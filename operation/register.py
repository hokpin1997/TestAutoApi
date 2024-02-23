# -*- coding:utf-8 -*-
from utils.otherUtils.read_data import GetYamlData, ensure_path_sep
from page.Register.registerPage import RegisterPage


config = GetYamlData(ensure_path_sep("common/conf.yaml")).get_yaml_data()
api_test_url = config["host"]["api_test"]


def phone_register(test_data):
    req_data = test_data["req_data"]
    dialCode = req_data.get("dialCode")
    firstName = req_data.get("firstName")
    verifyCode = req_data.get("verifyCode")
    phone = req_data.get("phone")
    password = req_data.get("password")
    json_data = {
        "phone": phone,
        "password": password,
        "firstName": firstName,
        "verifyCode": verifyCode,
        # "areaCode": "KH",
        "dialCode": dialCode,
        "lastName": ""
    }
    headers = {
        "Content-Type": "application/json"
    }
    res = RegisterPage(api_test_url, test_data).phone_register(json=json_data, headers=headers)
    return res
