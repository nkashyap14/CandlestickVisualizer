from abc import ABC, abstractmethod 

class Reader(ABC):

    @abstractmethod
    def read(self):
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
        #read from local text file
        pass