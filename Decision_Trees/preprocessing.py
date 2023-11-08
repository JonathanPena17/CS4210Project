import time


##Functions for preprocessing data
    #(global-data-on-sustainable-energy)


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
    print(f"Columns And # Missing Values:\n{missing_val_detected_collumncount_list}\n~~~~~~~~~~~~~~~~~~~~~~~")
    
    return parsed_headers, parsed_data_set




def removeSelectColumnsByName(headers, data_set, columns_to_remove):

    return 0


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
            elif isinstance(column_val, str): #Try to convert it to a number
                if("." in column_val):
                    entry_temp.append(float(column_val.replace(",", "")))
                else:
                    entry_temp.append(int(column_val.replace(",", "")))
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
    