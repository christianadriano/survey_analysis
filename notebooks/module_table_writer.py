import pandas as pd
import numpy as np
import os as os
import module_data_wrangling as dw

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
   
#--------------------------------------------------------------------------------

def filter_write_table_single_column(group_column_key, dict_column_names, df,
                       options_names_list, options_code_list, 
                       question_id, question_title, tables_path, tables_file_name):
    # Filter by enrolled
    group_categories = dict_column_names.keys()

    for group_category in group_categories:
        filtered_df = df[df[group_column_key] == group_category]    
        if(filtered_df.size > 0):#ignores group_categories that are not present 
           
            count_df = dw.percentage_options_single_column(df_data=filtered_df,
                                column_name = question_id,
                                options_names=options_names_list,
                                options_codes=options_code_list)
            if(count_df.size > 0):
                group_name = dict_column_names.get(group_category)
                print('Table for '+'"{}"'.format(group_name))
    
                #Rename columns before printing
                count_df = count_df.rename(columns={count_df.columns[0]: 'Answers'})
                display(count_df)

                latex_table = write_latex_table(count_df,False, group_category, 
                                    question_id, question_title,column_format='@{}lcc')
                table_to_file(latex_table,tables_path,tables_file_name)
            else:
                print('Table for '+'"{}"'.format(group_name)+ 'is empty')
                    
#-------------------------------------------------------------------------------

def filter_write_table_multiple_column(group_column_key, dict_column_names, df,
                       options_names_list, options_columns_list, selected_code, 
                       question_id, question_title, tables_path, tables_file_name):
    
    # Filter by enrolled
    group_categories = dict_column_names.keys()

    for group_category in group_categories:
        filtered_df = df[df[group_column_key] == group_category]    
        if(filtered_df.size > 0):#ignores group_categories that are not present            
            count_df = dw.percentage_options_multiple_columns(df_data = filtered_df,
                                options_columns=options_columns_list,
                                options_names=options_names_list,
                                selected_code=selected_code)
            group_name = dict_column_names.get(group_category)
    
        #Rename columns before printing
        if(count_df.size > 0):
            print('Table for '+'"{}"'.format(group_name))
            count_df = count_df.rename(columns={count_df.columns[0]: 'Answers'})
            display(count_df)

            latex_table = write_latex_table(count_df,False, group_category, 
                                    question_id, question_title,column_format='@{}lcc')
            table_to_file(latex_table,tables_path,tables_file_name)
        else:
            print('Table for '+ '"{}"'.format(group_name)+' is empty')
#-------------------------------------------------------------------------------