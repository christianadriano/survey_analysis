#Pre-Process data

import pandas as pd

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

#----------------------------------------------------------------
def count_percentages_options(filtered_df,options_columns,options_names,selected_code):
    
    # select the columns that will be counted.
    df_sum = filtered_df[options_columns]

    # Count occurrences of the number 2 in each column
    count_selected = df_sum(selected_code).sum()
    print(count_selected)

    total_count = df_sum.count()
    
    percentage_selected = (count_selected / total_count) * 100

    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        'Option': options_names,
        'Count': count_selected.values,
        'Percentage': percentage_selected.values
    })

    print(summary_df)
    
    #---------------------------------------------------------------