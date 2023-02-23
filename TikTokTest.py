#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Description:TikTok.py
@Date       :2023/02/11 13:06:23
@Author     :imgyh
@version    :1.0
@Github     :https://github.com/imgyh
@Mail       :admin@imgyh.com
-------------------------------------------------
Change Log  :
-------------------------------------------------
'''
import TikTokUtils
from TikTok import TikTok

def getAwemeInfo():
    share_link_video = "3.56 uSy:/ 复制打开抖音，看看【小透明的作品】没有女朋友就用我的吧哈哈哈哈 # 表情包锁屏  https://v.douyin.com/BugmVVD/"
    share_link_pic = "8.20 MJI:/ 复制打开抖音，看看【舍溪的图文作品】我又来放图集啦～还有你们要的小可爱大图也放啦～# ... https://v.douyin.com/BugrFTN/"
    tk = TikTok()

    url = tk.getShareLink(share_link_pic)
    key_type, key = tk.getKey(url)
    datanew, dataraw = tk.getAwemeInfo(key)
    print(datanew)

def getUserInfo():
    share_link_post = "1- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/BupCppt/"
    share_link_like = "2- 长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/BusJrfr/"
    tk = TikTok()

    url = tk.getShareLink(share_link_like)
    key_type, key = tk.getKey(url)
    awemeList = tk.getUserInfo(key, mode="like", count=35)
    print(awemeList)

def getLiveInfo():
    live_link = "https://live.douyin.com/40768897856"
    tk = TikTok()

    url = tk.getShareLink(live_link)
    key_type, key = tk.getKey(url)
    live_json = tk.getLiveInfo(key)
    print(live_json)

def getMixInfo():
    mix_link = 'https://v.douyin.com/B3J63Le/'
    tk = TikTok()

    url = tk.getShareLink(mix_link)
    key_type, key = tk.getKey(url)
    awemeList = tk.getMixInfo(key, count=35)
    print(len(awemeList))

def getUserAllMixInfo():
    user_all_mix_link = 'https://v.douyin.com/B38oovu/'
    tk = TikTok()

    url = tk.getShareLink(user_all_mix_link)
    key_type, key = tk.getKey(url)
    mixIdNameDict = tk.getUserAllMixInfo(key, count=35)
    print(mixIdNameDict)

def test():
    utils=TikTokUtils.Utils()
    user_all_mix_link = 'https://www.douyin.com/aweme/v1/web/aweme/post/?'+\
                        utils.getXbogus(url='device_platform=webapp&aid=6383&os_version=10&version_name=17.4.0&sec_user_id=MS4wLjABAAAA7G3S983y0b0m_7bcTSK7UzY-3hFJdHvMv-aVbbz0kIg&max_cursor=1626149119000&count=10')
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'referer': 'https://www.douyin.com/',
        'Cookie': 'ttwid=1%7CWBuxH_bhbuTENNtACXoesI5QHV2Dt9-vkMGVHSRRbgY%7C1677118712%7C1d87ba1ea2cdf05d80204aea2e1036451dae638e7765b8a4d59d87fa05dd39ff; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jc3IiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLVxyXG5NSUlCRFRDQnRRSUJBREFuTVFzd0NRWURWUVFHRXdKRFRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxXHJcbllYSmtNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUVKUDZzbjNLRlFBNUROSEcyK2F4bXAwNG5cclxud1hBSTZDU1IyZW1sVUE5QTZ4aGQzbVlPUlI4NVRLZ2tXd1FJSmp3Nyszdnc0Z2NNRG5iOTRoS3MvSjFJc3FBc1xyXG5NQ29HQ1NxR1NJYjNEUUVKRGpFZE1Cc3dHUVlEVlIwUkJCSXdFSUlPZDNkM0xtUnZkWGxwYmk1amIyMHdDZ1lJXHJcbktvWkl6ajBFQXdJRFJ3QXdSQUlnVmJkWTI0c0RYS0c0S2h3WlBmOHpxVDRBU0ROamNUb2FFRi9MQnd2QS8xSUNcclxuSURiVmZCUk1PQVB5cWJkcytld1QwSDZqdDg1czZZTVNVZEo5Z2dmOWlmeTBcclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'referer': 'https://www.douyin.com/',
        'Cookie': 'ttwid=1|sGp2L-Krm46cXHcK7BsKghavVeVQIIOYtQInA1LV0-w|1676899557|3e483426230c481bd34f4d6529d6252372c154b75be7d4a2baec8edbfd0a742c; __ac_signature=_02B4Z6wo00f01CEKaogAAIDBqkHxaCCYIyghKm4AAGu9c3; s_v_web_id=verify_ledo1j1t_0NwhDQFJ_nLca_42o5_8tAA_T8CWm5E2M6LF; msToken=%s;odin_tt=324fb4ea4a89c0c05827e18a1ed9cf9bf8a17f7705fcc793fec935b637867e2a5a9b8168c885554d029919117a18ba69;' % utils.generate_random_str(
            107)
    }
    import requests

    res = requests.get(user_all_mix_link,headers=headers1)
    print(res.text)

if __name__ == "__main__":
    # test()
    # getUserAllMixInfo()
    # getMixInfo()
    # getAwemeInfo()
    # getUserInfo()
    # getLiveInfo()
    pass
################################# 测试命令 ######################################################
# 直播
# python TikTokCommand.py -l https://live.douyin.com/759547612580 -p /mnt/c/project/test0
# .\TikTokCommand.exe -l https://live.douyin.com/759547612580 -p .\test0
# 视频
# python TikTokCommand.py -l https://v.douyin.com/BugmVVD/ -p /mnt/c/project/test1
# .\TikTokCommand.exe -l https://v.douyin.com/BugmVVD/ -p .\test1
# 图集
# python TikTokCommand.py -l https://v.douyin.com/BugrFTN/ -p /mnt/c/project/test2
# .\TikTokCommand.exe -l https://v.douyin.com/BugrFTN/ -p .\test2
# 主页作品(视频)
# python TikTokCommand.py -l https://v.douyin.com/BupCppt/ -p /mnt/c/project/test3
# .\TikTokCommand.exe -l https://v.douyin.com/BupCppt/ -p .\test3
# 主页作品(视频与图集混合)
# python TikTokCommand.py -l https://v.douyin.com/B72pdU5/ -p /mnt/c/project/test4
# .\TikTokCommand.exe -l https://v.douyin.com/B72pdU5/ -p .\test4
# 主页喜欢(视频)
# python TikTokCommand.py -l https://v.douyin.com/B72QgDw/ -p /mnt/c/project/test5 -M like
# .\TikTokCommand.exe -l https://v.douyin.com/B72QgDw/ -p .\test5 -M like
# 单个合集
# python TikTokCommand.py -l https://v.douyin.com/B3J63Le/ -p /mnt/c/project/test6
# .\TikTokCommand.exe -l https://v.douyin.com/B3J63Le/ -p .\test6
# 用户主页下所有合集
# python TikTokCommand.py -l https://v.douyin.com/B38oovu/ -p /mnt/c/project/test7 -M mix
# .\TikTokCommand.exe -l https://v.douyin.com/B38oovu/ -p .\test7 -M mix
#################################################################################################
