The project is aimed at automating the process of publishing 13F quarterly reports 
in the Seeking Alpha platform: https://seekingalpha.com/author/john-vincent . 
The reports analyze the trading activity of the top hedge funds. 

Below is a summary of the key automation tasks, associated programs/scripts along 
with their usages:  

1. Build an AI/ML model that summarizes the quarterly reports:   

The idea is to generate a TL;DR for the 13F quarterly reports. The summary 
along with the quarter-over-quarter comparison spreadsheet should provide the 
reader with 80% or more of the information in the report without having to read
through the whole text. A vanilla BART sequence-to-sequence encoder-decoder 
classifier can provide reasonable summaries:  

vanilla_summarizer.py: It takes the text of a quarterly report as input 
   and generates a summary using the default model used by the Hugging Face 
   transformer model API, sshleifer/distilbart-cnn-12-6.   

While BART is able to provide reasonable summaries, a fine-tuned model
should be more useful to the readership. We fine-tune the Google's mt5 model
(google/mt5-small) on a dataset that contains quarterly reports done over the 
last decade on the top hedge funds to generate summaries that can be directly 
used in the reports. The dataset for fine-tuning is collected and pushed to 
Hugging Face by running the following pipeline:    

a) copy_all_docx_to_output_folder.py: The script consolidates all the Microsoft
   word documents that contain quarterly reports of each of the hedge funds into
   an output folder.  

b) convert_all_docx_to_text.py: The script takes the folder containing the reports
   and converts them into corresponding text documents in another folder.  

c) convert_all_text_to_csv.py: The script takes the folder containing the text 
   documents and returns a csv file with title and body as the columns. The quarterly
   reports from all the hedge fund documents from the past decade are consolidated into
   a single file. This will be the dataset used for fine-tuning.  

d) push_to_hub_13F_Reports.ipyng: pushed to Hugging Face hub the 13F Reports dataset.  

This model is further optimized by training it with labeled data. Although 
fine-tuning an unsupervised BART model doesn't require label data, it can benefit from
it. To do this, we modify the training data generation pipeline to generate an extra
column in the csv file with training data:  

a) convert_all_text_to_csv_with_labels.py: The script takes the folder containing the text 
   documents and returns a csv file with title, body, and label as columns. The quarterly
   reports from all the hedge fund documents from the past decade are consolidated into
   a single file. This will be the dataset used for fine-tuning.    

b) 13F_Report_Summarization.ipynb: It fine tunes the t5 model (google/mt5-small) to create 
   an optimized model for 13F Reports summary using the jkv53/13F_Reports_with_labels 
   dataset in the Hugging Face Hub.   

Finally, a gradio UI is built that wraps the model interface in a web UI:

a) 13F_Summarizer_Gradio.ipynb: It provides a web interface for the 13F Summarizer 
   functionality. To use it, run the final cell in the notebook and copy/paste the 
   13F Quarterly report that needs to be summarized. The output box will contain a
   three-sentence summary of the full report.

2. Build a Quarter-over Quarter Comparison Spreadsheet: 13f-xml-to-csv.py  

The quarterly activities of the top hedge funds are available through EDGAR as 
xml files. To build a comparison spreadsheet, we use a python script 
13f-xml-to-csv.py which takes the xml file downloaded from EDGAR as input and
outputs a csv file that consolidates the information. The CSV content is then
incorporated into a Quarter-over-Quarter comparison spreadsheet which forms
a key component of the quarterly reports.  

3. Build a pipeline that reorders sections and explains the trading activity 
   of each stock in the 13F report:     

a) reorder_13F_report.py: The program takes a csv containing the quarter-over-quarter 
   activity along with the previous quarter's report text as input. The program then 
   looks at the share-count change of each position quarter-over-quarter in the csv 
   file to determine the section the activity should be reported under. It then
   re-organizes the report into sections based on the quarterly activity. The sections
   are "NEW STAKES", "STAKE DISPOSALS", "STAKE INCREASES", "STAKE DECREASES", and 
   "KEPT STEADY". The trading activity of each stock in the report is then updated to 
   include the activity that quarter and the current stock price.    
   NOTE: the program relies on the stock name and tickers in the csv to match the ones
   in the quarterly report. Use the utility extract_names_and_tickers.py to get them
   to match the first time (done after Q2 2023 - so just verify from this point on).

b) generate_13F_activity.py: The program takes a csv file containing the 
   quarter-over-quarter activity and outputs a line of text for each security that 
   explains the activity and the stock-price-range during the quarter.  
      





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
