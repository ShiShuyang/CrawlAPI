# -*- coding: utf8 -*-
import urllib2
import urllib
import cookielib
import time
import random

def addfriend():
    for i in ['media', 'star', 'grass', 'content']:
        for j in xrange(1, 45):
            url = 'http://weibo.cn/pub/top?cat={0}&page={1}'.format(i, str(j))
            content = openurl(url)
            place = content.find('/attention/add')
            place2 = content.find('\">', place)
            while place != -1:
                url = 'http://weibo.cn' + content[place:place2]
                url = url.replace('&amp;', '&')
                ans = openurl(url)
                place = content.find('/attention/add', place2)
                place2 = content.find('\">', place)
    
    

def openurl(url = "http://weibo.cn/", method = "GET", poststring = ""):
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    if method == "GET":
        req = urllib2.Request(url)
    if method == "POST":
        req = urllib2.Request(url = url, data = poststring)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.802.30 Safari/535.1 SE 2.X MetaSr 1.0')#添加浏览器信息（可以无视）
    cookie = "_T_WM=27bfa645d2536a9aef44db88391c5337; SUB=_2A254Mj42DeTxGeNL7FoY9SbNwzqIHXVb3UJ-rDV6PUJbrdANLVXukW0_Ro3zEEoC8DC949PNDXyDszfDGg..; gsid_CTandWM=4u2Za2311sjf9deZeDczHnplc30"
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

def randomstring():
    a = "=。=,广告位招租,"
    a = a + "(⌒▽⌒),（￣▽￣）,(=・ω・=),(｀・ω・´),(〜￣△￣)〜,(･∀･),(°∀°)ﾉ,"
    a = a + "(￣3￣),╮(￣▽￣)╭,( ´_ゝ｀),←_←,→_→,(\"▔□▔)/,(ﾟДﾟ≡ﾟдﾟ)!?,Σ(ﾟдﾟ;),"
    a = a + "Σ( ￣□￣||),(´；ω；`),（/TДT)/,(^・ω・^ ),(｡･ω･｡),(●￣(ｴ)￣●),"
    a = a + "ε=ε=(ノ≧∇≦)ノ,(´･_･`),（￣へ￣）,ヽ(`Д´)ﾉ,(╯°口°)╯(┴—┴,_(:3」∠)_,"
    a = a.split(",")
    ans = random.choice(a)
    return ans

def main():
    last = ""
    while True:
        try:
            content = openurl("http://weibo.cn/", "GET")
            p1 = content.find("http://weibo.cn/comment/")
            p2 = content.find("?", p1)
            commentid = content[p1+24:p2]
            print time.ctime(), commentid
            if last and last != commentid and len(commentid)<20:
                last = commentid
                url = "http://weibo.cn/comment/" + commentid
                content = openurl(url)
                p1 = content.find(";st=")
                p2 = content.find("\">", p1)
                st = content[p1+4: p2]
                url = "http://weibo.cn/comments/addcomment?st=" + st
                word = "沙发" + randomstring() + "、、好吧我每次都是用程序抢的沙发。"
                postdata = "srcuid=1667911443&rl=1&content=" + word + "&id=" + commentid
                content = openurl(url, "POST", postdata)
                print "success"
            if last == '':
                last = commentid
        except Exception ,e:
            print e, last
        time.sleep(5)
        if time.localtime()[3] == 22:
            time.sleep(60*60*18)
        
addfriend()
