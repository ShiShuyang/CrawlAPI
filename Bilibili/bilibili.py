import urllib2
import json
import time

f = open('290475975', 'r')
selfcookie = f.read()
f.close()

def judgecode(msg):
    code = ''
    ans = []
    for i in msg:
        if (i >= '0' and i <= '9') or (i >= 'A' and i <= 'F'):
            code += i
        else:
            code = ''
        if len(code) == 16:
            ans.append(str(code))
            code = ''
    return ans

def openurl(url, postarg = ''):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36')
    req.add_header('Cookie', selfcookie)
    try:
        return urllib2.urlopen(req, postarg, timeout = 10).read()
    except:
        print 'Timeout at', time.ctime(), 'withurl', url
        return openurl(url, postarg)

def exchange(code):
    print code,
    postarg = 'gift=' + code
    content = openurl('http://member.bilibili.com/store.html?act=gift&output=json', postarg)
    c = json.loads(content)
    if not c.has_key('msg'):
        postarg = 'confirm_gift=1&gift=' + code
        content = openurl('http://member.bilibili.com/store.html?act=gift&output=json', postarg)
        c = json.loads(content)
    print c['msg']

def opentopic(topicid, size = 20, page = 1):
    url = 'http://api.bilibili.com/feedback?type=jsonp&ver=3&mode=topic'
    url += '&tp_id={0}&pagesize={1}&page={2}'.format(str(topicid), str(size), str(page))                                               
    c = json.loads(openurl(url))
    msglist = []
    for i in c['list']:
        msg = c['list'][i]['msg']
        msglist.append(msg)
    return msglist

def openav(av, size = 20, page = 1):
    url = 'http://api.bilibili.com/feedback?type=jsonp&ver=3&mode=arc'
    url += '&aid={0}&pagesize={1}&page={2}'.format(str(av), str(size), str(page))                                               
    c = json.loads(openurl(url))
    msglist = []
    for i in c['list']:
        msg = c['list'][i]['msg']
        msglist.append(msg)
    return msglist

def useselfcoin():
    content = openurl('http://member.bilibili.com/message.do?act=notify_list&page=2')
    c = json.loads(content)
    for i in c:
        if i.isdigit():
            for j in judgecode(c[i]['msg']):
                exchange(j)

def getprize():
    url = 'http://www.bilibili.com/widget/ajaxGetGift'
    content = openurl(url, 'act=get_code&gift_id=75')
    return content
        
def main():
    used = []
    for i in xrange(285, 1000):
        print 'page', i 
        msglist = openav(2610147, 20, i)
        for i in msglist:
            for code in judgecode(i):
                if code not in used:
                    exchange(code)
                    used.append(code)
miaomiao = 1
if miaomiao:
    main()
else:                  
    for i in xrange(40):
        print getprize()
