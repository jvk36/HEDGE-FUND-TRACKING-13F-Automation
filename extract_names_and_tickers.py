#*****************************************************************************************************
#
# USAGE NOTES:
#
# The utility provides a way to sync the names in the Quarter-over-Quarter comparison spreadsheet
# to the names used in the report. It takes the latest report and outputs the list of stock names
# and tickers used that can be directly pasted into the comparison spreadsheet that is sorted
# by name. Once this is done for all the reports, we ensure it stays in sync by copying any new
# names that entters the report going forward is copied and pasted from the spreadsheet on to the
# report.
#
# Note: to ensure any discrepencies are addressed, copy the list generated on to a new column in the
# sorted spreadsheet and make any adjustments that might be needed.
#
#*****************************************************************************************************

import re

def extract_items(text_file):
  """Extracts items from a text file in the format "name(ticker):", where "name" and "ticker" can be any sequence of characters. Items can be either in a new line followed by a ":" or comma-separated and followed by a new line. In each case, ignore the characters after the ":" till EOL.

  Args:
    text_file: A file object containing the text file to extract items from.

  Returns:
    A list of extracted items.
  """

  items = []
  for line in text_file:
    # Extract the item name(s) and ticker(s).
    matches = re.findall(r"(?:^|,)[ ]*([^()]+)\(([^\)]+)\):?", line)
    item_names = [match[0] for match in matches]
    item_tickers = [match[1] for match in matches]

    # Add each item to the list.
    for item_name, item_ticker in zip(item_names, item_tickers):
      items.append(f"{item_name} ({item_ticker})")

  return items

def sort_items(items):
  """Sorts the given items in ascending order.

  Args:
    items: A list of items to sort.

  Returns:
    A sorted list of items.
  """

  return sorted(items)

def store_sorted_items(sorted_items, output_file):
  """Stores the given sorted items in the given output file, with each item on a new line.

  Args:
    sorted_items: A list of sorted items.
    output_file: A file object containing the output file to store the sorted items in.
  """

  for item in sorted_items:
    output_file.write(f"{item}\n")

def main():
  # Get the input and output file paths.
  # input_file_path = input("Enter the path to the input text file: ")
  # output_file_path = input("Enter the path to the output text file: ")

  # Open the input and output files.
  with open("txt_folder\\13F_R_I.txt", "r", errors="ignore") as input_file, open("txt_folder\\13F_R_O.txt", "w") as output_file:
    # Extract the items from the input file.
    items = extract_items(input_file)

    # Sort the extracted items.
    sorted_items = sort_items(items)

    # Store the sorted items in the output file, with each item on a new line.
    store_sorted_items(sorted_items, output_file)

if __name__ == "__main__":
  main()