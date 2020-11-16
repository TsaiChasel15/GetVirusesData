# -*- coding: UTF-8 -*-
import requests, re, datetime
from bs4 import BeautifulSoup
import pandas as pd

def initConf():
    global url, endPage, urlList, allarticles, saveFile, headers
    urlList = []
    allarticles = []
    endPage = 18
    url = 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/'
    now = datetime.datetime.now()
    saveFile = './ViruseDataSpidedByPython-' + str(now.year) + str(now.month) + str(now.day) + '.csv'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

def saveAllArticles(data):
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(saveFile, mode='a', index=False, sep=',', header=False, encoding='utf_8_sig')

def main():
    # 1. init all configure
    initConf()

    # 2. save all yqtb url to spider
    for page in range(1, endPage):
        index = 'index' if (page == 1) else 'index_' + str(page)
        new_url = url + index + '.html'
        r = requests.get(new_url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        for title in soup.find_all(attrs={'class': 'title'}):
            for content in title.find_all(href=re.compile("yqtb/content")):
                u = content.attrs['href']
                urlList.append(u)
                print(u)
        print('爬取第 ' + str(page) + ' 页疫情网址完成 ...')

    # 3. get all articles from every page
    for url_ in urlList:
        r0 = requests.get(url_, headers=headers, timeout=10)
        soup = BeautifulSoup(r0.text, "lxml")
        if soup.find_all(attrs={'class': 'detailed_box'}):
            # 3.1 get article title
            if soup.find_all('h4'):
                allarticles.append("《" + soup.find_all('h4')[0].get_text() + "》")
                print('正在爬取：《' + str(soup.find_all('h4')[0].get_text()) + "》")
            # 3.2 get article detail
            one = soup.find_all(attrs={'class': 'zoom_box'})
            for one_ in one[0].find_all(style=re.compile("text-align")):
                m = one_.get_text()
                if m.strip():
                    allarticles.append(m)
            allarticles.append('')
            allarticles.append('')

    # 4. save all articles to csv
    saveAllArticles(allarticles)

if __name__ == '__main__':
    main()
