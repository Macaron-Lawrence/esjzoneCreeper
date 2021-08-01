import urllib.request
import urllib.parse
import urllib.error
import opencc
from lxml import etree

def t2sconvert(txt):
    conv = opencc.OpenCC('jp2t.json')
    txt = conv.convert(txt)
    conv = opencc.OpenCC('t2s.json')
    txt = conv.convert(txt)
    return txt

def getBookInfo(url,heads):
    request = urllib.request.Request(url, headers = heads)
    html = ""
    bookinfo = {
        'title':'',
        'type':'',
        'author':'',
        'taiwantitle':'',
        'othertitle':'',
        'webraw':'',
        "booksraw":'',
        'uploadDate':'',
        'score':'',
        'link':'',
        'cover':'',
        'tags':[],
        'intro':[],
        'titleList':[],
        'linkList':[],
        'seniorTitles':[],
        'images':[],
        'content':[]
    }
    try:
        response = urllib.request.urlopen(request)
        html = etree.parse(response, etree.HTMLParser())

    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)

    def listifempty(arr):
        if arr:
            return ['']
        else:
            return arr


    bookinfo["title"] = t2sconvert(html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[1]/div[2]/h2/text()')[0])
    bookinfo["type"] = t2sconvert(html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[1]/div[2]/ul/li[1]/text()')[0])
    bookinfo["author"] = html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[1]/div[2]/ul/li[2]/a/text()')[0]
    bookinfo["taiwantitle"] = html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[1]/div[2]/ul/li[3]/text()')[0]
    bookinfo["othertitle"] = html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[1]/div[2]/ul/li[4]/text()')[0]
    bookinfo["webraw"] = listifempty(html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[1]/div[2]/ul/li[5]/a/text()'))[0]
    bookinfo["booksraw"] = listifempty(html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[1]/div[2]/ul/li[6]/a/text()'))[0]
    bookinfo["uploadDate"] = html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[1]/div[2]/ul/li[7]/text()')[0]
    bookinfo["score"] = html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[1]/div[1]/div[2]/div[1]/text()')[0]
    bookinfo["link"]= url
    bookinfo["cover"] = html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[1]/div[1]/div[1]/div[1]/a/@href')
    tags = html.xpath('//div[@class="offcanvas-wrapper"]/section/div/div[2]/section/a/text()')
    for _tags in tags:
        bookinfo['tags'].append(t2sconvert(_tags))

    intro = html.xpath('//*[@id="details"]/div/div/div/p/text()')
    for _intro in intro:
            bookinfo['intro'].append(t2sconvert(_intro))

    titles = html.xpath('//*[@id="chapterList"]/a')
    for _title in titles:
        bookinfo['titleList'].append(t2sconvert(_title.xpath('string(.)')))

    seniorTitles = html.xpath('//*[@id="chapterList"]/p[@class="non"]/following-sibling::a[1]/preceding-sibling::p[1]/descendant-or-self::*[text()]/text()')
    seniorTitlesNext = html.xpath('//*[@id="chapterList"]/p[@class="non" and descendant-or-self::text()]/following-sibling::a[1]/@href')
    links = html.xpath('//*[@id="chapterList"]/a/@href')
    for _link in links:
        if _link in seniorTitlesNext:
            sa = [seniorTitles[seniorTitlesNext.index(_link)],links.index(_link)]
            bookinfo['seniorTitles'].append(sa)
        bookinfo['linkList'].append(_link)
#        print(json.dumps(bookinfo, indent=2, ensure_ascii=False))
    print('>> 完成！')
    return bookinfo


        # print(html)