# -*- coding: utf8 -*-

import StringIO
import time
import gzip
import urllib2
import cookielib
import zhanghao
import random

cj = cookielib.MozillaCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

def tmp():
    captcha = "https://secure.bilibili.com/captcha"

def openurl(url, needgzip = True):
    req = urllib2.Request(url = url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.802.30 Safari/535.1 SE 2.X MetaSr 1.0')
    content = urllib2.urlopen(req).read()
    if needgzip:
        video_page_buffer = StringIO.StringIO(content)
        video_page_html = gzip.GzipFile(fileobj = video_page_buffer).read()
        return video_page_html
    else:
        return content

def posturl(url, postdata):
    req = urllib2.Request(url = url, data = postdata)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.802.30 Safari/535.1 SE 2.X MetaSr 1.0')
    content = urllib2.urlopen(req).read()
    return content


def login(userid, pw):
    f = open("url.txt", "a")
    url = "https://secure.bilibili.com/login"
    a = "act=login&gourl=http%3A%2F%2Fwww.bilibili.com%2F&keeptime=604800&userid=madokasama%40foxmail.com&pwd=koudai8hot&vdcode=6RHGG&keeptime=2592000"
    filedata = urllib2.urlopen("https://secure.bilibili.com/captcha").read()
    imagefiledata = cv.CreateMatHeader(1, len(filedata), cv.CV_8UC1)
    cv.SetData(imagefiledata, filedata, len(filedata))
    img0 = cv.DecodeImage(imagefiledata, cv.CV_LOAD_IMAGE_COLOR)
    cv.ShowImage("captchas", img0)
    cv.WaitKey()
    captchas = raw_input("Please enter the captchas:")
    cv.DestroyAllWindows()
    postdata = "act=login&gourl=http%3A%2F%2Fwww.bilibili.com%2F&keeptime=604800&userid="
    postdata += userid + "&pwd=" + pw + "&vdcode=" + captchas
    geturl = posturl(url, postdata)
    p1 = geturl.find("location='")
    p2 = geturl.find("\';", p1)
    geturl = geturl[p1+10: p2]
    print geturl
    f.write(geturl + "\n")
    f.close()

def foravrecord(times = 1):
    while (times):
        times -= 1
        c = openurl("http://www.bilibili.com/random")
        p1 = c.find("cid=")
        p2 = c.find("aid=", p1)
        cid = c[p1+4: p2-1]
        p1 = c.find("\"", p2)
        aid = c[p2+4: p1-1]
        print cid, aid
        url = "http://interface.bilibili.com/player?id=cid:"
        url += cid + "&aid=" + aid
        try:
            print openurl(url, False)
            url = "http://interface.bilibili.com/count?aid=" + aid
            openurl(url, False)
        except:
            pass
        time.sleep(80+random.randint(0,100))

def addview(av):
        c = openurl("http://www.bilibili.com/video/av" + str(av))
        p1 = c.find("cid=")
        p2 = c.find("aid=", p1)
        cid = c[p1+4: p2-1]
        p1 = c.find("\"", p2)
        aid = c[p2+4: p1]
        print cid, aid
        url = "http://interface.bilibili.com/player?id=cid:"
        url += cid + "&aid=" + aid
        try:
            openurl(url, False)
            url = "http://interface.bilibili.com/count?aid=" + aid
            openurl(url, False)
        except:
            pass

def shua():
    openurl("http://www.bilibili.com", False)
    foravrecord(6)
    
def needloginagain():
    f = open("url.txt", "w")
    f.close()
    a = zhanghao.zhanghao()
    for i in a:
        print i, a[i]
        login(i, a[i])
        cj.clear()

def comment(av):
    url = "http://www.bilibili.com/plus/comment.php"
    postdata = "rating=99&player=1&multiply=1&aid=" + str(av)
    return posturl(url, postdata).decode("utf8")

def main():

    a = zhanghao.readurl()
    for count in xrange(1, 100):
        for i in a:
            try:
                openurl(i, False)
                print openurl("http://interface.bilibili.com/nav.js", False)
                #shua()
                print comment(1654042)

                time.sleep(540)
                cj.clear()
            except:
                print "an error accoured"
    
main()    
    
    
