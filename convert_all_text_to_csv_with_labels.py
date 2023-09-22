import csv
import os


def convert_all_text_to_csv(input_folder_path, output_file_path):
  """Converts all TXT files in an input folder to a consolidated output CSV file,
  with the following criteria:

  - The CSV has three fields: Title, Body, and Label.
  - Titles start with the word 'Tracking' in a new line and is till the end-of-line (EOL).
  - Label is the next three lines after the Title.
  - Body starts at the end of the corresponding Label and continues till the next time the word 'Tracking' appears in a new line.
  - The CSV should contain text that is pre-processed in the following way:
     * Ignore end-of-line characters.

  Args:
    input_folder_path: The path to the input folder containing the TXT files.
    output_file_path: The path to the output CSV file.
  """

  with open(output_file_path, "w", newline="", encoding='utf-8') as output_file:
    csv_writer = csv.writer(output_file)

    for file_name in os.listdir(input_folder_path):
      if file_name.endswith(".txt"):
        input_file_path = os.path.join(input_folder_path, file_name)

        with open(input_file_path, "r", encoding="utf-8", errors="ignore") as input_file:
          title = ""
          body = ""
          label = ""
          label_lines = 0
          for line in input_file:
            if line.startswith("Tracking"):
              # If we have a previous title and body, write them to the CSV file.
              if title and body:
                csv_writer.writerow([f"\"{title}\"", f"\"{body}\"", f"\"{label}\""]) # enclose title, body, and label in double-quotes in the csv file to handle commas within fields.

              # Set the new title and body.
              title = line.strip()
              body = ""
              label = ""
              label_lines = 0
            else:
              # Add the line to the label or body.
              if label_lines < 3:
                if len(line) < 3:
                  pass
                else:
                  label += line.strip()
                  label_lines += 1
              else:
                body += line.strip()

          # Write the last title, body, and label to the CSV file.
          if title and body:
            csv_writer.writerow([f"\"{title}\"", f"\"{body}\"", f"\"{label}\""]) # enclose title, body, and label in double-quotes in the csv file to handle commas within fields.

    # Pre-process the CSV file by replacing commas and EOL characters with special sequences.
    with open(output_file_path, "r", encoding="utf-8") as input_file:
      csv_reader = csv.reader(input_file)

      preprocessed_rows = []
      for row in csv_reader:
        preprocessed_row = []
        for field in row:
          preprocessed_row.append(field.replace("\n", "")) # ignore EOL
        preprocessed_rows.append(preprocessed_row)

    # Overwrite the output CSV file with the preprocessed rows.
    with open(output_file_path, "w", newline="", encoding='utf-8') as output_file:
      csv_writer = csv.writer(output_file)

      for row in preprocessed_rows:
        csv_writer.writerow(row)


def main():
  """Converts all TXT files in the input folder to a consolidated output CSV file, using the criteria specified above."""

  input_folder_path = "txt_folder"
  output_file_path = "csv_folder\\output_all_with_labels.csv"

  convert_all_text_to_csv(input_folder_path, output_file_path)


if __name__ == "__main__":
  main()