import urllib.parse
import urllib.error
import sys
from modules.getBookInfo import getBookInfo
from modules.heads import heads
from modules.getContent import getContent
from modules.EPUBbuilder import EPUBgenerator



def main(src):
    print('>> 正在收集必要信息')
    BOOK = getContent(getBookInfo(src, heads()),heads())
    EPUBgenerator(BOOK)
    # print(getBookInfo(src, heads()))
    print('>> 程序运行完成！')

if __name__ == "__main__":
    # main('https://www.esjzone.cc/detail/1580565850.html')
    main(sys.argv[1])