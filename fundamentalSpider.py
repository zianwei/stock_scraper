from lxml import html
from lxml import etree
from string import ascii_uppercase
from items import fundamentalItem
from pipeline import StockPipeline
import requests
import re


def removeHyphen(xpath):
    if  xpath == '' or xpath == '-':
        return None
    return float(xpath)

def getFundamentalInfo():
    str = 'http://www.malaysiastock.biz/Listed-Companies.aspx?type=A&value='
    # runs through all the companies through alphabet index
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
                sector = y[1].xpath('./text()')[0]
                # don't process any stocks in below categories
                if (sector == 'KLSE ETF Stock' or sector == 'KLSE Warrants Stock' or sector
                     == 'KLSE KLCI-CALL Stock' or sector == 'KLSE KLCI-PUT Stock') == 0:
                    # scrape basic financial info
                    site1 = requests.get('http://www.malaysiastock.biz/%s' % href[0]).content
                    html2 = etree.HTML(site1)
                    dailyChanges = html2.xpath('//div[@id="MainContent_qouteBox"]/div')
                    dailyLast = float(dailyChanges[0].xpath('./label[@id="MainContent_lbQuoteLast"]/text()')[0])
                    financialInfo1 = html2.xpath('//div[@id="corporateInfoLeft2"]/div')
                    if len(financialInfo1) != 0:
                        marketCap = financialInfo1[1].xpath('./label/text()')[0][2:]
                        numShare = financialInfo1[3].xpath('./label/text()')[0][2:]
                        EPS = removeHyphen(financialInfo1[5].xpath('./label/text()')[0][2:-1])
                        PE = removeHyphen(financialInfo1[7].xpath('./label/text()')[0][2:])
                        ROE = removeHyphen(financialInfo1[9].xpath('./label/text()')[0][2:])
                        # print(EPS,PE,ROE)
                        # print('-------------')
                    financialInfo2 = html2.xpath('//div[@id="corporateInfoRight2"]/div')
                    if len(financialInfo2) != 0:
                        dividend = removeHyphen(financialInfo2[1].xpath('./label/text()')[0][2:-2])
                        divYield = removeHyphen(financialInfo2[3].xpath('./label/text()')[0][2:])
                        NTA = removeHyphen(financialInfo2[5].xpath('./label/text()')[0][2:])
                        parValue = removeHyphen(financialInfo2[7].xpath('./label/text()')[0][2:])
                    financialInfo3 = html2.xpath('//table[@id="MainContent_gvReport"]/tr')
                    count2 = 0
                    revenue = 0
                    EBIT = 0
                    netprofit = 0
                    date = 'text'
                    fundamentals = []
                    for i in financialInfo3:
                        if count2 != 0 and count2 != 13:
                            quarterReport = i.xpath('./td')
                            if date == 'text':
                                date = quarterReport[1].xpath('./text()')[0]
                                date = date[-4:]
                            currentDate = quarterReport[1].xpath('./text()')[0]
                            currentDate = currentDate[-4:]
                            if currentDate != date:
                                financial_dict = {'year': date, 'EBIT': EBIT}
                                fundamentals.append(financial_dict)
                                revenue = 0
                                EBIT = 0
                                netprofit = 0
                                date = currentDate
                            tmp1 = quarterReport[4].xpath('./text()')[0]
                            tmp1 = tmp1.replace(',', '')
                            tmp2 = quarterReport[5].xpath('./text()')[0]
                            tmp2 = tmp2.replace(',', '')
                            tmp3 = quarterReport[6].xpath('./text()')[0]
                            tmp3 = tmp3.replace(',', '')
                            revenue += int(tmp1)
                            EBIT += int(tmp2)
                            netprofit += int(tmp3)
                        count2 += 1
                    if len(fundamentals) == 1:
                        myStock = fundamentalItem(stockquote, sector, dailyLast, marketCap, numShare,
                                        PE, EPS, ROE, dividend, divYield, NTA, parValue,
                                        fundamentals[0]['EBIT'], None, None)
                    if len(fundamentals) == 2:
                        myStock = fundamentalItem(stockquote, sector, dailyLast, marketCap, numShare,
                                        PE, EPS, ROE, dividend, divYield, NTA, parValue,
                                        fundamentals[0]['EBIT'], fundamentals[1]['EBIT'], None)
                    if len(fundamentals) == 3:
                        myStock = fundamentalItem(stockquote, sector, dailyLast, marketCap, numShare,
                                        PE, EPS, ROE, dividend, divYield, NTA, parValue,
                                        fundamentals[0]['EBIT'], fundamentals[1]['EBIT'], fundamentals[2]['EBIT'])
                    # pipeline = StockPipeline()
                    # pipeline.process_fundamental_item(myStock)
                    myStock.print_details()

            count += 1

getFundamentalInfo()