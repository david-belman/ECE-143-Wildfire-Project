"""
Created on March 1, 2024

Written by: Jacob Brown and Aiden Rosen.

The goal of this script is to provide functions to perform analysis and visualize those analysis in order to gain new insights from dataset. The funstions we write here will be used in results.ipynb The data we
are using in our project has been sourced from:
https://open.alberta.ca/opendata/wildfire-data-1996-2005
"""

from Data_Extracting_and_Cleaning.Utils import Directory_utils as Dir
import pandas as pd

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
"""Start of the Funtion Definitions:"""

