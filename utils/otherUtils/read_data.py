# -*- coding:utf-8 -*-
import json
import os
import pytest
import yaml
from utils.cache_process.cache_control import CacheHandler
from utils.logUtils.log_control import INFO, ERROR
from utils.otherUtils.common import ensure_path_sep


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
                INFO.logger.info("加载 {} 文件......".format(self.file_dir))
                data = open(self.file_dir, 'r', encoding='utf-8')
                yaml_data = yaml.load(data, Loader=yaml.FullLoader)
            else:
                raise FileNotFoundError("文件路径不存在")
        except Exception as e:
            ERROR.logger.error(f"文件读取失败，路径：{self.file_dir}")
            pytest.skip(str(e))
        else:
            INFO.logger.info("读到数据: {} ".format(yaml_data))
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