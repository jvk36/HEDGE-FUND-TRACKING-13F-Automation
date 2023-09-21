INTRODUCTION:

The project is aimed at automating the process of publishing 13F quarterly reports 
that analyzes the trading activity of the top hedge funds. Below is a summary
of the key automation tasks, associated programs/scripts along with their usages:


1. Build an AI/ML model that summarizes the quarterly reports: 

The idea is to generate a TL;DR for the 13F quarterly reports. The summary 
along with the quarter-over-quarter comparison spreadsheet should provide the 
reader with 80% or more of the information in the report without having to read
through the whole text. A vanilla BART sequence-to-sequence encoder-decoder 
classifier can provide reasonable summaries:

vanilla_summarizer.py: TO DO. It takes the text of a quarterly report as input 
                       and generates a summary using the default model used 
                       by the Hugging Face transformer model API, 
                       sshleifer/distilbart-cnn-12-6. 

While BART is able to provide reasonable summaries, a more specialized model
should be more useful to the readership. We fine-tune the vanilla BART  model
on a dataset that contains quarterly reports done over the last decade on the 
top hedge funds to generate summaries that can be directly used in the reports.
The dataset for fine-tuning is collected by running the following pipeline:
a) copy_all_docx_to_output_folder.py: The script consolidates all the Microsoft
   word documents that contain quarterly reports of each of the hedge funds into
   an output folder.
b) convert_all_docx_to_text.py: The script takes the folder containing the reports
   and converts them into corresponding text documents in another folder.
c) convert_all_text_to_csv.py: The script takes the folder containing the text 
   documents and returns a csv file with title and body as the columns. The quarterly
   reports from all the hedge fund documents from the past decade are consolidated into
   a single file. This will be the dataset used for fine-tuning.

TO DO: Fine tuning the BART model and using it to generate summaries.


2. Build a Quarter-over Quarter Comparison Spreadsheet: 13f-xml-to-csv.py

The quarterly activities of the top hedge funds are available through EDGAR as 
xml files. To build a comparison spreadsheet, we use a python script 
13f-xml-to-csv.py which takes the xml file downloaded from EDGAR as input and
outputs a csv file that consolidates the information. The CSV content is then
incorporated into a Quarter-over-Quarter comparison spreadsheet which forms
a key component of the quarterly reports.

3. Build a program that reorders sections and explains the trading activity 
   of each stock in the 13F report: TO DO. 

The program should take a csv containing the quarter-over-quarter activity along
with the previous quarter's report text categorized in sections as input. The 
program then looks at the share-count change of each position quarter-over-quarter 
in the csv file to determine the section the activity should be reported under. It then
re-organizes the report into sections based on the quarterly activity. The sections
are "NEW STAKES", "STAKE DISPOSALS", "STAKE INCREASES", "STAKE DECREASES", and "KEPT STEADY".
The trading activity of each stock in the report is then updated to include the 
activity that quarter and the current stock price.

NOTE: The activities are clubbed together based on a percentage threshold.





### python -m venv .env
### 
### # Activate the virtual environment
### source .env/Scripts/activate OR source .env/bin/activate 
### # Deactivate the virtual environment
### source .env/Scripts/deactivate

### Run the following in the sallygen and web sub-directories to install 
### the required libraries into the python environment setup above
###
### pip install -r requirements.txt
###