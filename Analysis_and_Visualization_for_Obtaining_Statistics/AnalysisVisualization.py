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
#import altair as alt
#from altair import Chart
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
            Type of graph you want. Currently pie, bar, or barh
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
            ax.pie(series.values, radius=3, center=(4, 4),  
                labels = series.index, labeldistance = 1.3, autopct='%1.1f%%')
        case "bar":
            plt.bar(range(len(series.index)), series.values, width=1, edgecolor="white", linewidth=0.7)
            plt.xticks(range(len(series.index)), series.index, rotation='horizontal')
            ax.set_xlabel(axes[0])
            ax.set_ylabel(axes[1])
        case "barh":#horizontal bar graphs
            plt.barh(series.index, series.values, edgecolor="white")
            #plt.xticks(range(len(series.index)), series.index, rotation='vertical')
            ax.set_xlabel(axes[0])
            ax.set_ylabel(axes[1])
    ax.set_title(title, pad =8.0)




def get_operation_of_series_based_on_another_series(dataframe, column_names, op="mean", threshold= None):
    """
    Finds the operation of average_series corresponding to the indices in value_count. Current Operations are mean, sum, and norm(normalize)

    Parameters:
    ------------
        dataframe - pd.Dataframe
            a dataframe of the dataset
        column_names - list of str
            The titles of the columns such that the correspond to [the column you want to find the average of the values in here, the column containing the numbers to average]
        op - str
            Type of operation you want performed
        threshold - Float
            The lowest value before we cut it out of the output
    Returns:
    ----------
        a pd.Series that contains the names in the first column as an index and the operation in the value column 
    """
    assert isinstance(dataframe, pd.DataFrame), "dataframe input must be a pandas Dataframe datatype"
    assert isinstance(column_names, list) and len(column_names) == 2 and all([isinstance(i,str) for i in column_names]), "axes input must be a list of string"
    counts = dataframe[column_names[0]].value_counts(sort=False)
    output = []
    out_indices = []
    sum_of_counts = counts.values.sum()
    other = 0
    for type in counts.index:
        temp_query = dataframe.query(f'{column_names[0]} == @type')
        match op:
            case "mean":#computes mean
                operation_result = temp_query.loc[:,column_names[1]].mean(axis=0)
            case "sum":
                operation_result = temp_query.loc[:,column_names[1]].sum(axis=0)
            case "norm":
                operation_result = counts[type]/sum_of_counts * 100
        if None != threshold:#implements threshold to remove values below it
            if operation_result > threshold:
                output.append(operation_result)
                out_indices.append(type)
        else:
            output.append(operation_result)
            out_indices.append(type)

    return pd.Series(data = output, index = out_indices)



