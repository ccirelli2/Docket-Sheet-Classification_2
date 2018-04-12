
# IMPORT LIBRARIES

import os
import re
import nltk
import pandas as pd
import string
from nltk.stem import *
stemmer = PorterStemmer()
from nltk import corpus

# IMPORT TARGET FILE / DELIMIT ROWS / REMOVE ROWS PERIOD = NONE

def conditional_statement_row_isstr(dataframe):
    List = []
    for row in dataframe:
        Bool = isinstance(row, str)
        List.append(Bool)
    return List   
    
    
def format_docket_sheet_file(Excel_file, Write2Excel, destination_location):
    
    '''Documentation
    Purpose:        The purpose of this code is to transform the columns/rows of the test and training Docketsheets
                    to a uniform structure prior to their being fed into the model.  
    Operations:     i.) Conditional statement to determine which of the files is input, 
                    ii.) Drop irrelevant columns, iii.) Add missing columns, iv.) Remove rows with zero text.                 
    Input:          Either the training or test docket-sheet Excel file. 
    Output:         A dataframe formated for use for Step3 of the algorithm. 
    '''
    
    # Read Excel file in as a dataframe. 
    df_docketsheet = pd.read_excel(Excel_file)  
        
    # If the length of the docketsheet is less than 2000, then we know it is our training dock. 
    if len(df_docketsheet) < 5000:
        # Drop Last column. 
        # Amended on 03.28.2018: Changed from dataframe to reading a file.
        df_docket_sheets_fit = df_docketsheet.iloc[:,0:-1]
        # Select rows != None
        TimePeriod_notNone = df_docket_sheets_fit['Time_Period'] > 0
        # Return dataframe
        return df_docket_sheets_fit[TimePeriod_notNone]
    # Otherwise, it is our testing doc as it contains more than 20,000 rows. 
    else:     
        # Original Code
        delimiter = [isinstance(x,str) for x in df_docketsheet['docket_text']]
        df_limited = df_docketsheet[delimiter]
        
        # Drop Irrelevant Columns
        df_dropcols = df_limited.drop(['document_try_flag', 'document_flag', 'document_link', 
                                    'document_text', 'state', 'district', 'row_number'], axis = 1)
        
        #Add missing columns present in the original docketsheet
        df_dropcols['Index'] = [x for x in range(0,len(df_limited))]
        df_dropcols['Relevant'] = [x for x in range(0,len(df_limited))]
        df_dropcols['Time_Period'] = [x for x in range(0,len(df_limited))]
           
    # Write to Excel
    if Write2Excel == True:
        print('Writing dataframe to Excel')
        os.chdir(destination_location)
        File_name = 'Master_Docketsheet_transformed'
        print('File name => ' + File_name)
        write_to_excel(df_dropcols, destination_location, File_name)
        print('Your file has been saved to =>  ', destination_location, '\n', '\n')
        # Otherwise, return the dataframe to the user.    
    else:
        return df_dropcols
        
        
        
# GET KEY WORDS FROM FILE

def get_set_KeyWords_from_file(File):
    # Read file in as a dataframe
    df = File                   # Amended 03.28.2018.  Since we are creating a master pipeline, we are now passing a
                                # pandas dataframe where as before it was a file.  We should add an if elif statement here
                                # so that in the future we can still use the separated code. 
                                # used to be df = pd.read_excel(File), now df = File, which is actuall a dataframe. 
   


    # List of key words
    List = []
    # Iterate over dataframe columns
    for col in df.columns:
        
        # Iterate over each ngram in each column
        for ngram in df[col]:
            # Exclude None Values. 
            if isinstance(ngram, str):
                    # Create Tuples depending on the type of Ngrams.
                    # Amendment 03.28.2018:   We can no longer use the approach - if 'Nograms' in File as we are no longer
                    #                         dealing with the file names.  So we will use a diff approch here.
                    
                    # New Approach: Take the first Ngram from the dataframe, split on the space and take the length. 
                    Ngram_0 = File.iloc[0,0]
                    Ngram_split = Ngram_0.split(' ')
    
                    # Check the length of the first key word in our Dict
                    if len(Ngram_split) == 1:
                        List.append(ngram)
                    elif len(Ngram_split) == 2:
                        # Split on the quotes. 
                        ngram_split = ngram.split('\'')
                        # Create a tuple from the words. 
                        Tuple = (ngram_split[1], ngram_split[3])
                        List.append(Tuple)
                    elif len(Ngram_split) == 3:
                        ngram_split = ngram.split('\'')
                        Tuple = (ngram_split[1], ngram_split[3], ngram_split[5])
                        List.append(Tuple)
                    elif len(Ngram_split) == 4:
                        ngram_split = ngram.split('\'')
                        Tuple = (ngram_split[1], ngram_split[3], ngram_split[5], ngram_split[7])
                        List.append(Tuple)  
    # Return a set to the user.
    return set(List)



