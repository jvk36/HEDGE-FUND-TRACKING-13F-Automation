# !pip install requests
# !pip install yfinance
# OLD INFO - !pip install --force-reinstall yfinance==0.2.28 # the newer version caused an error and hence using the older one.

import yfinance as yf

def get_current_price(ticker):
  """Gets the current stock price of a US listed stock.

  Args:
    ticker: The ticker symbol of the stock.

  Returns:
    The current stock price, or None if the ticker symbol is invalid.
  """

  try:
    ticker = ticker.replace('.', '-')
    ticker_obj = yf.Ticker(ticker)
    # current_price = ticker_obj.info['currentPrice']
    current_price = ticker_obj.history()['Close'].iloc[-1]
    return current_price
  except Exception as e:
    print(f'Failed to get current stock price for ticker symbol "{ticker}": {e}')
    return 0

def get_price_range(ticker, start_date, end_date):
  """Gets the price range that a stock traded at during a given date range.

  Args:
    ticker: The ticker symbol of the security.
    start_date: The start date of the date range.
    end_date: The end date of the date range.

  Returns:
    A tuple containing the lowest and highest prices that the stock traded at during the given date range.
  """

  try:
    ticker = ticker.replace('.', '-')
    ticker_obj = yf.Ticker(ticker)
    historical_prices = ticker_obj.history(start=start_date, end=end_date)
    lowest_price = min(historical_prices['Close'])
    highest_price = max(historical_prices['Close'])
    return lowest_price, highest_price
  except Exception as e:
    print(f'Failed to get price range for ticker symbol "{ticker}": {e}')
    return 0, 0

if __name__ == '__main__':
  # Start date of the Quarter
  start_date = "2025-01-01"

  # End date of the Quarter
  end_date = "2025-03-31"

  # Process the CSV and text files.
  get_current_price("MSFT")
  get_price_range("MSFT", start_date, end_date)
  