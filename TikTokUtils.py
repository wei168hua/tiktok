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
from urllib.parse import urlencode, unquote
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

    def getXbogus(self, url, cookie=None, referer="https://www.douyin.com/"):
        urls = Urls()
        headers = {
            "cookie": cookie,
            "referer": referer,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        try:
            if isinstance(url, dict):
                params = eval(unquote(url, 'utf-8'))
                url = urlencode(params, safe="=")
                response = json.loads(requests.post(
                    urls.GET_XB_DICT + url,
                    headers=headers).text)
            if isinstance(url, str):
                url = url.replace('&', '%26')
                response = json.loads(requests.post(
                    urls.GET_XB_PATH + url,
                    headers=headers).text)
            else:
                print('[  提示  ]:传入的参数有误')
        except Exception as e:
            print('[  错误  ]:%s' % e)

        params = response["result"][0]["paramsencode"]
        xb = response["result"][0]["X-Bogus"]["0"]
        # print('[  调试  ]:%s' % self.params)
        return params #, xb


if __name__ == "__main__":
    pass
