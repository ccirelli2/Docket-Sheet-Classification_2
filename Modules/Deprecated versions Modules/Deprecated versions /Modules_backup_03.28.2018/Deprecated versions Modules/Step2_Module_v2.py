
# IMPORT LIBRARIES

import pandas as pd



#### FUNCTIONS TO GET TOP 5 WORDS WITH HIGHEST STDV FREQ WITH LOWEST AVG

def get_AVG_STDV_CV_Target_Stage(dataframe):
    '''
    Purpose:   The purpose of this code is to calculate three values from our word frequency distribution.
               1.) AVG  = The average frequecy of all stages that do not = 0.  This should ensure that our AVG is reflective of values 
                          that may approximate our target freq, and if that value be greater, then our AVG will have a better chance of 
                          reflecting this value by not including the stages that = 0. 
               2.) STDV = We use a unique calculation as the STDV.  From the target value we subtract the the AVG and multiple the 
                          result by the target.  This gives us a deviation about the mean while respecting the sign of the delta between 
                          the target and avg. 
               Input:     The frequency distribution dataframe. 
    Output:    The frequency distribution dataframe with three additional columns for each of our values. 
    '''
    
    # Define lists to capture avg and stdv values for each row. 
    List_AVG = []
    List_STDV = []
    
    # Iterate each row of the dataframe as a tuple. 
    for row in dataframe.itertuples():
        # row[0] = index, row[1] = target, row[2:11] = other stages
        # Create an object that only contains the values of the stages (other than the target stage) not = zero.
        # The sum of these values will be used for calculating our average.  
        Row_not_equal_0 = [x for x in row[2:] if x != 0]
        # Take the length of this list as the denominator for our calculation of the average. 
        Count_values_greater_zero = len(Row_not_equal_0)
      
        # If there are no values in the list, then all values were zero and the average and STDV should defaul to 0
        if Count_values_greater_zero == 0:
            List_AVG.append(0)
            List_STDV.append(0)
                
        else:
            # Otherwise, calculate the Average
            AVG = (sum(Row_not_equal_0) / Count_values_greater_zero)
            # Calculate the STDV as the (Target Freq / Avg) * Target Freq 
            STDV = (((row[1] - AVG)*row[1]))
            #Append Values to the lists
            List_AVG.append(AVG)
            List_STDV.append(STDV)
    
    # Create Columns for the AVG and STDV values
    dataframe['AVG'] = List_AVG
    dataframe['STDV'] = List_STDV
    
    # Return the dataframe with the calculated avg and stdv values 
    return dataframe

def get_df_top5words_highestCV_lowestAVG(dataframe, Stage):
    '''The purpose of this function is to create a new dataframe that includes the 5 words with the highest STDV when the AVG is 
       between 0 and 5% and Target Freq > 20%.  The purpose is to find words that are very unique to 
    
    Input      = Dataframe that includes the AVG and STDV calculated for the Life Cycle Stage in Question.  Stage is used to rename col. 
    Operations = Sort dataframe on CV column, limit to top 5 rows, create new dataframe with Index = 1-5, create col for words and STDVs
    Output     = Dataframe with 5 rows, 2 cols, top5 words w/ STDV values. 
    '''
    
    # Limit the dataframe to averages that are between 1 and 2%
    df_limit = dataframe.AVG.between(0, .1)
    df_avg_limited = dataframe[df_limit]
    df_limit_2 = df_avg_limited.iloc[:, 0] > .1
    df_target_limited = df_avg_limited[df_limit_2]
    
    # Sort the Dataframe col "CV" descending = True. 
    df_sorted = df_target_limited.sort_values(by = 'STDV', ascending = False)

    # Obtain First 5 Rows
    
    if len(df_sorted) > 4:
        df_sorted_topFive = df_sorted.iloc[:5,]
        
        # Create New Dataframe Whose Index = 1-5
        df_final = pd.DataFrame({}, index = [1,2,3,4,5])
    
        # Create a Column to capture the top 5 words. 
        df_final['Life Cycle Stage: '+str(Stage)] = df_sorted_topFive.index
    
        # Create a Column to Capture the STDV for each word.
        df_final['Stage 1: STDV'] = [row for row in df_sorted_topFive['STDV']]
    
    else:
        Range = len(df_sorted)
        df_sorted_topFive = df_sorted.iloc[:Range, ]
        
        # Create New Dataframe Whose Index = 1-5
        df_final = pd.DataFrame({}, index = range(0,Range))
    
        # Create a Column to capture the top 5 words. 
        df_final['Life Cycle Stage: '+str(Stage)] = df_sorted_topFive.index
    
        # Create a Column to Capture the STDV for each word.
        df_final['Stage 1: STDV'] = [row for row in df_sorted_topFive['STDV']]
    
    
    # Retun the final dataframe
    return df_final


