import sys

import numpy as np
import pandas as pd


def transform_to_single_row(inp_file, out_file):
    try:
        input_table = pd.read_csv(inp_file)
    except:
        print("Input file:", inp_file, "doesn't exist.")
        sys.exit(1)

    # create base case table and analysis types table 
    base_table = input_table[['Collection', 'Study ID', 'Subject ID', 'Image ID']].copy()
    base_table = base_table.drop_duplicates()
    base_table = base_table.reset_index()
    types_table = input_table[['Analysis type']]
    types_table = types_table.drop_duplicates()
    types_table = types_table.reset_index()

    # find all analysis types
    analysis_type_columns = list(types_table["Analysis type"])
    print('Analysis types: ', analysis_type_columns)

    # count the maximum number of instances for each analysis type
    print("Counting the maximum number of analysis type instances.")
    max_type_count = {}
    for i in analysis_type_columns:
        max_type_count[i] = 0
    for index, row in base_table.iterrows():
        row_filter = (input_table['Collection'] == row['Collection'])
        row_filter = row_filter & (input_table['Study ID'] == row['Study ID'])
        row_filter = row_filter & (input_table['Subject ID'] == row['Subject ID'])
        row_filter = row_filter & (input_table['Image ID'] == row['Image ID'])
        case_table = input_table.loc[row_filter]
        type_count = {}
        for i in analysis_type_columns:
            type_count[i] = 0
        a_list = []
        for index2, row2 in case_table.iterrows():
            analysis_type = str(row2['Analysis type'])
            if analysis_type == 'Human':
                h_list = str(row2['Execution ID']).split('_')
                h_id = ''
                for ii in range(len(h_list) - 2):
                    h_id = h_id + str(h_list[ii]) + '_'
                h_id = h_id + str(h_list[len(h_list) - 2])
                if h_id not in a_list:
                    a_list.append(h_id)
                    type_count[analysis_type] = type_count[analysis_type] + 1
            else:
                type_count[analysis_type] = type_count[analysis_type] + 1
        for i in analysis_type_columns:
            if type_count[i] > max_type_count[i]:
                max_type_count[i] = type_count[i]
    print('Maximum number of analysis type instances: ', max_type_count)

    expanded_columns = []
    for i in analysis_type_columns:
        for j in range(max_type_count[i]):
            expanded_columns.append(str(i) + "_" + str(j))

    cols = ['Collection', 'Study ID', 'Subject ID', 'Image ID']
    for i in expanded_columns:
        cols.append(i)
    print('Output CVS columns: ', cols)

    out_table = pd.DataFrame(columns=cols)

    total_cnt = len(base_table)
    for index, row in base_table.iterrows():
        print('Processing: ', index + 1, 'out of ', total_cnt)
        row_filter = (input_table['Collection'] == row['Collection'])
        row_filter = row_filter & (input_table['Study ID'] == row['Study ID'])
        row_filter = row_filter & (input_table['Subject ID'] == row['Subject ID'])
        row_filter = row_filter & (input_table['Image ID'] == row['Image ID'])
        case_table = input_table.loc[row_filter]
        out_table.at[index, 'Collection'] = row['Collection']
        out_table.at[index, 'Study ID'] = row['Study ID']
        out_table.at[index, 'Subject ID'] = row['Subject ID']
        out_table.at[index, 'Image ID'] = row['Image ID']
        type_count = {}
        for i in analysis_type_columns:
            type_count[i] = 0
        for index2, row2 in case_table.iterrows():
            analysis_type = str(row2['Analysis type'])
            if analysis_type != 'Human':
                analysis_type_col = analysis_type + "_" + str(type_count[analysis_type])
                out_table.at[index, analysis_type_col] = str(row2['Execution ID'])
                type_count[analysis_type] = type_count[analysis_type] + 1
            else:
                h_list = str(row2['Execution ID']).split('_')
                h_id = ''
                for i in range(len(h_list) - 2):
                    h_id = h_id + str(h_list[i]) + '_'
                h_id = h_id + str(h_list[len(h_list) - 2])
                if h_id not in a_list:
                    a_list.append(h_id)
                    analysis_type_col = analysis_type + "_" + str(type_count[analysis_type])
                    out_table.at[index, analysis_type_col] = h_id
                    type_count[analysis_type] = type_count[analysis_type] + 1

    out_table.to_csv(out_file, index=False)
    return
