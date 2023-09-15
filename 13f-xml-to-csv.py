#*****************************************************************************************************
#
# 1. Download the 13F information table for each fund tracked as an XML file into this directory
#    as input.xml.
# 2. Edit Line 30 of this program as indicated in the line comment, if needed.
# 3. Run this program to generate output.csv in the same directory. Save it into our fund-tracking
#    directory. 
# 4. Open output.csv and our tracking spreadsheet in Excel. 
# 5. Update the tracking spreadsheet by copying the information from output.csv.
#
# NOTE: The 2nd line of input.xml may have to be edited to read "<informationTable>" as the parser
#       runs into a problem with the sample below:
#    <informationTable xmlns="http://www.sec.gov/edgar/document/thirteenf/informationtable" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
#
#*****************************************************************************************************

# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
  
cols = ["nameOfIssuer", "value", "sshPrnamt"]
rows = []
  
# Parsing the XML file
xmlparse = Xet.parse('input.xml')
# root = xmlparse.getroot()
for i in xmlparse.findall("infoTable"):
    nameOfIssuer = i.find("nameOfIssuer").text
    # cusip = i.find("cusip").text
    value = int(i.find("value").text) # * 1000 # comment or uncomment "* 1000" depending on the 13F data
    j = i.find("shrsOrPrnAmt")
    sshPrnamt = int(j.find("sshPrnamt").text)
  
    rows.append({"nameOfIssuer": nameOfIssuer,
                 # "cusip": cusip,
                 "value": value,
                 "sshPrnamt": sshPrnamt})
df = pd.DataFrame(rows, columns=cols)

df = df.groupby(['nameOfIssuer'])[['value', 'sshPrnamt']].sum().reset_index()

# Writing dataframe to csv
df.to_csv('output.csv', header=False, index=False)
print(2)
