import time
import numpy as np
import pandas as pd #version 1.5.3
##Functions for preprocessing data
    #Ideal Dataset: (global-data-on-sustainable-energy)


##Group entries together by country into a sublist
    #Entries should also be ordered by year
    #Other than removing the country name, order of entry features is retained. 
#Returns a list of countries, and a list filled with sublists for each country's entries 
    #Country (i) corresponds to sublist (i) 
def separateCountries(raw_entries_list):
    country_list = []
    list_of_country_sublists = []

    #Countries are already in order so we only need to grab them until we get next country
    cur_country = raw_entries_list[0][0] #Name of first country
    country_list.append(cur_country)
    country_sublist_temp = []
    for entry in raw_entries_list:
        if (cur_country != entry[0]): #Done adding entries for previous country, moving on to next country 
            list_of_country_sublists.append(country_sublist_temp) #add previous country over to consolidated list 
            country_sublist_temp = []
            cur_country = entry[0]
            country_list.append(cur_country)
        country_sublist_temp.append(entry[1:]) #skip country name 

    return country_list, list_of_country_sublists


##Shift data in specified column up by number of indicies specified
    #Does not replace the column data left on the bottom entries in the data_set
    #Instead, leaves that column empty (or whatever empty character  (or number) is specified) for those instances 
#Returns dataset after column shifting 
def shiftColumnDataUp(data_set, column_index_to_shift, shift_n, remainder_col_replacement_char = ''):
    column_vec = [] #size will be len(data_set) - shift_n
    i = 0
    for entry in data_set:
        if (i >= shift_n):  #gather values for column vec starting after n entries 
            column_vec.append(entry[column_index_to_shift])
        i += 1

    parsed_dataset = []
    i = 0 
    for entry in data_set:
        parsed_entry = entry.copy()
        if (i >= len(data_set) - shift_n): #columns past the (len-shift) index will have no label due to shift
                                           #so we'll append something to it 
            parsed_entry[column_index_to_shift] = remainder_col_replacement_char
        else:
            parsed_entry[column_index_to_shift] = column_vec[i]
        parsed_dataset.append(parsed_entry)
        i += 1
        
    return parsed_dataset



##Removes entire column from data if missing values are present
#Returns list of headers and dataset with appropriate columns removed
def removeMissingValCollumns(headers, data_set):
    missing_val_detected_collumncount_list = [[col_name, 0, i] for i, col_name in enumerate(headers)]
    #First find columns that have missing values
    indexes_of_missingval_columns = set()
    for entry in data_set:
        for i, column_val in enumerate(entry):
            # if (i in indexes_of_missingval_columns): #already know we are removing this column
            #     continue
            if column_val == '':
                indexes_of_missingval_columns.add(i)
                missing_val_detected_collumncount_list[i][1] = (missing_val_detected_collumncount_list[i][1]) + 1 #Keep track of collumns that have missing values 
                
    #Remove columns 
    parsed_data_set = []
    for entry in data_set:
        parsed_entry = [column_val for i, column_val in enumerate(entry) if (i not in indexes_of_missingval_columns)]
        parsed_data_set.append(parsed_entry)

    parsed_headers = [header_name for i, header_name in enumerate(headers) if (i not in indexes_of_missingval_columns)]
        
    #Logging
    missing_val_detected_collumncount_list_sorted = missing_val_detected_collumncount_list.copy()
    missing_val_detected_collumncount_list_sorted.sort(key = lambda x: x[1], reverse=True)
    print(f"Parsed dataset and removed collumns that have missing values")
    print(f"Columns And # Missing Values:\n{missing_val_detected_collumncount_list_sorted}\n~~~~~~~~~~~~~~~~~~~~~~~")
    
    return parsed_headers, parsed_data_set



#Finds the index of each specified column label within a list of given headers to a dataset
    #Removes the columns specified
    #If column cannot be found, it is simply ignored
def removeSelectColumnsByName(headers, data_set, columns_to_remove):
    headers_temp = headers
    data_set_temp = data_set
    for col_label in columns_to_remove:
        if (col_label in headers_temp):
            headers_temp, data_set_temp = removeSelectColumnByIndex(headers_temp, data_set_temp, headers_temp.index(col_label))
    
    return headers_temp, data_set_temp


#Returns headers and dataset after the column was removed
def removeSelectColumnByIndex(headers, data_set, col_index_to_remove): 
    print(f"Removing Column: {col_index_to_remove}: ({headers[col_index_to_remove]})")
    parsed_headers = [header for i, header in enumerate(headers) if (i != col_index_to_remove)]
    parsed_dataset = []

    parsed_entry = []
    for entry in data_set: 
        parsed_entry = [val for i, val in enumerate(entry) if (i != col_index_to_remove)]
        parsed_dataset.append(parsed_entry)

    return parsed_headers, parsed_dataset



##Identifies missing values and simply treats them as 0 
    #Also parse string values into numbers while we are at it (PUT THIS FEATUER SOME WHER ELSE LATER)
def zeroOutMissingValues(data_set):
    parsed_dataset = []
    for entry in data_set:
        entry_temp = []
        for i, column_val in enumerate(entry):
            if column_val == '':
                entry_temp.append(0)      
            else:
                entry_temp.append(column_val)

        parsed_dataset.append(entry_temp)

    return parsed_dataset



##Returns a vector of the data_set from a specific column
    #Can take index or column name as input
        #If Column name is specified, headers must be provided
def getSpecificColumn(data_set, column, headers = None):
    index_to_get = column
    if (isinstance(column, str) and (headers != None)): #Column specified by name (and headers were provided to match)
        if (column in headers):
            index_to_get = headers.index(column)
        else:
            print("Column name not found in provided headers list")
    elif (isinstance(column, str)):
        print("Column name specified but no headers are provided")

    if (index_to_get >= len(data_set[0])):
        print("Index/Column specified is out of bounds for dataset provided")

    column_vector = []
    for entry in data_set:
        column_vector.append(entry[index_to_get])
    
    return column_vector
    


##Identifies collumns with data that is a number but in str format and tries to convert them to numbers
    #Does not handle converting true string entries to numbers (ie: discrete features)
#Returns dataset containing numerical data
def strNumbersToNumerical(data_set):
    parsed_dataset = []
    for entry in data_set:
        entry_temp = []
        for i, column_val in enumerate(entry):
            try:
                if isinstance(column_val, str): #Try to convert it to a number
                    if("." in column_val):
                        number_val = float(column_val.replace(",", ""))
                    else:
                        number_val = int(column_val.replace(",", ""))
                    entry_temp.append(number_val)
                else:
                    entry_temp.append(column_val) 
            except ValueError: #Catch cannot convert errors and leave it as a string
                entry_temp.append(column_val) 

        parsed_dataset.append(entry_temp)

    return parsed_dataset