# CREATE A SET OF ALL HUMAN NAMES FROM THE NLTK CORPUS LIBRARY

def get_set_human_names():
    '''
    Purpose:  obtain a set of all human names
    Input:    none
    Output:   Set of of both female and male names
    '''
    # Create a lise of Male names, convert to lower case, split on '\n' as the text reads in a string as unicode
    Male_names = corpus.names.open('male.txt').read().lower().split('\n')
    # Create a lise of female names, convert to lower case, split on '\n' as the text reads in a string as unicode
    Female_names = corpus.names.open('female.txt').read().lower().split('\n')
    # Return to the user a set of the concatenation of both lists. 
    return set(Male_names + Female_names)


# CLEAN & TOKENIZE CONCATENATED TEXT FILE & RETURN SET

def clean_andTokenize_text(Text_file):
    
    '''
    Input      = Text File
    Operations = Tokenize, lowercase, strip punctuation/stopwords/nonAlpha
    Return     = Object = Set; Set = cleaned, isalpha only tokens
    '''
    # Strip Lists
    Punct_list = set((punct for punct in string.punctuation))
    Stopwords = nltk.corpus.stopwords.words('english')
    Set_names = get_set_human_names()
    
    # Tokenize Text
    Text_tokenized = nltk.word_tokenize(Text_file)
    # Convert tokens to lowercase
    Text_lowercase = (token.lower() for token in Text_tokenized)
    # Strip Punctuation
    Text_tok_stripPunct = filter(lambda x: (x not in Punct_list), Text_lowercase)
    # Strip Stopwords
    Text_strip_stopWords = filter(lambda x: (x not in Stopwords), Text_tok_stripPunct)
    # Strip Non-Alpha
    Text_strip_nonAlpha = filter(lambda x: x.isalpha(), Text_strip_stopWords)
    # Strip 2 letter words
    Text_strip_2letter_words = filter(lambda x: len(x)>3, Text_strip_nonAlpha)
    # Strip names
    Text_strip_names_2 = filter(lambda x: x not in Set_names, Text_strip_2letter_words)
    # Take Stem of Each Token 
    Text_stem = [stemmer.stem(x) for x in Text_strip_names_2]
    # Note that we are not returning a set here as with Ngrams we are looking for patters which could be altered materially by using
    # a set function, which is better used outside the function if need be. 
    return Text_stem

# CODE TO CREATE NGRAMS

def get_Ngrams(Clean_tokenized_text, Ngram_selection):
    # Create a list to capture Ngrams
    List_Ngrams = []
    
    # If Bigrams selected
    
    if Ngram_selection == 'Nograms':
        [List_Ngrams.append(x) for x in Clean_tokenized_text]
        
    elif Ngram_selection == 'Bigrams':
        [List_Ngrams.append((x,y)) for x,y in zip(Clean_tokenized_text, 
                                               Clean_tokenized_text[1:])]  
    # If Trigrams selected
    elif Ngram_selection == 'Trigrams':
        [List_Ngrams.append((x,y,z)) for x,y,z in zip(Clean_tokenized_text, 
                                                    Clean_tokenized_text[1:], 
                                                    Clean_tokenized_text[2:])]
    # If Quadgrams selected. 
    elif Ngram_selection == 'Quadgrams':
        [List_Ngrams.append((w,x,y,z)) for w,x,y,z in zip(Clean_tokenized_text, 
                                                    Clean_tokenized_text[1:], 
                                                    Clean_tokenized_text[2:], 
                                                    Clean_tokenized_text[3:])]
    # Return Ngrams list
    return List_Ngrams

