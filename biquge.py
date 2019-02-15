import time
import random
import sys
import urllib
import requests
from bs4 import BeautifulSoup

# 搜索小说
def search_book(search_book_name):
    
    try:
        if search_book_name:

            new_search_book_name = urllib.parse.quote(search_book_name)

            search_url = 'https://www.biquge5200.cc/modules/article/search.php?searchkey=' + new_search_book_name

            novel_source = requests.get(search_url).text

            search_soup = BeautifulSoup(novel_source, "lxml")

            search_book_url = search_soup.find("div", id="hotcontent").find_all("td", class_="odd")

            if len(search_book_url) > 0:
                for item in search_book_url:
                    if item.text == search_book_name:
                        book_url = item.find("a").get('href')
                        return book_url

            else:
                print("未找到您要搜索的小说!")

        else:
            print("请输入小说名称")
    except Exception as e:
        print(e)
    

# 获取小说名称和下面各个章节的url地址
def get_all_chapter_href(search_url):
        
    try:
        if search_url:

            new_search_url = requests.get(search_url)

            # 通过F12查看笔趣阁小说页面html结构发现meta标签上gbk格式解析的，所以在这里转一下
            new_search_url.encoding = "gbk"

            chapter_soup = BeautifulSoup(new_search_url.text, "lxml")

            chapter_list = chapter_soup.find("div", id="list").find_all("a")

            booktitle = chapter_soup.find("div", id="maininfo").find("div", id="info").find("h1")
            print("正在下载的小说名称是: " + booktitle.text)            

            href_list = []

            for a in chapter_list:

                href_list.append(a.get('href'))
            
            return href_list, booktitle
        else:
            return None, None

    except Exception as e:
        print(e)

# 获取每个章节下的内容并下载到txt
def get_chapter_content(href_list,booktitle):
    try:
        if href_list != None and booktitle != None:
            for url in href_list:

                # 如果连接太过频繁会报错,所以这里用sleep休眠方式
                time.sleep(1 + random.random())

                chapter_url = requests.get(url)

                chapter_url.encoding = "gbk"

                text = chapter_url.text

                content_soup = BeautifulSoup(text, "lxml")

                bookname = content_soup.find("div", class_="bookname").find("h1")

                content = content_soup.find_all("div", id="content")[0].find_all("p")

                with open("E:" + "/\/" + booktitle.text + ".txt",'a', encoding='utf-8') as f:

                    f.write(bookname.text + "\n\r\r")
                    print("正在下载的章节名称是: " + bookname.text)

                    for book in content:

                        f.write(book.text + "\n\r")
        
        else:
            return 

    except Exception as e:
        print(e)

if __name__ == "__main__":

    search_book_name = input("请输入想要下载的小说名称: ")

    search_url = search_book(search_book_name)

    href, booktitle = get_all_chapter_href(search_url)

    get_chapter_content(href,booktitle)