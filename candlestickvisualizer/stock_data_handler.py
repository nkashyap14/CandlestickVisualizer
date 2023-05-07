from .readers import Reader
from .data_processor import DataProcessor
from .data_visualizer import DataVisualizer
from .visualization_emailer import VisualizationEmailer

class StockDataHandler:
    def __init__(self, reader: Reader, processor: DataProcessor, visualizer: DataVisualizer, emailer : VisualizationEmailer):
        self.reader = reader 
        self.processor = processor 
        self.visualizer = visualizer
        self.emailer = emailer
    
    def execute_flow(self):
        data = self.reader.read()
        processed_data = self.processor.process_data(data)
        visualizations = self.visualizer.visualize_data(processed_data)
        self.emailer.email_data()