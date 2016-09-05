import psycopg2
import datetime

class StockPipeline():
    def __init__(self):
        try:
            # When a pipeline is started, it will first try to connect to the database.
            # Enter your database credentials here
            self.conn = psycopg2.connect(
                "dbname='stocks' user='postgres' host='localhost' dbname='stocks' password='Zian6561'")
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        except:
            print("Error: Unable to connect to the database")
        # If it can't connect to db we should stop the spider and quit

        # Once we are connected to DB, we prepare today's date to be stored in the DB,
        # and store the value in a variable
        self.today_str = datetime.date.today().strftime('%Y-%m-%d')

    def process_daily_item(self, item):
        # this method will be called for every scraped item.
        # Here are we inserting each item into the database
        self.cur.execute(
            "INSERT INTO stock_daily_changes (statdate, stockquote, dailyPercentChange, dailyLast, dailyVolume, dailyOpen, dailyHigh, dailyLow) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (self.today_str, item['stockquote'], item['dailyPercentChange'], item['dailyLast'], item['dailyVolume'], item['dailyOpen'], item['dailyHigh'], item['dailyLow']))

    def process_fundamental_item(self, item):
        self.cur.execute(
            "INSERT INTO stock_fundamental (stockquote, sector, dailyLast, marketCap, numShare, PE, EPS, ROE, dividend, divYield, NTA, parValue, EBIT1, EBIT2, EBIT3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (item['stockquote'], item['sector'], item['dailyLast'], item['marketCap'], item['numShare'],item['PE'],
             item['EPS'], item['ROE'], item['dividend'], item['divYield'], item['NTA'], item['parValue'], item['EBIT1'], item['EBIT2'], item['EBIT3']))

    def update_pvt_item(self, stockquote):
        self.cur.execute(
            "UPDATE pvt_analysis_test "
        )