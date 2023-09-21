import csv

def preprocess_text(text):
  """Preprocess text by ignoring end-of-line characters.

  Args:
    text: The text to preprocess.

  Returns:
    The preprocessed text.
  """

#  text = text.replace(",", "[COMMA]")
  text = text.replace("\n", "") # ignore EOL
  return text

def convert_text_to_csv(input_file_path, output_file_path):
  """Converts a text file to a CSV file with two fields: Title and Body.

  Args:
    input_file_path: The path to the input text file.
    output_file_path: The path to the output CSV file.
  """

  with open(input_file_path, "r", errors="ignore") as input_file, open(output_file_path, "w", newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["Title", "Body"])

    current_title = None
    current_body = ""
    for line in input_file:
      line = preprocess_text(line)

      if line.startswith("Tracking"):
        # If we have a current title, write it to the CSV file.
        if current_title:
          writer.writerow([f"\"{current_title}\"", f"\"{current_body}\""]) # enclose title and body in double-quotes in the csv file to handle commas within fields.

        # Set the current title to the new line.
        current_title = line
        current_body = ""

      else:
        # Append the current line to the current body.
        current_body += line

    # Write the last title and body to the CSV file.
    if current_title:
      writer.writerow([f"\"{current_title}\"",  f"\"{current_body}\""]) # enclose title and body in double-quotes in the csv file to handle commas within fields.

def main():
  """Converts the input text file to a CSV file."""

  input_file_path = "txt_folder\\input.txt"
  output_file_path = "csv_folder\\output.csv"

  convert_text_to_csv(input_file_path, output_file_path)

if __name__ == "__main__":
  main()
  