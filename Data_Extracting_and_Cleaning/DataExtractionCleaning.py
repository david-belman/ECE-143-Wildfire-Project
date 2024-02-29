"""
Created on February 22, 2024

Written by: David Belman and Mahesh Ananthakrishnan Rameshkumar.

The goal of this script is to extract data from the wildfire database
and properly prapare the data for use within our final project. The data we
are using in our project has been sourced from:
https://open.alberta.ca/opendata/wildfire-data-1996-2005
"""

from Utils import Directory_utils as Dir
import pandas as pd
import math
import folium

# ensure to include Pyarrow when installing pandas(?):
"""
DeprecationWarning: 
    Pyarrow will become a required dependency of pandas in the next major release 
    of pandas (pandas 3.0), (to allow more performant data types, such as the Arrow 
    string type, and better interoperability with other libraries) but was not found 
    to be installed on your system. If this would cause problems for you, please 
    provide us feedback at https://github.com/pandas-dev/pandas/issues/54466
"""
# import Pyarrow

def Get_all_data(file_name):
    """
    Creates a dataframe that contains all data from our database.

    parameter:
        file_name - str
            The raw filename from 'Dataset/' directory

    Returns:
        df - pd.DataFrame
            Data frame that we can now use for analysis.
    """
    assert isinstance(file_name, str), "database filename must be a string."

    #this section automatically pulls the data from 'file_name' that is stored in 'Dataset/' and returns to the
    original_dir = Dir.Get_current_directory()
    target_dir = 'Dataset'
    Dir.To_directory(target_dir)
    df = pd.read_csv(file_name)
    Dir.To_directory(original_dir)

    df = df.drop( columns= ['fire_year', 'permit_detail_desc'] )
    dateColumns = [ 'assessment_datetime', 'fire_start_date','discovered_date', 
                   'reported_date', 'start_for_fire_date', 'fire_fighting_start_date',
                    'bh_fs_date', 'uc_fs_date', 'ex_fs_date', 'to_fs_date' ]
    df[dateColumns] = df[dateColumns].apply( pd.to_datetime )

    # Filling out the nan values
    df['fire_start_date'].fillna( df['start_for_fire_date'], inplace= True )
    df['det_agent_type'].fillna("Unknown", inplace= True)
    df['det_agent'].fillna("Unknow", inplace= True)
    df['fire_fighting_start_size'].fillna(0, inplace= True)
    df['true_cause'].fillna( -1, inplace= True )
    df['fire_position_on_slope'].fillna( "Unknown", inplace= True )
    df['initial_action_by'].fillna( "Unknown", inplace= True )
    df['industry_identifier_desc'].fillna("Non Industrial / Other Industry")
    df['responsible_group_desc'].fillna( "Unknown", inplace= True )
    df['activity_class'].fillna("Unknown", inplace= True)
    df['weather_conditions_over_fire'].fillna( "Unknown", inplace= True )

    # Dropping this column as it seems to be redundant from the dataset dictionary
    df = df.drop(columns= ['start_for_fire_date'])

    # Coding the general cause according to the data dictionary
    genCauseMap = { "Other Industry":0, "Lightning":1, "Resident":2, 
                 "Forest Industry":3, "Railroad":4, "Prescribed Fire":5, 
                 "Recreation":6, "Incendiary":7, "Miscellaneous Known":8,
                 "Power Line Industry":9, "Oil & Gas Industry":10, "Restart":11,
                 "Undetermined":12}
    df["general_cause_desc"] = df["general_cause_desc"].map( genCauseMap )

    # Coding true cause
    trueCauseMap = { 'Abandoned Fire':1, 'Burning Substance':7, 'Unsafe Fire':2, 
                    'Arson Suspected':12, 'Insufficient Buffer':5, 'Hot Exhaust':8, 
                    'Unpredictable Event':9, 'Unattended Fire':4, 'Arson Known':10, 
                    'High Hazard':11, 'Insufficient Resources':3, 'Flammable Fluids':6, 
                    'Permit Related':0}  
    df['true_cause'] = df['true_cause'].map(trueCauseMap)
    df['fire_type'] = df['fire_type'].str.strip()
    df['fire_type'].replace( '', 'Unknown', inplace= True )

    # Replacing nans in fuel_type and other_fuel_type with appropriate values.
    nullRow = df[ df['fuel_type'].isnull() & df['other_fuel_type'].isnull() ].index
    df.loc[nullRow, ['fuel_type', 'other_fuel_type']] = "Unknown"
    nullFuelRow = df[ df['fuel_type'].isnull() & df['other_fuel_type'].notnull() ].index
    df.loc[nullFuelRow, ['fuel_type']] = "Other Fuel"
    nullOtherRow = df[ df['fuel_type'].notnull() & df['other_fuel_type'].isnull() ].index
    df.loc[nullOtherRow, ['other_fuel_type']] = "Known Fuel"
    
    return df

