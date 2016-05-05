import urllib2
from StringIO import StringIO
import gzip
import pyodbc

f = open('cookie', 'r')
mycookie =  f.read()
f.close()

def openurl(url):
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    request.add_header('Cookie', mycookie)
    opener = urllib2.build_opener()
    try:
        f = opener.open(request, timeout = 10)
        isGzip = f.headers.get('Content-Encoding')
        if isGzip :
            compresseddata = f.read()
            compressedstream = StringIO(compresseddata)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            data = gzipper.read()
        else:
            data = f.read()
        return data
    except Exception, e:
        if '404' in str(e):
            return ''
        return openurl(url)

def gethtmlinfo(av):
    url = 'http://www.bilibili.com/video/av' + str(av)
    content = openurl(url)
    #print content
    p1 = content.find(',cid=')
    p2 = content.find('&', p1)
    if p1 > 0 and p2 > 0:
        cid = content[p1+5:p2]
    else:
        cid = ''    
    p1 = content.find('wb_title')
    p2 = content.find('\';', p1)
    title = content[p1+10:p2] 
    f = open('miao.txt', 'w')
    f.write(title)
    f.close()
    p1 = content.find('a class=\"name\" href=\"http://space.bilibili.com/')
    p2 = content.find('\" card', p1)
    if p1 > 0 and p2 > 0:
        upid = content[p1+47:p2]
    else:
        upid = ''
    p1 = content.find('<i>20')
    p2 = content.find('</i></time>')
    if p1 != -1:
        startDate = content[p1+3:p2]
    else:
        startDate = '2000-01-01 00:00:00.000'
    d = {'cid':cid, 'title':title, 'upid':upid, 'startDate':startDate}
    return d

def getxmlinfo(av, cid):
    url = 'http://interface.bilibili.com/player?id=cid:{0}&aid={1}'.format(str(cid), str(av))
    content = openurl(url)
    xmlitem = ['click',  'favourites', 'coins', 'acceptguest']
    d = {}
    
    for i in xmlitem:
        p1 = content.find('<{0}>'.format(i))
        p2 = content.find('</{0}>'.format(i))
        d[i] = content[p1+len(i)+2:p2]
    if d['acceptguest'] == 'true':
        d['acceptguest'] = 1
    else:
        d['acceptguest'] = 0
    return d

def add2db(d):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=127.0.0.1;DATABASE=bili;')
    cursor = cnxn.cursor()
    sql = "INSERT INTO baseinfo ("
    for i in d:
        sql += i + ','
    sql = sql[:-1] + ') VALUES ('
    for i in d:
        if type(d[i]) is type('miao') and not d[i].isdigit():
            sql += '\'' + str(d[i]).decode('utf8').replace('\'', '') + '\','
        else:
            sql += str(d[i]) + ','
    sql = sql[:-1] + ')'
    print sql
    cnxn.execute(sql)
    cnxn.commit()
    cnxn.close()

def getlastav():
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=127.0.0.1;DATABASE=bili;')
    cursor = cnxn.cursor()
    sql = 'SELECT TOP 1 av FROM baseinfo ORDER BY av DESC'
    cursor.execute(sql)
    row = cursor.fetchone()
    startav = row[0]
    cursor.close()
    cnxn.close()
    return startav

def main():
    for av in xrange(getlastav()+1, 1000000):        
        d = gethtmlinfo(av)
        if d['cid'] and d['upid']:
            d['av'] = av
            d.update(getxmlinfo(av, d['cid']))
            add2db(d)
            #print av, cid, title, upid, click, favourites, coins, acceptguest, startDate 

main()
