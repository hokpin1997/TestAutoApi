# -*- coding:utf-8 -*-
import ast
import json
from jsonpath import jsonpath
from utils.cache_process.cache_control import CacheHandler
from utils.otherUtils.common import jsonpath_replace, ensure_path_sep
from utils.otherUtils.exceptions import ValueNotFoundError
from utils.otherUtils.read_data import GetYamlData
from utils.otherUtils.regular_control import cache_regular, regular

config = GetYamlData(ensure_path_sep("common/conf.yaml")).get_yaml_data()
api_test_url = config["host"]


class DependentCase:
    """ 处理依赖相关的业务 """

    def __init__(self, dependent_yaml_case):
        self.__yaml_case = dependent_yaml_case

    @classmethod
    def get_cache(cls, case_id):
        """
        获取缓存用例池中的数据，通过 case_id 提取
        :param case_id:
        :return: case_id_01
        """
        _case_data = CacheHandler.get_cache(case_id)
        return _case_data

    @classmethod
    def replace_key(cls, dependent_data):
        """ 获取需要替换的内容 """
        try:
            _replace_key = dependent_data.get("replace_key")
            return _replace_key
        except KeyError:
            return None

    @classmethod
    def set_cache_value(cls, dependent_data):
        """
        获取依赖中是否需要将数据存入缓存中
        """
        try:
            return dependent_data.get("set_cache")
        except KeyError:
            return None

    @classmethod
    def jsonpath_data(cls, obj, expr):
        """
        通过jsonpath提取依赖的数据
        :param obj: 对象信息
        :param expr: jsonpath 方法
        :return: 提取到的内容值,返回是个数组

        对象: {"data": applyID} --> jsonpath提取方法: $.data.data.[0].applyId
        """
        _jsonpath_data = jsonpath(obj, expr)
        # 判断是否正常提取到数据，如未提取到，则抛异常
        if _jsonpath_data is False:
            raise ValueNotFoundError(
                f"jsonpath提取失败！\n 提取的数据: {obj} \n jsonpath规则: {expr}"
            )
        return _jsonpath_data

    def is_dependent(self):
        from utils.requestsUtils.request_control import RequestControl
        """
        判断是否有数据依赖
        :return:
        """

        # 获取用例中的dependent_type值，判断该用例是否需要执行依赖
        _dependent_type = self.__yaml_case.get("dependence_case")
        # 获取依赖用例数据
        _dependence_case_dates = self.__yaml_case.get("dependence_case_data")

        # 判断是否有依赖
        if _dependent_type is True:
            # 读取依赖相关的用例数据
            jsonpath_dates = {}
            # 循环所有需要依赖的数据
            try:
                for dependence_case_data in _dependence_case_dates:
                    _is_dependence_login = dependence_case_data.get("is_dependence_login")
                    _case_id = dependence_case_data.get("case_id")
                    # 判断依赖数据为sql，case_id需要写成self，否则程序中无法获取case_id
                    if _case_id == 'self':
                        pass
                    else:
                        test_data = eval(regular(str(self.get_cache(_case_id))))
                        if _is_dependence_login:
                            test_data["req_data"] = dependence_case_data.get("dependence_login").get("req_data")
                        test_data = ast.literal_eval(cache_regular(str(test_data)))
                        res = RequestControl(test_data).request()
                        if dependence_case_data.get("dependent_data") is not None:
                            dependent_data = dependence_case_data.get("dependent_data")
                            for i in dependent_data:
                                _case_id = dependence_case_data.get("case_id")
                                _jsonpath = i.get("jsonpath")
                                _request_data = self.__yaml_case.get("req_data")
                                _replace_key = self.replace_key(i)
                                _set_value = self.set_cache_value(i)
                                # 判断依赖数据类型, 依赖 response 中的数据
                                if i.get("dependent_type") == "response":
                                    self.dependent_handler(
                                        data=json.loads(res.response_text),
                                        _jsonpath=_jsonpath,
                                        set_value=_set_value,
                                        replace_key=_replace_key,
                                        jsonpath_dates=jsonpath_dates,
                                        dependent_type=0
                                    )

                                # 判断依赖数据类型, 依赖 request 中的数据
                                elif i.get("dependent_type") == "request":
                                    self.dependent_handler(
                                        data=res.response_text,
                                        _jsonpath=_jsonpath,
                                        set_value=_set_value,
                                        replace_key=_replace_key,
                                        jsonpath_dates=jsonpath_dates,
                                        dependent_type=1
                                    )

                                else:
                                    raise ValueError(
                                        "依赖的dependent_type不正确，只支持request、response、sql依赖\n"
                                        f"当前填写内容: {i.dependent_type}"
                                    )
                return jsonpath_dates
            except KeyError as exc:
                # pass
                raise ValueNotFoundError(
                    f"dependence_case_data依赖用例中，未找到 {exc} 参数，请检查是否填写"
                    f"如已填写，请检查是否存在yaml缩进问题"
                ) from exc
            except TypeError as exc:
                raise ValueNotFoundError(
                    "dependence_case_data下的所有内容均不能为空！"
                    "请检查相关数据是否填写，如已填写，请检查缩进问题"
                ) from exc
        else:
            return False

    def dependent_handler(self, _jsonpath, set_value, replace_key, jsonpath_dates, data, dependent_type):
        """ 处理数据替换 """
        if not _jsonpath:
            return
        jsonpath_data = self.jsonpath_data(
            data,
            _jsonpath
        )
        if set_value is not None:
            if len(jsonpath_data) > 1:
                CacheHandler.update_cache(cache_name=set_value, value=jsonpath_data)
            else:
                CacheHandler.update_cache(cache_name=set_value, value=jsonpath_data[0])
        if replace_key is not None:
            if dependent_type == 0:
                jsonpath_dates[replace_key] = jsonpath_data[0]
            self.url_replace(replace_key=replace_key, jsonpath_dates=jsonpath_dates,
                             jsonpath_data=jsonpath_data)

    def url_replace(self, replace_key, jsonpath_dates, jsonpath_data):
        """
        url中的动态参数替换
        # 如: 一般有些接口的参数在url中,并且没有参数名称, /api/v1/work/spu/approval/spuApplyDetails/{id}
        # 那么可以使用如下方式编写用例, 可以使用 $url_params{}替换,
        # 如/api/v1/work/spu/approval/spuApplyDetails/$url_params{id}
        :param jsonpath_data: jsonpath 解析出来的数据值
        :param replace_key: 用例中需要替换数据的 replace_key
        :param jsonpath_dates: jsonpath 存放的数据值
        :return:
        """

        if "$url_param" in replace_key:
            _url = self.__yaml_case.url.replace(replace_key, str(jsonpath_data[0]))
            jsonpath_dates['$.url'] = _url
        else:
            jsonpath_dates[replace_key] = jsonpath_data[0]

    def get_dependent_data(self):
        _dependent_data = DependentCase(self.__yaml_case).is_dependent()
        _new_data = None
        # 判断有依赖
        if _dependent_data is not None and _dependent_data is not False:
            # if _dependent_data is not False:
            for key, value in _dependent_data.items():
                # 通过jsonpath判断出需要替换数据的位置
                _change_data = key.split(".")
                # jsonpath 数据解析
                # 不要删 这个yaml_case
                yaml_case = self.__yaml_case
                _new_data = jsonpath_replace(change_data=_change_data, key_name='yaml_case')
                # 最终提取到的数据,转换成 __yaml_case.data
                _new_data += ' = ' + str(value)
                exec(_new_data)
