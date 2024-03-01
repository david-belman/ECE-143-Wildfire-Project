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
    
    I feel creating a lookup table would compromise the ease of access
    For the responsible group there are a few categories that dont have a specified 
    code and some have multiple codes so coding it might lead to ambiguities so left
    as is.

    For the true cause the nan value has been mapped to -1

    The permit_detail_desc is entirely null so that column is dropped 

    For firefighting_start_size the nan values are replaced with zero as they have 
    same effect. But need to discuss with the team.

    For the fuel_type column and other_fuel_type_column if both are null it is set to 
    unknown. If the fuel_type is null it is set to "Other Fuel" and if other_fuel_type
    is null it is set to "Known fuel".

    There are few columns that rarely have non-nan values, it might be reasonable 
    to exclude those rows as they might not have much of an impact.

    Two remaining tasks that might need consulting with the team would be:
        * Figuring out how to handle null values for dates possible 
          solutions are using a default time value outside the dataset
          range or calculating the time based on some average.
        * Need to figure out what the bh_fs_date and to_fs_date are.
        * Then for other_fuel_type some cleaning is required. But I
          feel this would take more time and Mahesh can help with this analysis.

## Analysis and Visualization for Obtaining Statistics

 -- fill this in --

## Making Predictions

 -- fill this in --
