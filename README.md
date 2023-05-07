Candlestick Visualizer is a Python application that fetches stock data from Azure Blob Storage, generates candlestick chart visualizations, and emails a compressed ZIP file containing the visualizations to the user. This project utilizes pandas, matplotlib, and smtplib libraries to provide a seamless experience to users who want to visualize stock trends and make informed decisions.

Table of Contents
Features
Requirements
Installation
Usage
Contributing
License
Features
Fetch stock data from Azure Blob Storage
Process stock data using pandas
Generate candlestick charts using matplotlib
Email visualizations as a ZIP file to the user
Requirements
Python 3.8+
Azure Blob Storage account
SMTP email service credentials
Installation
Clone the repository:
bash
Copy code
git clone https://github.com/nkashyap14/CandlestickVisualizer.git
Change directory to the cloned repository:
bash
Copy code
cd CandlestickVisualizer
Install required packages:
Copy code
pip install -r requirements.txt
Configure environment variables in .env file:
makefile
Copy code
AZURE_STORAGE_CONNECTION_STRING=your_azure_blob_storage_connection_string
SMTP_SERVER=your_smtp_server
SMTP_PORT=your_smtp_port
EMAIL_ADDRESS=your_email_address
EMAIL_PASSWORD=your_email_password
Usage
Run the main application:
css
Copy code
python main.py
Follow the prompts in the terminal to provide input for the stocks you want to visualize and the email address where you want to receive the ZIP file containing the visualizations.
Contributing
Fork the repository.
Create a new branch with your feature or bugfix.
Commit your changes and create a pull request.
License
This project is licensed under the MIT License. See LICENSE for details.
