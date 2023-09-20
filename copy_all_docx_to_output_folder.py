import os
import shutil

def copy_all_docx_to_output_folder(input_folder_path, output_folder_path):
  """Copies all the Word documents from a folder and its subfolders to an output folder.

  Args:
    input_folder_path: The path to the input folder containing the Word documents.
    output_folder_path: The path to the output folder where the Word documents will be copied to.
  """

  if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

  for root, dirs, files in os.walk(input_folder_path):
    for file_name in files:
      if file_name.endswith(".docx"):
        input_file_path = os.path.join(root, file_name)
        output_file_path = os.path.join(output_folder_path, file_name)

        shutil.copy2(input_file_path, output_file_path)

def main():
  """Copies all the Word documents from the input folder to the output folder."""

  input_folder_path = "D:\\MyDocs\\Investments\\Hedge-Funds-My-Research-for-cloning"
  output_folder_path = "input_folder"

  copy_all_docx_to_output_folder(input_folder_path, output_folder_path)

if __name__ == "__main__":
  main()
