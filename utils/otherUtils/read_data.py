# -*- coding:utf-8 -*-
import json
import os
import pytest
import yaml
from utils.cache_process.cache_control import CacheHandler
from utils.logUtils.logger import logger


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


class GetYamlData:
    """ 获取 yaml 文件中的数据 """

    def __init__(self, file_dir):
        self.file_dir = str(file_dir)

    def get_yaml_data(self) -> dict:
        """
        获取 yaml 中的数据
        :param: fileDir:
        :return:
        """
        # 判断文件是否存在
        try:
            if os.path.exists(self.file_dir):
                logger.info("加载 {} 文件......".format(self.file_dir))
                data = open(self.file_dir, 'r', encoding='utf-8')
                yaml_data = yaml.load(data, Loader=yaml.FullLoader)
            else:
                raise FileNotFoundError("文件路径不存在")
        except Exception as e:
            pytest.skip(str(e))
        else:
            logger.info("读到数据 ==>>  {} ".format(yaml_data))
            return yaml_data


class GetTestCase:

    @staticmethod
    def case_data(case_id_lists):
        case_dict = {}
        for i in case_id_lists:
            _data = CacheHandler.get_cache(i)
            case_dict[i] = _data

        return case_dict


if __name__ == '__main__':
    config = GetYamlData(ensure_path_sep("common/users.yaml")).get_yaml_data()
    print(json.dumps(config, ensure_ascii=False))