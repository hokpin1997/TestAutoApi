# -*- coding:utf-8 -*-
import requests
import json as complexjson
from utils.cache_process.cache_control import CacheHandler
from utils.logUtils.logger import logger
from utils.otherUtils.allure_tools import allure_step_no, allure_step
from utils.otherUtils.models import ResponseData


class RequestControl:

    def __init__(self, api_root_url, yaml_data):
        self.api_root_url = api_root_url
        self.session = requests.session()
        self.yaml_data = yaml_data
        self.res = None

    def get(self, url, **kwargs):
        return self.request(url, "GET", **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request(url, "POST", data, json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request(url, "PUT", data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, "DELETE", **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request(url, "PATCH", data, **kwargs)

    def request(self, url, method, data=None, json=None, **kwargs):
        url = self.api_root_url + url
        headers = kwargs.get("headers")
        params = kwargs.get("params")
        files = kwargs.get("files")
        cookies = kwargs.get("cookies")
        is_dependence_login = kwargs.get("is_dependence_login")
        if is_dependence_login:
            login_token = CacheHandler.get_cache("login_token")
            headers["Authorization"] = login_token
        if kwargs.get("is_dependence_login"):
            del kwargs['is_dependence_login']
        self.request_log(url, method, data, json, params, headers, files, cookies)
        self.request_allure_step(url, method, data, json, params, headers, files, cookies)
        if method == "GET":
            self.res = self.session.get(url, **kwargs)
        elif method == "POST":
            self.res = self.session.post(url, data, json, verify=False, **kwargs)
        elif method == "PUT":
            if json:
                # PUT 和 PATCH 中没有提供直接使用json参数的方法，因此需要用data来传入
                data = complexjson.dumps(json)
            self.res = self.session.put(url, data, **kwargs)
        elif method == "DELETE":
            self.res = self.session.delete(url, **kwargs)
        elif method == "PATCH":
            if json:
                data = complexjson.dumps(json)
            self.res = self.session.patch(url, data, **kwargs)
        _res_data = self._check_params(res=self.res, yaml_data=self.yaml_data)
        return _res_data

    def _check_params(self, res, yaml_data):
        data = {
            "url": res.url,
            "is_dependence_login": yaml_data.get("is_dependence_login"),
            "detail": yaml_data.get("detail"),
            "response_body": res,
            "response_json": res.json(),
            "response_text": res.text,
            "method": res.request.method,
            "yaml_data": yaml_data,
            "headers": res.request.headers,
            "cookie": res.cookies,
            "assert_data": yaml_data.get("assert_data"),
            "res_time": self.response_elapsed_total_seconds(res),
            "status_code": res.status_code,
        }
        # 抽离出通用模块，判断 http_request 方法中的一些数据校验
        return ResponseData(**data)

    @classmethod
    def response_elapsed_total_seconds(cls, res):
        """获取接口响应时长"""
        try:
            return round(res.elapsed.total_seconds() * 1000, 2)
        except AttributeError:
            return 0.00

    def request_log(self, url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None, **kwargs):
        logger.info("接口请求地址 ==>> {}".format(url))
        logger.info("接口请求方式 ==>> {}".format(method))
        logger.info("接口请求头 ==>> {}".format(complexjson.dumps(headers, indent=4, ensure_ascii=False)))
        logger.info("接口请求 params 参数 ==>> {}".format(complexjson.dumps(params, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 data 参数 ==>> {}".format(complexjson.dumps(data, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 json 参数 ==>> {}".format(complexjson.dumps(json, indent=4, ensure_ascii=False)))
        logger.info("接口上传附件 files 参数 ==>> {}".format(files))
        logger.info("接口 cookies 参数 ==>> {}".format(complexjson.dumps(cookies, indent=4, ensure_ascii=False)))

    def request_allure_step(self, url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None):
        """ 在allure中记录请求数据 """
        allure_step_no("接口请求地址 ==>> {}".format(url))
        allure_step_no("接口请求方式 ==>> {}".format(method))
        allure_step("接口请求头 ==>> ：", complexjson.dumps(headers, indent=4))
        allure_step("接口请求 params 参数 ==>> ：", complexjson.dumps(params, indent=4))
        allure_step("接口请求体 data 参数 ==>> ：", complexjson.dumps(data, indent=4))
        allure_step("接口请求体 json 参数 ==>> ：", complexjson.dumps(json, indent=4))
        if files:
            allure_step("接口上传附件 files 参数 ==>> ：", files)
        allure_step_no("接口 cookies 参数 ==>> {}".format(complexjson.dumps(cookies, indent=4)))
