# LDL Data Transformation tools:
LDL Data Transformation tools are the tools used in Louisiana digital Library ETL pipeline to transform data from xml, RDF files into csv files, and cleans those data to prepare them for the ingest to the new Louisiana Digital Library website. Bellow is the instruction for two tools that works as "transformation" phase in our ETL pipeline.

### 1. XML2Workbench Scrip Documentation:
This code appears to be a Python script that performs various operations on XML files, mainly related to extracting unique tags and attributes, checking for errors, and generating CSV reports based on the content of the XML files. Here's a high-level overview of the code's functionality: </br>
### &emsp;&emsp;1.	PART I: Get all the unique Tags and attributes, and write them into a CSV:
&emsp;&emsp;&emsp; a.	The script imports necessary libraries and defines some global variables and data structures. </br>
&emsp;&emsp;&emsp; b.	It defines a function process_command_line_arguments() to parse command-line arguments using the argparse library.</br>
&emsp;&emsp;&emsp; c.	The MODs function processes XML files in the specified input directory, extracts data from them, and yields the results.</br>
&emsp;&emsp;&emsp; d.	The unique_tag_attrib function populates dictionaries to count the occurrences of unique tags and attributes in the XML files.</br>
&emsp;&emsp;&emsp; e.	The uniq_data_to_dict function prepares the data for writing to a CSV file based on the counts of unique tags and attributes.</br>
#### Example of terminal command: 
`` python3 xml2csv.py -i FILE_DIRECTORY -oat OUTPUT_DIRECTORY/CSV_OUTPUT_NAME `` </br>

### &emsp;&emsp; 2. PART II: Get the XML Path, check for spelling, and errors:
&emsp;&emsp;&emsp; a.	The get_csv function reads a CSV file if provided and stores its data in a dictionary.</br>
&emsp;&emsp;&emsp; b.	The Path_repeat_check function counts the occurrences of unique XML paths.</br>
&emsp;&emsp;&emsp; c.	The error_repeat_check function identifies and stores unique error messages.</br>
&emsp;&emsp;&emsp; d.	The paths_to_dict function prepares data for writing to a CSV file based on the unique paths and error messages.</br>
#### Example of terminal command: 
`` python3 xml2csv.py -i FILE_DIRECTORY -c MASTER_CSV -o OUTPUT_DIRECTORY/CSV_OUTPUT_NAME ``

### &emsp;&emsp; 3. XML to CSV. Taking MODS XML files and converting them to a workbench csv:
&emsp;&emsp;&emsp; a.	A class xmlSet is defined to collect and process XML data.</br>
&emsp;&emsp;&emsp; b.	The xml2wb_parse_mods function extracts data from an XML file, including PID (a processed file name).</br>
&emsp;&emsp;&emsp; c.	The xml2wb_parse function processes XML content, extracting tags, attributes, and values.</br>
&emsp;&emsp;&emsp; d.	The compare_and_write function associates extracted values with the corresponding fields specified in a CSV file.</br>
&emsp;&emsp;&emsp; e.	The test_result function is for testing and displaying results.</br>
&emsp;&emsp;&emsp; f.	The main function processes the command-line arguments, reads CSV data, and processes XML files, generating CSV reports.</br>
#### Example of terminal command: 
`` python3 xml2csv.py -i FILE_DIRECTORY -cc MASTER_CSV -o OUTPUT_DIRECTORY/CSV_OUTPUT_NAME.csv `` </br>

### Important notes:
Master CSV is an edited csv file using output csv from mode 2 that Librarian should add informations (columns of field name associated with xpath)in the way that:</br></br>
•	If we want a attribute's value be written in a field specified in master, librarian need to specify the path's row in another column called "att_needed" and say yes to that and also mention the name of the field in the filed column as well</br>
•	If we want to only get the text, apperantly, the column "att_needed" should not be filled out and either should be No or empty and the field column should be filled out.</br>
•	the only paths that are important for us (either for writing the attribute's value or text in the xpath)</br>
•	If we want to have attribute's values in the metadata csv file, we need to have a column that value would be yes for the paths that we need attribute mapping (ex. att_need)</br>


