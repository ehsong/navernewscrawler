import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import time, random


def get_news(n_url):
    """
    Uses request to access url, parse using BeautifulSoup, appends title, date, company
    and text of a given news in the link in a list

    Parameters
    ----------
    n_url: a http:// url

    Yields
    ------
    list
    """
    news_detail = []
    breq = requests.get(n_url)
    bsoup = BeautifulSoup(breq.content, 'html.parser')
    title = bsoup.select('h3#articleTitle')[0].text
    news_detail.append(title)
    pdate = bsoup.select('.t11')[0].get_text()[:11]
    news_detail.append(pdate)
    _text = bsoup.select('#articleBodyContents')[0].get_text().replace('\n', " ")
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "")
    news_detail.append(btext.strip())
    pcompany = bsoup.select('#footer address')[0].a.get_text()
    news_detail.append(pcompany)
    return news_detail

def get_dates(start_date,end_date):
    """
    Creates a list of dates in string format 'Y-M-D'

    Yields
    ------
    list

    Note
    ------
    To change collection time frame, mend start_date and end_date
    """
    import datetime
    # the command argument is a string
    # convert the string dates to datetime object
    def ConvertDates(string_date):
        '''
        Convert string dates ("Y-M-D") to datetime object
        Parameters
        ----------
        string_date: a string
        Returns
        -------
        datetime object
        '''
        import datetime
        string_date = string_date.replace("-","")
        string_date = string_date.strip()
        date = datetime.datetime.strptime(string_date,"%Y%m%d").date()
        return date
    # create the date range
    date_range_list = []
    date_range = [ ConvertDates(start_date) + datetime.timedelta(n) for n in range(int ((ConvertDates(end_date) + datetime.timedelta(days=1) - ConvertDates(start_date)).days))]
    for date in date_range:
        date_range_list.append(str(date).replace("-","."))
    return(date_range_list)


def output(query,page,max_page,start_date,end_date):
    """
    Query a word and return the title, date, company, text of news in dictionary format
    and append all dictionaries in a list

    Parameters
    ----------
    query: a string
    page: start page
    max_page: maximum pages to be crawled per date

    Returns:
    List of dictionaries in a list, with keys title, date, company, text
    """
    news_dicts = []
    # best to concatenate urls here
    date_range = get_dates(start_date,end_date)
    for date in date_range:
        start_page = page
        s_date = date.replace(".","")
        while start_page < max_page:
            url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=0&ds=" + date + "&de=" + date + "&nso=so%3Ar%2Cp%3Afrom" + s_date + "to" + s_date + "%2Ca%3A&start=" + str(start_page)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            req = requests.get(url,headers=header)
            cont = req.content
            soup = BeautifulSoup(cont, 'html.parser')
            for urls in soup.select("._sp_each_url"):
                try:
                    if urls["href"].startswith("https://news.naver.com"):
                        news_detail = get_news(urls["href"])
                        adict = dict()
                        adict["title"] = news_detail[0]
                        adict["date"] = news_detail[1]
                        adict["company"] = news_detail[3]
                        adict["text"] = news_detail[2]
                        news_dicts.append(adict)
                except Exception as e:
                    continue
            start_page += 10
    return news_dicts
