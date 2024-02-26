# -*- coding:utf-8 -*-
import requests
import json as complexjson
from utils.cache_process.cache_control import CacheHandler
from utils.logUtils.log_decorator import log_decorator
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

    @log_decorator(True)
    def request(self, url, method, data=None, json=None, **kwargs):
        url = self.api_root_url + url
        headers = kwargs.get("headers")
        is_dependence_login = kwargs.get("is_dependence_login")
        if is_dependence_login:
            login_token = CacheHandler.get_cache("login_token")
            headers["Authorization"] = login_token
        if kwargs.get("is_dependence_login"):
            del kwargs['is_dependence_login']
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
            "request_body": yaml_data.get("req_data"),
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

