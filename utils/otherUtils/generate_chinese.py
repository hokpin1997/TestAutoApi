# -*- coding:utf-8 -*-
import random


def random_chinese(num):
    result = ''
    for i in range(num):
        char = chr(random.randint(0x4e00, 0x9fff))
        result += char
    return result


def generate_random_common_chinese_chars(count):
    common_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/一二三四五六七八九十百千万零'
    random_chars = ''.join(random.choices(common_chars, k=count))
    return random_chars


if __name__ == '__main__':
    # 生成 5 个汉字
    # 指定生成汉字数量
    num_chars = 10
    # 生成指定数量的随机汉字
    random_chars = generate_random_common_chinese_chars(num_chars)
    print("随机生成的汉字:", random_chars)