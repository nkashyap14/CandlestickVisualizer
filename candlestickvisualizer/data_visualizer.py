import os
import configparser
import mplfinance as mpf
from datetime import date

class DataVisualizer:  

    def __init__(self, configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        self.output_path = config.get("OUTPUT", "OUTPUT_PATH") + "\\" + str(date.today())
        print(self.output_path)

    def createIfDoesntExist(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("Directory is created")
            return
        print("Directory already exists")

    def visualize_data(self, data, weekOffset=104):
        """"Takes in stock data from Data Processor. Stock data is in form of dict where keys are stock tickers mapped 
        to daily granularity candlestick level data. This function then outputs a collection of candlestick charts. The window looked at
        depends on value of weekoffset. Weekoffset = 10 will plot candlestick charts for the last 10 weeks of data. Defaults to looking
        at last 2 years of data"""

        self.createIfDoesntExist(self.output_path)
        res = {}
        for ticker in data:
            output_path = self.output_path + "\\" + ticker + '.pdf'
            res[ticker] = mpf.plot(data[ticker].iloc[-weekOffset:], type="candle",
            title="{} Candlestick Chart for {} Weeks".format(ticker, str(weekOffset)), volume=True, savefig=output_path)
        return res
        pass
