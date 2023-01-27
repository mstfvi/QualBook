import os
import json
import pandas as pd

batch_size = 5000

last_project_crawled = 0 * 1000
last_project_to_be_crawled = 180 * 1000

# location of notebooks
path = 'data/KGT_dataset/'
directory = os.fsencode(path)

# Concatenate all str variables in a list and create a final long string
def list_to_str(ls):
    tmp = ''
    for x in ls:
        tmp += x
    return tmp


# define dataframes for markdown and codes separately
df_codes = pd.DataFrame(
    columns=['project_name', 'project_ID', 'cell_index', 'source', 'output_type', 'output', 'execution_count'])
df_markdown = pd.DataFrame(columns=['project_name', 'project_ID', 'cell_index', 'source'])
print(df_markdown)
print(df_codes)

# this df consist of two column which contains filename and a brief description of error
df_exceptions = pd.DataFrame(columns=['project_name', 'section'])

# make a unique combination for each row that could be our primary key for final dataframe.
name_to_id = pd.read_csv('data/project_name_ID.csv')
name_to_id = name_to_id.set_index('project_name')

# read files in a loop and extract their information
file_counter = 0
for file in os.listdir(directory):

    file_counter += 1
    if file_counter <= last_project_crawled:
        continue
    filename = os.fsdecode(file)
    try:
        project_ID = name_to_id.loc[filename]['KId']
    except:
        df_tmp = pd.DataFrame(
            {'project_name': filename, 'section': 'assigning ID'}, index=[0])
        df_exceptions = pd.concat([df_exceptions, df_tmp], ignore_index=True, axis=0)
        project_ID = None

    # Opening file section
    try:
        f = open(path + filename, encoding="utf8")
        data = json.load(f)
        print(file_counter, filename)
    except:
        df_tmp = pd.DataFrame(
                    {'project_name': filename, 'section': 'opening file'}, index=[0])
        df_exceptions = pd.concat([df_exceptions, df_tmp], ignore_index=True, axis=0)
        continue

    cnt_cell = 0
    for cell in data['cells']:
        cnt_cell += 1
        try:
            string_src = cell['source']
        except:
            df_tmp = pd.DataFrame(
                {'project_name': filename, 'section': 'cell[\'source\']'}, index=[0])
            df_exceptions = pd.concat([df_exceptions, df_tmp], ignore_index=True, axis=0)
            continue

        if type(string_src) is list:
            string_src = list_to_str(string_src)

        if cell['cell_type'] == 'code':
            try:
                output_type = cell['outputs'][0]['output_type']
                if output_type == 'stream':
                    output = cell['outputs'][0]['text']
                elif output_type == 'display_data':
                    output = cell['outputs'][0]['data']['text/plain']
                elif output_type == 'execute_result':
                    output = cell['outputs'][0]['data']['text/plain']
                elif output_type == 'error':
                    output = cell['outputs'][0]['ename']
                else:
                    output = None
                if type(output) is list:
                    output = list_to_str(output)
            except:
                output_type = None
                output = None

            try:
                df_tmp = pd.DataFrame(
                    {'project_name': filename, 'project_ID': project_ID, 'cell_index': cnt_cell, 'source': string_src, 'output_type': output_type,
                     'output': output, 'execution_count': cell['execution_count']}, index=[0])
                df_codes = pd.concat([df_codes, df_tmp], ignore_index=True, axis=0)
            except:
                df_tmp = pd.DataFrame(
                    {'project_name': filename, 'section': 'appending code cell'}, index=[0])
                df_exceptions = pd.concat([df_exceptions, df_tmp], ignore_index=True, axis=0)

        elif cell['cell_type'] == 'markdown':
            try:
                df_tmp = pd.DataFrame(
                    {'project_name': filename, 'project_ID': project_ID, 'cell_index': cnt_cell, 'source': string_src},
                    index=[0])
                df_markdown = pd.concat([df_markdown, df_tmp], ignore_index=True, axis=0)
            except:
                df_tmp = pd.DataFrame(
                    {'project_name': filename, 'section': 'appending markdown cell'}, index=[0])
                df_exceptions = pd.concat([df_exceptions, df_tmp], ignore_index=True, axis=0)
        else:
            f.close()
            continue

    f.close()

    if file_counter % batch_size == 0:
        print('#################### saving file #####################')
        bach_counter = 'batch_' + str(file_counter // batch_size + 1) + '.csv'
        df_codes.to_csv('1.code_batches/code_' + bach_counter, index=False)
        df_markdown.to_csv('2.markdown_batches/markdown_' + bach_counter, index=False)
        df_codes = pd.DataFrame(
            columns=['project_name', 'project_ID', 'cell_index', 'source', 'output_type', 'output', 'execution_count'])
        df_markdown = pd.DataFrame(columns=['project_name', 'project_ID', 'cell_index', 'source'])
        break
    if file_counter >= last_project_to_be_crawled:
        break


bach_counter = 'batch_' + 'the_final' + '.csv'
df_codes.to_csv('1.code_batches/code_' + bach_counter, index=False)
df_markdown.to_csv('2.markdown_batches/markdown_' + bach_counter, index=False)
df_exceptions.to_csv('exception_files', index=False)