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
    LDLdf = pd.DataFrame(pd.read_csv(csvs,encoding='utf-8'))
    LDLdf.rename(columns= {'PID' : 'id'},  inplace = True)
    coll_name = []
    coll_num = []
    obj_string = []
    id_to_list = LDLdf["id"].tolist() ###Putting the elements of id column to a list###
    for IDs in id_to_list:
        splitted_IDs= IDs.split(':')
        coll_name.append(splitted_IDs[0])
        coll_num.append(splitted_IDs[1])
    for colls in range(len(coll_name)):
        obj_string.append("{}_{}_OBJ".format(coll_name[colls], coll_num[colls]))
      # From directory we put the file names and their type to a dictionary istead of using multiple lists then will compare to the list of customized file names with _OBJ from file_name to see if the file in directory did not have obj retur empty
    file_dict = {}
    for file in os.listdir(OBJS):
        if "OBJ" in file:
            name, ext = os.path.splitext(file)
            file_dict[name] = ext
    #Filling the file_column list to fill the file column:
    file_column = []
    for each in obj_string:
        if each in file_dict:
            file_column.append("Data/{}{}".format(each, file_dict[each]))
        else:
            file_column.append("")

    LDLdf["file"] = file_column
    LDLdf["parent_id"] = ""
    LDLdf["field_weight"] = ""
    LDLdf["field_member_of"] = ""
    LDLdf["field_model"] = "" #The number of resource type according to collection, obj or any other kind in the resource types in drupal
    LDLdf["field_access_terms"] = "" #customized field for groups, which is a number associated with the group names number
    LDLdf["field_resource_type"] = "" #The number of resource type according to collection, obj or any other kind in the resource types in drupal
    LDLdf.drop("field_date_captured", inplace=True ,axis= 1, errors='ignore')
    LDLdf.drop("field_is_preceded_by", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("field_is_succeeded_by", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("field_form_URI", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("field_form_authURI", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("field_rights_statement", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("field_rights_statement_uri", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("nan", inplace=True ,axis= 1,errors='ignore')
    
    #fill nul values
    LDLdf = LDLdf.apply(lambda col: col.fillna(''))
    return LDLdf


#################### 2) fill field_member_of, parent_id, field_weight column ########################

def input_RDF(RDF_dir, LDL):
    data = glob.glob("{}/*.rdf".format(RDF_dir))
    tags = [] #getting none-splitted
    val = [] #adding values to
    tag_name = [] #ALL the Tags in the rdf
    attrib = []
    text = []
    weight_list= []
    parent = []
    date_issueds = []
    file_type = []
    content_type = []
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
    for num in range(len(tags)):
        if "isSequenceNumberOf" in tags[num]:
            weight_list.append(text[num])
        else:
            weight_list.append("")
    mylist = list(zip( tag_name, attrib, weight_list))
    mylist_to_list = [list(i) for i in mylist] ##Extra(To make each element from tuple to list)##
    splitting = []
    for each in mylist_to_list:
        if each[0] == ("RDF"):
            splitting.append(each)
        if each[0] == ("hasModel"):
            splitting.append(each)
        if each[0] == ("isConstituentOf"):
            splitting.append(each)
        #if each[0] == ("isPageOf"):
        #     splitting.append(each)
        if each[0] == ("isSequenceNumber"):
            splitting.append(each)
        if each[0] == ("isPageNumber"):
            splitting.append(each)
        if each[0] == ("isSection"):
            splitting.append(each)
        if each[0] == ("isMemberOf"):
            splitting.append(each)
        if each[0] == ("deferDerivatives"):
            splitting.append(each)
        if each[0] == ("generate_ocr"):
            splitting.append(each)
    new = [ones for ones in mylist_to_list if ones not in splitting] #only keeps Description, isSequenceNumberOf and isMemberOfCollection
    weight = []
    field_member_of = []
    parrent = []
    count = []
    
    for q in new:
        if "isPageOf" in q[0]:
            count.append(q)

    for r in range(len(new)):
        if r+1 > (len(new)):
            break   
        else:
            if "Description" in new[r][0]:
                if "isPageOf" in new[r+1][0]:
                    collectionName = RDF_dir.split("/")[1]
                    nameofnumber = new[r+1][1][0]
                    ParentNumber = nameofnumber.split(":")[2]
                    parrent.append("{}:{}".format(collectionName, ParentNumber))
                    weight.append(new[r+1][2])
                    
                if "Description" in new[r+1][0]:
                    collectionName = RDF_dir.split("/")[1]
                    parrent.append("{}:COLLECTION".format(collectionName))
                    weight.append("")
                                        
                if "isSequenceNumberOf" in new[r+1][0]:
                    collectionName = RDF_dir.split("/")[1]
                    nameofnumber = new[r+1][0]
                    ParentNumber = nameofnumber.split("_")[1]
                    parrent.append("{}:{}".format(collectionName, ParentNumber))
                    weight.append(new[r+1][2])
                                      
                if "isMemberOfCollection" in new[r+1][0]:
                    collectionMember = new[r+1][1][0].split("/")[1]
                    field_member_of.append(collectionMember)
                    parrent.append(collectionMember)
                    weight.append("")

                if "isMemberOfCollection" not in new[r+1][0]:
                    field_member_of.append("")
                    
          
    LDL["parent_id"] = parrent    
    LDL["field_weight"] = weight
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
    input = input_RDF(args.files_directory,LDLdf_1)
    output = write(input,args.output_directory)
main()



## Command:
# To process one file at a time >>> python3 LDL-post-processing.py -c LDL_Tracking_Spreadsheet/amistad-pgoudvis/xml2csv_amistad-pgoudvis.csv -f LDL_Tracking_Spreadsheet/amistad-pgoudvis/Data -o LDL_Tracking_Spreadsheet/amistad-pgoudvis
