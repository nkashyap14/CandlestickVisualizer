from collections import defaultdict
import pandas as pd
import yfinance as yf

class DataProcessor:
    def __init__(self):
        self.__options__ = ['Close', 'High', 'Low', 'Open', 'Volume']

    def process_data(self, stocks):
        """This class will read in a list of stocks as data. Apply an intermediate transformation and then send it downstream"""
        data = yf.download(stocks)
        res = self.transform_data(stocks, data)
        return res
        pass

    def transform_data(self, stocks, data):
        tickerData = defaultdict(list)
        for ticker in stocks:
            for date in data.index:
                tempEntry = {"date" : date.date().strftime("%Y-%m-%d")}
                for option in self.__options__:
                    tempEntry[option] = data[(option, ticker)].loc[date]
                    if pd.isna(data[(option, ticker)].loc[date]) and "date" in tempEntry.keys():
                        del tempEntry["date"]
                if len(tempEntry.keys()) == 6:
                    tickerData[ticker].append(tempEntry)
            tickerData[ticker] = pd.DataFrame(tickerData[ticker])
            tickerData[ticker]["date"] = pd.to_datetime(tickerData[ticker]["date"])
            tickerData[ticker].set_index("date", inplace=True)

        return tickerData
