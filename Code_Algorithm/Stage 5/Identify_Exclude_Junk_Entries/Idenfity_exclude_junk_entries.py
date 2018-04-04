'''Documentation

Purpose:    The purpose of this code is to identify those docketsheet entries that are deemed extraneous or unnecessary for our study.
Input:      i.) List of quadgrams that identify junk entries. ii.) Docketsheet with preclassified stages.
Output:     i.) Docketsheet with a column indicating if the entry is junk or not.
Operations: i.) import excel file with quadgrams ii.) create set of exclusionary quadgrams.
            iii.) Import into memory our docketsheet file. iv.) create funtion clean and tokenize each entry.
            v.) create a list to capture the value as to whether or not the entry is junk.
            vi.) write that list back to the docketsheet file as a separate columnself.
            vii.) incorporate this code into your Step1 code.
'''

# IMPORT PACKAGES
import os
import pandas as pd

# IMPORT MODULES
Dir = r'/home/ccirelli2/Desktop/Docket-Sheet-Classification/Modules'
os.chdir(Dir)
import Step2_P1_Module_Calculations_Central_Tendancy_version4_Ngrams
