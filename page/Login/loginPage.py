# -*- coding:utf-8 -*-
from utils.otherUtils.read_data import GetYamlData, ensure_path_sep
from utils.requestsUtils.requestControl import RequestControl


class LoginPage(RequestControl):

    def password_login(self, **kwargs):
        return self.post("/user/login", **kwargs)

    def verification_code(self, **kwargs):
        return self.post("/user/login", **kwargs)

    def forget_password(self):
        pass


if __name__ == '__main__':
    pass