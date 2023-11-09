# CS4210Project

## Goal
- Create regression tree models to predict country CO2 emissions 
    - Attempt to predict with 1yr, 2yr, 5yr, and 10yr outlook.  

## Requirements
This project primarily requires the decision tree model components of sklearn libraries
> pip install scikit-learn 

## Quick-run
> python main.py 

## Saving A Decision Tree Model
Use pickle to save any models you create that have favorable performance 
> import pickle
> model_location = "regression_tree_model"
> pickle.dump(regr_1, open(model_location, "wb"))

## Loading a Decision Tree Model
Or use pickle to revisit any existing models for testing/inferencing
> import pickle
> model_location = "regression_tree_model"
> model = pickle.load(open(model_location, "rb"))

## Dataset
https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy