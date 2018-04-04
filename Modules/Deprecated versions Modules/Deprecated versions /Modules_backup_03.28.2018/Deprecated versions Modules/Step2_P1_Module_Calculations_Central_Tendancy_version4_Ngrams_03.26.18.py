
# IMPORT LIBRARIES

import pandas as pd
import math


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

































