#<%- 程序作者：喵卡龙>

import urllib.parse
import urllib.error
import sys
from modules.getBookInfo import getBookInfo
from modules.heads import heads
from modules.getContent import getContent
from modules.EPUBbuilder import EPUBgenerator

def argcheck(arr):
    if len(arr) ==3:
        return arr[1],arr[2]
    elif len(arr) == 2:
        return arr[1],None
    elif len(arr) == 1:
        print('>> 未传递URL，请重试!')
        return False
    else:
        print('>> 传递参数过多，请重试!')
        return False

def main(_src):
    if argcheck(_src):
        (src, cover) = argcheck(_src)
        print('>> 正在收集必要信息')
        BOOK = getContent(getBookInfo(src, heads(),cover),heads())
        EPUBgenerator(BOOK)
    # print(getBookInfo(src, heads()))
    print('>> 运行结束！')

if __name__ == "__main__":
    # main('https://www.esjzone.cc/detail/1580565850.html')
    main(sys.argv)