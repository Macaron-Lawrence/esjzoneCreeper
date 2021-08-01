from modules.templateParser import apply
import urllib.request
import urllib.parse
import urllib.error
import opencc
from lxml import etree
import math


def t2sconvert(txt):
    conv = opencc.OpenCC('jp2t.json')
    txt = conv.convert(txt)
    conv = opencc.OpenCC('t2s.json')
    txt = conv.convert(txt)
    return txt

def selectStrAndImg(element,_imgcount,bookinfo):
    _o = ''
    _img = element.xpath('preceding-sibling::p[1]/.//img/@src')
    __img = element.xpath('self::*[not(following-sibling::p)]/.//img/@src')
    if _img != [] :
        _o += '%img%' + str(_imgcount) +'_%i_end%'
        _imgcount += 1
        bookinfo.append(_img[0])
    _o += t2sconvert(element.xpath('string(.)'))
    if __img !=[] :
        _o += '%img%' + str(_imgcount) +'_%i_end%'
        _imgcount += 1
        bookinfo.append(__img[0])
    return (_o,_imgcount,bookinfo)


def print33(indexnow,indextotal,title):
    A_count = math.floor(indexnow/indextotal*33)
    A = '#'*A_count
    B = '-'*(33-A_count)
    C = math.floor(indexnow/indextotal*1000)/10

    print('>> 正在抓取 |' + A + B + '| '+ str(C) + '% | ' + title,flush=True)
def getContent(bookinfo, heads): #url[array_of_links]
    _imgcount = 0
    print('>> 爬虫程序启动')
    print('>>')
    url = bookinfo['linkList']
    _content=[]
    _counter = 0
    _len = len(url)
    for _url in url:
        request = urllib.request.Request(_url, headers = heads)
        html = ""
        try:
            response = urllib.request.urlopen(request)
            html = etree.parse(response, etree.HTMLParser())
        except urllib.error.URLError as e:
            if hasattr(e,'code'):
                print(e.code)
            if hasattr(e,'reason'):
                print(e.reason)
        contentinfo = {
            'title':'',
            'uploader':'',
            'date': '',
            'contents': []
        }

        contentinfo['title'] = t2sconvert(html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/h2/text()')[0])
        contentinfo['uploader'] = html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[@class ="single-post-meta m-t-20"][1]/div[1]/a/text()')[0]
        contentinfo['date'] = html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[@class ="single-post-meta m-t-20"][1]/div[2]/text()')[1]

        contents = html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[@class="forum-content mt-3"]/p')
        print33(_counter,_len,contentinfo['title'])
        for _contents in contents:
            # _contents = _contents.xpath('string(.)')
            (__contents, _imgcount, bookinfo['images']) = selectStrAndImg(_contents,_imgcount,bookinfo['images'])
            contentinfo['contents'].append(__contents)
        _content.append(contentinfo)
        _counter += 1
    bookinfo['content'] = _content
    print('>> 完成！')
    return bookinfo