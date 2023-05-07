# Candlestick Visualizer

Candlestick Visualizer is a Python application that fetches a list of stock's preplaced in Azure Blob Storage, or local ath, generates candlestick chart visualizations, and emails a compressed ZIP file containing the visualizations to the user. This project utilizes `pandas`, `matplotlib`, `yfinance`, and `smtplib` libraries to provide a seamless experience to users who want to visualize stock trends and make informed decisions.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Fetch stock data from Azure Blob Storage
- Process stock data using pandas
- Generate candlestick charts using matplotlib
- Email visualizations as a ZIP file to the user

## Requirements

- Python 3.8+
- Azure Blob Storage account
- SMTP gmail email service credentials (Will require you to create an app password https://support.google.com/accounts/answer/185833?hl=en)

## Installation

1. Clone the repository: git clone https://github.com/nkashyap14/CandlestickVisualizer.git
2. Change directory to the cloned repository: cd CandlestickVisualizer
3. Install required packages: pip install -r requirements.txt
4. Configure environment variables in `.env` file: 
AZURE_STORAGE_CONNECTION_STRING=your_azure_blob_storage_connection_string
SMTP_SERVER=your_smtp_server
SMTP_PORT=your_smtp_port
EMAIL_ADDRESS=your_email_address
EMAIL_PASSWORD=your_email_password


## Usage

1. Run the main application:

2. Follow the prompts in the terminal to provide input for the stocks you want to visualize and the email address where you want to receive the ZIP file containing the visualizations.

## Contributing

1. Fork the repository.
2. Create a new branch with your feature or bugfix.
3. Commit your changes and create a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.



