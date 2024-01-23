# -*- coding:utf-8 -*-
import pytest
from utils.logUtils.logger import logger
from utils.otherUtils.read_data import GetYamlData, ensure_path_sep
from utils.requestsUtils.requestControl import RequestControl
from utils.resultUtils.result_base import ResultBase
import requests


config = GetYamlData(ensure_path_sep("common/conf.yaml")).get_yaml_data()
api_test = config["host"]["api_test"]


class LoginPage():

    def password_login(self, test_data: dict):
        """
        密码登录
        :param test_data: 登录参数集合
        :return: 自定义的返回结果 result
        """
        dialCode = test_data["dialCode"]
        password = test_data["password"]
        phone = test_data["phone"]
        deviceType = test_data["deviceType"]
        url = api_test + "/user/login"
        data = {
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
        result = ResultBase()
        res = requests.post(url=url, headers=headers, json=data)
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
        logger.info("登录用户 ==>> 返回结果 ==>> {}".format(result.response.text))
        return result

    def password_login1111(self, **kwargs):
        """
        密码登录
        :param test_data: 登录参数集合
        :return: 自定义的返回结果 result
        """
        dialCode = dict(**kwargs).get("dialCode")
        password = dict(**kwargs).get("password")
        phone = dict(**kwargs).get("phone")
        deviceType = dict(**kwargs).get("deviceType")
        url = api_test + "/user/login"
        self.post(api_test, **kwargs)
        data = {
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
        result = ResultBase()
        res = requests.post(url=url, headers=headers, json=data)
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
        logger.info("登录用户 ==>> 返回结果 ==>> {}".format(result.response.text))
        return result

    def verification_code(self):
        pass

    def forget_password(self):
        pass


if __name__ == '__main__':
    pass