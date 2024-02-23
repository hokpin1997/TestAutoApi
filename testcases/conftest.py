import allure
import pytest
from operation.login import password_login
from utils.cache_process.cache_control import CacheHandler
from utils.logUtils.logger import logger


@pytest.fixture(scope="session")
def work_login_init(request):
    """
    获取登录的cookie
    :return:
    """
    def do_login(test_data):
        resData = password_login(test_data)
        try:
            token = resData.response_json["data"]["token"]
            wecloudImToken = resData.response_json["data"]["wecloudImToken"]
            # 将登录后的cookie写入缓存中
            CacheHandler.update_cache(cache_name='login_token', value=token)
            CacheHandler.update_cache(cache_name='login_wecloudImToken', value=wecloudImToken)
        except Exception:
            logger.info(f"获取token 异常，接口响应: {resData.response_text}")
    return do_login





