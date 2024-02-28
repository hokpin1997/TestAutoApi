# -*- coding:utf-8 -*-
from utils import GetYamlData
from utils.otherUtils.exceptions import ValueNotFoundError


def get_case_host(case_id, case_data):
    """
    获取用例的 host
    :return:
    """
    try:
        _url = case_data.get("url", "")
        _host = case_data['host']
        _requestType = case_data['requestType']
        if _requestType != "ws" and _host is None:
            raise ValueNotFoundError(
                f"用例中的 host 不能为空！\n "
                f"用例ID: {case_id} \n "
            )
        return _host + _url if _url else _host
    except KeyError as exc:
        raise ValueNotFoundError() from exc


def case_process(file_dir):
    """
    数据清洗之后，返回该 yaml 文件中的所有用例
    @param case_id_switch: 判断数据清洗，是否需要清洗出 case_id, 主要用于兼容用例池中的数据
    :return:
    """

    dates = GetYamlData(file_dir).get_yaml_data()
    case_lists = []
    for key, values in dates.items():
        # 公共配置中的数据，与用例数据不同，需要单独处理
        case_date = {
            'detail': values["detail"],
            'is_run': values["is_run"],
            'url': get_case_host(case_id=key, case_data=values),
            'method': values["method"],
            'headers': values["headers"],
            'requestType': values["requestType"],
            'req_data': values["req_data"],
            'dependence_case': values["dependence_case"],
            'dependence_case_data': values["dependence_case_data"],
            "assert_data": values["assert_data"],

        }

        case_lists.append({key: case_date})
    return case_lists