# TURN CLEAN TOKENIZED TEXT INTO NGRAMS

def get_docketsheet_ngrams(Tokenized_text, File):
    '''
    Input      = a.) Tokenized Text, b.) Filename from which the key words are being sourced. 
    Operations = a.) Create an object to capture our Ngrams generated from the ngram function, 
                 b.) Use the filename to determine whether the ngrams within are No, Bi, Tri or Quadgrams. 
                     If no match is found, return statement to the user that a file not specifying the type of ngrams
                     has been passed to the function. 
                 e.) Generate the ngrams and populate the Ngrams_text object. 
    Output     = The docketsheet entry converted into the appropriate Ngrams. 
    '''   
    # Define the object Ngrams_text as an empty string
    Ngrams_text = '' # Deprecated
    
    Ngram_0 = File.iloc[0,0]
    Ngram_split = Ngram_0.split(' ')
    
    # Check the length of the first key word in our Dict
    if len(Ngram_split) == 1:
        Ngrams_text = get_Ngrams(Tokenized_text, 'Nograms')
    elif len(Ngram_split) == 2:
        Ngrams_text = get_Ngrams(Tokenized_text, 'Bigrams')
    elif len(Ngram_split) == 3:
        Ngrams_text = get_Ngrams(Tokenized_text, 'Trigrams')
    elif len(Ngram_split) == 4:
        Ngrams_text = get_Ngrams(Tokenized_text, 'Quadgrams')
    else:
        print('''Please be advised that the following file was passed to the functon that does not specify what type
                of Ngrams are contained within''', '\n', 'File => ', File, '\n')
    
    # Return to the user the Ngram_text
    return Ngrams_text


# WRITE FILE TO EXCEL

def write_to_excel(dataframe, location, filename):
    os.chdir(location)
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()


# CODE GET KEY WORD APPEARANCE IN DOCKET SHEET ENTRIES

