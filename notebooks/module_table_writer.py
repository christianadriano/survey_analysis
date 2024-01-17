import pandas as pd
import numpy as np
import os as os
    
def display_value_counts(data_frame, question_id, question_title, filter_column=None, 
                         filter_value=None, count_by_column=None, column_format="@{}lcc"):

    if filter_column and filter_value:
        filtered_df = data_frame[data_frame[filter_column] == filter_value]
    else:
        filtered_df = data_frame
        
    print(filter_value)
    
    if(count_by_column== None):
        counts=0
        percentages=0
    else:
        counts = filtered_df[count_by_column].value_counts()
        percentages = round((counts / counts.sum()) * 100,2)
        
    formattedList = ["%.2f" % member for member in percentages]
    print(formattedList)
    data = {
        'Counts': counts,
        'Percentages': formattedList
    }
    count_df = pd.DataFrame(data)
    count_df.reset_index(inplace=True)

    latex_table = write_latex_table(count_df,False, filter_value, 
                                    question_id, question_title,column_format)
    return latex_table 

#-----------------------------------------
def write_latex_table(data_df, show_index, filter_value, 
                      question_id, question_title,column_format):
    """ Generate Latex table and save to file"""
    
    #if styles is not None:
    #    count_df = data_df.style.set_table_styles(styles)
    #else:
    #    count_df=data_df

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
    print("file_name" + file_name)
    
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
   
