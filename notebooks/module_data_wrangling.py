#Pre-Process data

import pandas as pd
import numpy as np

#-----------------------------------------------------------------
def generate_options_dictionary(filtered_df, options_column_name):
    """LOAD Alternatives for the Question into a dictionary"""

    # Split the string into key-value pairs
    answer_options = filtered_df[options_column_name]

    # Split the string into key-value pairs and flatten the list of lists 
    # This is necessary because Pandas DataFrame is horrible, it always returns a series instead of a primitive object like a string or something.
    # Therefore, one needs these ugly two for-loops just to get f*ying single list of strings... f*ck...)
    all_options_list = [option for sublist in answer_options.str.split(';') for option in sublist]

    # Assuming all_options_list is defined earlier in your code

    if all_options_list is not None and all_options_list:
        # Create a dictionary to store the key-value pairs
        options_dict = {}

        # Iterate over the pairs and populate the dictionary
        for pair in all_options_list:
            # Check if the pair is not None
            if pair is not None:
                # Split the pair by ":" and handle potential errors
                try:
                    key, value = pair.split(":")
                    options_dict[key] = value
                except ValueError:
                    print(f"Error processing pair: {pair}")

        # Print the resulting dictionary
        print(options_dict)
    else:
        print("all_options_list is None or empty.")

    return options_dict

#----------------------------------------------------------------
def percentage_options_multiple_columns(df_data,options_columns,options_names,selected_code):
    
     # select the columns that will be counted.
    df = df_data[options_columns]

    # Count occurrences of the number 2 in each column
    count_selected = np.array([len(df[df[x]==selected_code]) for x in options_columns])
    total_count = sum(count_selected)
    if(total_count==0):
        return pd.DataFrame()
    else:
        count_column = np.append(count_selected,total_count)
        percentages = np.round((count_column / total_count) * 100,2)
        percentages_formatted = ["%.2f" % member for member in percentages]

        options_names=np.append(options_names,["TOTAL"])

        # Create a summary DataFrame
        count_df = pd.DataFrame({
            'Option': options_names,
            'Count': count_column,
            'Percentage': percentages_formatted   
        })
    
        return count_df

#------------------------------------------------------------------------
def percentage_options_single_column(df_data,column_name,options_names,options_codes):
    """ Count the number of occurrences of code in a given column """
     # select the columns that will be counted.
    df = df_data
    
    # Count occurrences of the number 2 in each column
    count_selected = np.array([len(df[df[column_name]==code]) for code in options_codes])
    total_count = sum(count_selected)
    if(total_count==0):
        return pd.DataFrame()
    else:
        count_column = np.append(count_selected,total_count)
        percentages = np.round((count_column / total_count) * 100,2)
        percentages_formatted = ["%.2f" % member for member in percentages]

        options_names=np.append(options_names,["TOTAL"])

        # Create a summary DataFrame
        count_df = pd.DataFrame({
            'Option': options_names,
            'Count': count_column,
            'Percentage': percentages_formatted   
        })
    
        return count_df

#------------------------------------------------------------------------
def replace_code_for_name(data_frame,column_key, dictionary_for_column):
        
    #names = dictionary_for_column.values()
    keys = dictionary_for_column.keys()
        
    for key in keys:
        name = dictionary_for_column.get(key)
        data_frame[column_key]= data_frame[column_key].replace(key, name)
    
    return data_frame

#------------------------------------------------------------------------
        
        