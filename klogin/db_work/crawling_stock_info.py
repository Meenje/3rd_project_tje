from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re

def crawling_info(code, num):
    page = urlopen("https://fchart.stock.naver.com/sise.nhn?symbol={}&timeframe=day&count={}&requestType=0".format(code, str(num)))
    document = page.read()
    page.close()

    soup = BeautifulSoup(document, 'html.parser')

    tag_datas = soup.findAll('item')

    codes=[]
    dates = []
    market_values = []
    high_prices = []
    low_prices = []
    closing_prices = []
    volumes = []

    for data in tag_datas:
        str_data = str(data)
        raw_data = re.findall('"([^"]*)"', str_data)
        row = re.findall('[^|]+', raw_data[0])
        codes.append(code)
        dates.append(row[0])
        market_values.append(int(row[1]))
        high_prices.append(int(row[2]))
        low_prices.append(int(row[3]))
        closing_prices.append(int(row[4]))
        volumes.append(int(row[5]))

    test_data = {
        'code': codes,
        'date': dates,
        'open': market_values,
        'high': high_prices,
        'low': low_prices,
        'close': closing_prices,
        'volume': volumes
    }
    df = pd.DataFrame(test_data)
    return df

def crawling_KOSPI200():
    names = []
    codes = []
    for i in range(1,21):
        page = urlopen("https://finance.naver.com/sise/entryJongmok.nhn?&page={}".format(str(i)))

        document = page.read()
        page.close()

        soup = BeautifulSoup(document, 'html.parser')
        tag_datas = soup.select('td.ctg')

        for t in tag_datas:
            s = str(t)
            code = re.findall('[^code=]*["$]',s)[3].replace('"',"")
            codes.append(code)
            names.append(t.text)
    return codes, names

def crawling_today(code):
    page = urlopen("https://fchart.stock.naver.com/sise.nhn?symbol={}&timeframe=day&count=1&requestType=0".format(code))
    document = page.read()
    page.close()

    soup = BeautifulSoup(document, 'html.parser')

    tag_datas = soup.findAll('item')

    data = tag_datas[0]
    str_data = str(data)
    raw_data = re.findall('"([^"]*)"', str_data)
    row = re.findall('[^|]+', raw_data[0])

    return row