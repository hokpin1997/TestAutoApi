# -*- coding:utf-8 -*-
from utils.logUtils.logger import logger
from utils.resultUtils.result_base import ResultBase
from page.Register.registerPage import registerPage


def phone_register(req_data):
    result = ResultBase()
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
    res = registerPage.phone_register(json=json_data, headers=headers)
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
