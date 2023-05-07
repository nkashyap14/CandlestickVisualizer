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
import zipfile
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


'''This file is the initial monolithic application I created before going on to separate file structure'''

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
        res = self.__transform_data__(stocks, data)
        return res
        pass

    def __transform_data__(self, stocks, data):
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


class VisualizationEmailer:
    def __init__(self, configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        self.zip_path = os.path.join(config.get("OUTPUT", "OUTPUT_PATH"), str(date.today()), str(date.today())) + '.zip'
        self.output_path =  os.path.join(config.get("OUTPUT", "OUTPUT_PATH"), str(date.today()))
        self.user = config.get("EMAIL", "USER")
        self.sender_email = config.get('EMAIL', "SENDER_EMAIL")
        self.sender_pass = config.get('EMAIL', 'SENDER_PASSWORD')
        self.recipient_email = config.get('EMAIL', 'RECIPIENT_EMAIL')
        #self.zip_path = self.output_path + "\\" + str(date.today())
        pass 

    def email_data(self):
        print("Entered email data function \n calling zip data function")
        self.__zip_data__()
        print("File zipped \n Generating email")

        subject = str(date.today()) + " Stocks Candlestick Visualiztaion for {}".format(self.user)

        print('email is {}'.format(self.sender_email))

        with open(self.zip_path, "rb") as attachment:

            part = MIMEBase("application", "octet-stream")
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(self.zip_path)}",
            )

        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = self.sender_email
        message['To'] = self.recipient_email
        html_part = MIMEText("Find Zip Attached")
        message.attach(html_part)
        message.attach(part)


        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(self.sender_email, self.sender_pass)
        server.sendmail(self.sender_email, self.recipient_email, message.as_string())
        server.quit()   
        print("Email has been sent")     
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


class StockDataHandler:
    def __init__(self, reader: Reader, processor: DataProcessor, visualizer: DataVisualizer, emailer : VisualizationEmailer):
        self.reader = reader 
        self.processor = processor 
        self.visualizer = visualizer
        self.emailer = emailer
    
    def execute_flow(self):
        print("Reading stock ticker data")
        data = self.reader.read()
        print("Tickers read. Now grabbing raw data")
        processed_data = self.processor.process_data(data)
        print("Now visualizing data")
        visualizations = self.visualizer.visualize_data(processed_data)
        print("now emailing data")
        self.emailer.email_data()

def main():
    reader = AzureBlobStorageReader('D:\Python Notes\Python Work\CandlestickVisualizer\config\env.config')
    processor = DataProcessor()
    visualizer = DataVisualizer('D:\Python Notes\Python Work\CandlestickVisualizer\config\env.config')
    emailer = VisualizationEmailer('D:\Python Notes\Python Work\CandlestickVisualizer\config\env.config')
    handler = StockDataHandler(reader, processor, visualizer, emailer)
    handler.execute_flow()
    #stocks = reader.read()
    #print(stocks)
    #processor = DataProcessor()
    #transformed_data = processor.process_data(stocks)
    #visualizer = DataVisualizer('D:\Python Notes\Python Work\CandlestickVisualizer\env.config')

if __name__ == "__main__":
    main()