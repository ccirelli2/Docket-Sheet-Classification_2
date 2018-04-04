
# IMPORT LIBRARIES
import pandas as pd
import os


# IMPORT LIBRARIES

import pandas as pd
import math


# WRITE FILE TO EXCEL

def write_to_excel(dataframe, location, filename):
    os.chdir(location)
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()


#### FUNCTIONS TO CALCULATE MEASUREMENTS OF CENTRAL TENDANCY

def get_Measurements_CentralTendancy(dataframe, measurement):
    '''
    Calculation_I:
        Input       = 'CalculationI_homebrew_STDV'
        Constraints = Not set up to work with COCOEF
        Description = 
        AVG         = Average value for all rows (including zeros)
        STDV        = Is our Target_Freq minus our average * Target_Freq.  This will decrease our target by both the average 
                      and its own frequency such that we will be able to find those words that are most unique to our target
                      in terms of both their frequency and deviation from the mean. By not squaring our delta we also preserve 
                      the sign such that a Target_Freq that is less than the average will be negative and automatically fall to 
                      the bottom of our list. 
    Calculation_II:
        Input       = 'CalculationII_AVG_not_zero'
        Constraints = Not set up to work with COCOEF
        Description = The purpose of this approach is to try to generate higher averages by focusing only on the non-zero
                      values.  This will ensure that a single value (other than our target) that has a very high freq does
                      not get overlooked by our model by dividing it by the total length of the row (10 in this case). 
        AVG         = Average of values not equal to zero. 
        STDV        = Using the Home_brew calculation from CalculationI. 
    
    Calculation_III:  
        Input       = 'CalculationIII_Correlation_Coefficient'
        Constraints = Not set up to work with any of the STDV calculations
        Description = Calculate teh correlation coefficient as our target variable to identify key words. Note that this
                      approach will not yeild negative numbers, so we should only capture one list of values in descending
                      order with the highest COCEF values. 
        AVG         = Use the same calculation for CalculationII to generate the AVG of non-zero values. 
        STDV        = Lets use the traditional calculation for STDV
        COCEF       = STDV / AVG
    
    Itertuples Columns
        row[0]      = Index
        row[1]      = col0, Ngram tuples
        row[2]      = Target stage
        row[3:12]   = Other stages 
    
    '''
        
    # LISTS TO CAPTURE MEASUREMENTS OF CENTRAL TENDANCY
    List_AVG = []
    List_STDV = []
    List_COCOEF = []
    
    # Iterate over the rows in the FreqDist dataframe
    for row in dataframe.itertuples():
        
        
        # CALCULATION I: HOME_BREW_STDV
        if measurement == 'CalculationI_homebrew_STDV':
            
            # Calculate Average using all of the rows
            AVG = sum(row[3:]) / len(row[3:])                           # changing row[2:] to row[3:]
                       
            # STDV_homebrew 
            STDV = (row[2] - AVG) * row[2]                                # changing row[1] to row[2]
             
            #Append Values to the lists
            List_AVG.append(AVG)
            List_STDV.append(STDV)
    
        # CALCULATION II:  EXCLUDE VALUES == 0
        elif measurement == 'CalculationII_AVG_not_zero':
            
            # Limit row to only those values that are != 0
            Row_not_equal_0 = [x for x in row[3:] if x != 0]              # changing from row[2:] to row[3:]
            
            # Calculate the denominator as the length of this list.  
            Count_values_greater_zero = len(Row_not_equal_0)
      
            # If the length of the denominator is 0, then all values in the row were zero.  Defaul AVG and STDV to 0. 
            if Count_values_greater_zero == 0:
                List_AVG.append(0)
                List_STDV.append(0)
                
            else:
                # Otherwise, calculate the Average
                AVG = (sum(Row_not_equal_0) / Count_values_greater_zero)
                # Calculate the STDV as the (Target Freq / Avg) * Target Freq 
                STDV = (row[2] - AVG) * row[2]                            # changing row[1] to row[2]
                #Append Values to the lists
                List_AVG.append(AVG)
                List_STDV.append(STDV)
        
        # CALCULATION III:  CORRELATION COEFFICIENT
        elif measurement == 'CalculationIII_Correlation_Coefficient':
            
            # Limit row to only those values that are != 0
            Row_not_equal_0 = [x for x in row[3:] if x != 0]              # changed row[2:] to row[3:]
        
            # Calculate the denominator as the length of this list.  
            Count_values_greater_zero = len(Row_not_equal_0)
        
            # If the length of the denominator is 0, then all values in the row were zero.  Defaul AVG and STDV to 0. 
            if Count_values_greater_zero == 0:
                List_AVG.append(0)
                List_STDV.append(0)
                List_COCOEF.append(0)
    
            else:
                # Otherwise, calculate the Average
                AVG = (sum(Row_not_equal_0) / Count_values_greater_zero)
                # Calculate the Variance & the Standard deviation by the book.  
                VAR = (row[2] - AVG) **2                                  # changed row[1] to row[2]
                STDV = math.sqrt(VAR)
                # Calculate the Correlation Coefficient
                COCOEF = STDV / AVG
                #Append Values to the lists
                List_AVG.append(AVG)
                List_STDV.append(STDV)
                List_COCOEF.append(COCOEF)
      
    # APPEND LISTS OF CENTRAL TENDANCY TO OUR DATAFRAME
    
    # If our selected measurement is either Calculation I or II, only append the AVG and STDV
    if measurement == 'CalculationI_homebrew_STDV' or measurement == 'CalculationII_AVG_not_zero':
        dataframe['AVG'] = List_AVG
        dataframe['STDV'] = List_STDV
    
    elif measurement == 'CalculationIII_Correlation_Coefficient':
        dataframe['AVG'] = List_AVG
        dataframe['STDV'] = List_STDV
        dataframe['COCOEF'] = List_COCOEF
        
    # Return the Dataframe to the user w/ the measurements of central tendancy
    return dataframe


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
        delimiter = dataframe.iloc[:,1] > .3     # changed to .03 on 03.31.2018
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

