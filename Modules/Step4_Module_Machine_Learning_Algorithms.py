
# IMPORT LIBRARIES

import os
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
import graphviz
from sklearn.tree import export_graphviz    
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GridSearchCV


#   Classifiers
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier

# WRITE FILE TO EXCEL

def write_to_excel(dataframe, location, filename):
    os.chdir(location)
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()

# CREATE DATAFRAMES FOR THE FEATURES AND TARGETS


def get_feature_target_dataframes(File, dataset = 'Features'):
    '''Documentation
    
    Input      = i.)  Raw file from hard drive. 
                 ii.) Choose whether to returnthe Feature or target dataset. 
                 
    Operations = i.)   Read in the file as a dataframe
                 ii.)  Reset the index as it contains the docket sheet names, which are not needed. 
                 iii.) Drop the index. 
                 iv.)  Create the feature dataset
                 v.)   Create the target dataset.     
    '''
    
    Return_df = ''
    
    # Read in file as a dataframe
    # Amendment 03.28.2018:  Since we are pipelining all of the stages, we will pass a dataframe.  Therefore, we need not
    #                        read a file in as a dataframe.  
    df = File
    # Reset Index as it currently contains the docket sheet names. 
    df_reset_index = df.reset_index()
    # Drop Col 0
    df_drop_col = df_reset_index.drop('index', axis = 1)
    # Create our feature columns
    if dataset == 'Features':
        Return_df = df_drop_col.drop('Life Cycle Stage', axis = 1)
    elif dataset == 'Targets':
        Return_df = df_drop_col['Life Cycle Stage']
    else:
        print('You must chose either Features or Targets')
    
    return Return_df



#   SIMPLE DECISION TREE MODEL 

