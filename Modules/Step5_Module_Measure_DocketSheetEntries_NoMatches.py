
# IMPORT LIBRARIES

import os
import re
import nltk
import pandas as pd
import string
from nltk.stem import *
stemmer = PorterStemmer()
from nltk import corpus


def get_count_nomatch_columns(File, Count = 'Count_zero'):
    
    # Read the file in as a pandas dataframe
    # Amendment 03.29.2018:  Working in memory so will pass directly the dataframe. 
    dataframe = File             
    # Drop target column
    df_drop_target = dataframe.drop(['Life Cycle Stage'], axis = 1)
    # Keep count of rows with no matches
    Count_all = 0
    Count_zero = 0
    # Iterate over each row
    for row in df_drop_target.itertuples():
        # Count Each Row
        Count_all +=1
        # Calculate the sum of the row
        if sum(row[1:]) == 0:
            # If the sum is 0, add one to the count. 
            Count_zero +=1
    
    if Count == 'Count_zero':
        return Count_zero
    elif Count == 'Count_all':
        return Count_all
    
    
    
def create_dataframe_all_Files_Freq_NoMatches(df_inmemory_name, dataframe_in_memory, Write2Excel = False, 
                                              Destination_location = None):
    Dict = {}
    
    Count_zero = get_count_nomatch_columns(dataframe_in_memory, Count = 'Count_zero')
    Count_all = get_count_nomatch_columns(dataframe_in_memory, Count = 'Count_all')
    Dict[df_inmemory_name] = (Count_zero, round(Count_zero/Count_all, 2))
        
    df = pd.DataFrame(Dict).transpose()
    
    # Write to Excel
    if Write2Excel == True:
        print('Writing dataframe to Excel')
        os.chdir(Destination_location)
        File_name = 'Result Calculation No Matches' + df_inmemory_name
        print('File name => ' + File_name)
        stp4.write_to_excel(df, Destination_location, File_name)
        print('Your file has been saved to =>  ', Destination_location, '\n', '\n')
        # Otherwise, return the dataframe to the user.    
    else:
        return df
    
    return df  