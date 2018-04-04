
# IMPORT LIBRARIES
import pandas as pd

'''ADJUSTMENTS TO ACCOMODATE NGRAMS

Index   = We can no longer refer to the index as the location for our Ngrams.  So when the function sorts on N calculation, the next step, 
          which is to append N rows to our new dataframe, the target is no longer the index, where the 'words' used to reside, rather
          column 0.  Therefore, all references to index to obtain our top words will need to be modified. 

'''



# FUNCTION TO LIMIT DATAFRAME BASED ON THE SELECTED METHODOLOGY 

def limit_dataframe(dataframe, methodology):
    '''
    Purpose   = To limit our dataframe based on the methodology chosen in our get_top_words function. 
    Input     = Dataframe, value by which to limit the average. 
    Output    = Our dataframe limited. 
    '''
    # Create an object to catch the limited dataframe. 
    df_limited = ''
    
    # Amendment:   Changing all methodologies to Top 15 as there are too many zero matches for docketsheet entries. 
    
    if methodology == 'Top5_highest_STDV_lowest_AVG':
        # If this methodology is selected, Limit AVG to the value input into the function.
        delimiter = dataframe.AVG.between(0, 0.05)
        df_limited = dataframe[delimiter]
          
    elif methodology == 'Top5_highest_STDV_AVG_below_20prct':
        # If this methodology is selected, limit the AVG to between 5 and 20%. 
        delimiter = dataframe.AVG.between(.05, 0.2)
        df_limited = dataframe[delimiter]
    
    elif methodology == 'Top5_lowest_STDV_highest_AVG':
        # If this methodology is selected, limit the STDV to less than 10%. 
        delimiter = dataframe['STDV'] < .10
        df_limited = dataframe[delimiter]
        
    elif methodology == 'Top5_lowest_COCOEF_highest_AVG':
        # If this methodology is selected, limit the COCOEF to less than 10%. 
        delimiter = dataframe['COCOEF'] < .10
        df_limited = dataframe[delimiter]
        
    elif methodology == 'Top15_highest_COCOEF' or methodology == 'Top15_highest_STDV':
        # If this methodology is selected, do nothing. 
        # Added 03.28.2018
        delimiter = dataframe.iloc[:,1] > .05     # changed to .05 on 03.28.2018
        df_limited = dataframe[delimiter]
        
        #df_limited = dataframe  * commented out due to the testing of the above change. 
    
    # Return our limited dataframe to the user. 
    return df_limited



# FUNCTION TO OBTAIN TOP WORDS BASED ON THE METHODOLOGY SELECTED


