# LDL Data Transformation tools Explained:
LDL Data Transformation tools are the tools used in Louisiana digital Library ETL pipeline to transform data in the from of xml, RDF and transform them into csv files, and clean to prepare them for the ingest to the new Louisiana Digital Library website.

## 1. XML to CSV Scrip:
This code appears to be a Python script that performs various operations on XML files, mainly related to extracting unique tags and attributes, checking for errors, and generating CSV reports based on the content of the XML files. Here's a high-level overview of the code's functionality: </br>

- ***Get all the unique Tags and attributes, and write them into a CSV:***
    - The script imports necessary libraries and defines some global variables and data structures. </br>
    - It defines a function process_command_line_arguments() to parse command-line arguments using the argparse library.</br>
    - The MODs function processes XML files in the specified input directory, extracts data from them, and yields the results.</br>
    - The unique_tag_attrib function populates dictionaries to count the occurrences of unique tags and attributes in the XML files.</br>
    - The uniq_data_to_dict function prepares the data for writing to a CSV file based on the counts of unique tags and attributes.</br>


- ***PART II: Get the XML Path, check for spelling, and errors:***
    - The get_csv function reads a CSV file if provided and stores its data in a dictionary.</br>
    - The Path_repeat_check function counts the occurrences of unique XML paths.</br>
    - The error_repeat_check function identifies and stores unique error messages.</br>
    - The paths_to_dict function prepares data for writing to a CSV file based on the unique paths and error messages.</br>


- ***XML to CSV. Taking MODS XML files and converting them to a workbench csv:***
    - A class xmlSet is defined to collect and process XML data.</br>
    - The xml2wb_parse_mods function extracts data from an XML file, including PID (a processed file name).</br>
    - The xml2wb_parse function processes XML content, extracting tags, attributes, and values.</br>
    - The compare_and_write function associates extracted values with the corresponding fields specified in a CSV file.</br>
    - The test_result function is for testing and displaying results.</br>
    - The main function processes the command-line arguments, reads CSV data, and processes XML files, generating CSV reports.</br>


- ***Important Notes:***
    - Final pre-processed CSV will be created according to a field mapping csv (columns of field name associated with xpath).

    - If we want a attribute's value be written in a field specified in master, librarian need to specify the path's row in another column called "att_needed" and say yes to that and also mention the name of the field in the filed column as well

    - If we want to only get the text, apperantly, the column "att_needed" should not be filled out and either should be No or empty and the field column should be filled out.

    - the only paths that are important for us (either for writing the attribute's value or text in the xpath)

    - If we want to have attribute's values in the metadata csv file, we need to have a column that value would be yes for the paths that we need attribute mapping (ex. att_need)


## 2) Post-Processing 
- This code performs a post-processing process for LDL (Library Digital Library) content migration using Islandora Workbench. It takes metadata in CSV format, extracts information from RDF files, and prepares the data for importing into Islandora Workbench. The processed data is then saved as a new CSV file.
- It extracts information from RDF files, updates the metadata, and prepares it for import into Islandora Workbench. The resulting CSV files can be used for further data management and curation tasks.</br>

***************

# LSU ETL Pipeline
## 1. Data Extraction:
### STEP1: Extract data Using drush
- collection_name:collection
```sh
cd /var/www/drupal7

drush -u 1 islandora_datastream_crud_fetch_pids --namespace=collection_name --pid_file=/tmp/collection_name.txt

drush -u 1 idcrudfd --pid_file=/tmp/collection_name.txt --datastreams_directory=/tmp/collection_name --dsid=MODS
drush -u 1 idcrudfd --pid_file=/tmp/collection_name.txt --datastreams_directory=/tmp/collection_name --dsid=RELS-EXT
drush -u 1 idcrudfd --pid_file=/tmp/collection_name.txt --datastreams_directory=/tmp/collection_name --dsid=OBJ
```

### STEP2: Place Extracted data
```sh
cd /tmp/collection_name
zip collection_name.zip *
ctl-D
ctl-D
```
### STEP3: Copy to the target location:
```sh
scp dgi-ingest:/tmp/collection_name/amistad-pgoudvis.zip ~/Downloads
cp ~/Downloads/collection_name.zip /meda/wwc/0A2C-888E/collection_name/

cd /media/wwc/0A2C-888E/collection_name
mkdir Data
cd Data
unzip ../collection_name.zip 

for f in *.jp2; do opj_decompress -i "$f" -OutFor PNG -o "${f%.*}.png"; done;
```

## 2. Data Transformation using xml2csv and post-processing python scripts:
### 2.1 Pre-processing:
- ***Commandline Arguments explained:***
  - ***-i or --input_directory:*** Path to the directory containing xml files.
  - ***-oat or --output_attribsTags:*** Path that user defines to the output of csv that contains attributes and tags.
  - ***-c or --input_csv:*** Path to the input csv, from step1 that we want to transform in step2.
  - ***-cc or --input_clear_csv:*** Path to the mapped csv containing xpaths and fields associated for each xpath.)
  - ***-o or --output_directory:*** Path to the output csv.
  - ***-ow or --output_directory_workbench:*** Path to the pre-processed output csv.

- ***STEP1: get the attribute and tags:***

```python3 '.\xml2csv_2.py' -i DATA_DIR -oat OUTPUT_DIR/CSV_NAME(no.csv)```

- ***STEP2: get paths and errors:*** 

```python3 '.\xml2csv.py' -i DATA_DIR -c STEP1_csv(NAME.CSV) v -o OUTPUT_DIR/CSV_NAME(no.csv)```


- ***STEP3: run xml to csv using the csv field mapping:***

```python3 '.\xml2csv.py' -i DATA_DIR -cc MAPPED_CSV -o OUTPUT_DIR/CSV_NAME(no.csv)```


- ***STEP4: Post-Processing CSV from STEP3:***
  - ***Commandline Arguments explained:***
    - ***-c or --csv_directory:*** Path to the directory containing CSV files with metadata.)
    - ***-f or --files_directory:*** Path to the directory containing object files (OBJs).)
    - ***-o or --output_directory:*** Path to the directory where the output CSV files will be saved.)

```python3 LDL-post-processing.py -c PRE_PROCESSED_CSV_NAME.csv -f DIRECTORY_OF_RDFS_AND_OBJS -o FINAL_CSV_OUTPUT_DIRECTORY```

  - ***FINAL_CSV_OUTPUT_DIRECTORY can be:***
    - Specified in a pre-existing folder within the current directory or another directory for the CSV output: -o output/FINAL_CSV_NAME.csv
    - Specified only the CSV name to save the file in the current directory: -o FINAL_CSV_NAME.csv



## Data Ingestion using Workbench tool :
```sh
./workbench --config CONFIG.yml --check
./workbench --config CONFIG.yml 
```


### Command Line Arguments
The code uses command-line arguments to specify the input and output directories and the CSV file with metadata.)</br>
Command Line Arguments:)</br>







