
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

def format_docket_sheet_file(dataframe):
    '''
    Input      = None
    Operations = Read file, select columns, eliminate time-period = None
    Return     = dataframe. 
    '''
    # Limit Columns
    df_docket_sheets_fit = dataframe.iloc[:,0:-1]
    # Select rows != None
    TimePeriod_notNone = df_docket_sheets_fit['Time Period'] > 0
    # Return dataframe
    return df_docket_sheets_fit[TimePeriod_notNone]

# GET KEY WORDS FROM FILE

def get_set_KeyWords_from_file(File):
    # Read file in as a dataframe
    df = pd.read_excel(File)
    # List of key words
    List = []
    # Iterate over dataframe columns
    for col in df.columns:
        # Iterate over each ngram in each column
        for ngram in df[col]:
            # Exclude None Values. 
            if isinstance(ngram, str):
                    # Create Tuples depending on the type of Ngrams. 
                    if 'Nograms' in File:
                        List.append(ngram)
                    elif 'Bigrams' in File:
                        # Split on the quotes. 
                        ngram_split = ngram.split('\'')
                        # Create a tuple from the words. 
                        Tuple = (ngram_split[1], ngram_split[3])
                        List.append(Tuple)
                    elif 'Trigrams' in File:
                        ngram_split = ngram.split('\'')
                        Tuple = (ngram_split[1], ngram_split[3], ngram_split[5])
                        List.append(Tuple)
                    elif 'Quadgrams' in File:
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
    Ngrams_text = ''
    # Check the length of the first key word in our Dict
    if 'Nograms' in File:
        Ngrams_text = get_Ngrams(Tokenized_text, 'Nograms')
    elif 'Bigrams' in File:
        Ngrams_text = get_Ngrams(Tokenized_text, 'Bigrams')
    elif 'Trigrams' in File:
        Ngrams_text = get_Ngrams(Tokenized_text, 'Trigrams')
    elif 'Quadgrams' in File:
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
                                             Write2Excel = False, Destination_location = None, 
                                            Transpose4mlModel = False):
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
    # Print Progress Report 1
    print('Working on key-word appearance for file =>', File ,'\n')
        
    # Format Docketsheet (rows / columns)
    Docketsheet_formated = format_docket_sheet_file(Docketsheet)
        
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
        List_Life_Cycles = [x for x in Docketsheet_formated['Time Period']]
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

























