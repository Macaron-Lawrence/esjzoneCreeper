import os

from requests import exceptions
import modules.toEpubTemplate as toEpubTemplate
import shutil
import requests
from io import BytesIO
from PIL import Image
from modules.heads import heads
from modules.templateParser import apply
import math
localaddress = os.getcwd() + "\\output"
File_Path1 = localaddress + '\\catch\\EPUB\\META-INF'
File_Path2 = localaddress + "\\catch\\EPUB\\OEBPS\\images"

def creatFile(src,str):
    try:
        with open('./output/catch/EPUB' + src,'w',encoding='utf-8') as F:
            F.write(str)
    except Exception as e:
        print(e)


def creatImg(src,url):
    # i = 0
    # while i <3:
        try:
            response = requests.get(url, headers = heads(), stream=True, timeout=(5,20))
            if  response.status_code == 200:
                _img = Image.open(BytesIO(response.content)).convert('RGB')
            else:
                _img = Image.open('./modules/templateFiles/error_404.jpg',mode='r')
                print('      404：获取图片失败')
            _img.save('./output/catch/EPUB' + src,'jpeg')
            (x,y) = _img.size
            return x,y
        except Exception as e:
            # i += 1
            # print('      下载超时！正在尝试重新下载 | 当前重试次数为第 ' + str(i) + ' 次')
            print(e)



def dirGenerator():
    os.makedirs(File_Path1,exist_ok = True)
    os.makedirs(File_Path2,exist_ok = True)

def fileGenerator(bookinfo):
    dirGenerator()
    for element in bookinfo.values():
        creatFile(element['src'],element['content'])
    print('    正在下载封面')
    (coverwidth, coverheight) = creatImg('/OEBPS/images/cover.jpg',bookinfo['mimetype']['coverlink'])
    _images = bookinfo['mimetype']['images']
    for i in range(0,len(_images)):
        print('    正在下载插图: url = ' +  _images[i])
        creatImg('/OEBPS/images/img_'+ str(i) +'.jpg', _images[i])
    coverratio = min(min(1200/coverwidth,1200/coverheight),1)
    (_coverwidth,_coverheight) = (math.floor(coverwidth*coverratio),math.floor(coverheight*coverratio))
    coverguilde = apply('coverguide.xhtml', {
        'width': str(_coverwidth),
        'height' : str(_coverheight)
    })
    creatFile('/OEBPS/coverguide.xhtml',coverguilde)
    shutil.make_archive(localaddress + '\\output_catch','zip', localaddress + '\\catch\\EPUB')
    shutil.move(localaddress + '\\output_catch.zip',localaddress + '\\' + bookinfo['mimetype']['title'] + '.epub')
    shutil.rmtree(localaddress + '\\catch\\EPUB')
    print('>> 完成！')

def EPUBgenerator(_B):
    print('>> 正在生成EPUB文件')
    fileGenerator(toEpubTemplate.template(_B))

