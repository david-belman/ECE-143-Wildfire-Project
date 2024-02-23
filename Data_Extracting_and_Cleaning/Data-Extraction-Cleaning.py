"""
Created on February 22, 2024

Written by: David Belman and Mahesh
Ananthakrishnan Rameshkumar.

The goal of this script is to extract data from the wildfire database
and properly prapare it for use within our project
"""

import pandas as pd
import numpy as np
# ensure to include Pyarrow when installing pandas(?):
"""
DeprecationWarning: 
    Pyarrow will become a required dependency of pandas in the next major release of pandas (pandas 3.0),
    (to allow more performant data types, such as the Arrow string type, and better interoperability with other libraries)
    but was not found to be installed on your system.
    If this would cause problems for you,
    please provide us feedback at https://github.com/pandas-dev/pandas/issues/54466
"""
# import Pyarrow

from Utils import Directory_utils as Dir

def Get_all_data(file_name):
    """
    Creates a dataframe that contains all data from our database.
    """

    assert isinstance(file_name, str), "database filename must be a string."
    original_dir = Dir.Get_current_directory()
    target_dir = 'Dataset'
    Dir.To_directory (target_dir)
    df = pd.read_csv(file_name) # Moving to the main branch (ECE-143-Wildfire-Project)
    Dir.To_directory (original_dir) # Returning to original dir

    # df.drop('fire_name', axis=1, inplace=True) #removing since it is in face empty

    # formatting the date and time of fires properly:
    df[['date', 'time']] = df['ex_fs_date'].str.split(' ', expand=True)
    # df.drop(['ex_fs_date'], axis=1, inplace=True)
    return df


def Checking_column_data(df, stopping_point = 3):
    """
    currently using this to check if certain columns are mainly
    empty or not off of first glance.

    Temporarily used so that we do not actually print out all of
    the data now.
    """
    column_names_list = list(df.columns)  # Get all column names directly from the DataFrame
    for name in column_names_list:
        print(f"Column: '{name}'")
        for index, value in enumerate(df[name]):
            if index < stopping_point:
                print("\t", value)
            else:
                break


def Get_all_df_columns(df):
    """
    Returns a list of all columns within the dataframe.
    """
    assert isinstance (df, pd.DataFrame), "Input must be a pandas dataframe."
    assert all(isinstance(name, str) for name in df.columns), "Dataframe column names must be of type str."

    total_columns = Get_number_of_df_columns(df)
    half_columns = total_columns // 2
    # len_half_columns = len(total_columns // 2)
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
    return list(df.columns)

def Get_number_of_df_columns(df):
    """
    Returns the number of columns in the dataframe.
    """
    return len(df.columns)

def Create_df_with(df, column_name_list):

    """
    Allows us to create a dataframe with any columns we wish.

    order in which column names are in the lsit (from left to right) is
    the order in which the columns are inputted into the dataframe.
    """
    assert df is not None, "No df was entered."
    assert column_name_list is not None, "No column_names were entered"
    assert column_name_list is not [], "column_names_list is empty."
    assert isinstance(df, pd.DataFrame), "database filename must be a string."
    assert all(isinstance(name, str) for name in df.columns), "Dataframe column names must be of type str."
    assert isinstance(column_name_list, list), "Desired column names must be entered in as a list."
    assert all(isinstance(names, str) for names in column_name_list), "Column names must be strings."
    assert all(name in df.columns for name in column_name_list), \
    (f"At least one name in {column_name_list} does not exist within the DataFrame columns: "
     f"{set(column_name_list) - set(df.columns)}.")

    new_df = pd.DataFrame()

    for name in column_name_list:
        new_df[name] = df[name]

    return new_df

def Get_valid_fire_names_df(unfiltered_df, fire_number = 0):
    """
    gives us a df that only contains entires that have names for fires.
    """
    filtered_df = df[df['fire_name'].notna() & (df['fire_name'].str.strip() != "")]
    return filtered_df

def Get_only_complete_data(unfiltered_df):
    """
    Returns only rows that are not missing one piece of data. Does not remove columns.
    """
    columns_list = Get_all_df_columns(unfiltered_df)
    filtered_df = pd.DataFrame()

    # Create a mask for rows with complete data in all columns
    row_mask = unfiltered_df[columns_list].notna().all(axis=1)

    # Filter the DataFrame based on the mask
    filtered_df = unfiltered_df[row_mask]
    return filtered_df


def stop():
    """
    used only for testing to quickly add a stopping point. Delete when testing is over.
    """
    exit(1)



df = Get_all_data("af-historic-wildfires-1996-2005-data.csv")


# Checking_column_data(df, 10) # checking to see if some columns are in fact empty.
print("---------- done! ----------")


temp = pd.DataFrame()
# from initial tests, these are columns that could be majority empty. Fire name is a special case and not included here
checking = ['industry_identifier_desc', 'permit_detail_desc', 'fire_fighting_start_date',
 'fire_fighting_start_size', 'other_fuel_type', 'other_fuel_type', 'to_fs_date',
 'to_hectares', 'to_hectares']

temp = Create_df_with(df, checking)
# Checking_column_data(temp, 10)

Get_valid_fire_names_df(df)


filtered_df = Get_only_complete_data(df)




