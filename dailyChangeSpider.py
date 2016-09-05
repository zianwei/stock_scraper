from lxml import html
from lxml import etree
from string import ascii_uppercase
from items import dailyItem
from pipeline import StockPipeline
import requests

def getDailyChanges():
    # main website
    str = 'http://www.malaysiastock.biz/Listed-Companies.aspx?type=A&value='
    # loop through all company pages from A - Z
    for alphabet in ascii_uppercase:
        strTemp = str
        strTemp = strTemp + alphabet[-1]
        site = requests.get(strTemp).content
        html1 = etree.HTML(site)
        row = html1.xpath('//table[@id="MainContent_tStock"]/tr')
        count = 0
        for x in row:
            y = x.xpath('./td/h3')
            if count % 3 == 0:
                href = y[0].xpath('./a/@href')
                stockquote = y[0].xpath('./a/text()')[0]
                site1 = requests.get('http://www.malaysiastock.biz/%s' % href[0]).content
                html2 = etree.HTML(site1)
                dailyChanges = html2.xpath('//div[@id="MainContent_qouteBox"]/div')
                dailyPercentChange = dailyChanges[0].xpath('./label[@id="MainContent_lbQuoteChangePerc"]/text()')
                if dailyPercentChange != []:
                    dailyPercentChange = dailyPercentChange[0]
                else:
                    dailyPercentChange = 0
                dailyLast = float(dailyChanges[0].xpath('./label[@id="MainContent_lbQuoteLast"]/text()')[0])
                dailyVolume = dailyChanges[2].xpath('./label/text()')[0][2:]
                dailyVolume = int(dailyVolume.replace(',', ''))
                dailyOpen = float(dailyChanges[8].xpath('./label/text()')[0][2:])
                dailyHigh = float(dailyChanges[10].xpath('./label/text()')[0][2:])
                dailyLow = float(dailyChanges[12].xpath('./label/text()')[0][2:])

                myStock = dailyItem(stockquote, dailyPercentChange, dailyLast, dailyVolume, dailyOpen, dailyHigh, dailyLow)
                pipeline = StockPipeline()
                pipeline.process_daily_item(myStock)
                # myStock.print_details()
                # print(myStock['dailyLast'])
            count += 1


getDailyChanges()