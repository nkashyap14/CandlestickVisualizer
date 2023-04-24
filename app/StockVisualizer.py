from abc import ABC, abstractmethod 
import yfinance as yf
from collections import defaultdict
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import configparser

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
        with open("D:\Python Notes\Python Work\CandlestickVisualizer\data\stock.txt", "wb") as file:
            file.write(blob_client.download_blob().readall())
        
        print("File Downloaded")
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
        self.__options__ = ['Close', 'High', 'Low', 'Open']

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
                if len(tempEntry.keys()) == 5:
                    tickerData[ticker].append(tempEntry)
        
        return tickerData

class DataTransformer:  
    def transform_data(self, data):
        """"Takes in stock data from Data Processor. Stock data is in form of dict where keys are stock tickers mapped 
        to daily granularity candlestick level data. This function then outputs a collection of candlestick charts"""
        #To do: Implement basic candlestick visualization
        #to do: implement the ability to customize the candlestick visualizations in terms of aesthetics
        pass

    
class StockDataHandler:
    def __init__(self, reader: DataReader, processor: DataProcessor, transform: DataTransformer):
        self.reader = reader 
        self.processor = processor 
        self.transformer = transformer
    
    def handle_data(self):
        data = self.reader.read()
        processed_data = self.processor.process_data(data)
        transformed_data = self.transformer.transform_data(processed_data)


def main():
    reader = AzureBlobStorageReader('D:\Python Notes\Python Work\CandlestickVisualizer\env.config')
    processor = DataProcessor()
    transformer = DataTransformer()