#*****************************************************************************************************
#
# USAGE NOTES:
#
# Ensure the following variable values in the main program are updated before running this script:
# 1. Replace the start_date to be the beginning of the quarter (YYYY-MM-DD). Ex: "2023-01-01"
# 2. Replace the end_date to be the end of the quarter (YYYY-MM-DD). Ex: "2023-03-31" 
# 3. Replace input_csv_file, if you need to change the default 'csv_folder\\13F_INPUT.csv'
# 4. Replace output_text_file_path, if you need to change the default 'txt_folder\\13F_ACTIVITY.txt'
#
# Also ensure input_csv_file_path & output_text_file_path values in the main program are updated.
#
# Input File:
#
#   input_csv_file_path - To create the csv, do the following:
#   Do "Save As" in Excel from the spreadsheet that will be published. This is to ensure
#   that the list is sorted by position size as it should be in the final report.
#
# Output File:
#
#   output_text_file_path - The output file that will contain a line for each row in the CSV
#   that explains the activity that quarter, price-range the position traded at, and the 
#   current price. 
#
# NOTE: The generated acitivity can be directly used in the new report to reflect the updated 
# activity for each position.
#
#*****************************************************************************************************

# !pip install requests
# !pip install --force-reinstall yfinance==0.2.28 # the newer version caused an error and hence using the older one.

import csv
import yfinance as yf
import re

def extract_ticker(input_string):
  """Extracts the ticker symbol within brackets i.e. () in the input string.

  Args:
    input_string: A string.

  Returns:
    A string containing the sub-string within brackets, or an empty string if no
    brackets are found.
  """

  match = re.search(r'\(([^)]+)\)', input_string)
  if match:
    return match.group(1)
  else:
    return None

def get_current_price(ticker):
  """Gets the current stock price of a US listed stock.

  Args:
    ticker: The ticker symbol of the stock.

  Returns:
    The current stock price, or None if the ticker symbol is invalid.
  """

  try:
    ticker_obj = yf.Ticker(ticker)
    current_price = ticker_obj.info['currentPrice']
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
    ticker_obj = yf.Ticker(ticker)
    historical_prices = ticker_obj.history(start=start_date, end=end_date)
    lowest_price = min(historical_prices['Close'])
    highest_price = max(historical_prices['Close'])
    return lowest_price, highest_price
  except Exception as e:
    # print(f'Failed to get price range for ticker symbol "{ticker}": {e}')
    return 0, 0


def convert_string_to_number(string_value):
  """Converts the given string value to a number, removing any commas.

  Args:
    string_value: The string value to convert.

  Returns:
    The converted number, or None if the string value cannot be converted to a number.
  """

  try:
    return int(string_value.replace(',', ''))
  except ValueError:
    return 0

def get_indicator_and_activity(first_column_value, third_column_value, sixth_column_value, start_date, end_date):
  """Gets the activity text to output for the position.

  Args:
    first_column_value: The name and ticker of the position in the format <name>(<ticker>)
    third_column_value: The size of the position this quarter.
    sixth_column_value: The size of the position in the previous quarter.
    start_date: YYYY-MM-DD
    end_date: YYYY-MM-DD

  Returns:
    indicator - A string indicating whether the value decreased, increased, kept steady, was disposed, or was new.
    activity - The name & ticker passed in along with associated text that explains the activity.
  """

  activity = first_column_value + ": "
  ticker = extract_ticker(activity)
  if ticker is not None:
    lowest_price, highest_price = get_price_range(ticker, start_date, end_date)
  third_value = convert_string_to_number(third_column_value)
  sixth_value = convert_string_to_number(sixth_column_value)
  price_range_text = "."
  if lowest_price != 0 or highest_price != 0:
    price_range_text = f" at prices between ${lowest_price:.2f} and ${highest_price:.2f}." 
    current_price = get_current_price(ticker)
    current_price_text = ""
    if current_price != 0:
      current_price_text = f"The stock currently trades at ${current_price:.2f}."

  if third_value != 0 and sixth_value == 0:
    return 'New Stakes', activity + "The position was established" + price_range_text + current_price_text
  elif third_value == 0 and sixth_value != 0:
    return 'Stake Disposals', activity + "The stake was disposed" + price_range_text + current_price_text
  elif third_value > sixth_value:
    percentage_change = abs(third_value - sixth_value) * 100 / sixth_value
    return 'Stake Increases', activity + f"The position was increased by {percentage_change:.0f}% this quarter" + price_range_text + current_price_text
  elif third_value < sixth_value:
    percentage_change = abs(third_value - sixth_value) * 100 / sixth_value
    return 'Stake Decreases', activity + f"The stake was decreased by {percentage_change:.0f}% this quarter" + price_range_text + current_price_text
  else:
    return 'Kept Steady', activity + "The position was kept steady this quarter." + current_price_text

def process_csv_file(input_csv_file_path, output_text_file_path, start_date, end_date):
  """Processes the given CSV file and outputs a text file with the first column values and a line 
     explaining the activity, prefixed with ": ", organized in sections based on the type of activity.

  Args:
    input_csv_file_path: The path to the input CSV file.
    output_text_file_path: The path to the output text file.
    start_date: YYYY-MM-DD
    end_date: YYYY-MM-DD
  """

  with open(input_csv_file_path, 'r') as input_csv_file, open(output_text_file_path, 'w') as output_text_file:
    csv_reader = csv.reader(input_csv_file)

    # Create a dictionary to store the first column values and their corresponding lines from the text file, organized by indicator.
    indicators_dict = {}
    for indicator in ['New Stakes', 'Stake Disposals', 'Stake Increases', 'Stake Decreases', 'Kept Steady']:
      indicators_dict[indicator] = []

    # Iterate over the rows in the input CSV file.
    for row in csv_reader:
      # Get the first column value and indicator.
      indicator, activity = get_indicator_and_activity(row[0], row[2], row[5], start_date, end_date)
      # Add the first column value.
      indicators_dict[indicator].append(activity)

    # Write the first column values and their corresponding lines to the output text file, organized in sections based on the indicators.
    for indicator, activities in indicators_dict.items():
      output_text_file.write(f'{indicator}:\n\n')

      for line in activities:
        output_text_file.write(f'{line}\n')


if __name__ == '__main__':
  # Path to the input CSV file.
  input_csv_file_path = 'csv_folder\\13F_INPUT.csv'

  # Path to the output text file.
  output_text_file_path = 'txt_folder\\13F_ACTIVITY.txt'

  # Start date of the Quarter
  start_date = "2023-07-01"

  # End date of the Quarter
  end_date = "2023-09-30"

  # Process the CSV and text files.
  process_csv_file(input_csv_file_path, output_text_file_path, start_date, end_date)
