from candlestickvisualizer import *

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