def simple_decision_tree(Max_Depth , TrainTest, Metric, Docketsheet_known, Docketsheet_unknown, TrainTestMode):
    '''Documentation:
    Input:      i.)   Docketsheet_train: This represents the KeyNgram matches for the docketsheet with pre-classified
                      time periods.  We will always use this dataframe in order to train our model.
                ii.)  Docketsheet_test:  This represents the KeyNgram matches for the docketsheet with unknown targets. 
                      After our model has been trained, we will use this dataframe in order to generate our predictions
                      to the unknown docketsheet entries. 
    Operations  i.)   Docketsheet_type:  This conditional statement will allow the user to chose between training and 
                      testing mode.  Training_mode will be reserved for when the user wants to train the model on known 
                      data.  Testing mode will be for when the user wants to train on known data and make predictions 
                      to unknown data.    
    '''
    
    # Create Training Objects Outside of Conditional Statements
    
    
    # TOGGLE TRAINING VS TESTING MODE
    
    # Determine if we are working exclusively with the Docketsheet Data that was pre-classified.  If so, then we 
    # are looking to train our model. 
       
    # If we are working with Unknown data, then we want to train using our known data and predict using the unknown. 
    # Added 04.03.2018
    if TrainTestMode == 'Prediction_Mode_Unknown_Data':
        # Get Features & Targets for known dataset. 
        Features_known = get_feature_target_dataframes(Docketsheet_known, dataset = 'Features')
        Targets_known  = get_feature_target_dataframes(Docketsheet_known, dataset = 'Targets')
        # Get Features & Targets for unknown dataset. 
        Features_unknown = get_feature_target_dataframes(Docketsheet_unknown, dataset = 'Features')
        Targets_unknown  = get_feature_target_dataframes(Docketsheet_unknown, dataset = 'Targets')
        # Define our training and test sets by training on the known data and making predictions for the unknown. 
        #  Idea: We train on the entirety of our known data and then predict the unknown. 
        X_train = Features_known
        y_train = Targets_known
        X_test  = Features_unknown
        y_test  = Targets_unknown 
        
        # Assign the decision tree to the objet clf. 
        clf = DecisionTreeClassifier(max_depth = Max_Depth, random_state = None)
        
        # Fit Algorithm
        clf.fit(X_train, y_train)     #****Why 
    
        #   Training Set
        # Amendment 03.31.2018: amended to
        print('Generating prediction for the unknown dataset\n')        
        clf_pred_train = clf.predict(X_test)                                      
        #report_train = sklearn.metrics.classification_report(y_train, clf_pred_train)
        #matrix_train = sklearn.metrics.confusion_matrix(y_train, clf_pred_train)
        #accuracy_train = sklearn.metrics.accuracy_score(y_train, clf_pred_train)
        
        print('Returning prediction for the unknown dataset: \n')
        return clf_pred_train
        
        # Test
        clf_pred_test = clf.predict(X_test)  # Why is this X_test and if so, why are we printing the matrix for y_test?   
        report_test = sklearn.metrics.classification_report(y_test, clf_pred_test)
        matrix_test = sklearn.metrics.confusion_matrix(y_test, clf_pred_test)
        accuracy_test = sklearn.metrics.accuracy_score(y_test, clf_pred_test)
    
    if TrainTestMode == 'Training_Mode_Known_Data':
        # Get Features & Targets
        Features = get_feature_target_dataframes(Docketsheet_known, dataset = 'Features')
        # Amended 04.03.2018
        Targets  = get_feature_target_dataframes(Docketsheet_known, dataset = 'Targets')
        # Amended 03:30.2018:  Added the feature to define the train and test size, set to 0.8 and 0.2
        X_train, X_test, y_train, y_test = train_test_split(Features, Targets, train_size = 0.9, test_size = 0.1)
        # Amended 03.31.2018: Random state needs to be set to 0. Think about moving this to the Driver function. 
        clf = DecisionTreeClassifier(max_depth = Max_Depth, random_state = 30) # Since this is the training mode we can
                                                                                # use a random state. 
    
        # Fit Algorithm
        clf.fit(X_train, y_train)     #****Why 
    
        #   Training Set
        # Amendment 03.31.2018: amended to
        clf_pred_train = clf.predict(X_train)                                      
        report_train = sklearn.metrics.classification_report(y_train, clf_pred_train)
        matrix_train = sklearn.metrics.confusion_matrix(y_train, clf_pred_train)
        accuracy_train = sklearn.metrics.accuracy_score(y_train, clf_pred_train)
    
        # Test
        clf_pred_test = clf.predict(X_test)  # Why is this X_test and if so, why are we printing the matrix for y_test?   
        report_test = sklearn.metrics.classification_report(y_test, clf_pred_test)
        matrix_test = sklearn.metrics.confusion_matrix(y_test, clf_pred_test)
        accuracy_test = sklearn.metrics.accuracy_score(y_test, clf_pred_test)
    
    
        # Generate Results Based on Metric / TrainTest Selection
        # Amendment made 03.31.2018:  Consolidated Report, Matrix and Accuracy functions to return Train and Test results  at the same time. 
        if Metric == 'Report':
            print('Returning training report:\n')
            print(report_train, '\n')
            print('Returning test report:\n')
            print(report_test, '\n')
              
        # Confusion Matrix
        elif Metric == 'Matrix':
            print('Returning training confusion matrix:\n')
            print(matrix_train, '\n')
            print('Returning test confusion matrix:\n')
            print(matrix_test, '\n')
              
        # Accuracy Score. 
        elif Metric == 'Accuracy':
            print('Returning training accuracy score:')
            Accuracy_score_train = round(accuracy_train, 2)
            print('\tAccuracy_score for the training set => ', Accuracy_score_train, '\n')
            Accuracy_score_test = round(accuracy_test, 2)
            print('Returning test accuracy score:')
            print('\tAccuracy score for test set =>', Accuracy_score_test, '\n')
            
        #Amendment 03.31.2018, added object to house predictions.  Will need to capture the index as there will
        # be no other way to reference back to the original docketsheet which entries were used. 
    
        elif Metric == 'Export_Indv_Predictions' and TrainTest == 'Train':   
            df_Indv_Predictions = pd.DataFrame({}, index = range(0,len(y_train)))
            df_Indv_Predictions['y_train'] = list(y_train)
            df_Indv_Predictions['clf_pred_train'] = list(clf_pred_train)
            print('\n', 'Returning the individual predictions for y_train (actual) and clf_pred_train (predicted values) ', '\n')
            return df_Indv_Predictions
    
        elif Metric == 'Export_Indv_Predictions' and TrainTest == 'Test':   
            df_Indv_Predictions = pd.DataFrame({}, index = range(0,len(y_test)))
            df_Indv_Predictions['y_test'] = list(y_test)
            df_Indv_Predictions['clf_pred_test'] = list(clf_pred_test)
            print('\n', 'Returning the individual predictions for y_test (actual) and clf_pred_test (predicted values) ', '\n')
            return df_Indv_Predictions      
    
        elif stp4_Metric == 'Export_All':
            df_x_train = pd.DataFrame(X_train)
            df_x_test = pd.DataFrame(X_test)
            df_y_train = pd.DataFrame(y_train)
            df_y_test = pd.DataFrame(y_test)
            df_clf_pred_test = pd.DataFrame(clf_pred_test)
            print('Step4: Generating the predictions...\n')
            print('X_train\n', df_x_train.head(),'\n')
            print('X_test\n', df_x_test.head(),'\n')
            print('y_train\n', df_y_train.head(),'\n')
            print('y_test\n', df_y_test.head(),'\n')
            print('clf_pred_test', clf_pred_test)
        
    # BREAK

    
    
# WRITE FILE TO EXCEL

def write_to_excel(dataframe, location, filename):
    os.chdir(location)
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()

    # BREAK
    
    
    
    
    
    
    
    
    
    
    


# *****DEPRECATED VERSION OF THE DECISION TREE DRIVER.  NO LONGER IN USE

