"""
Created on March 1, 2024

Written by: Jacob Brown and Aiden Rosen.

The goal of this script is to provide functions to perform analysis and visualize those analysis in order to gain new insights from dataset. The funstions we write here will be used in results.ipynb The data we
are using in our project has been sourced from:
https://open.alberta.ca/opendata/wildfire-data-1996-2005
"""

from Data_Extracting_and_Cleaning.Utils import Directory_utils as Dir
import pandas as pd
import matplotlib.pyplot  as plt
import numpy as np
trueCauseMap = { 'Abandoned Fire':1, 'Burning Substance':7, 'Unsafe Fire':2, 
                    'Arson Suspected':12, 'Insufficient Buffer':5, 'Hot Exhaust':8, 
                    'Unpredictable Event':9, 'Unattended Fire':4, 'Arson Known':10, 
                    'High Hazard':11, 'Insufficient Resources':3, 'Flammable Fluids':6, 
                    'Permit Related':0}  
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

def plot_graph_of_series(series, graph_type = "pie", title = "",axes = ["",""] ):
    """
    Creates a graph of the given pandas series count

    Parameters:
    ------------
        series - pd.series
            Should be a pandas series containing names on the left side and a count on the right side
        Graph_type - str
            Type of graph you want. Currently pie or bar
        title - str
            TItle of the graph
        Axis - list of str
            The titles of the axes such that the correspond to [x,y]
    Returns:
    ----------
        None but prints a graph of desired type
    """
    assert isinstance(series, pd.Series), "series input must be a pandas series datatype"
    assert isinstance(graph_type, str), "graph_type input must be a str"
    assert isinstance(title, str), "title input must be a str"
    assert isinstance(axes, list) and len(axes)>0 and all([isinstance(i,str) for i in axes]), "axes input must be a list of string"
    fig, ax = plt.subplots()

    
    match graph_type:
        case "pie":
            '''wedgeprops={"linewidth": 1, "edgecolor": "white"},'''
            ax.pie(series.values, radius=3, center=(4, 4),  
                labels = series.index, labeldistance = 1.3, autopct='%1.1f%%')
        case "bar":
            ax.bar(series.index, series.values, width=1, edgecolor="white", linewidth=0.7)
            ax.set_xlabel(axes[0])
            ax.set_ylabel(axes[1])
    ax.set_title(title, pad =8.0)