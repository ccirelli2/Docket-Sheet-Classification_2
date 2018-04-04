
# IMPORT LIBRARIES

import os
import re
import nltk
import pandas as pd
import string
from nltk.stem import *
stemmer = PorterStemmer()
from nltk import corpus




def measure_dependencies(File):
    '''
    Input  =     The location of a single Excel document that needs to be read into memory as a dataframe
    Output =     For each dataframe that is passed through this function, the return value will be the % to which 
                 the key words in all stages overlap. 
    Operations = a.) Create a list of all words in the file
                 b.) Take the len of that list. 
                 c.) Create a set of the list of key word and take its len. 
                 d.) Divide the len of the set by the len of the list and subtract the product by 1. 
                 e.) Return this value to the user as the value that represents the % of dependencies between 
                     all of the stages. 
    '''   
    # Import File 
    df = File                       # Amendment 03.31.2018:  Changed to File from reading a file in using pandas.  In memory work. 
    # Create list of columnnames
    df_columns = df.columns
    # Define the list to catch key words
    List_top_words = []
    # Loop over each column to obtain the key words removing any non string values (including none)
    for stage in df.columns:
        for word in df[stage]:
            if isinstance(word, str):
                List_top_words.append(word)
    # Create a set of the list of top words. 
    Set_topwords = set(List_top_words)
    
    # Calculate dependencies
    Length_list = len(List_top_words)
    Length_set = len(Set_topwords)
    Measure_dependency = (Length_list - Length_set)/Length_list
    
    return round(Measure_dependency,1)*100



def measure_dependencies_allDocs(List_dir):
    
    Dict = {}
    
    for file in List_dir:
        Measure_of_dependencies = measure_dependencies(file)
        Dict[str(file)] = Measure_of_dependencies
    
    df = pd.DataFrame(Dict, index = ['Percentage Dependency']).transpose().sort_values(
        by = 'Percentage Dependency',  ascending = True)
    
    return df





