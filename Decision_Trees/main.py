# Import the necessary modules and libraries
from sklearn.tree import DecisionTreeRegressor
import csv
import preprocessing
import time 
import random

##Get Data
data_file = open("archive/global-data-on-sustainable-energy (1).csv", "r")
csv_obj = csv.reader(data_file)

headers = []
data_entries = []
for i, line in enumerate(csv_obj):
    if (i == 0):
        headers = line
    else:
        data_entries.append(line)
print(headers)
print(f"Example entry (before parsing):\n{data_entries[0]}")
print(len(data_entries))


##Parse Data
    #separate countries for usage later
country_list, list_of_country_data_sublists = preprocessing.separateCountries(data_entries)
# print(country_list[0])
# print([entry[0] for entry in list_of_country_data_sublists[0]]) #list of years from Afghanistan


##Parse data for training
    #Removing country from data set
parsed_data = [entry[1:] for entry in data_entries] 
parsed_headers = headers[1:] 


    #Remove select collumns based on our choice 
# unwanted_columns_by_name = ["Latitude", "Longitude"]
# parsed_headers, parsed_data = preprocessing.removeSelectColumnsByName(parsed_headers, parsed_data, unwanted_columns_by_name)

    ##Handle Missing Values
    #Remove collumns with missing values
# parsed_headers, parsed_data = preprocessing.removeMissingValCollumns(parsed_headers, parsed_data) #Right now removes too may collumns, but good for logging 
    #OR handle missing values by leaving them as 0
parsed_data = preprocessing.zeroOutMissingValues(parsed_data)


##Extract Label from data 
class_label = 'Value_co2_emissions_kt_by_country' #also known as column 12 
class_vector = preprocessing.getSpecificColumn(parsed_data, class_label, parsed_headers)
parsed_headers, parsed_data_no_class = preprocessing.removeSelectColumnByIndex(parsed_headers, parsed_data, 12)

# print(class_vector[0:10])
# print(parsed_headers)
# print([entry[12] for entry in parsed_data[0:10]])

print(len(parsed_data_no_class))
print(len(class_vector))


##Fit regression model
X = parsed_data_no_class
y = class_vector
regr_1 = DecisionTreeRegressor(max_depth=10) #play with depth => max number of features it will integrate into decision paths
# regr_2 = DecisionTreeRegressor(max_depth=5)
regr_1.fit(X, y)
# regr_2.fit(X, y)


## Predict
instance_index_random_pick = random.randint(0, len(parsed_data_no_class)-1)
X_test = parsed_data_no_class[instance_index_random_pick] #use a random entry from the training data... (because lazy)
y_1 = regr_1.predict([X_test])
# y_2 = regr_2.predict(X_test)


##Compare
print(f"Prediction For CO2 Based On Immediate Data: {y_1[0]}")
print(f"Ground truth CO2 From Instance Tested: {class_vector[instance_index_random_pick]}")

