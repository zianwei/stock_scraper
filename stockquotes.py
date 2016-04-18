from lxml import html 
from lxml import etree
from string import ascii_uppercase
import requests
import csv

class stock:
	def __init__(self,stockquote,sector,dailyPercentChange,dailyLast,dailyVolume,
		dailyChange,dailyOpen,dailyHigh,dailyLow,marketCap,numShare,EPS,peRatio,ROE,dividend,NTA,parValue):
		self.financials = {
			'stockquote': stockquote,
			'sector': sector,
			'dailyPercentChange': dailyPercentChange,
			'dailyLast': dailyLast,
			'dailyVolume': dailyVolume,
			'dailyChange': dailyChange,
			'dailyOpen': dailyOpen,
			'dailyHigh': dailyHigh,
			'dailyLow': dailyLow,
			'marketCap': marketCap,
			'numShare': numShare,
			'EPS': EPS,
			'peRatio': peRatio,
			'ROE': ROE,
			'dividend': dividend,
			'NTA': NTA,
			'parValue': parValue
		}

def getStockInfo():
	str = 'http://www.malaysiastock.biz/Listed-Companies.aspx?type=A&value='
	ofile = open('stock.csv','w')
	fieldnames = ['stockquote','sector','dailyPercentChange','dailyLast','dailyVolume','dailyChange',
		'dailyOpen','dailyHigh','dailyLow','marketCap','numShare','EPS','peRatio','ROE','dividend','NTA','parValue']
	writer = csv.DictWriter(ofile, fieldnames=fieldnames)
	writer.writeheader()
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
				stockquote = y[0].xpath('./a/text()')
				sector = y[1].xpath('./text()')
				site1 = requests.get('http://www.malaysiastock.biz/%s' %href[0]).content
				html2 = etree.HTML(site1)
				dailyChanges = html2.xpath('//div[@id="MainContent_qouteBox"]/div')
				dailyPercentChange = dailyChanges[0].xpath('./label[@id="MainContent_lbQuoteChangePerc"]/text()')
				if dailyPercentChange != []:
					dailyPercentChange = dailyPercentChange[0]
				dailyLast = dailyChanges[0].xpath('./label[@id="MainContent_lbQuoteLast"]/text()')
				dailyVolume = dailyChanges[2].xpath('./label/text()')
				dailyChange = dailyChanges[4].xpath('./label/text()')
				dailyOpen = dailyChanges[8].xpath('./label/text()')
				dailyHigh = dailyChanges[10].xpath('./label/text()')
				dailyLow = dailyChanges[12].xpath('./label/text()')
				financialInfo1 = html2.xpath('//div[@id="corporateInfoLeft2"]/div')
				if len(financialInfo1) != 0:
					marketCap = financialInfo1[1].xpath('./label/text()')
					numShare = financialInfo1[3].xpath('./label/text()')
					EPS = financialInfo1[5].xpath('./label/text()')
					peRatio = financialInfo1[7].xpath('./label/text()')
					ROE = financialInfo1[9].xpath('./label/text()')
				financialInfo2 = html2.xpath('//div[@id="corporateInfoRight2"]/div')
				if len(financialInfo2) != 0:
					dividend = financialInfo2[1].xpath('./label/text()')
					NTA = financialInfo2[1].xpath('./label/text()')
					parValue = financialInfo2[1].xpath('./label/text()')
				myStock = stock(stockquote[0],sector[0],dailyPercentChange,dailyLast[0],dailyVolume[0][2:],
					dailyChange[0][2:],dailyOpen[0][2:],dailyHigh[0][2:],dailyLow[0][2:],marketCap[0][2:],numShare[0][2:],
					EPS[0][2:-1],peRatio[0][2:],ROE[0][2:],dividend[0][2:-2],NTA[0][2:-2],parValue[0][2:-2])
				writer.writerow(myStock.financials)
			count += 1
	ofile.close()	

getStockInfo()
