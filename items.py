class fundamentalItem:
    def __init__(self, stockquote, sector, dailyLast, marketCap, numShare, PE, EPS, ROE, dividend, divYield, NTA, parValue, EBIT1, EBIT2, EBIT3):
        self.financials = {
            'stockquote': stockquote,
            'sector': sector,
            'dailyLast': dailyLast,
            'marketCap': marketCap,
            'numShare': numShare,
            'PE': PE,
            'EPS': EPS,
            'ROE': ROE,
            'dividend': dividend,
            'divYield': divYield,
            'NTA': NTA,
            'parValue': parValue,
            'EBIT1': EBIT1,
            'EBIT2': EBIT2,
            'EBIT3': EBIT3
        }

    # getter function to return temp data
    def __getitem__(self, x):
        return self.financials[x]

    # to print data for troubleshooting
    def print_details(self):
        print(self.financials)


# declare a dict variable to store data temporarily
class dailyItem:
    def __init__(self, stockquote, dailyPercentChange, dailyLast, dailyVolume, dailyOpen, dailyHigh,
                 dailyLow):
        self.financials = {
            'stockquote': stockquote,
            'dailyPercentChange': dailyPercentChange,
            'dailyLast': dailyLast,
            'dailyVolume': dailyVolume,
            'dailyOpen': dailyOpen,
            'dailyHigh': dailyHigh,
            'dailyLow': dailyLow
        }

    # getter function to return temp data
    def __getitem__(self, x):
        return self.financials[x]

    # to print data for troubleshooting
    def print_details(self):
        print(self.financials)

