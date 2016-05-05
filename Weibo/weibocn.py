# -*- coding: utf8 -*-
import urllib2
import urllib
import cookielib
import time
import random

def openurl(url = "http://weibo.cn/", method = "GET", poststring = ""):
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    if method == "GET":
        req = urllib2.Request(url)
    if method == "POST":
        req = urllib2.Request(url = url, data = poststring)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.802.30 Safari/535.1 SE 2.X MetaSr 1.0')#添加浏览器信息（可以无视）
    cookie = "SUB=_2A257FnLvDeTxGeVI6VUZ-SjEyziIHXVY-R6nrDV6PUJbvNBeLVTFkW1GQh4R35MKIzjiFQUxJZaCuMcRhA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWMSv5OVnqiISM9L4KQVeNL5JpX5K-t; SUHB=0vJYV66RDAA76K; SSOLoginState=1444020927; _T_WM=277c9e8f68ba6f2f94b3112785653136"
    req.add_header('Cookie', cookie)
    content = urllib2.urlopen(req, timeout = 10).read()
    return content
    
def fanslist(userid, MAX_page = 20):
    l = []
    for i in xrange(MAX_page):
        url = "http://weibo.cn/" + str(userid) + "/fans?page=" + str(i+1)
        content = openurl(url)
        p1 = content.find("name=\"uidList\" value=")
        if p1 == -1:
            return l
        p2 = content.find("\" ", p1+15)
        for j in content[p1+22: p2].split(","):
            l.append(j)
    return l

def homepage(userid):
    content = openurl("http://weibo.cn/u/" + str(userid))
    return content


def main():
    for i in xrange(60, 500):
        c = openurl('http://weibo.cn/xwyt990?page=' + str(i))
        if ('张尧学' in c) or ('透明计算' in c) or ('自然' in c):
            print i

main()
