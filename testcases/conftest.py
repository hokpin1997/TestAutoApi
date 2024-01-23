import allure
import pytest


# @pytest.fixture(scope="function", autouse=True)
# @pytest.fixture()
# def test_data(request):
#     data = request.param
#     allure.dynamic.title(data["detail"])
#     return data


# @pytest.fixture(scope="function", autouse=True)
# def test_data(request):
#     yaml_data = request.param
#     testcase_name = request.function.__name__
#     test_data = yaml_data[testcase_name]
#     return test_data