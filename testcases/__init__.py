#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.otherUtils.read_data import GetYamlData
from utils.cache_process.cache_control import _cache_config, CacheHandler
from utils.otherUtils.common import ensure_path_sep, get_all_files


def write_case_process():
    """
    获取所有用例，写入用例池中
    :return:
    """

    # 循环拿到所有存放用例的文件路径
    for i in get_all_files(file_path=ensure_path_sep("data")):
        # 循环读取yaml文件中的数据
        case_datas = GetYamlData(i).get_yaml_data()
        if case_datas is not None:
            for k, v in case_datas.items():
                # 判断 case_id 是否已存在
                case_id_exit = k in _cache_config.keys()
                # 如果case_id 不存在，则将用例写入缓存池中
                if case_id_exit is False:
                    CacheHandler.update_cache(cache_name=k, value=v)
                # 当 case_id 为 True 存在时，则跑出异常
                elif case_id_exit is True:
                    raise ValueError(f"case_id: {k} 存在重复项, 请修改case_id\n"
                                     f"文件路径: {i}")


write_case_process()
