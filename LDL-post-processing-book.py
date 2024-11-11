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
        obj_string.append("{}_{}_PDF".format(coll_name[colls], coll_num[colls]))
    # From directory we put the file names and their type to a dictionary istead of using multiple lists then will compare to the list of customized file names with _OBJ from file_name to see if the file in directory did not have obj retur empty
    file_dict = {}
    for file in os.listdir(OBJS):
        if "PDF" in file:
            name, ext = os.path.splitext(file)
            file_dict[name] = ext
    #Filling the file_column list to fill the file column:
    file_column = []
    for each in obj_string:
        if each in file_dict:
            file_column.append("Data/{}{}".format(each, file_dict[each]))
        else:
            file_column.append("")

    #id slice of the 
    keys = ['amistad', 'apl', 'cppl', 'dcc', 'ebrpl', 'fpoc', 'hicks', 'hnoc', 'lsa', 'lasc', 'lsm', 'lsu', 'lsua', 'lsus', 'lsuhsc', 'lsuhscs', 'latech', 'loyno', 'louisiananewspapers', 'mcneese', 'nojh', 'nicholls', 'nsu', 'oplib', 'slu', 'subr', 'sowela', 'state', 'tahil', 'tulane', 'ull', 'ulm', 'uno']
    values = ['Amistad', 'APL', 'CPPL', 'DCC', 'EBRPL', 'FPOC', 'Hicks', 'HNOC', 'LSA', 'LASC', 'LSM', 'LSU', 'LSUA', 'LSUS', 'LSUHSC', 'LSUSHCS', 'LATECH', 'LOYNO', 'LouisianaNewspapers', 'McNeese', 'NOJH', 'Nicholls', 'NSU', 'OPLIB', 'SLU', 'SUBR', 'SOWELA', 'State', 'TAHIL', 'Tulane', 'ULL', 'ULM', 'UNO']
  
    map_terms = {}

    for k in range(len(keys)):
        map_terms[keys[k]] = values[k]


    field_access_terms = []
    for i in id_to_list:
        field_access_terms.append(map_terms[i.split('-')[0]])


    LDLdf["file"] = file_column
    LDLdf["parent_id"] = ""
    LDLdf["field_weight"] = ""
    LDLdf["field_member_of"] = ""
    LDLdf["field_model"] = "" #The number of resource type according to collection, obj or any other kind in the resource types in drupal
    LDLdf["field_access_terms"] = field_access_terms #customized field for groups, which is a number associated with the group names number
    LDLdf["field_resource_type"] = "" #The number of resource type according to collection, obj or any other kind in the resource types in drupal
    LDLdf.drop("field_date_captured", inplace=True ,axis= 1, errors='ignore')
    LDLdf.drop("field_is_preceded_by", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("field_is_succeeded_by", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("field_form_URI", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("field_form_authURI", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("field_rights_statement", inplace=True ,axis= 1,errors='ignore')
    LDLdf.drop("rights_statement_uri", inplace=True ,axis= 1,errors='ignore')
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
    text_list = []
    weight_list = []
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
    # loop through text to extract dateIssued text, if no text then append empty string
    for snippet in text:
        if snippet != None and "\n" not in snippet and snippet != 'true' and len(snippet) > 4:
                text_list.append(snippet)
        else:
            text_list.append('')
    for i in range(len(text_list)):
        date_issueds.append(text_list[i])
    for num in range(len(tags)):
        name_tag = tags[num].split('}')
        if "isSequenceNumberOf" in name_tag[1]:
            weight_list.append(text[num])
        else:
            weight_list.append("")
    mylist = list(zip(tag_name, attrib, weight_list, date_issueds))

    #loop through all tupels and group each item's tupels into a list
    item_list = []
    group_list = []
    viewer = []
    for tupel_item in mylist:
        group_list.append(list(tupel_item))
        if tupel_item[0] == 'RDF' and len(group_list) > 1:
            item_list.append(group_list)
            group_list = [list(tupel_item)]
    if group_list:
        item_list.append(group_list)
    
    for i in range(len(item_list)):
        if item_list[i][2][1][0] == 'info:fedora/islandora:bookCModel':
            content_type.append('Document')
            viewer.append('PDF.js')
        if item_list[i][2][1][0] == 'info:fedora/islandora:sp_large_image_cmodel':
            content_type.append('Image')
            viewer.append('OpenSeadragon')
        if item_list[i][2][1][0]  == 'info:fedora/islandora:sp-audioCModel':
            content_type.append('Audio')
            viewer.append('')
        if item_list[i][2][1][0]  == 'info:fedora/islandora:sp_videoCModel':
            content_type.append('Video')
            viewer.append('')
        if item_list[i][3][0] != 'deferDerivatives':
            if item_list[i][3][1][0] == 'info:fedora/islandora:collectionCModel':
                content_type.append('Collection')
                viewer.append('')
        if item_list[i][2][1][0] == 'info:fedora/islandora:newspaperCModel':
            content_type.append('Newspaper')
            viewer.append('')
        if item_list[i][2][1][0] == 'info:fedora/islandora:newspaperIssueCModel':
            content_type.append('Publication Issue')
            viewer.append('PDF.js')
        if item_list[i][2][1][0] == 'info:fedora/islandora:sp_pdf':
            content_type.append('Document')
            viewer.append('PDF.js')
        if item_list[i][2][1][0] == 'info:fedora/islandora:compoundCModel':
            content_type.append('Compound Object')
            viewer.append('')
        if item_list[i][3][0]  == 'hasModel':
            if item_list[i][3][1][0] == 'info:fedora/islandora:bookCModel':
                content_type.append('Paged Content')
                viewer.append('Mirador')
            if item_list[i][3][1][0] == 'info:fedora/islandora:sp_large_image_cmodel':
                content_type.append('Image')
                viewer.append('OpenSeadragon')
            if item_list[i][3][1][0]  == 'info:fedora/islandora:sp-audioCModel':
                content_type.append('Audio')
                viewer.append('')
            if item_list[i][3][1][0]  == 'info:fedora/islandora:sp_videoCModel':
                content_type.append('Video')
                viewer.append('')
            if item_list[i][3][1][0] == 'info:fedora/islandora:newspaperCModel':
                content_type.append('Newspaper')
                viewer.append('')
            if item_list[i][3][1][0] == 'info:fedora/islandora:newspaperIssueCModel':
                content_type.append('Publication Issue')
                viewer.append('PDF.js')
            if item_list[i][3][1][0] == 'info:fedora/islandora:sp_pdf':
                content_type.append('Document')
                viewer.append('PDF.js')
            if item_list[i][3][1][0] == 'info:fedora/islandora:compoundCModel':
                content_type.append('Compound Object')
                viewer.append('')
        
    weight = []
    field_member_of = []
    count = []

    #modified this loop to get isMemberOf value for each issue's parent_id
    for item in item_list:
        if item[3][0] == 'isMemberOf':
            parent_pid = item[3][1][0].split("/")
            parent.append(parent_pid[1])
            weight.append('')
        if item[2][0] == 'isMemberOf':
            parent_pid = item[2][1][0].split("/")
            parent.append(parent_pid[1])
            weight.append('') 
        if item[2][0] == 'isMemberOfCollection' and item[2][1][0].split('/')[1] == 'islandora:root':
            parent.append('')
            weight.append('')
        if item[2][0] == 'isMemberOfCollection' and item[2][1][0].split('/')[1] != 'islandora:root':# and item[4][0] != 'isConstituentOf':
            if len(item) > 5:
                if len(item) > 7:
                    parent.append(item[5][1][0].split('/')[1])
                    weight.append(item[6][2])
                if item[4][0] == 'isConstituentOf':
                    parent.append(item[4][1][0].split('/')[1])
                    weight.append(item[5][2])
                elif len(item) == 6:
                    parent.append(item[2][1][0].split('/')[1])
                    weight.append('')
            else:
                parent.append(item[2][1][0].split('/')[1])
                weight.append('')
        if item[3][0] == 'isMemberOfCollection':
            parent.append(item[3][1][0].split('/')[1])
            # parent.append('')
            weight.append('')
        if item[3][0] == 'isConstituentOf':
            parent.append(item[3][1][0].split('/')[1])
            weight.append(item[4][2])
        if item[3][0] == 'deferDerivatives':
            parent.append(item[4][1][0].split('/')[1])        
            weight.append('')

    issue_dates = []
    for r in range(len(item_list)):
        if r+1 > (len(item_list)):
            break
        else:
            if "isSequenceNumberOf" in item_list[r][0]:
                collectionName = RDF_dir.split("/")[6]
                nameofnumber = item_list[r][0]
                ParentNumber = nameofnumber.split("_")[1]
                # parent.append("{}:{}".format(collectionName, ParentNumber))
                # weight.append(item_list[r][2])
            if "dateIssued" == item_list[r][-3][0]:
                issue_dates.append(item_list[r][-3][3])
            else:
                issue_dates.append("")
                  
    # print(parent)
    LDL["parent_id"] = parent    
    LDL["field_weight"] = weight
    LDL["field_model"] = content_type
    LDL["field_viewer_override"] = viewer
    LDL["field_edtf_date_issued"] = issue_dates
    LDL["field_edtf_date_created"] = ""
    LDL["field_linked_agent"] = ""
    LDL.sort_values(by='field_identifier', ascending=False, inplace=True)
    LDL.sort_values(by='parent_id', ascending=True, inplace=True)
    LDL.sort_values(by='field_weight', ascending=True, inplace=True)
    LDL.sort_values(by='field_model', ascending=True, inplace=True)


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
