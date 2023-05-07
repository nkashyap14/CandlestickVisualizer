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
        '''Transforming the data into proper structure as for downstream visualization purposes'''
        tickerData = defaultdict(list)
        for ticker in stocks:
            for date in data.index:
                tempEntry = {"date" : date.date().strftime("%Y-%m-%d")}
                for option in self.__options__:
                    tempEntry[option] = data[(option, ticker)].loc[date]
                    #if any of the options are missing a value remove the date key so as to ensure we don't collect this entry
                    if pd.isna(data[(option, ticker)].loc[date]) and "date" in tempEntry.keys():
                        del tempEntry["date"]
                #If there is a missing value for this point in time than we drop the date
                if len(tempEntry.keys()) == 6:
                    tickerData[ticker].append(tempEntry)
            tickerData[ticker] = pd.DataFrame(tickerData[ticker])
            tickerData[ticker]["date"] = pd.to_datetime(tickerData[ticker]["date"])
            tickerData[ticker].set_index("date", inplace=True)

        return tickerData