#### FUNCTIONS TO GET TOP 5 WORDS WITH HIGHEST STDV & AVG > 2%. 

def get_df_top5words_AVG_greater2_less10(dataframe, Stage):
    '''The purpose of this function is to create a new dataframe that includes the 5 words with the highest STDV
    
    Input      = Dataframe that includes the AVG and STDV calculated for the Life Cycle Stage in Question
    Operations = Sort dataframe on STDV column, limit to top 5 rows, create new dataframe with Index = 1-5, create col for words and STDVs
    Output     = Dataframe with 5 rows, 2 cols, top5 words w/ STDV values. 
    '''
    
    # Limit the dataframe to averages that are between 5 and 15%
    df_limit = dataframe.AVG.between(.101, .2)
    df_avg_limited = dataframe[df_limit]
    df_limit_2 = df_avg_limited.iloc[:, 0] > .2
    df_target_limited = df_avg_limited[df_limit_2]
    
    # Sort the Dataframe col "CV" descending = True. 
    df_sorted = df_target_limited.sort_values(by = 'STDV', ascending = False)

    # Obtain First 5 Rows
    
    if len(df_sorted) > 4:
        df_sorted_topFive = df_sorted.iloc[:5,]
        
        # Create New Dataframe Whose Index = 1-5
        df_final = pd.DataFrame({}, index = [1,2,3,4,5])
    
        # Create a Column to capture the top 5 words. 
        df_final['Life Cycle Stage: '+str(Stage)] = df_sorted_topFive.index
    
        # Create a Column to Capture the STDV for each word.
        df_final['Stage 1: STDV'] = [row for row in df_sorted_topFive['STDV']]
    
    else:
        Range = len(df_sorted)
        df_sorted_topFive = df_sorted.iloc[:Range, ]
        
        # Create New Dataframe Whose Index = 1-5
        df_final = pd.DataFrame({}, index = range(0,Range))
    
        # Create a Column to capture the top 5 words. 
        df_final['Life Cycle Stage: '+str(Stage)] = df_sorted_topFive.index
    
        # Create a Column to Capture the STDV for each word.
        df_final['Stage 1: STDV'] = [row for row in df_sorted_topFive['STDV']]
        
    # Retun the final dataframe
    return df_final



def get_df_top5words_Target_nearZero_highest_AVG(dataframe, Stage):
    '''The purpose of this function is to create a new dataframe that includes the 5 words with the highest STDV
    
    Input      = Dataframe that includes the AVG and STDV calculated for the Life Cycle Stage in Question
    Operations = Sort dataframe on STDV column, limit to top 5 rows, create new dataframe with Index = 1-5, create col for words and STDVs
    Output     = Dataframe with 5 rows, 2 cols, top5 words w/ STDV values. 
    '''
    
    # Limit our target stage frequency distribution % to less than 5%. 
    df_limit = dataframe.iloc[:,0] < .2
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
    df_final['Stage 1: STDV'] = [row for row in df_sorted_topFive['STDV']]
    
    # Retun the final dataframe
    return df_final



































