import pandas as pd
import xml.etree.ElementTree as ET
import glob
from os import listdir , sep, path
import os
import argparse
from dateutil import parser

def process_command_line_arguments():
    parser = argparse.ArgumentParser(description='Post Processing Process For LDL Content Migration Using Islandora Workbench')
    parser.add_argument('-c', '--csv_directory', type=str, help='Path to metadata', required=False)
    parser.add_argument('-f', '--files_directory', type=str, help='Path to the files', required=False)
    parser.add_argument('-o', '--output_directory', type=str, help='Path to the output csv containing paths, frequency, and error reports', required=False)
    args = parser.parse_args()
    return args

################### 1) Getting data and fill the file column if files exist in the Data directory ########################
def input_directory(csvs, OBJS):
    collection = csvs.split(".")[0]
    LDLdf = pd.DataFrame(pd.read_csv(csvs,encoding='utf-8'))
    LDLdf.rename(columns= {'PID' : 'id'},  inplace = True)
    coll_name = []
    coll_num = []
    file_name = []
    id_to_list = LDLdf["id"].tolist() ###Putting the elements of id column to a list###
    for IDs in id_to_list:
        print(IDs)
        splitted_IDs= IDs.split(':')
        coll_name.append(splitted_IDs[0])
        coll_num.append(splitted_IDs[1])
    for colls in range(len(coll_name)):
        file_name.append("{}_{}_PDF".format(coll_name[colls], coll_num[colls]))
        
    ObjFiles = [] #getting the names of the OBJ FILES 
    file_format = "" #getting the file type of OBJ FILES
    
    FILES = os.listdir(OBJS)
    for file in FILES:
        if "PDF" in file:
            ObjFiles.append(file.split(".")[0])
            file_format =  ".{}".format(file.split(".")[1])
        if "OBJ" in file:
            ObjFiles.append(file.split(".")[0])
            file_format =  ".{}".format(file.split(".")[1])    

    #Filling the file_column list to fill the file column:
    file_column = []
    for files in file_name:
        if files in ObjFiles:
            file_column.append("Data/{}{}".format(files,file_format)) #EDIT >>> deleted Collection form formating the name because we do not have a folder consist of data for each collection
        else:
            file_column.append("")
    # print("This will be concat of the the name of File column generated for the files that are Objects: \n{}".format(file_column))
    # print("------------------------------------------------")


    LDLdf["file"] = file_column
    del file_format
    LDLdf["parent_id"] = ""
    LDLdf["field_weight"] = ""
    LDLdf["field_member_of"] = ""
    LDLdf["field_model"] = "" #The number of resource type according to collection, obj or any other kind in the resource types in drupal
    LDLdf["field_access_terms"] = "LouisianaNewspapers" #customized field for groups, which is a number associated with the group names number
    LDLdf["field_resource_type"] = "" #The number of resource type according to collection, obj or any other kind in the resource types in drupal
    LDLdf.drop("field_date_captured", inplace=True ,axis= 1, errors='ignore')
    LDLdf.drop("field_is_preceded_by", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("field_is_succeeded_by", inplace=True ,axis= 1,errors='ignore')
    
    #fill nul values
    LDLdf = LDLdf.apply(lambda col: col.fillna(''))
    return LDLdf


#################### 2) fill field_member_of, parent_id, field_weight column ########################

def input_RDF(RDF_dir, LDL):
    data = glob.glob("{}/*.rdf".format(RDF_dir))
    # print("List of the RDF files in the directory: \n{}".format(data))
    tags = [] #getting none-splitted
    val = [] #adding values to
    tag_name = [] #ALL the Tags in the rdf
    attrib = []
    text = []
    #added list of values found in text with snippet loop
    text_list = []
    weightList= []
    #added parrent
    parrent = []
    #added date issues
    date_issueds = []
    data.sort()
    
    for dirs in data:
        rdf = ET.parse("{}".format(dirs))
        itter = rdf.iter()
        for inner in itter:
            tags.append(inner.tag)
            val.append(inner.attrib)
            text.append(inner.text)

    for tag in tags:
        split_tags = tag.split('}')
        tag_name.append(split_tags[1]) # ALL THE TAGS
    for vals in val:
        attrib.append(list(vals.values()))
    # loop through text to extract dateIssued text, if no text then
    for snippet in text:
        if snippet != None and "\n" not in snippet and snippet != 'true' and len(snippet) > 4:
                text_list.append(snippet)
        else:
            text_list.append('')
    for i in range(len(text_list)):
        date_issueds.append(text_list[i])
    for num in range(len(tags)):
        name_tag = tags[num].split('}')
        if "isSequenceNumberOf" == name_tag[1]:
            weightList.append(text[num])
        if "isSequenceNumber" == name_tag[1]:
            weightList.append(text[num])    
        else:
            weightList.append("")
    #mylist list of all tupels 2907 in this case
    mylist = list(zip(tag_name, attrib, weightList, date_issueds))
    # print(len(mylist))

    #loop through all tupels and group each item's tupels into a list
    item_list = []
    group_list = []
    for tupel_item in mylist:
        group_list.append(list(tupel_item))
        if tupel_item[0] == 'RDF' and len(group_list) > 1:
            item_list.append(group_list)
            group_list = [list(tupel_item)]
    if group_list:
        item_list.append(group_list)
    
    #Replaced this code for generating the new list and instead used the item_list and group_list above
    # mylist_to_list = [list(i) for i in mylist] ##Extra(To make each element from tuple to list)##
    # splitting = []
    # for each in mylist_to_list:
    #     if each[0] == ("RDF"):
    #         splitting.append(each)
    #     if each[0] == ("hasModel"):
    #         splitting.append(each)
    #     if each[0] == ("isConstituentOf"):
    #         splitting.append(each)
    #     #if each[0] == ("isPageOf"):
    #     #     splitting.append(each)
    #     if each[0] == ("isSequenceNumber"):
    #         splitting.append(each)
    #     if each[0] == ("isPageNumber"):
    #         splitting.append(each)
    #     if each[0] == ("isSection"):
    #         splitting.append(each)
    #     if each[0] == ("isMemberOf"):
    #         splitting.append(each)
    #     if each[0] == ("deferDerivatives"):
    #         splitting.append(each)
    #     if each[0] == ("generate_ocr"):
    #         splitting.append(each)
    # new = [ones for ones in mylist_to_list if ones not in splitting] #only keeps Description, isSequenceNumberOf and isMemberOfCollection
    weight = []
    field_member_of = []
    count = []

    #modified this loop to get isMemberOf value for each issue's parent_id

    for item in item_list:
        if item[2][0] == 'isMemberOf':
            print('got-an-issue')
            parent_pid = item[2][1][0].split("/")
            parrent.append(parent_pid[1])
        if item[2][0] == 'isMemberOfCollection':
            print(item[2][1][0].split('/')[1])
            parrent.append(item[2][1][0].split('/')[1])
            if "isPageOf" in item[0]:
                count.append(item)
   

    issue_dates = []
    for r in range(len(item_list)):
        if r+1 > (len(item_list)):
            break
        else:
            if "isSequenceNumber" == item_list[r][4][0]:
                collectionName = RDF_dir.split("/")[6]
                nameofnumber = item_list[r][4][2]
                weight.append(nameofnumber)
            if "isSequenceNumberOf" in item_list[r][0]:
                #collectionName = RDF_dir.split("/")[1]
                collectionName = RDF_dir.split("/")[6]
                nameofnumber = item_list[r][0]
                ParentNumber = nameofnumber.split("_")[1]
                parrent.append("{}:{}".format(collectionName, ParentNumber))
                weight.append(item_list[r][2])
            if "dateIssued" == item_list[r][-3][0]:
                issue_dates.append(item_list[r][-3][3])
            else:
                issue_dates.append("")

            if "isMemberOfCollection" == item_list[r][2][0]:
                coll = item_list[r][2][1][0].split("/")[1]
                field_member_of.append(coll)
                weight.append("")
                    
    LDL["parent_id"] = parrent    
    LDL["field_weight"] = weight
    LDL["field_edtf_date_issued"] = issue_dates
    LDL["field_edtf_date_created"] = ""
    LDL["field_linked_agent"] = ""

    # change the date to EDTF format Skip for now!
    # LDL['field_date'] = pd.to_datetime(LDL['field_date']).dt.strftime('%Y-%m-%d')
    # print(LDL[['field_date', 'id']])
    # print('Data is written in dataframe ...')

    return LDL

def write(input_df, output_filename):
    Workbench_ready_csv = input_df.to_csv("{}".format(output_filename), index=False)
    print('*******************************************\nData post processed and written to csv ...\n*******************************************')
    return Workbench_ready_csv


def main():
    args = process_command_line_arguments()
    LDLdf_1 = input_directory(args.csv_directory,args.files_directory)
    input_file = input_RDF(args.files_directory,LDLdf_1)
    output = write(input_file,args.output_directory)
main()



## Command:
# To process one file at a time >>> python3 LDL-post-processing.py -c LDL_Tracking_Spreadsheet/amistad-pgoudvis/xml2csv_amistad-pgoudvis.csv -f LDL_Tracking_Spreadsheet/amistad-pgoudvis/Data -o LDL_Tracking_Spreadsheet/amistad-pgoudvis
