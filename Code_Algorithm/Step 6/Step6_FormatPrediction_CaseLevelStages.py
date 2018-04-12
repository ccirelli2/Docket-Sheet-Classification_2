import os
import pandas as pd

# Change directory
os.chdir('/home/ccirelli2/Desktop/Docket-Sheet-Classification-v2/Stage5_Predictions_Results')

# # Load Excel Files
Chunk1_docketsheet_entries = r'Step5_Prediction_Appended_Docketsheet_Chunk1.xlsx'
Chunk1_case_predictions = r'Case_Level_Predictions_Chunk1.xlsx'
df1_chunk1_ds_entries = pd.read_excel(Chunk1_docketsheet_entries)
df2_case_predictions = pd.read_excel(Chunk1_case_predictions)


def get_collocation_stg8_stg11(df1, df2):

    Dict = {}

    List_final_values = []

    for x,y in zip(df2.itertuples(), df2[1:].itertuples()):
        print(x[0])
        # List = []
        # if y[-1] != 11:
        #     List.append(y[-1])
        #     Dict[y[0]] = ''
        #
        #

get_collocation_stg8_stg11(df1df1_chunk1_ds_entries, df2df2_case_predictions)
