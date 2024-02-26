# -*- coding:utf-8 -*-
import os


def root_path():
    """ 获取项目根路径 """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return project_root


def ensure_path_sep(path):
    """兼容 windows 和 linux 不同环境的操作系统路径 """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return root_path() + os.path.sep + path


def get_all_files(file_path):
    """
    获取所有文件路径
    :param file_path: 目录路径
    :return:
    """
    filenames = []
    for root, dirs, files in os.walk(file_path):
        for _file_path in files:
            path = os.path.join(root, _file_path)
            if 'yaml' in path or '.yml' in path:
                filenames.append(path)

    return filenames


def jsonpath_replace(change_data, key_name, data_switch=None):
    """处理jsonpath数据"""
    _new_data = key_name + ''
    for i in change_data:
        if i == '$':
            pass
        elif data_switch is None and i == "data":
            _new_data += '.data'
        elif i[0] == '[' and i[-1] == ']':
            _new_data += "[" + i[1:-1] + "]"
        else:
            _new_data += '[' + '"' + i + '"' + "]"
    return _new_data
