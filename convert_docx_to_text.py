import docx

def convert_docx_to_text(input_file_path, output_file_path):
  """Converts a Word document to text while ignoring all characters it cannot handle and writing a new line only after each paragraph.

  Args:
    input_file_path: The path to the input Word document.
    output_file_path: The path to the output text file.
  """

  with open(output_file_path, "w", encoding="utf-8") as output_file:
    document = docx.Document(input_file_path)


    for paragraph in document.paragraphs:
      # Create a flag to indicate the start of a new paragraph.
      new_paragraph_flag = True
      for run in paragraph.runs:
        # Try to encode the text using the `utf-8` encoding.
        try:
          text = run.text.encode("utf-8").decode("utf-8")
        except UnicodeDecodeError as e:
          # If the encode fails, print the error message to the console and continue.
          print(e)
          continue

        # If the new paragraph flag is set, write a newline character to the output file.
        if new_paragraph_flag:
          output_file.write("\n")

        # Write the text to the output file.
        output_file.write(text)

        # Reset the new paragraph flag.
        new_paragraph_flag = False

      # If the last paragraph in the document does not end with a newline character, write one to the output file.
      if not new_paragraph_flag:
        output_file.write("\n")

def main():
  """Converts the input Word document to text."""

  input_file_path = "input.docx"
  output_file_path = "output.txt"

  convert_docx_to_text(input_file_path, output_file_path)

if __name__ == "__main__":
  main()