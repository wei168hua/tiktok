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
Change Log  : 2023/02/11 修改接口
-------------------------------------------------
'''

import re
import requests
import json
import time
import os
import copy

from TikTokUtils import Utils
from TikTokUrls import Urls
from TikTokResult import Result


class TikTok(object):

    def __init__(self):
        self.urls = Urls()
        self.utils = Utils()
        self.result = Result()
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'referer': 'https://www.douyin.com/',
        'Cookie': 'ttwid=1|sGp2L-Krm46cXHcK7BsKghavVeVQIIOYtQInA1LV0-w|1676899557|3e483426230c481bd34f4d6529d6252372c154b75be7d4a2baec8edbfd0a742c; __ac_signature=_02B4Z6wo00f01CEKaogAAIDBqkHxaCCYIyghKm4AAGu9c3; s_v_web_id=verify_ledo1j1t_0NwhDQFJ_nLca_42o5_8tAA_T8CWm5E2M6LF; msToken=%s;odin_tt=324fb4ea4a89c0c05827e18a1ed9cf9bf8a17f7705fcc793fec935b637867e2a5a9b8168c885554d029919117a18ba69;' % self.utils.generate_random_str(107)
        }


    # 从分享链接中提取网址
    def getShareLink(self, string):
        # findall() 查找匹配正则表达式的字符串
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)[0]

    # 得到 作品id 或者 用户id
    # 传入 url 支持 https://www.iesdouyin.com 与 https://v.douyin.com
    def getKey(self, url):
        key = None
        key_type = None

        try:
            r = requests.get(url=url, headers=self.headers)
        except Exception as e:
            print('[  错误  ]:输入链接有误！\r')
            return key_type, key

        # 抖音把图集更新为note
        # 作品 第一步解析出来的链接是share/video/{aweme_id}
        # https://www.iesdouyin.com/share/video/7037827546599263488/?region=CN&mid=6939809470193126152&u_code=j8a5173b&did=MS4wLjABAAAA1DICF9-A9M_CiGqAJZdsnig5TInVeIyPdc2QQdGrq58xUgD2w6BqCHovtqdIDs2i&iid=MS4wLjABAAAAomGWi4n2T0H9Ab9x96cUZoJXaILk4qXOJlJMZFiK6b_aJbuHkjN_f0mBzfy91DX1&with_sec_did=1&titleType=title&schema_type=37&from_ssr=1&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme
        # 用户 第一步解析出来的链接是share/user/{sec_uid}
        # https://www.iesdouyin.com/share/user/MS4wLjABAAAA06y3Ctu8QmuefqvUSU7vr0c_ZQnCqB0eaglgkelLTek?did=MS4wLjABAAAA1DICF9-A9M_CiGqAJZdsnig5TInVeIyPdc2QQdGrq58xUgD2w6BqCHovtqdIDs2i&iid=MS4wLjABAAAAomGWi4n2T0H9Ab9x96cUZoJXaILk4qXOJlJMZFiK6b_aJbuHkjN_f0mBzfy91DX1&with_sec_did=1&sec_uid=MS4wLjABAAAA06y3Ctu8QmuefqvUSU7vr0c_ZQnCqB0eaglgkelLTek&from_ssr=1&u_code=j8a5173b&timestamp=1674540164&ecom_share_track_params=%7B%22is_ec_shopping%22%3A%221%22%2C%22secuid%22%3A%22MS4wLjABAAAA-jD2lukp--I21BF8VQsmYUqJDbj3FmU-kGQTHl2y1Cw%22%2C%22enter_from%22%3A%22others_homepage%22%2C%22share_previous_page%22%3A%22others_homepage%22%7D&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme
        # 合集
        # https://www.douyin.com/collection/7093490319085307918
        urlstr = str(r.request.path_url)

        if "/share/user/" in urlstr:
            # 获取用户 sec_uid
            if '?' in r.request.path_url:
                for one in re.finditer(r'user\/([\d\D]*)([?])', str(r.request.path_url)):
                    key = one.group(1)
            else:
                for one in re.finditer(r'user\/([\d\D]*)', str(r.request.path_url)):
                    key = one.group(1)
            key_type = "user"
        elif "/share/video/" in urlstr:
            # 获取作品 aweme_id
            key = re.findall('video/(\d+)?', urlstr)[0]
            key_type = "aweme"
        elif "/collection/" in urlstr:
            # 获取作品 aweme_id
            key = re.findall('collection/(\d+)?', urlstr)[0]
            key_type = "mix"
        elif "live.douyin.com" in r.url:
            key = r.url.replace('https://live.douyin.com/', '')
            key_type = "live"

        if key is None or key_type is None:
            print('[  错误  ]:输入链接有误！无法获取 id\r')
            return key_type, key

        return key_type, key

    # 传入 aweme_id
    # 返回 数据 字典
    def getAwemeInfo(self, aweme_id):
        print('[  提示  ]:正在请求的作品 id = %s\r\n' % aweme_id)
        if aweme_id is None:
            return None

        # 单作品接口返回 'aweme_detail'
        # 主页作品接口返回 'aweme_list'->['aweme_detail']
        jx_url = self.urls.POST_DETAIL + self.utils.getXbogus(
            url=f'aweme_id={aweme_id}&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333')
        try:
            raw = requests.get(url=jx_url, headers=self.headers).text
            datadict = json.loads(raw)
        except Exception as e:
            print("[  错误  ]:接口未返回数据, 请检查后重新运行!\r")
            return None

        # 清空self.awemeDict
        self.result.clearDict(self.result.awemeDict)

        if datadict['aweme_detail'] is None:
            print('[  错误  ]:作品不存在, 请检查后重新运行!\r')
            return None
        # 默认为视频
        awemeType = 0
        try:
            # datadict['aweme_detail']["images"] 不为 None 说明是图集
            if datadict['aweme_detail']["images"] is not None:
                awemeType = 1
        except Exception as e:
            print("[  警告  ]:接口中未找到 images\r")

        # 转换成我们自己的格式
        self.result.dataConvert(awemeType, self.result.awemeDict, datadict['aweme_detail'])

        return self.result.awemeDict, datadict

    # 传入 url 支持 https://www.iesdouyin.com 与 https://v.douyin.com
    # mode : post | like 模式选择 like为用户点赞 post为用户发布
    def getUserInfo(self, sec_uid, mode="post", count=35):
        print('[  提示  ]:正在请求的用户 id = %s\r\n' % sec_uid)
        if sec_uid is None:
            return None

        max_cursor = 0
        awemeList = []

        print("[  提示  ]:正在获取所有作品数据请稍后...\r")
        print("[  提示  ]:会进行多次请求，等待时间较长...\r\n")
        times = 0
        while True:
            times = times + 1
            print("[  提示  ]:正在进行第 " + str(times) + " 次请求...\r")
            if mode == "post":
                url = self.urls.USER_POST + self.utils.getXbogus(
                        url=f'sec_uid={sec_uid}&count={count}&max_cursor={max_cursor}')
            elif mode == "like":
                url = self.urls.USER_FAVORITE_A + self.utils.getXbogus(
                    url=f'sec_user_id={sec_uid}&count={count}&max_cursor={max_cursor}&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333')
            else:
                print("[  错误  ]:模式选择错误, 仅支持post、like、mix, 请检查后重新运行!\r")
                return None

            while True:
                # 接口不稳定, 有时服务器不返回数据, 需要重新获取
                try:
                    res = requests.get(url=url, headers=self.headers)
                    datadict = json.loads(res.text)
                    print('[  提示  ]:本次请求返回 ' + str(len(datadict["aweme_list"])) + ' 条数据')
                    if datadict is not None and datadict["status_code"] == 0:
                        break
                except Exception as e:
                    print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

            for aweme in datadict["aweme_list"]:
                # 获取 aweme_id
                aweme_id = aweme["aweme_id"]
                # 深拷贝 dict 不然list里面全是同样的数据
                datanew, dataraw = self.getAwemeInfo(aweme_id)
                awemeList.append(copy.deepcopy(datanew))

            # 更新 max_cursor
            max_cursor = datadict["max_cursor"]

            # 退出条件
            if datadict["has_more"] == 0 or datadict["has_more"] == False:
                print("[  提示  ]:所有作品数据获取完成...\r\n")
                break
            else:
                print("[  提示  ]:第 " + str(times) + " 次请求成功...\r\n")

        return awemeList

    def getLiveInfo(self, web_rid: str):
        print('[  提示  ]:正在请求的直播间 id = %s\r\n' % web_rid)

        # web_rid = live_url.replace('https://live.douyin.com/', '')

        live_api = 'https://live.douyin.com/webcast/room/web/enter/?aid=6383&device_platform=web&web_rid=%s' % (web_rid)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'cookie' : '__ac_nonce=063f2f2fe002b0c1cf5a3; ttwid=1|_P0qI1eym6Of_Wz2s3FhDRThixb46o2hSYqHFIcdaHM|1676866302|3dd715d4512ff13abbd1aaedc19257b8bfe55b2bbbcad6a95de237776729ba54'
        }

        try:
            response = requests.get(live_api, headers=headers)
            live_json = json.loads(response.text)
        except Exception as e:
            print("[  错误  ]:接口未返回数据, 请检查后重新运行!\r")
            return None

        if live_json == {} or live_json['status_code'] != 0:
            print("[  错误  ]:接口未返回信息\r")
            return None

        # 清空字典
        self.result.clearDict(self.result.liveDict)

        # 是否在播
        self.result.liveDict["status"] = live_json['data']['data'][0]['status']

        if self.result.liveDict["status"] == 4:
            print('[   📺   ]:当前直播已结束，正在退出')
            return self.result.liveDict

        # 直播标题
        self.result.liveDict["title"] = live_json['data']['data'][0]['title']

        # 观看人数
        self.result.liveDict["user_count"] = live_json['data']['data'][0]['user_count_str']

        # 昵称
        self.result.liveDict["nickname"] = live_json['data']['data'][0]['owner']['nickname']

        # sec_uid
        self.result.liveDict["sec_uid"] = live_json['data']['data'][0]['owner']['sec_uid']

        # 直播间观看状态
        self.result.liveDict["display_long"] = live_json['data']['data'][0]['room_view_stats']['display_long']

        # 推流
        self.result.liveDict["flv_pull_url"] = live_json['data']['data'][0]['stream_url']['flv_pull_url']

        try:
            # 分区
            self.result.liveDict["partition"] = live_json['data']['partition_road_map']['partition']['title']
            self.result.liveDict["sub_partition"] = live_json['data']['partition_road_map']['sub_partition']['partition'][
                'title']
        except Exception as e:
            self.result.liveDict["partition"] = '无'
            self.result.liveDict["sub_partition"] = '无'

        info = '[   💻   ]:直播间：%s  当前%s  主播：%s 分区：%s-%s\r' % (
            self.result.liveDict["title"], self.result.liveDict["display_long"], self.result.liveDict["nickname"],
            self.result.liveDict["partition"], self.result.liveDict["sub_partition"])
        print(info)

        flv = []
        print('[   🎦   ]:直播间清晰度')
        for i, f in enumerate(self.result.liveDict["flv_pull_url"].keys()):
            print('[   %s   ]: %s' % (i, f))
            flv.append(f)

        rate = int(input('[   🎬   ]输入数字选择推流清晰度：'))

        # 显示清晰度列表
        print('[   %s   ]:%s' % (flv[rate], self.result.liveDict["flv_pull_url"][flv[rate]]))

        print('[   📺   ]:复制链接使用下载工具下载')
        return self.result.liveDict

    def getMixInfo(self, mix_id: str, count=35):
        print('[  提示  ]:正在请求的合集 id = %s\r\n' % mix_id)
        if mix_id is None:
            return None

        cursor = 0
        awemeList = []

        print("[  提示  ]:正在获取合集下的所有作品数据请稍后...\r")
        print("[  提示  ]:会进行多次请求，等待时间较长...\r\n")
        times = 0
        while True:
            times = times + 1
            print("[  提示  ]:正在进行第 " + str(times) + " 次请求...\r")

            url = 'https://www.douyin.com/aweme/v1/web/mix/aweme/?' + self.utils.getXbogus(
                url=f'device_platform=webapp&aid=6383&os_version=10&version_name=17.4.0&mix_id={mix_id}&cursor={cursor}&count={count}')

            while True:
                # 接口不稳定, 有时服务器不返回数据, 需要重新获取
                try:
                    res = requests.get(url=url, headers=self.headers)
                    datadict = json.loads(res.text)
                    print('[  提示  ]:本次请求返回 ' + str(len(datadict["aweme_list"])) + ' 条数据')
                    if datadict is not None:
                        break
                except Exception as e:
                    print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

            for aweme in datadict["aweme_list"]:
                # 获取 aweme_id
                aweme_id = aweme["aweme_id"]
                # 深拷贝 dict 不然list里面全是同样的数据
                datanew, dataraw = self.getAwemeInfo(aweme_id)
                awemeList.append(copy.deepcopy(datanew))

            # 更新 max_cursor
            cursor = datadict["cursor"]

            # 退出条件
            if datadict["has_more"] == 0 or datadict["has_more"] == False:
                print("\r\n[  提示  ]:合集下所有作品数据获取完成...\r\n")
                break
            else:
                print("[  提示  ]:第 " + str(times) + " 次请求成功...\r\n")

        return awemeList

    def getUserAllMixInfo(self, sec_uid, count=35):
        print('[  提示  ]:正在请求的用户 id = %s\r\n' % sec_uid)
        if sec_uid is None:
            return None

        cursor = 0
        mixIdNameDict = {}

        print("[  提示  ]:正在获取所有合集 id 数据请稍后...\r")
        print("[  提示  ]:会进行多次请求，等待时间较长...\r\n")
        times = 0
        while True:
            times = times + 1
            print("[  提示  ]:正在进行第 " + str(times) + " 次请求...\r")

            url = self.urls.USER_MIX_LIST + self.utils.getXbogus(
                url=f'device_platform=webapp&aid=6383&os_version=10&version_name=17.4.0&sec_user_id={sec_uid}&count={count}&cursor={cursor}')

            while True:
                # 接口不稳定, 有时服务器不返回数据, 需要重新获取
                try:
                    res = requests.get(url=url, headers=self.headers)
                    datadict = json.loads(res.text)
                    print('[  提示  ]:本次请求返回 ' + str(len(datadict["mix_infos"])) + ' 条数据')
                    if datadict is not None and datadict["status_code"] == 0:
                        break
                except Exception as e:
                    print("[  警告  ]:接口未返回数据, 正在重新请求!\r")

            for mix in datadict["mix_infos"]:
                mixIdNameDict[mix["mix_id"]] = mix["mix_name"]

            # 更新 max_cursor
            cursor = datadict["cursor"]

            # 退出条件
            if datadict["has_more"] == 0 or datadict["has_more"] == False:
                print("[  提示  ]:所有合集 id 数据获取完成...\r\n")
                break
            else:
                print("[  提示  ]:第 " + str(times) + " 次请求成功...\r\n")

        return mixIdNameDict

    # 来自 https://blog.csdn.net/weixin_43347550/article/details/105248223
    def progressBarDownload(self, url, filepath):
        start = time.time()  # 下载开始时间
        response = requests.get(url, stream=True, headers=self.headers)
        size = 0  # 初始化已下载大小
        chunk_size = 1024  # 每次下载的数据大小
        content_size = int(response.headers['content-length'])  # 下载文件总大小
        try:
            if response.status_code == 200:  # 判断是否响应成功
                print('[ 开始下载 ]:文件大小:{size:.2f} MB'.format(
                    size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
                with open(filepath, 'wb') as file:  # 显示进度条
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        print('\r' + '[ 下载进度 ]:%s%.2f%%' % (
                            '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
            end = time.time()  # 下载结束时间
            print('\n' + '[ 下载完成 ]:耗时: %.2f秒\n' % (
                    end - start))  # 输出下载用时时间
        except Exception as e:
            # 下载异常 删除原来下载的文件, 可能未下成功
            if os.path.exists(filepath):
                os.remove(filepath)
            print("[  错误  ]:下载出错\r")

    def awemeDownload(self, awemeDict: dict, music=True, cover=True, avatar=True, savePath=os.getcwd()):
        if awemeDict is None:
            return
        if not os.path.exists(savePath):
            os.mkdir(savePath)

        try:
            # 使用作品 创建时间+描述 当文件夹
            file_name = self.utils.replaceStr(awemeDict["create_time"] + " " + awemeDict["desc"])
            aweme_path = os.path.join(savePath, file_name)
            if not os.path.exists(aweme_path):
                os.mkdir(aweme_path)

            # 保存获取到的字典信息
            print("[  提示  ]:正在保存获取到的信息到result.json\r\n")
            with open(os.path.join(aweme_path, "result.json"), "w", encoding='utf-8') as f:
                f.write(json.dumps(awemeDict, ensure_ascii=False, indent=2))
                f.close()

            # 下载  视频
            if awemeDict["awemeType"] == 0:
                print("[  提示  ]:正在下载视频...\r")
                video_path = os.path.join(aweme_path, file_name + ".mp4")

                if os.path.exists(video_path):
                    print("[  提示  ]:视频已存在为您跳过...\r\n")
                else:
                    try:
                        url = awemeDict["video"]["play_addr"]["url_list"]
                        if url != "":
                            self.progressBarDownload(url, video_path)
                    except Exception as e:
                        print("[  错误  ]:无法获取到视频url\r\n")

            # 下载 图集
            if awemeDict["awemeType"] == 1:
                print("[  提示  ]:正在下载图集...\r")
                for ind, image in enumerate(awemeDict["images"]):
                    image_path = os.path.join(aweme_path, "image" + str(ind) + ".jpeg")
                    if os.path.exists(image_path):
                        print("[  提示  ]:图片已存在为您跳过...\r\n")
                    else:
                        try:
                            url = image["url_list"][0]
                            if url != "":
                                self.progressBarDownload(url, image_path)
                        except Exception as e:
                            print("[  错误  ]:无法获取到图片url\r\n")

            # 下载  音乐
            if music:
                print("[  提示  ]:正在下载音乐...\r")
                music_name = self.utils.replaceStr(awemeDict["music"]["title"])
                music_path = os.path.join(aweme_path, music_name + ".mp3")

                if os.path.exists(music_path):
                    print("[  提示  ]:音乐已存在为您跳过...\r\n")
                else:
                    try:
                        url = awemeDict["music"]["play_url"]["url_list"][0]
                        if url != "":
                            self.progressBarDownload(url, music_path)
                    except Exception as e:
                        print("[  错误  ]:无法获取到音乐url\r\n")

            # 下载  cover
            if cover and awemeDict["awemeType"] == 0:
                print("[  提示  ]:正在下载视频cover图...\r")
                cover_path = os.path.join(aweme_path, "cover.jpeg")

                if os.path.exists(cover_path):
                    print("[  提示  ]:cover 已存在为您跳过...\r\n")
                else:
                    try:
                        url = awemeDict["video"]["cover_original_scale"]["url_list"][0]
                        if url != "":
                            self.progressBarDownload(url, cover_path)
                    except Exception as e:
                        print("[  错误  ]:无法获取到cover url\r\n")

            # 下载  avatar
            if avatar:
                print("[  提示  ]:正在下载用户头像...\r")
                avatar_path = os.path.join(aweme_path, "avatar.jpeg")

                if os.path.exists(avatar_path):
                    print("[  提示  ]:avatar 已存在为您跳过...\r\n")
                else:
                    try:
                        url = awemeDict["author"]["avatar"]["url_list"][0]
                        if url != "":
                            self.progressBarDownload(url, avatar_path)
                    except Exception as e:
                        print("[  错误  ]:无法获取到avatar url\r\n")
        except Exception as e:
            print("[  错误  ]:请检查json信息是否正确\r\n")

    def userDownload(self, awemeList: list, music=True, cover=True, avatar=True, savePath=os.getcwd()):
        if awemeList is None:
            return
        if not os.path.exists(savePath):
            os.mkdir(savePath)
        for ind, aweme in enumerate(awemeList):
            print("[  提示  ]:正在下载 %s 的作品 %s/%s\r"
                  % (aweme["author"]["nickname"], str(ind + 1), len(awemeList)))

            self.awemeDownload(aweme, music, cover, avatar, savePath)
            # time.sleep(0.5)


if __name__ == "__main__":
    pass
