"""
Created on February 22, 2024

Written by: David Belman and Mahesh
Ananthakrishnan Rameshkumar.

The goal of this script is to extract data from the wildfire database
and properly prapare it for use within our project
"""

import pandas as pd
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

def Extract_data(fname):
    # assertations
    assert isinstance(fname, str), "database filename must be a string."


    # cleaning the data (if needed):

    # something to consider: if a datapoint is non-existant, make it NaN

    # sorting the data


Extract_data("Dataset/af-historic-wildfires-1996-2005-data.csv")