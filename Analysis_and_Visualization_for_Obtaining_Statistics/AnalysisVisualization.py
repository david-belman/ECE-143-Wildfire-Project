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
import seaborn as sns
import folium
from folium.plugins import HeatMap
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



def plot_latlong_heatmap(dataframe, column_names):
    '''A customized function used to plot
    the latitude and longitude as a heat map
    on a set of coordinate axes'''
    assert isinstance(dataframe, pd.DataFrame), "dataframe input must be a pandas Dataframe datatype"
    assert isinstance(column_names, list)


    # sns.kdeplot(data=dataframe[[column_names[0],column_names[1]]], x=column_names[0], y=column_names[1], fill=True,)
    lat = dataframe[column_names[0]].tolist()
    long = dataframe[column_names[1]].tolist()

    data = []

    for i in range(0,len(lat)):
        data.append([lat[i],long[i]])
    #ax = sns.kdeplot([[lat],[long]], cmap="Blues", shade=True, shade_lowest=False)


    m = folium.Map([54, -115], zoom_start=8)
    
    HeatMap(data).add_to(m)

    display(m)

def seaborn_plot_latlong_heatmap(dataframe, column_names):
    '''A customized function used to plot
    the latitude and longitude as a heat map
    on a set of coordinate axes'''
    assert isinstance(dataframe, pd.DataFrame), "dataframe input must be a pandas Dataframe datatype"
    assert isinstance(column_names, list)


    sns.kdeplot(data=dataframe[[column_names[1],column_names[0]]], x=column_names[1], y=column_names[0], fill=True)

def pca_display(dataframe, column_names):
    '''A function to perform PCA on a limited number of 
    the columns to detect singular values. This function
    takes quite smoe time to run.'''
    dfToMatrix = []
    for i in column_names:
        dfToMatrix.append(dataframe[i].astype(float).tolist())
        
    data = np.array(dfToMatrix)
    
    standardized_data = (data - data.mean(axis = 0)) / data.std(axis = 0)
    standardized_data = standardized_data[np.isfinite(standardized_data).any(axis=1)]

    ### Step 2: Calculate the Covariance Matrix
    # use `ddof = 1` if using sample data (default assumption) and use `ddof = 0` if using population data
    covariance_matrix = np.cov(standardized_data, ddof = 1, rowvar = False)
    covariance_matrix = np.nan_to_num(covariance_matrix)
    #print(covariance_matrix)
    
    ### Step 3: Eigendecomposition on the Covariance Matrix
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
    
    
    ### Step 4: Sort the Principal Components
    # np.argsort can only provide lowest to highest; use [::-1] to reverse the list
    order_of_importance = np.argsort(eigenvalues)[::-1] 
    
    # utilize the sort order to sort eigenvalues and eigenvectors
    sorted_eigenvalues = eigenvalues[order_of_importance]
    sorted_eigenvectors = eigenvectors[:,order_of_importance] # sort the columns
    
    
    ### Step 5: Calculate the Explained Variance
    # use sorted_eigenvalues to ensure the explained variances correspond to the eigenvectors
    explained_variance = sorted_eigenvalues / np.sum(sorted_eigenvalues)
    
    
    ### Step 6: Reduce the Data via the Principal Components
    k = 2 # select the number of principal components
    reduced_data = np.matmul(standardized_data, sorted_eigenvectors[:,:k]) # transform the original data
    
    
    ### Step 7: Determine the Explained Variance
    total_explained_variance = sum(explained_variance[:k])
    
    
    ### Potential Next Steps: Iterate on the Number of Principal Components
    plt.plot(np.cumsum(explained_variance))
    plt.xlim(0, 5)
    plt.show

def plot_correlation(dataframe, column_names):
        
        """
        Given two columns plots the correlation or the contingency table 
        between the two columns
        """

        assert isinstance(dataframe, pd.DataFrame), "Please provide a dataframe"
        assert isinstance(column_names, (list, tuple)), "Provide the column names in list or tuple format"
        assert len(column_names) == 2, "Provide two columns"
        assert all( isinstance(col, str) and len(col) > 0 and col in dataframe.columns for col in column_names ), "Provide valid column names"

        dataframe[column_names[0]] = dataframe[column_names[0]].fillna('Other')
        # Create a contingency table
        contingency_table = pd.crosstab(dataframe[column_names[1]], dataframe[column_names[0]])
        # Plot heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(contingency_table, annot=True, cmap='YlGnBu', fmt='d')
        plt.title('Relationship between Fire Type and Fuel Type')
        plt.xlabel('Fuel Type')
        plt.ylabel('Fire Type')
        plt.show()