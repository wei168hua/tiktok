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

import re
import requests
import json
import time
import os
import copy

import TikTokUtils

'''
作品详情
https://www.iesdouyin.com/aweme/v1/web/aweme/detail/?aweme_id=%s&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333
1080p视频
https://aweme.snssdk.com/aweme/v1/play/?video_id=%s&ratio=1080p&line=0
主页作品
https://www.iesdouyin.com/aweme/v1/web/aweme/post/?sec_user_id=%s&count=%s&max_cursor=%s&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333
主页喜欢
https://www.iesdouyin.com/web/api/v2/aweme/like/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333
'''

class TikTok(object):

    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66',
            'Cookie': 'msToken=%s' % TikTokUtils.generate_random_str(107)
        }

        # 作者信息
        self.authorDict = {
            "avatar_thumb": {
                "height": "",
                "uri": "",
                "url_list": [],
                "width": ""
            },
            "avatar": {
                "height": "",
                "uri": "",
                "url_list": [],
                "width": ""
            },
            "cover_url": {
                "height": "",
                "uri": "",
                "url_list": [],
                "width": ""
            },
            # 喜欢的作品数
            "favoriting_count": "",
            # 粉丝数
            "follower_count": "",
            # 关注数
            "following_count": "",
            # 昵称
            "nickname": "",
            # 是否允许下载
            "prevent_download": "",
            # 用户 url id
            "sec_uid": "",
            # 是否私密账号
            "secret": "",
            # 短id
            "short_id": "",
            # 签名
            "signature": "",
            # 总获赞数
            "total_favorited": "",
            # 用户id
            "uid": "",
            # 用户自定义唯一id 抖音号
            "unique_id": "",
            # 年龄
            "user_age": "",

        }
        # 图片信息
        self.picDict = {
            "height": "",
            "mask_url_list": "",
            "uri": "",
            "url_list": [],
            "width": ""
        }
        # 音乐信息
        self.musicDict = {
            "cover_hd": {
                "height": "",
                "uri": "",
                "url_list": [],
                "width": ""
            },
            "cover_large": {
                "height": "",
                "uri": "",
                "url_list": [],
                "width": ""
            },
            "cover_medium": {
                "height": "",
                "uri": "",
                "url_list": [],
                "width": ""
            },
            "cover_thumb": {
                "height": "",
                "uri": "",
                "url_list": [],
                "width": ""
            },
            # 音乐作者抖音号
            "owner_handle": "",
            # 音乐作者id
            "owner_id": "",
            # 音乐作者昵称
            "owner_nickname": "",
            "play_url": {
                "height": "",
                "uri": "",
                "url_key": "",
                "url_list": [],
                "width": ""
            },
            # 音乐名字
            "title": "",
        }
        # 视频信息
        self.videoDict = {
            "play_addr": {
                "uri": "",
                "url_list": "",
            },
            "cover_original_scale": {
                "height": "",
                "uri": "",
                "url_list": [],
                "width": ""
            },
            "dynamic_cover": {
                "height": "",
                "uri": "",
                "url_list": [],
                "width": ""
            },
            "origin_cover": {
                "height": "",
                "uri": "",
                "url_list": [],
                "width": ""
            },
            "cover": {
                "height": "",
                "uri": "",
                "url_list": [],
                "width": ""
            }
        }
        # 作品信息
        self.awemeDict = {
            # 作品创建时间
            "create_time":"",
            # awemeType=0 视频， awemeType=1 图集
            "awemeType": "",
            # 作品 id
            "aweme_id": "",
            # 作者信息
            "author": self.authorDict,
            # 作品描述
            "desc": "",
            # 图片
            "images": [],
            # 音乐
            "music": self.musicDict,
            # 视频
            "video": self.videoDict,
            # 作品信息统计
            "statistics": {
                "admire_count": "",
                "collect_count": "",
                "comment_count": "",
                "digg_count": "",
                "play_count": "",
                "share_count": ""
            }
        }
        # 用户作品信息
        self.awemeList = []
        # 直播信息
        self.liveDict = {
            # 是否在播
            "status": "",
            # 直播标题
            "title": "",
            # 观看人数
            "user_count": "",
            # 昵称
            "nickname": "",
            # sec_uid
            "sec_uid": "",
            # 直播间观看状态
            "display_long": "",
            # 推流
            "flv_pull_url": "",
            # 分区
            "partition": "",
            "sub_partition": ""
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
            print('[  警告  ]:输入链接有误！\r')
            return key_type, key

        # 抖音把图集更新为note
        # 作品 第一步解析出来的链接是share/video/{aweme_id}
        # https://www.iesdouyin.com/share/video/7037827546599263488/?region=CN&mid=6939809470193126152&u_code=j8a5173b&did=MS4wLjABAAAA1DICF9-A9M_CiGqAJZdsnig5TInVeIyPdc2QQdGrq58xUgD2w6BqCHovtqdIDs2i&iid=MS4wLjABAAAAomGWi4n2T0H9Ab9x96cUZoJXaILk4qXOJlJMZFiK6b_aJbuHkjN_f0mBzfy91DX1&with_sec_did=1&titleType=title&schema_type=37&from_ssr=1&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme
        # 用户 第一步解析出来的链接是share/user/{sec_uid}
        # https://www.iesdouyin.com/share/user/MS4wLjABAAAA06y3Ctu8QmuefqvUSU7vr0c_ZQnCqB0eaglgkelLTek?did=MS4wLjABAAAA1DICF9-A9M_CiGqAJZdsnig5TInVeIyPdc2QQdGrq58xUgD2w6BqCHovtqdIDs2i&iid=MS4wLjABAAAAomGWi4n2T0H9Ab9x96cUZoJXaILk4qXOJlJMZFiK6b_aJbuHkjN_f0mBzfy91DX1&with_sec_did=1&sec_uid=MS4wLjABAAAA06y3Ctu8QmuefqvUSU7vr0c_ZQnCqB0eaglgkelLTek&from_ssr=1&u_code=j8a5173b&timestamp=1674540164&ecom_share_track_params=%7B%22is_ec_shopping%22%3A%221%22%2C%22secuid%22%3A%22MS4wLjABAAAA-jD2lukp--I21BF8VQsmYUqJDbj3FmU-kGQTHl2y1Cw%22%2C%22enter_from%22%3A%22others_homepage%22%2C%22share_previous_page%22%3A%22others_homepage%22%7D&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme
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
        elif "live.douyin.com" in r.url:
            key = r.url.replace('https://live.douyin.com/', '')
            key_type = "live"

        if key is None or key_type is None:
            print('[  警告  ]:输入链接有误！无法获取 id\r')
            return key_type, key
        print('[  提示  ]:作品或者用户的 id = %s\r' % key)

        return key_type, key

    # 将得到的json数据（dataRaw）精简成自己定义的数据（dataNew）
    # 转换得到的数据
    def dataConvert(self, awemeType, dataNew, dataRaw):
        for item in dataNew:
            try:
                # 作品创建时间
                if item == "create_time":
                    dataNew['create_time'] = time.strftime(
                    "%Y-%m-%d %H.%M.%S", time.localtime(dataRaw['create_time']))
                    continue
                # 设置 awemeType
                if item == "awemeType":
                    dataNew["awemeType"] = awemeType
                    continue
                # 当 解析的链接 是图片时
                if item == "images":
                    if awemeType == 1:
                        for image in dataRaw[item]:
                            for i in image:
                                self.picDict[i] = image[i]
                            # 字典要深拷贝
                            self.awemeDict["images"].append(copy.deepcopy(self.picDict))
                    continue
                # 当 解析的链接 是视频时
                if item == "video":
                    if awemeType == 0:
                        self.dataConvert(awemeType, dataNew[item], dataRaw[item])
                    continue
                # 将小头像放大
                if item == "avatar":
                    for i in dataNew[item]:
                        if i == "url_list":
                            for j in self.awemeDict["author"]["avatar_thumb"]["url_list"]:
                                dataNew[item][i].append(j.replace("100x100", "1080x1080"))
                        elif i == "uri":
                            dataNew[item][i] = self.awemeDict["author"]["avatar_thumb"][i].replace("100x100",
                                                                                                   "1080x1080")
                        else:
                            dataNew[item][i] = self.awemeDict["author"]["avatar_thumb"][i]
                    continue

                # 原来的json是[{}] 而我们的是 {}
                if item == "cover_url":
                    self.dataConvert(awemeType, dataNew[item], dataRaw[item][0])
                    continue

                # 根据 uri 获取 1080p 视频
                if item == "play_addr":
                    dataNew[item]["uri"] = dataRaw["bit_rate"][0]["play_addr"]["uri"]
                    # 使用 这个api 可以获得1080p
                    dataNew[item]["url_list"] = "https://aweme.snssdk.com/aweme/v1/play/?video_id=%s&ratio=1080p&line=0" \
                                                % dataNew[item]["uri"]
                    continue

                # 常规 递归遍历 字典
                if isinstance(dataNew[item], dict):
                    self.dataConvert(awemeType, dataNew[item], dataRaw[item])
                else:
                    # 赋值
                    dataNew[item] = dataRaw[item]
            except Exception as e:
                print("[  警告  ]:转换数据时在接口中未找到 %s\r" % (item))

    def clearDict(self, data):
        for item in data:
            # 常规 递归遍历 字典
            if isinstance(data[item], dict):
                self.clearDict(data[item])
            elif isinstance(data[item], list):
                data[item] = []
            else:
                data[item] = ""

    # 传入 aweme_id
    # 返回 数据 字典
    def getAwemeInfo(self, aweme_id):
        if aweme_id is None:
            return None
        # 官方接口
        # 旧接口22/12/23失效
        # jx_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={self.aweme_id[i]}'
        # 23/01/11
        # 此ies domian暂时不需要xg参数
        # 单作品接口返回 'aweme_detail'
        # 主页作品接口返回 'aweme_list'->['aweme_detail']
        jx_url = f'https://www.iesdouyin.com/aweme/v1/web/aweme/detail/?aweme_id={aweme_id}&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333'
        raw = requests.get(url=jx_url, headers=self.headers).text
        datadict = json.loads(raw)

        # 清空self.awemeDict
        self.clearDict(self.awemeDict)

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
        self.dataConvert(awemeType, self.awemeDict, datadict['aweme_detail'])

        return self.awemeDict

    # 传入 url 支持 https://www.iesdouyin.com 与 https://v.douyin.com
    # mode : post | like 模式选择 like为用户点赞 post为用户发布
    def getUserInfo(self, sec_uid, mode="post", count=35):
        if sec_uid is None:
            return None
        # 旧接口于22/12/23失效
        # post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=%s&count=35&max_cursor=0&aid=1128&_signature=PDHVOQAAXMfFyj02QEpGaDwx1S&dytk=' % (
        #     self.sec)
        # 23/1/11
        # 暂时使用不需要xg的接口
        max_cursor = 0
        self.awemeList = []

        print("[  提示  ]:正在获取接口数据请稍后...\r\n")

        while True:
            if mode == "post":
                post_url = 'https://www.iesdouyin.com/aweme/v1/web/aweme/post/?sec_user_id=%s&count=%s&max_cursor=%s&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333' % (
                    sec_uid, count, max_cursor)
            elif mode == "like":
                post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/like/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333' % (
                    sec_uid, count, max_cursor)
            else:
                print("[  错误  ]:模式选择错误, 仅支持post和like, 请检查后重新运行!\r")
                return None
            res = requests.get(url=post_url, headers=self.headers)

            datadict = json.loads(res.text)
            if not datadict["aweme_list"]:
                print("[  错误  ]:未找到数据, 请检查后重新运行!\r")
                return None

            for aweme in datadict["aweme_list"]:
                # 获取 aweme_id 使用这个接口 https://www.iesdouyin.com/aweme/v1/web/aweme/detail/
                aweme_id = aweme["aweme_id"]
                # 深拷贝 dict 不然list里面全是同样的数据
                self.awemeList.append(copy.deepcopy(self.getAwemeInfo(aweme_id)))

                # time.sleep(0.5)

            # 更新 max_cursor
            max_cursor = datadict["max_cursor"]

            # 退出条件
            if datadict["has_more"] != 1:
                break

        return self.awemeList

    def getLiveInfo(self, web_rid: str):

        # web_rid = live_url.replace('https://live.douyin.com/', '')

        live_api = 'https://live.douyin.com/webcast/web/enter/?aid=6383&web_rid=%s' % (web_rid)

        # 必须用这个 headers
        headers = {
            'Cookie': 'msToken=tsQyL2_m4XgtIij2GZfyu8XNXBfTGELdreF1jeIJTyktxMqf5MMIna8m1bv7zYz4pGLinNP2TvISbrzvFubLR8khwmAVLfImoWo3Ecnl_956MgOK9kOBdwM=; odin_tt=6db0a7d68fd2147ddaf4db0b911551e472d698d7b84a64a24cf07c49bdc5594b2fb7a42fd125332977218dd517a36ec3c658f84cebc6f806032eff34b36909607d5452f0f9d898810c369cd75fd5fb15; ttwid=1%7CfhiqLOzu_UksmD8_muF_TNvFyV909d0cw8CSRsmnbr0%7C1662368529%7C048a4e969ec3570e84a5faa3518aa7e16332cfc7fbcb789780135d33a34d94d2'
        }

        response = requests.get(live_api, headers=headers)

        live_json = json.loads(response.text)

        if live_json == {} or live_json['status_code'] != 0:
            print("[  警告  ]:接口未返回信息\r")
            return None

        # 清空字典
        self.clearDict(self.liveDict)

        # 是否在播
        self.liveDict["status"] = live_json['data']['data'][0]['status']

        if self.liveDict["status"] == 4:
            print('[   📺   ]:当前直播已结束，按回车退出')
            return self.liveDict

        # 直播标题
        self.liveDict["title"] = live_json['data']['data'][0]['title']

        # 观看人数
        self.liveDict["user_count"] = live_json['data']['data'][0]['user_count_str']

        # 昵称
        self.liveDict["nickname"] = live_json['data']['data'][0]['owner']['nickname']

        # sec_uid
        self.liveDict["sec_uid"] = live_json['data']['data'][0]['owner']['sec_uid']

        # 直播间观看状态
        self.liveDict["display_long"] = live_json['data']['data'][0]['room_view_stats']['display_long']

        # 推流
        self.liveDict["flv_pull_url"] = live_json['data']['data'][0]['stream_url']['flv_pull_url']

        try:
            # 分区
            self.liveDict["partition"] = live_json['data']['partition_road_map']['partition']['title']
            self.liveDict["sub_partition"] = live_json['data']['partition_road_map']['sub_partition']['partition'][
                'title']
        except Exception as e:
            self.liveDict["partition"] = '无'
            self.liveDict["sub_partition"] = '无'

        info = '[   💻   ]:直播间：%s  当前%s  主播：%s 分区：%s-%s\r' % (
            self.liveDict["title"], self.liveDict["display_long"], self.liveDict["nickname"],
            self.liveDict["partition"], self.liveDict["sub_partition"])
        print(info)

        flv = []
        print('[   🎦   ]:直播间清晰度')
        for i, f in enumerate(self.liveDict["flv_pull_url"].keys()):
            print('[   %s   ]: %s' % (i, f))
            flv.append(f)

        rate = int(input('[   🎬   ]输入数字选择推流清晰度：'))

        # 显示清晰度列表
        print('[   %s   ]:%s' % (flv[rate], self.liveDict["flv_pull_url"][flv[rate]]))

        print('[   📺   ]:复制链接使用下载工具下载')
        return self.liveDict

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
        try:
            # 使用作品 创建时间+描述 当文件夹
            file_name = TikTokUtils.replaceStr(awemeDict["create_time"] + awemeDict["desc"])
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
                music_name = TikTokUtils.replaceStr(awemeDict["music"]["title"])
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
            time.sleep(0.5)


if __name__ == "__main__":
    pass
