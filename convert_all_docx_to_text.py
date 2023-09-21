import os
from convert_docx_to_text import convert_docx_to_text

def convert_all_docx_to_txt(input_folder_path, output_folder_path):
  """Converts all the docx files in a folder to corresponding txt files.

  Args:
    input_folder_path: The path to the input folder containing the docx files.
    output_folder_path: The path to the output folder where the txt files will be saved.
  """

  if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

  for file_name in os.listdir(input_folder_path):
    if file_name.endswith(".docx"):
      input_file_path = os.path.join(input_folder_path, file_name)
      output_file_path = os.path.join(output_folder_path, file_name[:-5] + ".txt")

      convert_docx_to_text(input_file_path, output_file_path)

def main():
  """Converts all the docx files in the input folder to txt files."""

  # to supply absolute path, use the following format - "D:\\Users\\asvar\\HEDGE-FUND-TRACKING-13F-Automation\\input_folder\\"
  input_folder_path = "input_folder"
  output_folder_path = "output_folder"

  convert_all_docx_to_txt(input_folder_path, output_folder_path)

if __name__ == "__main__":
  main()