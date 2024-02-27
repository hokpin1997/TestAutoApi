# -*- coding:utf-8 -*-
from utils.otherUtils.read_data import GetYamlData, ensure_path_sep
from utils.requestsUtils.request_control import RequestControl


class RegisterPage(RequestControl):

    def phone_register(self, **kwargs):
        return self.post("/user/register", **kwargs)


if __name__ == '__main__':
    pass