def get_KeyWordAppearance_DocketsheetEntries(Docketsheet, File, 
                                             Write2Excel, Destination_location, 
                                            Transpose4mlModel):
    '''
    Purpose     = The purpose of this code is to generate a dataframe whose rows are the docketsheet entries, columns
                  the key ngrams and the values the appearance of these ngrams in each docketsheet entry. 
    Input       = 1.) A dataframe representing the docketsheet limited to only those applicable rows and columns. 
                  2.) A file containing the list of key words for a particular calculation + methodology
                      combination.  
    Operations  = 1.) Create a dataframe to house the rows and columns 
                  2.) Since the names of each docketsheet entry do not indicate their position in the dataframe, create
                      and object to keep the count of the num of rows that we iterate over, which will later be used in
                      the naming of the rows in the new dataframe returned to the user. 
                  3.) Create a list to capture the values 0/1 that will represent the appearance or not of each of the
                      Ngrams.  This list is the row of values for each docketsheet entry. 
                  4.) Clean and tokenize the text in the same manner as was done in Stage1. 
                  5.) Create Ngrams of the docketsheet rows in the same manner as was done in Stage1. 
                  6.) Iterate over each Ngram in the List of Ngrams input into this function. 
                  7.) Determine if the Ngram is present and add values to the List_word_matches defined earlier .
                  8.) Define our row. 
                  9.) Append the row to our dataframe. 
    
    '''
             
    # Format Docketsheet (rows / columns)
    Docketsheet_formated = format_docket_sheet_file(Excel_file = Docketsheet, 
                                                    Write2Excel = Write2Excel,
                                                    destination_location = Destination_location)
        
    # Get Key Words From File
    Set_key_words = get_set_KeyWords_from_file(File)
        
    # Create New Dataframe
    df_DAT = pd.DataFrame({}, index = Set_key_words)
    
    # Count of Rows
    Count = 0
       
    # Iterate over row of the docketsheet df as an enumerated tuple. 
    for row in Docketsheet_formated.itertuples():
                
        # Star the Count of the rows
        Count += 1
        
        # Status Report:
        if Count == int((len(Docketsheet_formated)/4)):
            print('\t25% completed')
        elif Count == int((len(Docketsheet_formated)/2)):
            print('\t50% completed')
        elif Count == int(len(Docketsheet_formated)- (len(Docketsheet_formated)/4)):
            print('\t75% completed\n')
        
        # List to capture each row.  List will reset on each iteration of the code. 
        List_word_matches_single_row = []
                
        # Clean row[4], which is the text column of the docketsheet. 
        clean_tokenize_row = clean_andTokenize_text(row[4])                
            
        # Once the text of the row is tokenized, we need to create the Ngrams
        docketsheet_ngrams = get_docketsheet_ngrams(clean_tokenize_row, File)
        
        # So iterate every word in key_word_list for each rows 
        for Ngram in Set_key_words:

            #Check to see if the word is in the clean text
            if Ngram in docketsheet_ngrams:
                # If there is a match, append 1 to the list
                List_word_matches_single_row.append(1)
            else: 
            # If not, append 0
                List_word_matches_single_row.append(0)
        
        # Create a string from the counter to add to your column name. 
        Row_num = 'row' + str(Count) + ' ' 
        
        # Create a column in your new datafrmae to capture the case number and list of matches. 
        df_DAT[Row_num + row[1] + ' ' + str(row[2])] = List_word_matches_single_row        

    if Transpose4mlModel == True:
        df_final = df_DAT.transpose()
        List_Life_Cycles = [x for x in Docketsheet_formated['Time_Period']]
        df_final['Life Cycle Stage'] = List_Life_Cycles
        
        # Write to Excel
        if Write2Excel == True:
            print('Writing dataframe to Excel')
            os.chdir(Destination_location)
            File_name = 'DocketSheet_WordMatches' + '_' + File
            print('File name => ' + File_name)
            write_to_excel(df_final, Destination_location, File_name)
            print('Your file has been saved to =>  ', Destination_location, '\n', '\n')
         # Otherwise, return the dataframe to the user.    
        else:
            return df_final
    
    else:
        # Write to Excel
        if Write2Excel == True:
            print('Writing dataframe to Excel')
            os.chdir(Destination_location)
            File_name = 'DocketSheet_WordMatches' + '_' + File
            print('File name => ' + File_name)
            write_to_excel(df_DAT, Destination_location, File_name)
            print('Your file has been saved to =>  ', Destination_location, '\n', '\n')
        # Otherwise, return the dataframe to the user.    
        else:
            return df_DAT
    
    # BREAK




# STEP3: FINAL CODE GET KEY WORD APPEARANCE IN THE DOCKETSHEET. 

