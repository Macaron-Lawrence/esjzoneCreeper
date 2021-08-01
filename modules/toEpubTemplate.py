import json
import modules.templateParser as Praser
# B = {};

# with open('./output/test.json','r',encoding='utf-8') as f1:
#     B = json.load(f1)


_template = {
    'mimetype':{
        'src':'/mimetype',
        'content':''
    },
    'container.xml':{
        'src':'/META-INF/container.xml',
        'content':''
        },
    'content.opf':{
        'src':'/OEBPS/content.opf',
        'content':''
    },
    'copyright.xhtml':{
        'src':'/OEBPS/copyright.xhtml',
        'content':''
    },
    'cover.xhtml':{
        'src':'/OEBPS/cover.xhtml',
        'content':''
    },
    'intro.xhtml':{
        'src':'/OEBPS/intro.xhtml',
        'content':''
    },
    'page-template.xpgt':{
        'src':'/OEBPS/page-template.xpgt',
        'content':''
    },
    'stylesheet.css':{
        'src':'/OEBPS/stylesheet.css',
        'content':''
    },
    'title_page.xhtml':{
        'src':'/OEBPS/title_page.xhtml',
        'content':''
    },
    'toc.ncx':{
        'src':'/OEBPS/toc.ncx',
        'content':''
    },
    'toc.xhtml':{
        'src':'/OEBPS/toc.xhtml',
        'content':''
    },

}



def toObj(src):
    with open(src, 'r') as f:
        BOOK = json.load(f)
    return BOOK

def tagGenerator(arr):
    o = ''
    for i in arr:
        o = o + i
    return o

def tocXHTML(arr, S_arr):
    count = len(arr)
    text = ''
    S_position = []
    for _S_p in S_arr:
        S_position.append(_S_p[1])
    S = []
    for _S in S_arr:
        S.append(_S[0])
    S_count = 0

    for i in range(0,count):
        if i in S_position:
            text += '<h4>' + S[S_count] + '</h4>\n'
            S_count += 1

        _i = str(i)
        text += '<p><a href="chap'+_i+'.xhtml">'+ arr[i] +'</a></p>\n'
    return text
#['第一部', 1], ['第二部', 51]

def arr2P(arr):
    text = ''
    for p in arr:
        _p = p.replace('%img%','</p><br/>\n<img alt="image" src="images/img_').replace('_%i_end%','.jpg" />\n<br/><p>')
        text += '<p>' + _p + '</p>\n'
    return text


def manifestChap(arr):
    count = len(arr)
    text = ''
    for i in range(0,count):
        _i = str(i)
        text += '<item id="chapter' + _i + '" href="chap' + _i +'.xhtml" media-type="application/xhtml+xml"/>'
    return text

def manifestImg(arr):
    count = len(arr)
    text = ''
    for i in range(0,count):
        text += '<item id="img_'+ str(i) +'" href="images/img_'+str(i)+'.jpg" media-type="image/jpeg"/>'
    return text
def spineChap(arr):
    count = len(arr)
    text = ''
    for i in range(0,count):
        _i = str(i)
        text += '<itemref idref="chapter' + _i +'"/>'
    return text


def tocNCX(arr, S_arr):
    count = len(arr)
    text = ''
    S_position = []
    for _S_p in S_arr:
        S_position.append(_S_p[1])
    S = []
    for _S in S_arr:
        S.append(_S[0])
    S_count = 0
    _playorder = 1

    for i in range(0,count):
        _i = str(i)
        if i in S_position:
            text += '''
<navPoint id="seniortitle0'''+ str(S_count + 1) +'''" playOrder="'''+ str(_playorder) +'''">
<navLabel>
<text>'''+S[S_count]+'''</text>
</navLabel>
<content src="chap'''+ _i +'''.xhtml"/>'''
            S_count += 1
            _playorder +=1

        text += '''
<navPoint id="chapter'''+ _i +'''" playOrder="'''+ str(_playorder) +'''">
<navLabel>
<text>''' + arr[i] + '''</text>
</navLabel>
<content src="chap'''+ _i +'''.xhtml"/>
</navPoint>
'''
        _playorder +=1

        if i+1 in S_position[1:] or i == count-1:
            text += '</navPoint>'

    return text


def template(B):
    BOOK = _template
    _len = len(B['titleList'])
    BOOK['container.xml']['content'] = Praser.apply('container.xml',{})
    BOOK['mimetype']['content'] = Praser.apply('mimetype',{})
    BOOK['mimetype']['coverlink'] = B['cover']
    BOOK['mimetype']['title'] = B['title']
    BOOK['mimetype']['images'] = B['images']
    BOOK['copyright.xhtml']['content'] = Praser.apply('copyright.xhtml',{
        'bookname':B['title'],
        'booklink':B['link'],
        'bookauthor':B['author'],
        'taiwantitle':B['taiwantitle'],
        'othertitle':B['othertitle'],
        'webraw':B['webraw'],
        'booksraw':B['booksraw'],
        'uploadDate':B['uploadDate'],
        'score':B['score'],
        'tags':tagGenerator(B['tags']),
        'bookmaker':'喵卡龙',
        'type':B['type'],
    })
    BOOK['content.opf']['content'] = Praser.apply('content.opf',{
        'title':B['title'],
        'creater':B['author'],
        'publisher':'喵卡龙',
        'ID':B['link'],
        'manifest:chap':manifestChap(B['titleList']),
        'spine:chap':spineChap(B['titleList']),
        'manifest:img':manifestImg(B['images'])
    })
    BOOK['cover.xhtml']['content'] = Praser.apply('cover.xhtml',{
        'title':B['title'],
    })

    BOOK['intro.xhtml']['content'] = Praser.apply('intro.xhtml',{
        'intro' : arr2P(B['intro'])
    })
    BOOK['page-template.xpgt']['content'] = Praser.apply('page-template.xpgt',{})
    BOOK['stylesheet.css']['content'] = Praser.apply('stylesheet.css',{})
    BOOK['title_page.xhtml']['content'] = Praser.apply('title_page.xhtml',{
        'title':B['title'],
        'othertitle':B['othertitle'],
        'author':B['author']
    })
    BOOK['toc.xhtml']['content'] = Praser.apply('toc.xhtml',{
        'toc' : tocXHTML(B['titleList'],B['seniorTitles'])
    })
    BOOK['toc.ncx']['content'] = Praser.apply('toc.ncx',{
        'toc' : tocNCX(B['titleList'],B['seniorTitles'])
    })
    for i in range(0,_len):
        _i = str(i)
        BOOK['chap' + _i + '.xhtml'] = {
            'src':'',
            'content':''
        }
        BOOK['chap' + _i + '.xhtml']['src'] = '/OEBPS/'+ 'chap' + _i + '.xhtml'
        BOOK['chap' + _i + '.xhtml']['content'] = Praser.apply('chap.xhtml',{
            'title' : B['titleList'][i],
            'content': arr2P(B['content'][i]['contents']),
            'title_sub': B['content'][i]['title'],
            'uploader': B['content'][i]['uploader'],
            'date': B['content'][i]['date']
        })
    return BOOK

