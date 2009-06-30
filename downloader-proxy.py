#!/bin/python
# -*- coding: UTF-8 -*-

from sgmllib import SGMLParser
import re, urllib, os, urllib2, cookielib, time, pickle, sys
import template
from operator import itemgetter

singletonlock = "/tmp/wfbrood-downloader-lock"
finished = set()
failed = set()
global titles

logfile = open('log.txt', 'a')
htmlconf = {
    u'title': 'title',
    u'playlist': '',
    u'dir': '',
    }

def cleanText(text):
    return text.replace('&nbsp;', ' ')
    
class WfbroodParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.link = []
        self.aOpen = False

    def start_a(self, attrs):
        # The first 12 links are what we need
        if len(self.link) >= 12:
            return
        for (k, v) in attrs:
            if (k == "href"): 
                m = re.search('movie_(\d+)\.html', v)
                if m:
                    title = ''
                    for (k1, v1) in attrs:
                        if k1 == 'title': title = v1
                    if title == '': continue
                    self.link.append((v, m.group(1), cleanText(title.decode('gbk').encode('utf-8'))))
                    self.aOpen = True

    def handle_data(self, text):
        pass
        
    def end_a(self):
        self.aOpen = False

    def result(self):
        return self.link

class FlvParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.link = []
        self.aOpen = False

    def start_a(self, attrs):
        for (k, v) in attrs:
            if (k == "href"):
                m = re.search('http://f\.youku\.com/player/getFlvPath', v)
                if m:
                    self.link.append(v)
                    self.aOpen = True

    def handle_data(self, text):
        pass
        
    def end_a(self):
        self.aOpen = False

    def result(self):
        return self.link

def getFlv(url):
    htmlurl = 'http://www.flvcd.com/parse.php?kw=' + url
    conn = urllib2.urlopen(htmlurl)
    parser = FlvParser()
    html = conn.read()
    parser.feed(html)
    links = parser.result()
    print links
    return links

def downloadFlv(links, number):
    if not os.path.exists(number): os.mkdir(number)
    for (i, link) in enumerate(links):
        if True:
            filename = '%s/%d.flv' % (number, i)
            print 'downloading %s...' % filename
            fp = urllib2.urlopen(link)
            data = fp.read()
            fp.close()

            file=open(filename, 'w+b')
            file.write(data)
            file.close()
            print "file %s downloaded" % filename
            

def genIndex(number, title):
    if not os.path.exists(number):
        os.mkdir(number)

    nfiles = len(os.listdir(number))
    try:
        title = title.encode('utf-8')
    except:
        pass
    htmlconf[u'title'] = title
    htmlconf[u'dir'] = number
    htmlconf[u'playlist'] = u''
    for i in range(30):
        if not os.path.exists(number + '/%d.flv' % i):
            break
        if i == 0:
            htmlconf[u'playlist'] += u"""
            <a href="0.flv" class="first">
                %(title)s #0
            </a>"""
        else:
            htmlconf[u'playlist'] += u"""
            <a href="%d.flv" class="first">
                %c(title)s #%d
            </a>""" % (i, '%', i)


    for x in htmlconf.iterkeys():
        try:
            htmlconf[x] = htmlconf[x].encode('utf-8')
        except:
            pass

    file = open(number + '/index.html', 'w')
    content = template.html.encode('utf-8') % htmlconf % htmlconf
    file.write(content)
    file.close()
    
if __name__ == '__main__':
    if os.path.exists(singletonlock):
        print 'Another instance is already running'
        quit()

    try:
        os.system('touch ' + singletonlock)
        failed = pickle.load(open('failed.log', 'r'))
        finished = pickle.load(open('finished.log', 'r'))
        titles = pickle.load(open('titles.log', 'r'))

        cookie = cookielib.CookieJar()
        proxy = urllib2.ProxyHandler ({'http':'http://10.132.141.124:808'}) 
        opener = urllib2.build_opener(proxy, urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)

        conn = urllib2.urlopen('http://www.wfbrood.com/movie/')
        html = conn.read()
        parser = WfbroodParser()
        parser.feed(html)
        links = parser.result()

        for (link, number, title) in links:
            print link, title
            if not titles.has_key(number):
                titles[number] = title

        leftfile = open('left.html', 'w')
        leftcontent = ''
        for (number, title) in sorted(titles.iteritems(), key=itemgetter(0), reverse=True):
            if number in finished:
                genIndex(number, title)
                leftcontent += '<a href="%s/index.html" target="right">%s</a><br />\n'% (number, title)
            else:
                print '%s not finished' % number

        leftfile.write(template.left % leftcontent)
        leftfile.close()
        pickle.dump(titles, open('titles.log', 'w'))
        if len(sys.argv) <= 1 or sys.argv[1] != 'download':
            quit()
        
        # Download flvs
        for (i, l) in enumerate(links):
            print '%d of %d movies' % (i + 1, len(links))
            if l[1] in finished:
                print '%s has already been downloaded, skip it.' % l[1]
                continue
            try:
                if i > 0: time.sleep(20)
                print l[2], l[0]
                flvs = getFlv(l[0])
                if len(flvs) == 0:
                    failed.add(l[1])
                    continue
                downloadFlv(flvs, l[1])
                finished.add(l[1])
                print '%s finished' % l[1]
                logfile.write('%s\t%s\t%s\n' % (l[0], l[1], l[2]))
            except:
                failed.add(l[1])
                logfile.write('%s failed\n' % l[1])

        logfile.close()
        pickle.dump(failed, open('failed.log', 'w'))
        pickle.dump(finished, open('finished.log', 'w'))
    finally:
        os.system('rm ' + singletonlock)
        