def Get_all_df_columns(df, printing = False):
    """
    Returns a list of all columns within the dataframe.

    parameters:
        df - pd.DataFrame
            The dataframe whose columns we wish to get.

        printing - bool
            Decides whether we would like to see all columns printed in the
            terminal as well. Can be useful for ensuring the data frame
            columns you are currently working with has the columns you expect
            it to have.

    Returns:
        df_columns_list - list
            A list containing all columns from the entered dataset (df).
    """
    assert isinstance (df, pd.DataFrame), "Input must be a pandas dataframe."
    assert all(isinstance(name, str) for name in df.columns), "Dataframe column names must be of type str."

    if printing:
        total_columns = Get_total_number_of_df_columns(df)
        half_columns = total_columns // 2
        left_columns = df.columns[:half_columns]
        right_columns = df.columns[half_columns:]
        column_number = 0
        shift = 40
        title = f"All column names (total columns: {total_columns})"
        line = "--" * len(title)
        print(title.center(2*shift))
        print(line.center(2*shift))
        for left_column, right_column in zip(left_columns, right_columns):
            if column_number < 10:
                print(f"Column {column_number}: {left_column.ljust(shift)}"
                      f" Column {column_number + half_columns}: {right_column.rjust(0)}")
            else:
                print(
                    f"Column {column_number}: {left_column.ljust(shift - 1)} Column {column_number + half_columns}: {right_column.rjust(0)}")
            column_number += 1

        if total_columns % 2 == 1:
            column_name = df.columns[column_number + half_columns]
            column_and_number = "Column " + str(column_number + half_columns)
            offset = 20
            print(f"{column_and_number.rjust(shift + offset)}: {column_name}")
    df_columns_list = list(df.columns)
    return df_columns_list

def Get_total_number_of_df_columns(df):
    """
    Returns the number of columns in the dataframe.

    Parameter:
        df - pd.DataFrame
            The dataframe inputted.

    Returns:
        len(df.columns) - int
            The number of columns in the dataframe
    """
    return len(df.columns)

def Checking_column_data(df, stopping_point = 3):
    """
    currently using this to check if certain columns are mainly empty or not
    from an initial glance. Used for quick testing of the first the data set entries.

    Parameters:
        df - pd.DataFrame
            Data frame inputted.

        stopping_point - int
            The number of rows we wish to check in each column.

    Returns: None
    """
    assert isinstance(df, pd.DataFrame), "Input must be a pandas dataframe."
    assert all(isinstance(name, str) for name in df.columns), "Dataframe column names must be of type str."
    assert isinstance(stopping_point, int) & stopping_point > 0, "Stopping_point must be an integer and > zero."

    # Get all column names directly from the DataFrame
    column_names_list = list(df.columns)
    for name in column_names_list:
        print(f"Column: '{name}'")
        for index, value in enumerate(df[name]):
            if index < stopping_point:
                print("\t", value)
            else:
                break

def Create_df_with(unfiltered_df, column_name_list):
    """
    Allows us to create a dataframe with any columns we wish. The order in which
    column names are within the list (from left to right) is the order that the
    columns are inputted into the dataframe.

    Parameters:
        unfiltered_df - pd.DataFrame
            The Dataframe that we will be filtering our desired data from.

        column_name_list - list
            The list of column names that we will be extracting from unfiltered_df.
            These column names will also be the names of the columns in the new dataset.

    Returns:
        new_df - pd.DataFrame
            The new dataset that has only the desired columns.
    """
    assert unfiltered_df is not None, "No df was entered."
    assert column_name_list is not None, "No column_names were entered"
    assert column_name_list is not [], "column_names_list is empty."
    assert isinstance(unfiltered_df, pd.DataFrame), "database filename must be a string."
    assert all(isinstance(name, str) for name in unfiltered_df.columns), "Dataframe column names must be of type str."
    assert isinstance(column_name_list, list), "Desired column names must be entered in as a list."
    assert all(isinstance(names, str) for names in column_name_list), "Column names must be strings."
    assert all(name in unfiltered_df.columns for name in column_name_list), \
    (f"At least one name in {column_name_list} does not exist within the DataFrame columns: "
     f"{set(column_name_list) - set(unfiltered_df.columns)}.")

    new_df = pd.DataFrame()
    for name in column_name_list:
        new_df[name] = unfiltered_df[name]

    return new_df

def Get_valid_fire_names_df(unfiltered_df = None):
    """
    Extracts the existing fire names from the dataframe. Plans are to use it
    to create a lookup dataframe for the fire names based on each fire's unique
    fire ID.

    Parameters:
        unfiltered_df pd.DataFrame
            The data frame that contains all original data.

    Returns:
         filtered_df - pd.DataFrame
            Data frame that will be used to create the lookup table.
    """
    assert unfiltered_df is not None, "Insert a pandas dataframe."
    assert all(isinstance(column_name, str) for column_name in unfiltered_df.columns), "Not all column names of the dataframe are strings."

    columns_to_keep = ['fire_name', 'fire_number'] # can be adjusted if needed

    filtered_df = unfiltered_df[columns_to_keep]
    filtered_df = filtered_df[filtered_df['fire_name'].notna() & (unfiltered_df['fire_name'].str.strip() != "")]
    return filtered_df

