from abc import ABC, abstractmethod 
import configparser
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

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
