# -*- coding:utf-8 -*-
from page.Login.loginPage import LoginPage
from utils.logUtils.logger import logger
from utils.resultUtils.result_base import ResultBase
from utils.otherUtils.read_data import GetYamlData, ensure_path_sep

config = GetYamlData(ensure_path_sep("common/conf.yaml")).get_yaml_data()
api_test_url = config["host"]["api_test"]


def password_login(test_data):
    is_dependence_login = test_data.get("is_dependence_login")
    if is_dependence_login:
        req_data = test_data["dependence_login"]["req_data"]
    else:
        req_data = test_data.get("req_data")
    dialCode = req_data.get("dialCode")
    password = req_data.get("password")
    phone = req_data.get("phone")
    deviceType = req_data.get("deviceType")
    json_data = {
        "deviceInfo": "",
        "deviceType": deviceType,
        "deviceUuid": "",
        "deviceVersion": "",
        "dialCode": dialCode,
        "loginType": 0,
        "mosVersion": "",
        "password": password,
        "phone": phone,
        "qrCode": ""
    }
    headers = {
        "Content-Type": "application/json"
    }
    resData = LoginPage(api_test_url, test_data).password_login(json=json_data, headers=headers)
    return resData


def verification_code(test_data):
    req_data = test_data.get("req_data")
    dialCode = req_data.get("dialCode")
    captcha_code = req_data.get("captcha_code")
    phone = req_data.get("phone")
    json_data = {
        "phone": phone,
        "password": captcha_code,
        "loginType": 1,
        "deviceVersion": "17.2.1",
        "deviceType": 1,
        "mosVersion": "1.8.112",
        "dialCode": dialCode,
    }
    headers = {
        "Content-Type": "application/json"
    }
    resData = LoginPage(api_test_url, test_data).password_login(json=json_data, headers=headers)
    return resData


def forget_password():
    pass
