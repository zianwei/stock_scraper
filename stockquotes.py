from lxml import html 
from lxml import etree
import requests
import csv

def writeFile():
	ofile = open('eggs.csv', 'w', newline='')
    writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
	for row in reader:
   		writer.writerow(row)


site = requests.get('http://www.malaysiastock.biz/Listed-Companies.aspx?type=A&value=A').content
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
			dividendYield = financialInfo2[1].xpath('./label/text()')
			NTA = financialInfo2[1].xpath('./label/text()')
			parValue = financialInfo2[1].xpath('./label/text()')
	count += 1