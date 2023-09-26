#*****************************************************************************************************
#
# USAGE NOTES:
#
# Ensure input_csv_file_path, input_text_file_path & output_text_file_path values in the main program
# are updated, if you need to change the defaults - 
#   csv_folder\\13F_INPUT.csv, txt_folder\\13F_INPUT.txt, and txt_folder\\13F_REORDERED.txt.
#
# Input Files:
#
# 1. input_csv_file_path -  only minor adjustments should need to be done to create the new report. 
#      As such, ensure the csv is created as follows:
#       a) Do "Save As" in Excel from the spreadsheet that will be published. This is to ensure
#          that the list is sorted by position size as it should be in the final report.
#       b) Ensure that the first column that has the Company Names and Ticker matches the 
#          names used in the report exactly. This is so that the reordering logic finds the 
#          matching reports in the input text file. 
#          NOTE: extract_names_and_tickers script may be used to sync the names in the csv and the
#           report, if need be.
# 2. input_text_file_path - The text file can be a cut and paste from the word document
#      that contains the prior quarter report with the following edits: 
#       a) Remove everthing other than the quarterly activity of the positions - this includes 
#          headings, introduction, etc. 
#       b) Make sure every position whose activity is individually described is in its own para/line -
#          i.e., If there are additional Notes, then include them within the same para/line. Also,
#          if multiple positions are combined, separate them. 
#
# Output File:
#
# output_text_file_path - The reorodered output file can be used to organize the quarterly report
#   for the current quarter. 
#
# NOTE: To generate the template for the new report, do the following:
#  a) Copy and paste the prior report and make the changes to reflect the new quarter
#     in the Word document that contains all the reports for a particular Hedge Fund. 
#  b) In the output text file, ensure Notes are in separate lines and combine the positions with 
#     no explanations into a comma-separated list under each of the sections.
#  c) Replace each section in the new report template with the content from the generated text file. 
#     For the comma-separated list with no explanation, use the explanation in the template for 
#     the new report.
#
#*****************************************************************************************************

import csv

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

def get_indicators(third_column_value, sixth_column_value):
  """Gets the indicator for the given third and sixth column values.

  Args:
    third_column_value: The third column value.
    sixth_column_value: The sixth column value.

  Returns:
    A string indicating whether the value decreased, increased, kept steady, was disposed, or was new.
  """

  third_value = convert_string_to_number(third_column_value)
  sixth_value = convert_string_to_number(sixth_column_value)
  if third_value != 0 and sixth_value == 0:
    return 'New Stakes'
  elif third_value == 0 and sixth_value != 0:
    return 'Stake Disposals'
  elif third_value > sixth_value:
    return 'Stake Increases'
  elif third_value < sixth_value:
    return 'Stake Decreases'
  else:
    return 'Kept Steady'

def process_csv_file(input_csv_file_path, input_text_file_path, output_text_file_path):
  """Processes the given CSV and text files and outputs a text file with the first column values and their corresponding lines from the text file, prefixed with ": ", organized in sections based on the indicators.

  Args:
    input_csv_file_path: The path to the input CSV file.
    input_text_file_path: The path to the input text file.
    output_text_file_path: The path to the output text file.
  """

  with open(input_csv_file_path, 'r') as input_csv_file, open(input_text_file_path, 'r') as input_text_file, open(output_text_file_path, 'w') as output_text_file:
    csv_reader = csv.reader(input_csv_file)
    text_file_lines = input_text_file.readlines()

    # Create a dictionary to store the first column values and their corresponding lines from the text file, organized by indicator.
    indicators_dict = {}
    for indicator in ['New Stakes', 'Stake Disposals', 'Kept Steady', 'Stake Increases', 'Stake Decreases']:
      indicators_dict[indicator] = []

    # Iterate over the rows in the input CSV file.
    for row in csv_reader:
      # Get the first column value and indicator.
      first_column_value = row[0]
      indicator = get_indicators(row[2], row[5])

      # Search through the text file lines for a line that starts with the first column value followed by a colon.
      for line in text_file_lines:
        if line.startswith(first_column_value + ':'):
          # Add the first column value and the line to the list of first column values and lines for the given indicator.
          indicators_dict[indicator].append(line)
          break

      # If no match was found, add the first column value only to the list of first column values for the given indicator.
      else:
        indicators_dict[indicator].append(first_column_value)

    # Write the first column values and their corresponding lines to the output text file, organized in sections based on the indicators.
    for indicator, activities in indicators_dict.items():
      output_text_file.write(f'{indicator}:\n\n')

      for line in activities:
        output_text_file.write(f'{line}\n')


if __name__ == '__main__':
  # Get the path to the input CSV file.
  input_csv_file_path = 'csv_folder\\13F_INPUT.csv'

  # Get the path to the input text file.
  input_text_file_path = 'txt_folder\\13F_INPUT.txt'

  # Get the path to the output text file.
  output_text_file_path = 'txt_folder\\13F_REORDERED.txt'

  # Process the CSV and text files.
  process_csv_file(input_csv_file_path, input_text_file_path, output_text_file_path)
