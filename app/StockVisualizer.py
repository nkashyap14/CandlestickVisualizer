from abc import ABC, abstractmethod 
import yfinance as yf
from collections import defaultdict
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import configparser
import sys
import pandas as pd
import mplfinance as mpf
from datetime import date
import os
import shutil
import zipfile

class Adapter(ABC):
    @abstractmethod
    def convert(self):
        """This method will convert a collection of candlestick visualizations into the desired output format
        and deliver it"""
        pass 

class Deliverer(ABC):
    @abstractmethod
    def deliver(self):
        """This method will take the results of an adapter"""
        pass 

class Reader(ABC):

    @abstractmethod
    def read(self):
        """This method will read from some path and return a list of stock tickers"""
        pass
    

class AzureBlobStorageReader(Reader):

    def __init__(self, configPath):
        #load data from config file here
        config = configparser.ConfigParser()
        config.read(configPath)

        connection= config.get("AZURE", "STORAGE_ACCOUNT_CONNECTION_STRING")
        self.__container__ = config.get("AZURE", "CONTAINER_NAME")
        self.__blob__ = config.get("AZURE", "BLOB_NAME")

        #settingi up service client
        self.__service_client__ = BlobServiceClient.from_connection_string(connection)
        pass

    def read(self):
        #use configured client in init to read data 
        container_client = self.__service_client__.get_container_client(self.__container__)
        blob_client = container_client.get_blob_client(self.__blob__)
        res = blob_client.download_blob(encoding='UTF-8').readall().split('\n')[:-1]
        
        print("File Downloaded")
        return res
        pass

class LocalReader(Reader):
    def __init__(self, path):
        self.__path__ = path
        pass

    def read(self):
        try:
            with open(self.path, 'r') as fp:
                res = []
                for stock in fp:
                    res.append(stock[:-1])
                return res
        except:
            print("Exception thrown. Please pass in a valid filename")

        pass

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
        #To do: Implement basic candlestick visualization
        #to do: implement the ability to customize the candlestick visualizations in terms of aesthetics

        self.createIfDoesntExist(self.output_path)
        res = {}
        for ticker in data:
            output_path = self.output_path + "\\" + ticker + '.pdf'
            res[ticker] = mpf.plot(data[ticker].iloc[-weekOffset:], type="candle",
            title="{} Candlestick Chart for {} Weeks".format(ticker, str(weekOffset)), volume=True, savefig=output_path)
        return res
        pass

    
class StockDataHandler:
    def __init__(self, reader: Reader, processor: DataProcessor, transformer: DataVisualizer):
        self.reader = reader 
        self.processor = processor 
        self.transformer = transformer
    
    def handle_data(self):
        data = self.reader.read()
        processed_data = self.processor.process_data(data)
        transformed_data = self.transformer.transform_data(processed_data)

class VisualizationEmailer:
    def __init__(self, configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        self.zip_path = os.path.join(config.get("OUTPUT", "OUTPUT_PATH"), str(date.today()), str(date.today())) + '.zip'
        self.output_path =  os.path.join(config.get("OUTPUT", "OUTPUT_PATH"), str(date.today()))
        #self.zip_path = self.output_path + "\\" + str(date.today())
        pass 

    def email_data(self):
        print("Entered email data function \n calling zip data function")
        self.__zip_data__()
        print("File zipped \n Generating email")
        pass 

    def __zip_data__(self):
        #shutil.make_archive(self.output_path, 'zip', self.zip_path)
        with zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.output_path):
                for file in files:
                    if '.zip' not in file:
                        zipf.write(os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file),
                        os.path.join(self.output_path, '.')))
        pass

def main():
    reader = AzureBlobStorageReader('D:\Python Notes\Python Work\CandlestickVisualizer\env.config')
    stocks = reader.read()
    print(stocks)
    processor = DataProcessor()
    transformed_data = processor.process_data(stocks)
    visualizer = DataVisualizer('D:\Python Notes\Python Work\CandlestickVisualizer\env.config')
    visualizations = visualizer.visualize_data(transformed_data)
    print(len(visualizations))
    emailer = VisualizationEmailer('D:\Python Notes\Python Work\CandlestickVisualizer\env.config')
    emailer.email_data()

if __name__ == "__main__":
    main()