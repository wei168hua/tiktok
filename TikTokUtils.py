#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Description:TikTok.py
@Date       :2023/01/27 19:36:18
@Author     :imgyh
@version    :1.0
@Github     :https://github.com/imgyh
@Mail       :admin@imgyh.com
-------------------------------------------------
Change Log  :
-------------------------------------------------
'''

import random
import re
import json
import requests
from TikTokUrls import Urls


class Utils(object):
    def __init__(self):
        pass

    def generate_random_str(self, randomlength=16):
        """
        根据传入长度产生随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
        length = len(base_str) - 1
        for _ in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    def replaceStr(self, filenamestr: str):
        """
        替换非法字符，缩短字符长度，使其能成为文件名
        """
        # 匹配 汉字 字母 数字 空格
        match = "([0-9A-Za-z\u4e00-\u9fa5 -._]+)"

        result = re.findall(match, filenamestr)

        result = "".join(result).strip()
        if len(result) > 80:
            result = result[:80]
        # 去除前后空格
        return result

    def getXbogus(self, url, headers=None):
        urls = Urls()
        try:
            response = json.loads(requests.post(
                url= urls.GET_XB_PATH, data={"param" : url}, headers=headers).text)
        except Exception as e:
            print('[  错误  ]:%s' % e)

        params = response["param"]
        xb = response["X-Bogus"]

        return params #, xb


if __name__ == "__main__":
    pass