def Get_only_complete_data(unfiltered_df):
    """
    Returns only rows that are not missing one piece of data. Will become more
    useful once we are able to filter and clean all data.

    Parameter:
        unfiltered_df - pd.DataFrame
            the unfiltered data frame that will be purged of complete columns of data.

    Returns:
        filtered_df - pd.DataFrame
            Contains only rows that are not missing any data. When a value is 'NaN',
            the value is set to zero.
   """
    columns_list = Get_all_df_columns(unfiltered_df)

    # Create a mask for rows with complete data in all columns
    row_mask = unfiltered_df[columns_list].notna().all(axis=1)

    # Filter the DataFrame based on the mask
    filtered_df = unfiltered_df[row_mask]
    return filtered_df

def Get_burn_area_radius(hectares = None):
    """
    Returns general burn radius of a fire (in meters).

    Parameter:
        hectares - float
            The area that has been affected by the fire

    Returns:
        radius - float
            A circle's radius whose area would cover the same
            area as the affected area in hectares.
    """
    # NOTE: Converting hectares to meters squared is: 1 hectare = 10, 000 meters squared

    digits_after_decimal = 4
    area_in_meters = round(hectares * 10000, digits_after_decimal)
    radius = round(math.sqrt(area_in_meters/math.pi), digits_after_decimal)
    return radius

def displaying_burn_area(latitude=None, longitude=None, radius=None, zoom = 20, plotting_circle = True):
    """
    Creates a .html map that shows the general burn area. Shown by a circle.

    Parameters:
    ------------
        latitude - float
            Can be either positive or negative.
        longitude - float
            Can be either positive or negative.
        radius - float
            The radius of that the fire covers in meters. Obtain this by first getting return
            value from Get_burn_area_radius().
    Returns:
    ----------
        burn_area - .html file
            You can open the file called 'burn_area.html' that is created in your current
            working directory.
    """
    assert latitude is not None and longitude is not None, "Must provide both a latitude and longitude."
    assert radius is not None and radius > 0, "Must provide a radius parameter greater than 0."
    isinstance(zoom, (int, float)), "Must provide a valid zoom value."
    assert isinstance(plotting_circle, bool), "Must provide a bool for plotting_circle."

    # this section aims to properly auto adjust the zoom when creating burn_area
    attenuation = 1
    max_zoom = 20
    if plotting_circle:
        if radius < 30:
            zoom = max_zoom
        elif 30 < radius < 38:
            zoom = 18.5
        else:
            temp = radius - 30
            while temp > 0:
                zoom -= 0.5/attenuation
                temp -= 10
                attenuation += 0.3
                zoom = round(zoom, 5)
            zoom = min(zoom, 18.35)

    # create the map
    Mymap = folium.Map(location=[latitude, longitude], zoom_start=zoom)

    # creating the burn area circle
    if plotting_circle:
        folium.Circle(
            location=[latitude, longitude],
            radius=radius,
            color='grey',
            fill=True,
            fill_color='red',
            fill_opacity=0.2
        ).add_to(Mymap)

    Mymap.save('burn_area.html')

def stop():
    """
    used only for testing to quickly add a stopping point. Delete when testing is over.
    """
    exit(1)


#testing the functions written above:
print("getting data...")
df = Get_all_data("af-historic-wildfires-1996-2005-data.csv")
print("finished getting data.\n\n")

print("getting column names:")
all_columns = Get_all_df_columns(df, True)
print("---------- finnished printing and getting column names ----------\n\n")

print("checking columns data:")
Checking_column_data(df, 5)
print("---------- finished checking columns data! ----------\n\n")


# from initial tests, these are columns that could be majority empty. Fire name is a special case and not included here
checking = ['industry_identifier_desc', 'true_cause',
            'fire_fighting_start_date', 'fire_fighting_start_size', 'other_fuel_type',
            'other_fuel_type', 'to_fs_date', 'to_hectares', 'to_hectares']

print("creating a filtered df:")
temp = Create_df_with(df, checking)
Checking_column_data(temp, 3)
print("---------- finished creating a filtered df! ----------\n\n")

print("getting valid fire names:")
names = Get_valid_fire_names_df(df)
print("\nfire names and their fire number:\n", names)
print("---------- finished getting valid fire names! ----------\n\n")

print("getting filtered df:")
filtered_df = Get_only_complete_data(df)
print("---------- finished getting filtered df! ----------\n\n")

#testing the burn area map:
hectares = 100
print("hectares:", hectares)
radius = Get_burn_area_radius(hectares)
print("radius:", radius, "m")
displaying_burn_area(32.8812, -117.2344, radius)

