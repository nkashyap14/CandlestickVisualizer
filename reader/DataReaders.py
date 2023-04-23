from abc import ABC, abstractmethod 

class Reader(ABC):

    @abstractmethod
    def read(self):
        """This method will read from some path and return a list of stock tickers"""
        pass
    

class AzureBlobStorageReader(Reader):

    def __init__(self):
        #load data from config file here
        pass

    def read(self):
        #use configured client in init to read data 
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