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

if __name__ == "__main__":
    # getAwemeInfo()
    # getUserInfo()
    # getLiveInfo()
    pass
################################# 测试命令 ######################################################
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
#################################################################################################
