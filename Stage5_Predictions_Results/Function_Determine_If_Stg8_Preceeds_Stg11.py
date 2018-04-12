
import os
import pandas as pd

# Change directory
os.chdir('/home/ccirelli2/Desktop/Docket-Sheet-Classification-v2/Stage5_Predictions_Results')

# # Load Excel Files
Chunk1_ds_entries = r'Step5_Prediction_Appended_Docketsheet_Chunk1.xlsx'
Chunk1_case_predictions = r'Case_Level_Predictions_Chunk1.xlsx'
# Create DataFrames
df_chunk1_ds_entries = pd.read_excel(Chunk1_ds_entries)
df_case_predictions = pd.read_excel(Chunk1_case_predictions)

Count = 0
for x,y,z in zip(df_chunk1_ds_entries.itertuples(), df_case_predictions.itertuples(), df_case_predictions[1:].itertuples()):
    Count +=1
    if Count < 2:
        print(x,y,z)
