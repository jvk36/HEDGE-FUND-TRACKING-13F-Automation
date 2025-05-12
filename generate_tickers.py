#*****************************************************************************************************
#
# USAGE NOTES:
#
# Ensure the following variable values in the main program are updated before running this script:
# 1. Replace input_csv_file, if you need to change the default 'csv_folder\\13F_INPUT.csv'
# 2. Replace output_text_file_path, if you need to change the default 'txt_folder\\TICKERS.txt'
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
#   with just the ticker associated. 
#
#*****************************************************************************************************

import csv
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

def process_csv_file(input_csv_file_path, output_text_file_path):
  """Processes the given CSV file and outputs a text file with the tickers in separate lines.

  Args:
    input_csv_file_path: The path to the input CSV file.
    output_text_file_path: The path to the output text file.
  """

  with open(input_csv_file_path, 'r') as input_csv_file, open(output_text_file_path, 'w') as output_text_file:
    csv_reader = csv.reader(input_csv_file)

    # Iterate over the rows in the input CSV file.
    for row in csv_reader:
      # Get the first column value and indicator.
      ticker = extract_ticker(row[0])
      output_text_file.write(f'{ticker}\n')


if __name__ == '__main__':
  # Path to the input CSV file.
  input_csv_file_path = 'csv_folder\\13F_INPUT.csv'

  # Path to the output text file.
  output_text_file_path = 'txt_folder\\TICKERS.txt'

  # Process the CSV and text files.
  process_csv_file(input_csv_file_path, output_text_file_path)
