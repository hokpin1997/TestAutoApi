# -*- coding:utf-8 -*-
import ast

import requests
from utils.logUtils.log_decorator import log_decorator
from utils.otherUtils.models import ResponseData
from utils.otherUtils.regular_control import cache_regular
from utils.requestsUtils.dependent_case import DependentCase
from requests_toolbelt import MultipartEncoder


class RequestControl:

    def __init__(self, yaml_data):
        self.yaml_data = yaml_data

    @classmethod
    def check_headers_str_null(cls, headers):
        """
        兼容用户未填写headers或者header值为int
        @return:
        """
        headers = ast.literal_eval(cache_regular(str(headers)))
        if headers is None:
            headers = {"headers": None}
        else:
            for key, value in headers.items():
                if not isinstance(value, str):
                    headers[key] = str(value)
        return headers

    @classmethod
    def multipart_in_headers(cls, request_data, header):
        """ 判断处理header为 Content-Type: multipart/form-data"""
        header = ast.literal_eval(cache_regular(str(header)))
        request_data = ast.literal_eval(cache_regular(str(request_data)))

        if header is None:
            header = {"headers": None}
        else:
            # 将header中的int转换成str
            for key, value in header.items():
                if not isinstance(value, str):
                    header[key] = str(value)
            if "multipart/form-data" in str(header.values()):
                # 判断请求参数不为空, 并且参数是字典类型
                if request_data and isinstance(request_data, dict):
                    # 当 Content-Type 为 "multipart/form-data"时，需要将数据类型转换成 str
                    for key, value in request_data.items():
                        if not isinstance(value, str):
                            request_data[key] = str(value)

                    request_data = MultipartEncoder(request_data)
                    header['Content-Type'] = request_data.content_type

        return request_data, header

    def request_type_for_json(self, headers, method, **kwargs):
        import requests.packages.urllib3
        requests.packages.urllib3.disable_warnings()
        """ 判断请求类型为json格式 """
        _headers = self.check_headers_str_null(headers)
        _data = self.yaml_data.get("req_data")
        _url = self.yaml_data.get("url")
        res = requests.request(
            method=method,
            url=cache_regular(str(_url)),
            json=ast.literal_eval(cache_regular(str(_data))),
            data={},
            headers=_headers,
            verify=False,
            params=None,
            **kwargs
        )
        return res

    def request_type_for_params(self, headers, method, **kwargs):

        """处理 requestType 为 params """
        _data = self.yaml_data.get("req_data")
        url = self.yaml_data.get("url")
        if _data is not None:
            # url 拼接的方式传参
            params_data = "?"
            for key, value in _data.items():
                if value is None or value == '':
                    params_data += (key + "&")
                else:
                    params_data += (key + "=" + str(value) + "&")
            url = url + params_data[:-1]
        _headers = self.check_headers_str_null(headers)
        res = requests.request(
            method=method,
            url=cache_regular(url),
            headers=_headers,
            verify=False,
            data={},
            params=None,
            **kwargs)
        return res

    def request_type_for_file(self, method, headers, **kwargs):
        pass

    def request_type_for_data(self, headers, method, **kwargs):
        """判断 requestType 为 data 类型"""
        data = self.yaml_data.get("req_data")
        _data, _headers = self.multipart_in_headers(
            ast.literal_eval(cache_regular(str(data))),
            headers
        )
        _url = self.yaml_data.get("url")
        res = requests.request(
            method=method,
            url=cache_regular(_url),
            data=_data,
            headers=_headers,
            verify=False,
            **kwargs)

        return res

    @log_decorator(True)
    def request(self, **kwargs):
        requests_type_mapping = {
            "json": self.request_type_for_json,
            "params": self.request_type_for_params,
            "file": self.request_type_for_file,
            "data": self.request_type_for_data,
        }

        dependence_case = self.yaml_data.get("dependence_case")
        if dependence_case is True:
            DependentCase(self.yaml_data).get_dependent_data()
        headers = self.yaml_data.get("headers")
        method = self.yaml_data.get("method")
        res = requests_type_mapping.get(self.yaml_data.get("requestType"))(
            headers=headers,
            method=method,
            **kwargs
        )
        _res_data = self._check_params(res=res, yaml_data=self.yaml_data)
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
