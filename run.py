# -*- coding:utf-8 -*-
import os
import traceback

import pytest


def run():

    pytest.main(['-s', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                 '--alluredir', './report', "--clean-alluredir"])

    """
           --reruns: 失败重跑次数
           --count: 重复执行次数
           -v: 显示错误位置以及错误的详细信息
           -s: 等价于 pytest --capture=no 可以捕获print函数的输出
           -q: 简化输出信息
           -m: 运行指定标签的测试用例
           -x: 一旦错误，则停止运行
           --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
           "--reruns=3", "--reruns-delay=2"
    """
    # 生成测试html报告
    os.system(r"allure generate ./report -o ./report/html -clean")

    # 程序运行之后，自动启动报告，如果不想启动报告，可注释这段代码
    os.system(f"allure serve ./report -h 127.0.0.1 -p 9999")


if __name__ == '__main__':
    run()