def drop_measures_CT(dataframe_with_measures_CT, Calculation_meth):
    '''
    The purpose of this function is to drop the columns that are being appended directly to the df_rename_col dataframe. 
    '''
    # Create a dataframe to capture the new df without these column headings. 
    df_final = ''
    
    if Calculation_meth == 'CalculationIII_Correlation_Coefficient':
        df_final = dataframe_with_measures_CT.drop(['AVG', 'STDV', 'COCOEF'], axis = 1)
     
    else:
        df_final = dataframe_with_measures_CT.drop(['AVG', 'STDV'], axis = 1)
    
    return df_final




def get_top_words_toggle_methodology(stp2_FreqDist_file = None, stp2_Calculation_meth = None, 
                                     stp2_methodology_top_words = None, stp2_write2excel = False, 
                                     stp2_destination_location = None, stp2_Ngram_type = None):
    '''
    INPUTS:
                    a.) dataframe_freq_distribution = The pandas dataframe that represents the freq dist
                        created for each of our 4 ngram types (No, Bi, Tri and Quadgrams)
                    d.) Methodology_CT = type of calculation to be performed (see options below)
                    c.) Methodology_top_words = type of methodology to be performed (see options below)
                    d.) Destination_location = destination to write the file. 
                    e.) Ngram_type = Type of Ngram we are dealing with. 
    
    FUNCTION_I:     Methodology_CT - Calculation of Central Tendencys
        Input       a.) The dataframe containing the word frequency distributions. b.) One of the below cal methodologies. sza
        Options     'CalculationI_homebrew_STDV', 
                    'CalculationII_AVG_not_zero', 
                    'CalculationIII_Correlation_Coefficient'
    
    FUNCTION_II:    Methodology - Top Words
        Input       a.) The dataframe containing the word frequency distribution, b.) One of the below methodologies, 
                    c.) The stage, which is defined within this namespace. 
        Options     'Top15_highest_STDV', 
                    'Top15_highest_COCOEF', 
                    'Top5_highest_STDV_lowest_AVG', 
                    'Top5_highest_STDV_AVG_below_20prct', 
                    'Top5_lowest_STDV_highest_AVG', 
                    'Top5_lowest_COCOEF_highest_AVG'
    '''

    
    # Rename Col[0] of our dataframe to 'Ngrams', which is the column that contains our tuples
    df_rename_cols = stp2_FreqDist_file.rename(index = str, columns = {0: 'Ngrams'})  
       
    # Create a new dataframe to capture the top words and set the index to 0-15.  
    # This is the dataframe that will be returned to our user. 
    df_top_words = pd.DataFrame({}, index = [x for x in range(0,15)])
    
    # Reset df_rename_cols to just the columns 0-12
    if len(df_rename_cols.columns) > 12:                                            # changed from 11 to 12
        df_rename_cols = df_rename_cols.iloc[:, 0:12]                               # changed from [:, 0:12] to [:, 0:12]
        
    # Create an object to keep count of our Life Cycle Stage
    Stage = ''

    # Instead of using the column names to keep count of our position in the code, we use a range function.
    # this is the value to which 100 will be added in the below loop before we sort our columns. 
    for num in range(1,13):                                                         # No change.  We ony want to rotate
                                                                                    # the cols containing stages
               
        # Loop Starts at Life Cycle 1.  Set Condition that when it reaches 11 it stops. 
        if df_rename_cols.columns[1] != 101:                                       # Changed from column[0] to column[1]
            
            # Stage
            Stage = df_rename_cols.columns[1]                                      # changed to columns[1], which is stage 1
            
            # Calculate Measures of Central Tendancy
            df_with_measures_of_CT = get_Measurements_CentralTendancy(df_rename_cols, 
                                                                                  stp2_Calculation_meth)
            # Get Top Words
            Top_words_all_calc = get_top_words(df_with_measures_of_CT, 
                                                              stp2_methodology_top_words, 
                                                              Stage)
            
            # Create a String of the current column name
            Col_name = str(Top_words_all_calc.columns[1])                          # Changed to column[1] from [0]
            
            # Capture all rows (top words) and only the target column of the dataframe. 
            Top_words_target_stage = Top_words_all_calc.iloc[:,0]                  # Changed to iloc[:,1] from [:,0]

            # Append to our dataframe that will be returned to the user the top 5 words for each Life Cycle Stage.  
            df_top_words[Col_name] = Top_words_target_stage
            
            # Reset df_rename_cols to just the columns 0-11
            if len(df_rename_cols.columns) > 12:                                   # Changed to 12 from 11
                df_rename_cols = df_rename_cols.iloc[:, 0:12]                      # Changed to [:,0:12] from [:,0:11]
            
            # Rename the first column to = num + 100.  Num = Original Col1 at each iteration.
            df_col_increased_by100 = df_rename_cols.rename(index = str, columns = {num: num+100})
            
            # With the first column renamed, sort ascending, * but only on a slice of the dataframe that
            # containts our stages.  
            df_rotate = df_col_increased_by100.iloc[:,1:12].sort_index(ascending = True, axis = 1)  # Changed to add a slicer
                                                                                             # so as to only sort the 
                                                                                             # columns containing stages. 
                                                                                             # Not sure if this will work. 
            # Re-insert our Ngram column into the dataframe at position 0. 
            df_rotate.insert(loc = 0, column = 'Ngrams', value = df_rename_cols['Ngrams'])
            # Rename or sorted dataframe to df_rename_cols, which will be entered into our function at the start of the loop. 
            df_rename_cols = df_rotate
    
    # Write to Excel
    if stp2_write2excel == True:
        print('Writing dataframe to Excel')
        os.chdir(stp2_destination_location)
        File_name = 'TopWords' + '_' + str(stp2_Ngram_type) + '_' + stp2_Calculation_meth + '_' +stp2_methodology_top_words
        print('File name => ' + File_name)
        write_to_excel(df_top_words, stp2_destination_location, File_name)
        print('Your file has been saved to:  ', stp2_destination_location, '\n')
    # Once the list of ngrams is complete, return it to the user.
    
    return df_top_words
            
            





