import ast
import time
import pytest
from utils import ensure_path_sep
from utils.cache_process.cache_control import CacheHandler
from utils.otherUtils.regular_control import cache_regular
from utils.logUtils.log_control import ERROR, INFO, WARNING
from utils.requestsUtils.request_control import RequestControl
from utils.otherUtils.read_data import GetYamlData

conf = GetYamlData(ensure_path_sep("common/conf.yaml")).get_yaml_data()
host = conf.get("host")


@pytest.fixture(scope="session", autouse=True)
def work_login_init():
    """
    获取登录的cookie
    :return:
    """
    try:
        test_data = {
            "detail": "获取工作token",
            "url": host + "/user/login",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json;"
            },
            "requestType": "json",
            "req_data": {
                "loginType": "0",
                "dialCode": "855",
                "password": "flgpGS1oMqfvM4ewFrQSBg==",
                "phone": "60000002",
                "deviceType": "1",
            },
            "dependence_case": None,
            "dependence_case_data": None,
            "assert_data": None,
        }
        resData = RequestControl(test_data).request()
        token = resData.response_json["data"]["token"]
        wecloudImToken = resData.response_json["data"]["wecloudImToken"]
        # 将登录后的cookie写入缓存中
        CacheHandler.update_cache(cache_name='login_token', value=token)
        CacheHandler.update_cache(cache_name='login_wecloudImToken', value=wecloudImToken)
    except Exception as e:
        ERROR.logger.error(f"获取token 异常，接口响应")
        raise e


@pytest.fixture(scope="function", autouse=True)
def case_skip(test_data):
    """处理跳过用例"""
    detail = test_data.get("detail")
    if ast.literal_eval(cache_regular(str(test_data.get("is_run")))) is False and detail != "获取工作token":
        # allure.dynamic.title(in_data.detail)
        # allure_step_no(f"请求URL: {in_data.is_run}")
        # allure_step_no(f"请求方式: {in_data.method}")
        # allure_step("请求头: ", in_data.headers)
        # allure_step("请求数据: ", in_data.data)
        # allure_step("依赖数据: ", in_data.dependence_case_data)
        # allure_step("预期数据: ", in_data.assert_data)
        pytest.skip()


def pytest_collection_modifyitems(items):
    """
    内置hook函数，当测试用例收集完成时调整执行顺序
    :return:
    """

    # 期望用例顺序,填写testcase方法名
    appoint_items = ["test_password_login", "test_verification_code", "test_cancel_account", "test_phone_register"]

    # 指定运行顺序
    run_items = []
    for i in appoint_items:
        for item in items:
            module_item = item.name.split("[")[0]
            if i == module_item:
                run_items.append(item)

    for i in run_items:
        run_index = run_items.index(i)
        items_index = items.index(i)

        if run_index != items_index:
            n_data = items[run_index]
            run_index = items.index(n_data)
            items[items_index], items[run_index] = items[run_index], items[items_index]


def pytest_terminal_summary(terminalreporter):
    """
    内置hook函数，用例执行完后收集测试结果
    """

    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime
    INFO.logger.error(f"用例总数: {_TOTAL}")
    INFO.logger.error(f"异常用例数: {_ERROR}")
    ERROR.logger.error(f"失败用例数: {_FAILED}")
    WARNING.logger.warning(f"跳过用例数: {_SKIPPED}")
    INFO.logger.info("用例执行时长: %.2f" % _TIMES + " s")

    try:
        _RATE = _PASSED / _TOTAL * 100
        INFO.logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        INFO.logger.info("用例成功率: 0.00 %")