def get_DocketSheet_KeyWord_Appearance_Master(stp3_Docketsheet, 
                                              stp3_DirNgramLoc, 
                                              stp3_Iterable,
                                              stp3_KeyPhrase,
                                              stp3_Destination_location, 
                                              stp3_Transpose4mlModel, 
                                              stp3_Write2Excel,
                                              stp3_Target_file ):
    '''Documentation
    Input      = i.)   Docketsheet:  the original docketsheet with pre-classified entries. 
                 ii.)  DirNgramLoc:  The location where our KeyWordSelection files have been saved. 
                 iii.) Iterable:     If we plan to iterate over a list of files or just use one file. 
                 iv.)  Target_file:  If Iterable is False, then we need to specify the singular file for 
                                     which we would like generate the Docketsheet key word appearance 
                                     dataframe.
                 v.)   KeyPhase:     Rather than read the data from each file of KeyWords to identify the
                                     Ngram type, and because we have a uniform approach to defining our 
                                     KeyWord Excel files that specify the Ngram, we use the title to determine
                                     which type of Ngram we are dealing with. 
                 vi.)  Destination_loc
                                     Where we would like to write the excel file to.
                 vii.) Transpose     Whether or not we want to transpose the dataframe.  Note that this 
                                     will need to be done for any dataframes that the user plans to feed 
                                     into the machine learning algorithms. 
                 viii.)Write2Excel   Whether the user wants to write to Excel or return the dataframe in 
                                     memory. 
    
    KeyPhrase  = Chose the key phrase in the file name that will limit the files that are use in the code. 
                 Example:  Use 'Bigrams' to only obtain results for those files using Bigrams, 
                           or 'Avg_not_zero for files using that methodology. 
    
    '''
    
    
    # Obtain Word Appearance for All Files In Dir
    if stp3_Iterable == True:
        # Change directory to where the Ngram Key Words are saved
        os.chdir(stp3_DirNgramLoc)
        # Obtain Files
        List_files = [file for file in os.listdir() if stp3_KeyPhrase in file]
        
        
        # Loop over directory of files
        for file in List_files:
                # Change directory back to where our files are saved. 
                os.chdir(stp3_DirNgramLoc)
                
                # Run Algorithm to obtain KeyWordAppearance. 
                DocketSheet_KeyWord_Appearance = get_KeyWordAppearance_DocketsheetEntries(
                                                Docketsheet = stp3_Docketsheet, 
                                                File = file, 
                                                Write2Excel = stp3_Write2Excel, 
                                                Destination_location = stp3_Destination_location, 
                                                Transpose4mlModel = stp3_Transpose4mlModel)
                # Generally we would not want to return a dataframe in a loop like this unless we plan to 
                # embed this code into another function that can use the resulting dataframe. 
                
                                    
    # If you only want results for a single file         
    else:
        DocketSheet_KeyWord_Appearance = get_KeyWordAppearance_DocketsheetEntries(
                                                Docketsheet = stp3_Docketsheet, 
                                                File = stp3_Target_file, 
                                                Write2Excel = stp3_Write2Excel, 
                                                Destination_location = stp3_Destination_location, 
                                                Transpose4mlModel = stp3_Transpose4mlModel)
        return DocketSheet_KeyWord_Appearance
    
    
    
# TRANSFORM THE MASTER DOCKETSHEET FOR USE IN OUR MACHINE LEARNING ALGORITHM DRIVER FUNCTION
# Added on 03.31.2018. 

def transform_Master_Docketsheet(Excel_file, Write2Excel, destination_location):
    '''Documentation
    Purpose:        The purpose of this code is to transform the columns of the Master Docketsheet file to 
                    match that of the original Docketsheet file so that it may be fed into our existing
                    functions for processing
    Operations:     i.) Drop irrelevant columns, ii.) Add missing columns, iii.) Test                
    '''
    
    # Read File in as a pandas dataframe
    df_master = pd.read_excel(Excel_file)
    
    # Remove from dataframe rows == None
    delimiter = [row for row in df_master if isinstance(row, str)]
    df_limited = df_master[delimiter]
    
    # Drop Irrelevant Columns
    df_dropcols = df_limited.drop(['document_try_flag', 'document_flag', 'document_link', 
                                  'document_text', 'state', 'district', 'row_number'], axis = 1)
    # Add missing columns present in the original docketsheet
    df_dropcols['Index'] = [x for x in range(0,len(df_limited))]
    df_dropcols['Relevant'] = [x for x in range(0,len(df_limited))]
    df_dropcols['Time_Period'] = [x for x in range(0,len(df_limited))]
    df_dropcols['Unnamed'] = [x for x in range(0,len(df_limited))]
    
    # Write to Excel
    if Write2Excel == True:
        print('Writing dataframe to Excel')
        os.chdir(destination_location)
        File_name = 'Master_Docketsheet_transformed'
        print('File name => ' + File_name)
        write_to_excel(df_dropcols, destination_location, File_name)
        print('Your file has been saved to =>  ', destination_location, '\n', '\n')
        # Otherwise, return the dataframe to the user.    
    else:
        return df_dropcols
    
    
















