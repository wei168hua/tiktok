import requests, re, os, time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class TikTok(object):

    # 利用selenium可以获取cookies
    def __init__(self):
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')  # 设置option
        # option.add_argument("--headless")
        # option.add_argument('--disable-gpu')  # 一些情况下使用headless GPU会有问题（我没遇到）
        # option.add_argument('window-size=1920x1080')  # 页面部分内容是动态加载得时候，无头模式默认size为0x0，需要设置最大化窗口并设置windowssize，不然会出现显示不全的问题
        # option.add_argument('--start-maximized')  # 页面部分内容是动态加载得时候，无头模式默认size为0x0，需要设置最大化窗口并设置windowssize，不然会出现显示不全的问题
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
        # self.driver.get("https://www.douyin.com")
        # # 获取cookie
        # cookie_items = self.driver.get_cookies()
        # cookie_str = ""
        # # 组装cookie字符串
        # for item_cookie in cookie_items:
        #     item_str = item_cookie["name"] + "=" + item_cookie["value"] + "; "
        #     cookie_str += item_str
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }

    def videoShareLinkConvert(self, shareLink="https://v.douyin.com/kcvMpuN/"):
        temp = shareLink.split("com/")[1].split("/")[0]
        shareUrl = "https://v.douyin.com/" + temp
        # 获取 awemeId
        r = requests.get(shareUrl, self.headers)
        awemeId = r.url.split('/')[5]
        # print(awemeId)
        return "https://www.douyin.com/video/" + awemeId

    # 视频基本信息
    def oneVideoInfo(self, url="https://www.douyin.com/video/6915675899241450760"):
        self.driver.get(url)
        html = self.driver.page_source
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        # 视频资源地址
        list = soup.findAll(name="source")
        # print(list)
        videoRealUrl = list[2].get("src")
        videoRealUrl = "https:" + videoRealUrl.split('&')[0] + "&ratio=1080p&line=0"

        print(videoRealUrl)
        return videoRealUrl

    def userShareLinkConvert(self, shareLink="https://v.douyin.com/kcvSCe9/"):
        temp = shareLink.split("com/")[1].split("/")[0]
        shareUrl = "https://v.douyin.com/" + temp
        # 获取 userId
        r = requests.get(shareUrl, self.headers)
        userId = r.url.split("?")[0].split("user/")[1]
        # print(userId)
        return "https://www.douyin.com/user/" + userId

    # 用户基本信息
    def userVideoInfo(self, url="https://www.douyin.com/user/MS4wLjABAAAA06y3Ctu8QmuefqvUSU7vr0c_ZQnCqB0eaglgkelLTek"):
        self.driver.get(url)
        # 模拟鼠标下滑
        js = "var q=document.documentElement.scrollTop=100000"
        while True:
            self.driver.execute_script(js)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            # print(len(soup.findAll(name="div", attrs={"class": "Sr905S5u"})))
            # 滑到底部 Sr905S5u 这个div会消失
            if len(soup.findAll(name="div", attrs={"class": "Sr905S5u"})) == 0:
                break
            time.sleep(1)
        # 视频资源地址
        list = soup.findAll(name="a", attrs={"class": "B3AsdZT9 chmb2GX8"})
        userVideoUrls = []
        for i in list:
            # print("https://www.douyin.com" + i.get("href"))
            videoRealUrl = self.oneVideoInfo("https://www.douyin.com" + i.get("href"))
            userVideoUrls.append(videoRealUrl)
        return userVideoUrls

tk = TikTok()
# tk.oneVideoInfo()
tk.userVideoInfo()
tk.driver.quit()
