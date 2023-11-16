# Import the necessary modules and libraries
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import csv
import preprocessing
import time 
import random
import sklearn.model_selection as skmodel
import os 

##Get Data
data_file = open("archive\\global-data-on-sustainable-energy (1).csv", "r")
csv_obj = csv.reader(data_file)

headers = []
data_entries = []
for i, line in enumerate(csv_obj):
    if (i == 0):
        headers = line
    else:
        data_entries.append(line)
#print(list(enumerate(headers)))
#print(f"Example entry (before parsing):\n{data_entries[0]}")
#print(len(data_entries))


##Parse Data
    #separate countries to perform label shifting on them
country_list, list_of_country_data_sublists = preprocessing.separateCountries(data_entries)
# print(country_list[0])
# print([entry[0] for entry in list_of_country_data_sublists[0]]) #list of years from Afghanistan

    #For each country, shift it's CO2 Class label up by numbers of years we want the model to predict by. 
        #Keep in mind this reduces the total amount of instances we will have, since later years have no data from future to match with, so these rows should be discarded 
class_label_index = headers.index('Value_co2_emissions_kt_by_country' ) -1 # -1 since we removed first column (countries) from the data, and headers hasn't been updated to reflect that  
year_prediction_window = 1 #n = number of years the instance data is offset by compared to its class label
parsed_data = []
unlabled_entries = [] #Remainder entries that end up without a class label due to label shift step (may be useful later for inferencing)

for country_entries in list_of_country_data_sublists: #Shift CO2 entries by country 
    shifted_entries = preprocessing.shiftColumnDataUp(country_entries, class_label_index, year_prediction_window, remainder_col_replacement_char = '')
    unlabled_entries.extend([entry for i, entry in enumerate(shifted_entries) if (i >= len(shifted_entries) - year_prediction_window)])
    parsed_data.extend([entry for i, entry in enumerate(shifted_entries) if (i < len(shifted_entries) - year_prediction_window)])

    #Checking if shift was performed correctly 
#print(list_of_country_data_sublists[0][0][12])
#print(list_of_country_data_sublists[0][0 + year_prediction_window][12])
#print(parsed_data[0][12]) 


##Parse data for training
    #Removing country from data set
parsed_data = parsed_data #country already removed in previous step 
parsed_headers = headers[1:] 
# unlabled_entries = unlabled_entries #parse unlabled entries if we want to do something with them later for inferencing

    #Remove select collumns based on our choice 
# unwanted_columns_by_name = ["Latitude", "Longitude"]
# parsed_headers, parsed_data = preprocessing.removeSelectColumnsByName(parsed_headers, parsed_data, unwanted_columns_by_name)

    ##Handle Missing Values
    #Remove collumns with missing values
# parsed_headers, parsed_data = preprocessing.removeMissingValCollumns(parsed_headers, parsed_data) #Right now removes too may collumns, but good for logging which columns have missing vals 
    #OR handle missing values by leaving them as 0
parsed_data = preprocessing.zeroOutMissingValues(parsed_data)

    #Ensure all data (that should be a number) is in numerical format 
parsed_data = preprocessing.strNumbersToNumerical(parsed_data)


##Extract Label from data 
class_label = 'Value_co2_emissions_kt_by_country' #also known as column 12 
class_vector = preprocessing.getSpecificColumn(parsed_data, class_label, parsed_headers)
parsed_headers, parsed_data_no_class = preprocessing.removeSelectColumnByIndex(parsed_headers, parsed_data, parsed_headers.index(class_label))

#print(len(parsed_data_no_class)) #Data and Class sizes match 
#print(len(class_vector))

#Split data into training and testing sets
#Test size = x% of data that is used for testing
#Random_state is a number that keeps the same columns picked each time. it can be any number
#but keeping it the same will keep the same split
X_train, X_test, y_train, y_test = skmodel.train_test_split(parsed_data_no_class, class_vector, test_size=0.1, random_state=42)


##Fit regression model 
#uncomment this and comment out skmodel.train_test_split line if not using training/testing splits
#X_train = parsed_data_no_class
#y_train = class_vector
#if you input the same number it creates the same decision tree each time. no need to save and load, 
#unless training takes a long time
regr_1 = DecisionTreeRegressor(max_depth=20, random_state=10) #play with depth => max number of features it will integrate into decision paths
#regr_1 = RandomForestRegressor(n_estimators=100, random_state=32)
regr_1.fit(X_train, y_train) 


## Predict
instance_index_random_pick = random.randint(0, len(X_test)-1)
#X_test = parsed_data_no_class[instance_index_random_pick] #use a random entry from the training data... (because lazy)
y_1 = regr_1.predict([X_test[instance_index_random_pick]])


##Compare
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nUsing A Random Training Instance For Testing")
print(f"{year_prediction_window} Year Prediction For CO2 Output: {y_1[0]}")
print(f"Ground truth CO2 From Instance Tested: {class_vector[instance_index_random_pick]}")


##Save Model On Disk
# import pickle
# model_location = "regression_tree_model"
# # pickle.dump(regr_1, open(model_location, "wb"))
# model = pickle.load(open(model_location, "rb"))