def get_top_words(dataframe, methodology, Stage):
    '''
    INPUTS (ALL):
    dataframe     =
    methodology   = 
    Stage         = ?
    
    
    Methodology_I:
    Input         = 'Top15_highest_STDV', 
                    get_Measurements_CentralTendancy == 'CalculationI_homebrew_STDV' or 'CalculationII_AVG_not_zero'
    Description   = Obtain the 15 words with the highest STDV using our Homebrew calculation. 
    Operations    = Sort STDV column in descending order, return to the user the top 10 words for our target var. 
    
    Methodology_II:
    Input         = 'Top15_highest_COCOEF', 
                    get_Measurements_CentralTendancy == 'CalculationIII_Correlation_Coefficient'
    Description   = Obtain the 15 words with the highest Correlation Coefficient
    Operations    = 
    
    Methodology_III:
    Input         = 'Top5_highest_STDV_lowest_AVG'
                    get_Measurements_CentralTendancy == 'CalculationI_homebrew_STDV' or 'CalculationII_AVG_not_zero'
    Description   = Obtain the top 5 words with the highest STDV and lowest ADV using our Homebrew calculation.  This should
                    result in very unique words for our Target_stage. 
    Operations    = Limit the AVG to less than 5% and then sort the STDV column in descending order.  Take the top 5. 
    
    Methodology_IV:
    Input         = 'Top5_highest_STDV_AVG_below_20prct'
                    get_Measurements_CentralTendancy == 'CalculationI_homebrew_STDV' or 'CalculationII_AVG_not_zero'
    Description:  = Obtain the top 5 words with the highest STDV and an AVG of between 5.1 to 20%.  This should result in 
                    somewhat unique words for our Target_stage.  Still unique, but with some overlap with the other stages. 
    Operations    =  Limit AVG to between 5.1 and 20.0.  Sort the STDV column in descending order. Take the top 5. 
    
    Methodology_V:
    Input         = 'Top5_lowest_STDV_highest_AVG'
                    get_Measurements_CentralTendancy == 'CalculationI_homebrew_STDV' or 'CalculationII_AVG_not_zero'
    Description   = The objective is to identify those words with the lowest correlation to our Target stage. 
    
    Methodology_VI:
    Input         = 'Top5_lowest_COCOEF_highest_AVG'
                    get_Measurements_CentralTendancy == 'CalculationI_homebrew_STDV' or 'CalculationII_AVG_not_zero'
    Description   = The objective is to identify those words with the lowest correlation to our Target stage. 
    
    '''
    
    DF_TOP_WORDS = ''
    
    # STEP1:  LIMIT DATAFRAME BY THE METHODOLOGY CHOSEN
    df_limited = limit_dataframe(dataframe, methodology)
    
    # STEP2:  GET TOP WORDS
      
    if methodology == 'Top15_highest_STDV':
        # Sort Dataframe by STDV in descending order
        df_sorted = df_limited.sort_values(by = 'STDV', ascending = False)
        # Get first 15 rows
        # Amendment:  changed to top 40 from 15 on 03.28.2018
        df_sorted_topNgrams = df_sorted.iloc[:40,] 
        
        # Create New Dataframe Whose Index = 0-15
        # Amendment:  amended range to len of df_sorted_topNgrams 03.28.2019
        df_final = pd.DataFrame({}, index = [x for x in range(0,len(df_sorted_topNgrams))]) 
                
        # Create a col in the new df to capture the top 15 words. 
        # amendment:  changed from df_sorted_top5.index to 'Ngram's.  In the jupyter code we change the first column from 
                     # whatever it used to be to 'Ngrams' and that is how we reference the col here.  Its our target col. 
        df_final['Life Cycle Stage: '+str(Stage)] = [x for x in df_sorted_topNgrams['Ngrams']]    
        # Create a Column to Capture the STDV for each word.       
        # Amendment:  changed from df_sorted_top5
        df_final['Stage' + str(Stage) + ': ' + 'STDV'] = [row for row in df_sorted_topNgrams['STDV']]     
        # Assign the value of df_final to our DF_TOP_WORDS dataframe that will be returned to the user. 
        DF_TOP_WORDS = df_final

    elif methodology == 'Top15_highest_COCOEF':
        # Sort Dataframe by COCEOF in descending order
        df_sorted = df_limited.sort_values(by = 'COCOEF', ascending = False)
                
        # Get first 15 rows
        #  Amendment:  changed from 15 to 40 on 03.28.2018. 
        df_sorted_topNgrams = df_sorted.iloc[:40,]
        
        # Create New Dataframe Whose Index = 0-15
        #  Amendment:  changed the range from 0,15 to 0,len(df_sorted_topNgrams. 
        df_final = pd.DataFrame({}, index = [x for x in range(0,len(df_sorted_topNgrams))])
        
        # Create a col in the new df to capture the top 15 words. 
        df_final['Life Cycle Stage: '+str(Stage)] = [x for x in df_sorted_topNgrams['Ngrams']]
        # Create a Column to Capture the COCEOF for each word.
        df_final['Stage' + str(Stage) + ': ' + 'COCOEF'] = [row for row in df_sorted_topNgrams['COCOEF']]
        # Assign the value of df_final to our DF_TOP_WORDS dataframe that will be returned to the user. 
        DF_TOP_WORDS = df_final
    
    elif methodology == 'Top5_highest_STDV_lowest_AVG':
        # Amendment:  Changed from top 5 to top 15. 
        # Sort Dataframe by STDV in descending order
        df_sorted = df_limited.sort_values(by = 'STDV', ascending = False)
        
        # Check to see if the length of the dataframe is 5 or more. 
        if len(df_sorted) > 4:
            df_sorted_topFive = df_sorted.iloc[:15,]
            # Create New Dataframe Whose Index = 0-4
            df_final = pd.DataFrame({}, index = [x for x in range(0,len(df_sorted_topFive ))]) 
            # Create a Column to capture the top 5 words. 
            df_final['Life Cycle Stage: '+str(Stage)] = [x for x in df_sorted_topFive['Ngrams']]
            # Create a Column to Capture the STDV for each word.
            df_final['Stage' + str(Stage) + ': ' + 'STDV'] = [row for row in df_sorted_topFive['STDV']]
            DF_TOP_WORDS = df_final
        # Otherwise, we need to define the index of our new df as the length of the df_sorted.     
        else:
            # Measure the length of our df. 
            Range = len(df_sorted)
            # Obtain the top N words
            df_sorted_topFive = df_sorted.iloc[:Range, ]
            # Create New Dataframe Whose Index = 1-5
            df_final = pd.DataFrame({}, index = [x for x in range(0,len(df_sorted_topFive))]) 
            # Create a Column to capture the top 5 words. 
            df_final['Life Cycle Stage: '+str(Stage)] = [x for x in df_sorted_topFive['Ngrams']]
            # Create a Column to Capture the STDV for each word.
            df_final['Stage' + str(Stage) + ': ' + 'STDV'] = [row for row in df_sorted_topFive['STDV']]
            DF_TOP_WORDS = df_final
    
    elif methodology == 'Top5_highest_STDV_AVG_below_20prct':
        # Sort the Dataframe col "CV" descending = True. 
        df_sorted = df_limited.sort_values(by = 'STDV', ascending = False)

        # Check to see if the length of the dataframe is 5 or more. 
        if len(df_sorted) > 4:
            df_sorted_topFive = df_sorted.iloc[:15,]
            # Create New Dataframe Whose Index = 0-4
            df_final = pd.DataFrame({}, index = [x for x in range(0,len(df_sorted_topFive ))]) 
            # Create a Column to capture the top 5 words. 
            df_final['Life Cycle Stage: '+str(Stage)] = [x for x in df_sorted_topFive['Ngrams']]
            # Create a Column to Capture the STDV for each word.
            df_final['Stage' + str(Stage) + ': ' + 'STDV'] = [row for row in df_sorted_topFive['STDV']]
            DF_TOP_WORDS = df_final
        # Otherwise, we need to define the index of our new df as the length of the df_sorted. 
        else:
            Range = len(df_sorted)
            df_sorted_topFive = df_sorted.iloc[:Range, ]
            # Create New Dataframe Whose Index = 1-5
            df_final = pd.DataFrame({},  index = [x for x in range(0,len(df_sorted_topFive ))]) 
            # Create a Column to capture the top 5 words. 
            df_final['Life Cycle Stage: '+str(Stage)] = [x for x in df_sorted_topFive['Ngrams']]
            # Create a Column to Capture the STDV for each word.
            df_final['Stage' + str(Stage) + ': ' + 'STDV'] = [row for row in df_sorted_topFive['STDV']]
            DF_TOP_WORDS = df_final
            
    elif methodology == 'Top5_lowest_STDV_highest_AVG':
        # Sort the Dataframe col "CV" descending = True. 
        df_sorted = df_limited.sort_values(by = 'AVG', ascending = False)
        # Obtain First 5 Rows
        df_sorted_topFive = df_sorted.iloc[:15,]
        # Create New Dataframe Whose Index = 0-4
        df_final = pd.DataFrame({},  index = [x for x in range(0,len(df_sorted_topFive ))]) 
        # Create a Column to capture the top 5 words. 
        df_final['Life Cycle Stage: '+str(Stage)] = [x for x in df_sorted_topFive['Ngrams']]
        # Create a Column to Capture the STDV for each word.
        df_final['Stage' + str(Stage) + ': ' + 'STDV'] = [row for row in df_sorted_topFive['STDV']]
        DF_TOP_WORDS = df_final
    
    elif methodology == 'Top5_lowest_COCOEF_highest_AVG':
        # Sort the Dataframe col "CV" descending = True. 
        df_sorted = df_limited.sort_values(by = 'COCOEF', ascending = False)       
        # Obtain First 5 Rows
        df_sorted_topFive = df_sorted.iloc[:15,]
        # Create New Dataframe Whose Index = 0-4
        df_final = pd.DataFrame({}, index = [x for x in range(0,len(df_sorted_topFive ))]) 
        # Create a Column to capture the top 5 words. 
        df_final['Life Cycle Stage: '+str(Stage)] = [x for x in df_sorted_topFive['Ngrams']]    
        #** We can no longer refer to index as 
        # Create a Column to Capture the STDV for each word.          # the place where our Ngrams reside. 
        df_final['Stage' + str(Stage) + ': ' + 'COCOEF'] = [row for row in df_sorted_topFive['COCOEF']]              # it must be col[0]
        DF_TOP_WORDS = df_final      
            
    # Return to the user the dataframe with top word selection
    return DF_TOP_WORDS
        

### DEPRECATED CODE NO LONGER IN USE. 

# DROP MEASURES OF CENTRAL TENDANCY THAT ARE APPENDED TO THE DATAFRAME IN OUR CODE.  

def drop_measures_CT(dataframe_with_measures_CT, methodology_CT):
    '''
    The purpose of this function is to drop the columns that are being appended directly to the df_rename_col dataframe. 
    '''
    # Create a dataframe to capture the new df without these column headings. 
    df_final = ''
    
    if methodology_CT == 'CalculationIII_Correlation_Coefficient':
        df_final = dataframe_with_measures_CT.drop(['AVG', 'STDV', 'COCOEF'], axis = 1)
     
    else:
        df_final = dataframe_with_measures_CT.drop(['AVG', 'STDV'], axis = 1)
    
    return df_final










