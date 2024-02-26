"""
Created on February 22, 2024

Written by: David Belman and Mahesh
Ananthakrishnan Rameshkumar.

The goal of this script is to extract data from the wildfire database
and properly prapare the data for use within our final project. The data we
are using in our project has been sourced from:

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
    original_dir = Dir.Get_current_directory()
    target_dir = 'Dataset'
    Dir.To_directory(target_dir)
    df = pd.read_csv(file_name) # Moving to the main branch (ECE-143-Wildfire-Project)
    Dir.To_directory(original_dir) # Returning to original dir

    # formatting additional the date and time columns if needed:
    df[['date', 'time']] = df['ex_fs_date'].str.split(' ', expand=True)
    # df.drop(['ex_fs_date'], axis=1, inplace=True)
    return df

def Get_all_df_columns(df, printing = False):
    """
    Returns a list of all columns within the dataframe.

    parameters:
        df - pd.DataFrame
            The dataframe whose columns we wish to get.

        printing - bool
            Decides whether we would like to see all columns printed in the
            terminal as well. Can be useful for troubleshooting the data frame
            you are currently working with.

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
    from an initial glance. Used for quick testing of the data set entries.

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
    column_names_list = list(df.columns)  # Get all column names directly from the DataFrame
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
    to create a lookup table for the fire names based on each fire's unique
    fire ID.

    Parameters:
        unfiltered_df pd.DataFrame
            The data frame that contains all original data.

    Returns:
         filtered_df - pd.DataFrame
            Data frame that will be used to create the lookup table.
    """
    assert unfiltered_df is not None, "Insert a dataframe."
    assert all(isinstance(column_name, str) for column_name in unfiltered_df.columns), "Not all column names of the dataframe are strings."

    columns_to_keep = ['fire_name', 'fire_number'] # can be adjusted if needed

    filtered_df = unfiltered_df[columns_to_keep]
    filtered_df = filtered_df[filtered_df['fire_name'].notna() & (unfiltered_df['fire_name'].str.strip() != "")]
    # filtered_df.set_index('fire_number', inplace=True)
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
    filtered_df = pd.DataFrame()

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
    # print("area in meters:", area_in_meters)
    radius = round(math.sqrt(area_in_meters/math.pi), digits_after_decimal)
    # print("radius we are returning is:", radius)
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

    Mymap = folium.Map(location=[latitude, longitude], zoom_start=zoom)

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




print("getting data...")
df = Get_all_data("af-historic-wildfires-1996-2005-data.csv")
print("finished getting data.\n\n")

print("getting column names:")
all_columns = Get_all_df_columns(df, True)
print("---------- done printing and getting column names ----------\n\n")

print("checking columns data:")
Checking_column_data(df, 5) # checking to see if some columns are in fact empty.
print("---------- done! ----------\n\n")



# from initial tests, these are columns that could be majority empty. Fire name is a special case and not included here
checking = ['industry_identifier_desc', 'true_cause', 'permit_detail_desc',
            'fire_fighting_start_date', 'fire_fighting_start_size', 'other_fuel_type',
            'other_fuel_type', 'to_fs_date', 'to_hectares', 'to_hectares']
# take out the hours from the fire_star_date column?
# further inspect 'det_agent_type' & 'det_agent' and see if we can decode it for the others.
# figure out what the fire class rating is
# ensure 'general_cause_desc' is all filled out.
# 'industry_identifier_desc' this is mainly empty as far as I can see. need to look into what the columns means.
# ensure that 'responsible_group_desc' is fully filled out. it Nan is present, put 'unknown' in its place
# ensure that 'activity_class' is fully filled out. it Nan is present, put 'unknown' in its place
# ensure that 'true_cause'  is fully filled out. it Nan is present, put 'unknown' in its place
# further look into 'permit_detail_desc' --> could we use this to track fires made by people without permite to be in the area?
# clean up 'fire_start_date' into a datetime column? Ensure the column is fully filled out.
#ensure 'discovered_date' is fully filled out.
# ensure 'reported_date' is fully filled out.
# ensure 'start_for_fire_date' is fully filled out. otherwise, put unknown.
# ensure 'fire_fighting_start_date' is fully filled out. otherwise, put unknown.
# ensure 'fire_fighting_start_size' is fully filled out. otherwise, make it nan.
# ensure 'initial_action_by' is filled out. otherwise, put unknown.
# ensure 'fire_type' is fully filled out. otherwise, put unknown.
# not sure if 'fire_position_on_slope' is needed. ask mahesh about deleting it.
# ensure 'weather_conditions_over_fire' is fully filled out. otherwise, put unknown.
# ensure 'fuel_type' is fully filled out. otherwise, put unknown.
# ensure 'other_fuel_type' is fully filled out. if nan, put unknown.
# look into what 'bh_fs_date' is. determine if it's something we think we can delete.
# continue working on the rest of the columns, starting with bh_hectares.


temp = pd.DataFrame()
temp = Create_df_with(df, checking)
Checking_column_data(temp, 3)

names = Get_valid_fire_names_df(df)
print("\nfire names and their fire number:\n", names)

filtered_df = Get_only_complete_data(df)

#testing the burn area map:
hectares = 1
print("hectares:", hectares)
radius = Get_burn_area_radius(hectares)
print("radius:", radius, "m")
displaying_burn_area(32.8812, -117.2344, radius)
