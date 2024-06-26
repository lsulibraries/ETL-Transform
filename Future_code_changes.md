# Pre processing
### Make Changes
- add mapping to titleInfo>title in LDL_mapping.csv otherwise field title wont be created and title is essential for the ingest

### Changed
- Changed output csv formatting: Changed the output directory format for steps 1 and 2 so that for all 3 steps we pass -o csvName.csv instead of -o csvname to ensure consistency between input and output CSV arguments.
  
# Post-processing:
### Make Changes
- Change the File directory string write from Data/Colname_nm.obj to Data/Colname/Colname_nm.obj
- Parse for field_model and put the right field_model to output csv

### Changed
- Changed output csv formatting
