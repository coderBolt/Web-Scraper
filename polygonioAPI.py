import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = 'YOUR_API_KEY'

def get_option_prices(symbol, expiration_date):
    endpoint = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/minute/{expiration_date}?apiKey={API_KEY}'
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            return data['results']
    return None

def calculate_strategy_value(options_data):
    return sum(options_data)

def main():
    symbol = 'AAPL'  # Ticker Symbol
    expiration_date = '2023-01-20'  # Expiration Date

    while True:
        stock_price_endpoint = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?apiKey={API_KEY}'
        stock_price_response = requests.get(stock_price_endpoint)
        stock_price = stock_price_response.json()['results'][0]['c']

        option_prices = get_option_prices(symbol, expiration_date)

        if option_prices:
            df = pd.DataFrame(option_prices)
            df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
            df.set_index('timestamp', inplace=True)

            option_data = df[['o', 'h', 'l', 'c']].mean(axis=1)

            strategy_value = calculate_strategy_value(option_data)

            print(f"Stock Price: {stock_price}, Strategy Value: {strategy_value}")
            print(option_data)

        else:
            print("Error fetching option prices.")
        import time
        time.sleep(60)

if __name__ == "__main__":
    main()
