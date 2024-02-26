# -*- coding:utf-8 -*-
from utils.requestsUtils.request_control import RequestControl


class SetupPage(RequestControl):

    def cancel_account(self, **kwargs):
        return self.post("/user/cancellation", **kwargs)


if __name__ == '__main__':
    pass