
# WazirX Trading Bot

## Introduction

This project is a Python trading bot that connects to the WazirX cryptocurrency exchange using the WazirX API. It allows you to set up and manage stop-limit orders for trading. The bot uses the WazirX WebSocket API to stream real-time market data, and it includes a Flask web interface for configuring trading parameters.

Please note that trading cryptocurrencies involves risk, and this bot is provided for educational and experimental purposes. Use it responsibly and at your own risk.

## Features

- Real-time market data streaming via the WazirX WebSocket API.
- Ability to create, update, and monitor stop-limit orders.
- A web-based interface for configuring trading parameters and initiating trading.

## Prerequisites

Before running this trading bot, you need the following:

- Python 3.x installed on your system.
- Dependencies installed as specified in the project.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/deysanjeeb/wazirX-trailstop.git
   cd wazirX-trailstop
   ```

2. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the bot, configure your API keys in the `config.py` file. Make sure to keep your API keys secure and do not share them in your code.

```python
API_KEY = 'your_api_key'
SECRET_KEY = 'your_secret_key'
```

## Usage

1. Start the trading bot:

   ```bash
   python trail.py
   ```

2. Access the web interface by opening a web browser and navigating to [http://localhost:8080/](http://localhost:8080/).

3. Log in with your API keys and set your trading parameters.

4. Click the "Start Trading" button to initiate the trading process.

## Support and Contribution

- If you encounter any issues or have questions, please [create an issue](https://github.com/deysanjeeb/wazirX-trailstop/issues).
- Contributions to this project are welcome. Fork the repository, make your changes, and create a pull request.

## Disclaimer

- This trading bot is provided for educational purposes only and is not intended for real trading without proper testing and risk management.
- Use this bot at your own risk. The developers are not responsible for any financial losses.




## License

This project is licensed under the [MIT License](LICENSE).
