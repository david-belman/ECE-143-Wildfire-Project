# ECE-143-Wildfire-Project

The Group Repository containing everyone's code.

**team members:** David Belman, Aiden Rosen, Mahesh  
Ananthakrishnan Rameshkumar, Boran Jia, & Jacob Brown  

## Objective  

The Purpose of this project is to Perform comprehensive analysis on forest fires, analyzing cause, size of fire, seasonal  effects, spatial effects and terrain effects.  

## Extracting and Cleaning Data

 -- fill this in --

    The fire year can be fiscal or calendar year so it has been dropped. 

    Kept the calendar year for easier grouping of fires in a year

    Converted all the dates to datetime types from string

    The start_for_fire_date and fire_start_date are the same hence the start_for_fire_date
    is dropped

    For the weather column replaced nan with unknown

    In the case of the general_cause_desc it has been mapped to the values as specified
    But in case it is zero the industry can be checked using the industry_identifier_desc
    which is nan for all gen_desc values except 0. 
    
    For the responsible group there are a few categories that dont have a specified 
    code and some have multiple codes so coding it might lead to ambiguities so left
    as is.

    For the true cause the nan value has been mapped to -1

    The permit_detail_desc is entirely null so that column is dropped 
    
    For the fuel_type column and other_fuel_type_column if both are null it is set to 
    unknown. If the fuel_type is null it is set to "Other Fuel" and if other_fuel_type
    is null it is set to "Known fuel".

    There are few columns that rarely have non-nan values, it might be reasonable 
    to exclude those rows as they might not have much of an impact.


## Analysis and Visualization for Obtaining Statistics

 -- fill this in --

## Making Predictions

We apply three machine learning algorithms to predict the size of fire
Support Vector Machines
Gradient Boosting Regressor
Random Forest

Selection of feature variables and target variables
Random Forest & Gradient Boosting Regressor：
  X: fire_year， fire_location_latitude，
 fire_location_longitude， fuel_type
  Y：assessment_hectares

Support Vector Machines
 X：numeric features 
(i.e. features with data type float64 or int64)
Y：assessment_hectares

Model evaluation criteria
Mean square error (MSE)
coefficient of determination (R²)

