# LDL Data Transformation tools:
LDL Data Transformation tools are the tools used in Louisiana digital Library ETL pipeline to transform data from xml, RDF files into csv files, and cleans those data to prepare them for the ingest to the new Louisiana Digital Library website. Bellow is the instruction for two tools that works as "transformation" phase in our ETL pipeline.</br></br>

## 1. XML2Workbench Scrip Documentation:
This code appears to be a Python script that performs various operations on XML files, mainly related to extracting unique tags and attributes, checking for errors, and generating CSV reports based on the content of the XML files. Here's a high-level overview of the code's functionality: </br>
### 1-A) Get all the unique Tags and attributes, and write them into a CSV:
a.	The script imports necessary libraries and defines some global variables and data structures. </br>
b.	It defines a function process_command_line_arguments() to parse command-line arguments using the argparse library.</br>
c.	The MODs function processes XML files in the specified input directory, extracts data from them, and yields the results.</br>
d.	The unique_tag_attrib function populates dictionaries to count the occurrences of unique tags and attributes in the XML files.</br>
e.	The uniq_data_to_dict function prepares the data for writing to a CSV file based on the counts of unique tags and attributes.</br>
#### Example of terminal command: 
`` python3 xml2csv.py -i FILE_DIRECTORY -oat OUTPUT_DIRECTORY/CSV_OUTPUT_NAME `` </br></br>

### 1-B) PART II: Get the XML Path, check for spelling, and errors:
a.	The get_csv function reads a CSV file if provided and stores its data in a dictionary.</br>
b.	The Path_repeat_check function counts the occurrences of unique XML paths.</br>
c.	The error_repeat_check function identifies and stores unique error messages.</br>
d.	The paths_to_dict function prepares data for writing to a CSV file based on the unique paths and error messages.</br>
#### Example of terminal command: 
`` python3 xml2csv.py -i FILE_DIRECTORY -c MASTER_CSV -o OUTPUT_DIRECTORY/CSV_OUTPUT_NAME `` </br></br>

### 1-C) XML to CSV. Taking MODS XML files and converting them to a workbench csv:
a.	A class xmlSet is defined to collect and process XML data.</br>
b.	The xml2wb_parse_mods function extracts data from an XML file, including PID (a processed file name).</br>
c.	The xml2wb_parse function processes XML content, extracting tags, attributes, and values.</br>
d.	The compare_and_write function associates extracted values with the corresponding fields specified in a CSV file.</br>
e.	The test_result function is for testing and displaying results.</br>
f.	The main function processes the command-line arguments, reads CSV data, and processes XML files, generating CSV reports.</br>
#### Example of terminal command: 
`` python3 xml2csv.py -i FILE_DIRECTORY -cc MASTER_CSV -o OUTPUT_DIRECTORY/CSV_OUTPUT_NAME.csv `` </br></br>

### Important notes:
Master CSV is an edited csv file using output csv from mode 2 that Librarian should add informations (columns of field name associated with xpath)in the way that:</br></br>
•	If we want a attribute's value be written in a field specified in master, librarian need to specify the path's row in another column called "att_needed" and say yes to that and also mention the name of the field in the filed column as well</br>
•	If we want to only get the text, apperantly, the column "att_needed" should not be filled out and either should be No or empty and the field column should be filled out.</br>
•	the only paths that are important for us (either for writing the attribute's value or text in the xpath)</br>
•	If we want to have attribute's values in the metadata csv file, we need to have a column that value would be yes for the paths that we need attribute mapping (ex. att_need)</br>


## 2) Post-Processing 
This code performs a post-processing process for LDL (Library Digital Library) content migration using Islandora Workbench. It takes metadata in CSV format, extracts information from RDF files, and prepares the data for importing into Islandora Workbench. The processed data is then saved as a new CSV file.
It extracts information from RDF files, updates the metadata, and prepares it for import into Islandora Workbench. The resulting CSV files can be used for further data management and curation tasks.</br>

***************

# LSU ETL Pipeline:
## Data Extraction:
### 1. Extract data Using drush
- collection_name:collection
```sh
cd /var/www/drupal7

drush -u 1 islandora_datastream_crud_fetch_pids --namespace=collection_name --pid_file=/tmp/collection_name.txt

drush -u 1 idcrudfd --pid_file=/tmp/collection_name.txt --datastreams_directory=/tmp/collection_name --dsid=MODS
drush -u 1 idcrudfd --pid_file=/tmp/collection_name.txt --datastreams_directory=/tmp/collection_name --dsid=RELS-EXT
drush -u 1 idcrudfd --pid_file=/tmp/collection_name.txt --datastreams_directory=/tmp/collection_name --dsid=OBJ
```
### 2. Place Extracted data
```sh
cd /tmp/collection_name
zip collection_name.zip *
ctl-D
ctl-D
```
### 3. Copy to the target location:
```sh
scp dgi-ingest:/tmp/collection_name/amistad-pgoudvis.zip ~/Downloads
cp ~/Downloads/collection_name.zip /meda/wwc/0A2C-888E/collection_name/

cd /media/wwc/0A2C-888E/collection_name
mkdir Data
cd Data
unzip ../collection_name.zip 

for f in *.jp2; do opj_decompress -i "$f" -OutFor PNG -o "${f%.*}.png"; done;
```

## Data Transformation using xml2csv python script:
### STEP1: get the attribute and tags:
- For windows: ```python3 '.\xml2csv_2.py' -i DATA_DIR -oat OUTPUT_DIR/CSV_NAME(no.csv)```

### STEP2: get paths and errors: 
- For windows: ```python3 '.\xml2csv.py' -i DATA_DIR -c STEP1_csv(NAME.CSV) v -o OUTPUT_DIR/CSV_NAME(no.csv)```

### STEP3: run xml to csv using the csv field mapping:
- For windows: ```python3 '.\xml2csv.py' -i DATA_DIR -cc MAPPED_CSV -o OUTPUT_DIR/CSV_NAME(no.csv)```


## Data Ingestion using Workbench tool :
```sh
./workbench --config CONFIG.yml --check
./workbench --config CONFIG.yml 
```

***************
### Functions
The code is organized into several functions: </br>
a.	process_command_line_arguments():</br>
This function processes command-line arguments using the argparse library and returns the parsed arguments as an object.</br></br>
b.	files_directories(all_files):</br>
This function takes a directory path and returns a list of file paths in that directory.</br></br>
c.	csv_directories(metadata_csv):</br>
This function takes a directory path and returns a list of CSV files in that directory.</br></br>
d.	objects_to_df(csvs, OBJS)</br>

***************

### Command Line Arguments
The code uses command-line arguments to specify the input and output directories and the CSV file with metadata.)</br>
Command Line Arguments:)</br>
-c or --csv_directory: Path to the directory containing CSV files with metadata.)</br>
-f or --files_directory: Path to the directory containing object files (OBJs).)</br>
-o or --output_directory: Path to the directory where the output CSV files will be saved.)</br>






