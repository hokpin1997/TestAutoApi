# -*- coding:utf-8 -*-
from utils.otherUtils.common import ensure_path_sep

from utils.otherUtils.models import Config
from utils.otherUtils.read_data import GetYamlData

_data = GetYamlData(ensure_path_sep("common/conf.yaml")).get_yaml_data()
config = Config(**_data)