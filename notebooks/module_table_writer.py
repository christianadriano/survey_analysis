import pandas as pd
import numpy as np
import os as os
    
def display_value_counts(data_frame, question_id, question_title, filter_column=None, 
                         filter_value=None, styles=None,column_format="@{}lcc"):

    if filter_column and filter_value:
        filtered_df = data_frame[data_frame[filter_column] == filter_value]
    else:
        filtered_df = data_frame
        
    print(filter_value)
    
    counts = filtered_df['Options'].value_counts()
    percentages = round((counts / counts.sum()) * 100,2)
    formattedList = ["%.2f" % member for member in percentages]
    print(formattedList)
    data = {
        'Counts': counts,
        'Percentages': formattedList
    }
    count_df = pd.DataFrame(data)
    count_df.reset_index(inplace=True)
        
    if styles is not None:
        count_df_styled = count_df.style.set_table_styles(styles)
        display(count_df_styled)
    else:
        display(count_df)
    

    latex_table = write_latex_table(count_df,False, filter_value, 
                                    question_id, question_title,column_format)
    return latex_table 

#-----------------------------------------
def write_latex_table(data_df, show_index, filter_value, 
                      question_id, question_title,column_format):
    """ Generate Latex table and save to file"""
    table_caption=f'{filter_value} answers for {question_id}-{question_title}'
    label_name = f'{question_id}-{filter_value}_table'
    label_name = label_name.replace('(','')
    label_name = label_name.replace(')','')
    label_name = label_name.replace(',','')
    latex_table = data_df.to_latex(index=show_index,
                                    caption=table_caption, 
                                    label=label_name,
                                    column_format=column_format)
    return latex_table 

#-----------------------------------------

def table_to_file(df_data, tables_path, tables_file_name):

    if (not os.path.isdir(tables_path)):
        os.makedirs(tables_path)

    file_name = f'{tables_path}{tables_file_name}_tables.tex'
    
    if(not os.path.isfile(file_name)):
        with open(file_name, 'w') as out:
            out.write(f'%Data Tables for Question: {tables_file_name}\n')
            out.write("\\rowcolors{1}{}{lightgray}\n")
            out.write(df_data)
    else:
        with open(file_name, 'a') as out:
            out.write("%--------------------------------\n")
            out.write("\\rowcolors{1}{}{lightgray}\n")
            out.write(df_data)
   
#-----------------------------------------------------------------
def generate_options_dictionary(filtered_df):
    """LOAD Alternatives for the Question into a dictionary"""

    # Split the string into key-value pairs
    answer_options = filtered_df['Alternatives']

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