def make_predictions_decisionTree(stp4_Target_dir, stp4_Depth, stp4_KeyWord, stp4_Write2Excel, 
                                  stp4_Destination_location, stp4_Iterable, stp4_Single_File, 
                                  stp4_Metric, df_inmemory_name):
    '''Documentation
    
    Purpose                          i) To provide the user the ability to select various measurement options. 
                                    ii.) To provide the option to iterate over a series of files to make multiple 
                                     predictions or a single predictions. 
    
    Input:      i.)    Target_dir  = location where our docketsheet key word appearance dataframes are located. 
                ii.)   Depth       = the depth that we want to use for our tree.  If not specified default 
                                     to 8. 
                iii.)  Write2Excel = if we want to write to Excel or work with the results in memory. 
                                     this feature is not yet set up for the confusion matrix or class report. 
                iv.)   Destination = where we want to write our results to. 
                v.)    Iterable    = whether we are working with a single or multiple files. 
                vi.)   Single_file = if we chose False for the Iterable, then we will need to specify the 
                                     file we want to use. 
                vii.)  Metric      = the metric that we want to use to guage the performance of our model. 
                                     default to 'Accuracy'.  Can also chose 'Matrix' to return the confusion
                                     matrix. 
                viii.) KeyWord     = Choose the key word that you want to use to group the files (approachs)
                                     to be used in the ML model. Examples include using the names of the 
                                     ngrmas ('Bigrams') or it could be STDV vs COCOEF, etc. 
                ix.)   df_inmemory_name 
                                   = Added on 03.29.2018:  added to accomodate the fact that we are working with an in
                                     memory dataframe and we need a name to pass to our Dict function below that identifies
                                     the characteristics of the file we are passing through to the ML tree. 
    Operations i.)     The main operation here is either to iterate a list of files in a directory to 
                       generate the predictions or to work with one file.  That and the code is set up so 
                       that the user can have various choices as can be inferred from the input explanations. 
                       
    '''
    # Dictionary to house values
    Dict = {}

    # Change Directory
    os.chdir(stp4_Target_dir)
    
    # If you are looking to iterate over an entire directory of files
    if stp4_Iterable == True:
    
        #Loop over files
        for file in os.listdir():
        
            # Choose the key word to group the files that are chosen by the code.  
            if stp4_KeyWord in file:                       
                                                          
                # Mark start of process                            
                print('Generating prediction for =>', '\n', file, '\n')
                # Create the Feature & Target dataframes. 
                Features = get_feature_target_dataframes(file, dataset = 'Features')
                Targets  = get_feature_target_dataframes(file, dataset = 'Targets')
                # Generate The Training Results
                Accuracy_train = simple_decision_tree(Features, Targets, 
                                                   stp4_Metric, Max_Depth = stp4_Depth, TrainTest = 'Train')
                # Generate the Test Results. 
                Accuracy_test = stp4.simple_decision_tree(Features, Targets, 
                                                   stp4_Metric, Max_Depth = stp4_Depth, TrainTest = 'Test')
            
                # Add your results to the dictionary object using file name as the key. 
                Dict[file] = (Accuracy_train, Accuracy_test)
    
    # If the user only wants to work with one file. 
    elif stp4_Iterable == False:
        
        # Mark start of process
        print('Generating prediction for the dataframe passed from memory')
        # Get Features & Targets
        Features = get_feature_target_dataframes(stp4_Single_File, dataset = 'Features')
        Targets  = get_feature_target_dataframes(stp4_Single_File, dataset = 'Targets')
        # Generate Prediction
        Accuracy_train = simple_decision_tree(Features, Targets, 
                                                  Max_Depth = stp4_Depth, TrainTest = 'Train', 
                                                  Metric = stp4_Metric)
        Accuracy_test = simple_decision_tree(Features, Targets, 
                                                  Max_Depth = stp4_Depth, TrainTest = 'Test', 
                                                  Metric = stp4_Metric)
        
        # Amendment 03.29.2018:  df_in_memory_name has been added as a new object and is defined
        # in the driver program for Step4. 
                
        # Append results to a dictionary object. 
        Dict[df_inmemory_name] = (Accuracy_train, Accuracy_test)

    # Create Dataframe from dictionary object. 
    df = pd.DataFrame(Dict)
    df_transpose = df.transpose()
    # Define the column names.  In the future, if we add more measures, we can change this. 
    df_rename_cols = df_transpose.rename(index = str, columns = {0: 'Accuracy_train', 
                                                                 1: 'Accuracy_test'}) 
    df_final = df_rename_cols.sort_values(by = 'Accuracy_test', ascending = False)
    
    # Write to Excel
    if stp4_Write2Excel == True:
        print('Writing dataframe to Excel')
        os.chdir(stp4_Destination_location)
        File_name = 'Decision Tree Results for' + '_' + df_inmemory_name
        print('File name => ' + File_name)
        write_to_excel(df_final, stp4_Destination_location, File_name)
        print('Your file has been saved to =>  ', stp4_Destination_location, '\n', '\n')
    # If the user does not want to write to Excel return to them the dataframe in memory.     
    else:    
        print('Accuracy train', '\n', Accuracy_train)
        print('Accuracy test', '\n', Accuracy_test)
        return df_final










