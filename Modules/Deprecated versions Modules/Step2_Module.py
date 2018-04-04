
# IMPORT LIBRARIES

import pandas as pd



#### FUNCTIONS TO GET TOP 5 WORDS WITH HIGHEST STDV FREQ WITH LOWEST AVG

def get_AVG_STDV_CV_Target_Stage(dataframe):
    '''
    Purpose:   The purpose of this code is to calculate three values from our word frequency distribution.
               1.) AVG  = The average frequecy of all stages other than the target stage. We multiple by the AVG by 100 to get a real num. 
               2.) STDB = The standard deviation of our target stage vs the average of the other stages
               3.) CV   = The correlation coefficient to obtain the percentage for which our STDV varies from the mean. 
    Input:     The frequency distribution dataframe. 
    Output:    The frequency distribution dataframe with three additional columns for each of our values. 
    '''
    
    # Define lists to capture avg and stdv values for each row. 
    List_AVG = []
    List_STDV = []
    List_CV = []
    
    for row in dataframe.itertuples():
        # Note that when iterating tuples the index is col 0
        # Get the Average of row for all columns but col 1. 
        AVG = (sum(row[2:]) / 10)
        # Get the Standard Deviation of row[1] / Avg. 
        STDV = (((row[1] - AVG)*100)**2)
        # Get Correlection Coefficient
        CV = STDV/(AVG*100)
        
        #Append Values to the lists
        List_AVG.append(AVG)
        List_STDV.append(STDV)
        List_CV.append(CV)
    
    # Create Columns for the AVG and STDV values
    dataframe['AVG'] = List_AVG
    dataframe['STDV'] = List_STDV
    dataframe['CV'] = List_CV
    
    # Return the dataframe with the calculated avg and stdv values 
    return dataframe

def get_df_top5words_highestCV_lowestAVG(dataframe, Stage):
    '''The purpose of this function is to create a new dataframe that includes the 5 words with the highest STDV
    
    Input      = Dataframe that includes the AVG and STDV calculated for the Life Cycle Stage in Question.  Stage is used to rename col. 
    Operations = Sort dataframe on CV column, limit to top 5 rows, create new dataframe with Index = 1-5, create col for words and STDVs
    Output     = Dataframe with 5 rows, 2 cols, top5 words w/ STDV values. 
    '''
    
    # Limit the dataframe to averages that are between 1 and 2%
    df_limit = dataframe.AVG.between(0.01, .02)
    df_avg_range = dataframe[df_limit]
    
    # Sort the Dataframe col "CV" descending = True. 
    df_sorted = df_avg_range.sort_values(by = 'CV', ascending = False)
    
    # Obtain First 5 Rows
    df_sorted_topFive = df_sorted.iloc[:5,]
    
    # Create New Dataframe Whose Index = 1-5
    df_final = pd.DataFrame({}, index = [1,2,3,4,5])
    
    # Create a Column to capture the top 5 words. 
    df_final['Life Cycle Stage: '+str(Stage)] = df_sorted_topFive.index
    
    # Create a Column to Capture the STDV for each word.
    df_final['Stage 1: CV'] = [row for row in df_sorted_topFive['CV']]
    
    # Retun the final dataframe
    return df_final


#### FUNCTIONS TO GET TOP 5 WORDS WITH HIGHEST STDV & AVG > 2%. 

def get_df_top5words_AVG_greater2_less10(dataframe, Stage):
    '''The purpose of this function is to create a new dataframe that includes the 5 words with the highest STDV
    
    Input      = Dataframe that includes the AVG and STDV calculated for the Life Cycle Stage in Question
    Operations = Sort dataframe on STDV column, limit to top 5 rows, create new dataframe with Index = 1-5, create col for words and STDVs
    Output     = Dataframe with 5 rows, 2 cols, top5 words w/ STDV values. 
    '''
    
    # Limit our target stage frequency distribution % to between 2.1 and 10%. 
    df_limit = dataframe.AVG.between(0.021, .10)
    df_avg_range = dataframe[df_limit]
    
    # Sort the Dataframe col "CV" descending = True. 
    df_sorted = df_avg_range.sort_values(by = 'CV', ascending = False)
    
    # Obtain First 5 Rows
    df_sorted_topFive = df_sorted.iloc[:5,]
    
    # Create New Dataframe Whose Index = 1-5
    df_final = pd.DataFrame({}, index = [1,2,3,4,5])
    
    # Create a Column to capture the top 5 words. 
    df_final['Life Cycle Stage: '+str(Stage)] = df_sorted_topFive.index
    
    # Create a Column to Capture the STDV for each word.
    df_final['Stage 1: CV'] = [row for row in df_sorted_topFive['CV']]
    
    # Retun the final dataframe
    return df_final



def get_df_top5words_Target_nearZero_highest_AVG(dataframe, Stage):
    '''The purpose of this function is to create a new dataframe that includes the 5 words with the highest STDV
    
    Input      = Dataframe that includes the AVG and STDV calculated for the Life Cycle Stage in Question
    Operations = Sort dataframe on STDV column, limit to top 5 rows, create new dataframe with Index = 1-5, create col for words and STDVs
    Output     = Dataframe with 5 rows, 2 cols, top5 words w/ STDV values. 
    '''
    
    # Limit our target stage frequency distribution % to less than 5%. 
    df_limit = dataframe.iloc[:,0] < .05
    df_avg_range = dataframe[df_limit]
    
    # Sort the Dataframe col "CV" descending = True. 
    df_sorted = df_avg_range.sort_values(by = 'AVG', ascending = False)
    
    # Obtain First 5 Rows
    df_sorted_topFive = df_sorted.iloc[:5,]
    
    # Create New Dataframe Whose Index = 1-5
    df_final = pd.DataFrame({}, index = [1,2,3,4,5])
    
    # Create a Column to capture the top 5 words. 
    df_final['Life Cycle Stage: '+str(Stage)] = df_sorted_topFive.index
    
    # Create a Column to Capture the STDV for each word.
    df_final['Stage 1: CV'] = [row for row in df_sorted_topFive['CV']]
    
    # Retun the final dataframe
    return df_final



































