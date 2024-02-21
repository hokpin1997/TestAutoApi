# -*- coding:utf-8 -*-
from page.Login.loginPage import loginPage
from utils.logUtils.logger import logger
from utils.resultUtils.result_base import ResultBase


def password_login(req_data):
    result = ResultBase()
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
    res = loginPage.password_login(json=json_data, headers=headers)
    res_json = res.json()
    if res_json["code"] == 0:
        result.success = True
        result.token = res_json["data"]["token"]
        result.wecloudImToken = res_json["data"]["wecloudImToken"]
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res_json["code"], res_json["message"])
    result.msg = res_json["message"]
    result.code = res_json["code"]
    result.response = res
    logger.info("返回结果 ==>> {}".format(result.response.text))
    return result


def verification_code(req_data):
    result = ResultBase()
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
    res = loginPage.verification_code(json=json_data, headers=headers)
    res_json = res.json()
    if res_json["code"] == 0:
        result.success = True
        result.token = res_json["data"]["token"]
        result.wecloudImToken = res_json["data"]["wecloudImToken"]
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res_json["code"], res_json["message"])
    result.msg = res_json["message"]
    result.code = res_json["code"]
    result.response = res
    logger.info("返回结果 ==>> {}".format(result.response.text))
    return result


def forget_password():
    pass
