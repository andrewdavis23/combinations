from tkinter import *
# from numpy import right_shift
from tkcalendar import *
from tkinter import filedialog
from datetime import date
import pandas as pd
import os

# user will have to pick the outdate as the day before 
# (i.e. the date of the evening that the sec is removed)

current_year = date.today().year
current_month = date.today().month
current_day = date.today().day
date_1 = ''
date_2 = ''

in_out = 0
prog_size = 0
program_folder = ''
program_file = ''

df_event = pd.DataFrame()
df_filter = pd.DataFrame()
df_caps = pd.DataFrame()

def standard_sec_logic(row):
    if row['CasePack'] == 1:
        return row['CasePack'] * 3
    elif row['CasePack'] * 2 > row['Capacity']:
        return row['CasePack']
    else:
        return row['CasePack'] * 2

def print_message(message, delete):
    if delete:
        files_txt.config(state=NORMAL)
        files_txt.delete('1.0', END)
        files_txt.insert(END, message)
        files_txt.config(state=DISABLED)
    else:
        files_txt.config(state=NORMAL)
        files_txt.insert(END, message)
        files_txt.config(state=DISABLED)

def load_program():
    global prog_size
    message = ''
    global program_folder
    global program_file
    global df_event
    global df_filter
    global df_caps

    # User picks program file, return if user cancels fialdialog ''
    program_file = filedialog.askopenfilenames()
    if program_file == '': return
    program_file = program_file[0]

    # extract folder and program name
    program_folder = os.path.dirname(program_file)

    # Process each sheet in workbook
    try:
        df_event = pd.read_excel(program_file, sheet_name='tbl_Event',)
        df_filter = pd.read_excel(program_file, sheet_name='tbl_Master_Filter')
        df_caps = pd.read_excel(program_file, sheet_name='tbl_Pog_Capacity')
        message += '\nSuccessfully loaded data from\n   {}\n'.format(os.path.basename(program_file))
        message += '\n# of (rows, columns) loaded:\n'
        message += '   {} in Event Data\n'.format(df_event.shape)
        message += '   {} in Store Data\n'.format(df_filter.shape)
        message += '   {} in Capacity Data\n'.format(df_caps.shape)
        message += '\nFilter sizes {}'.format(df_filter['BA_Filter'].unique())
        message += '          Caps sizes {}\n'.format(df_caps['Size'].unique())
    except:
        message += '\nFailed to load data from\n   {}\n'.format(os.path.basename(program_file))

    # check kraft filter for not null, then drop column
    if not(df_filter['Kraft_Filter'].isna().all()):
        message += '\nSTOP! Kraft_Filter is not null.\nDo this program manually.'
        print_message(message, False)
    df_filter = df_filter.drop(['Kraft_Filter'], axis=1)

    # some stats about the program
    prog_size = len(list(df_event.Half.unique()))
    message += '\n1 part or 2 part program: {}'.format(prog_size)

    print_message(message, True)

def produce_file():
    # clean data, calculate secondary capacity, create trans files for program, save files
    global program_folder
    global prog_size
    global df_event
    global df_filter
    global df_caps
    global date_1
    global date_2
    message = ''

    # clean data. Prepare for matching BA_Filter to Size.
    df_filter = df_filter[df_filter['BA_Filter'] != 'NO']
    df_filter = df_filter.dropna()

    print('\n{}\n{}\n{}\n'.format('CAPS '*20,df_caps['Size'].unique(),df_caps.dtypes['Size']))
    print('\n{}\n{}\n{}\n'.format('FLTR '*20,df_filter['BA_Filter'].unique(),df_filter.dtypes['BA_Filter']))

    # df_caps['Size'] = df_caps['Size'].astype(int)
    df_caps['Size'] = df_caps['Size'].str.upper()
    # df_filter['BA_Filter'] = df_filter['BA_Filter'].astype(int)
    df_filter['BA_Filter'] = df_filter['BA_Filter'].str.upper()

    print('\n{}\n{}\n{}\n'.format('CAPS '*20,df_caps['Size'].unique(),df_caps.dtypes['Size']))
    print('\n{}\n{}\n{}\n'.format('FLTR '*20,df_filter['BA_Filter'].unique(),df_filter.dtypes['BA_Filter']))

    # calculate secondary capacity, then drop columns
    df_caps['Sec_Cap'] = df_caps.apply(standard_sec_logic, axis=1)
    df_caps = df_caps.drop(['Capacity','CasePack'], axis=1)

    if prog_size == 1:
        if date_1 == '':
            message += 'ENTER OUT DATE 1 (USE EVENING REMOVAL DATE)'
            print_message(message, False)
            return

        # join the stores and items where half
        df_trans_in = pd.merge(df_caps.loc[(df_caps['Sec_Cap']>0) & (df_caps['Half']==1)], df_filter, how='inner', left_on=['Division','Size'], right_on=['Div','BA_Filter'])
        
        # drop columns not needed in transmission file
        df_trans_in = df_trans_in.drop(['Half','Size','Division','Div','BA_Filter'], axis=1)

        # add/rename columns needed in transmission file
        df_trans_in = df_trans_in.rename(columns={'StoreNum': 'STR_NUM', 'ItemNum': 'REF_NUM', 'Sec_Cap':'STR_MAINT_NUM'})
        df_trans_in.insert(0,'STR_MAINT_TRANS_ID','')
        df_trans_in['STR_ID'] = df_trans_in['STR_NUM']
        df_trans_in['STR_MAINT_TRANS_CD'] = 'IPSC'
        df_trans_in['STR_MAINT_CD'] = 'N'
        df_trans_in['STR_MAINT_CHAR_TXT'] = '(null)'
        df_trans_in['PRCS_CD'] = 'T'
        df_trans_in['USER_ID'] = 'nuajd15'
        df_trans_in['CRT_TS'] = '(null)'
        #'2020/12/17:03:49:00 PM' pd.datetime being buggy
        # will have to get using look up half=2....
        p_start = df_event.iloc[0,0]
        p_year = str(p_start.year)
        p_month = str(p_start.month).rjust(2,'0')
        p_day = str(p_start.day-1).rjust(2,'0')
        p_in = p_year+'/'+p_month+'/'+p_day+':03:49:00 PM'
        df_trans_in['PRCS_TS'] = p_in

        # reorder columns
        df_trans_in = df_trans_in.reindex(columns = ['STR_MAINT_TRANS_ID','STR_ID','STR_NUM','REF_NUM','STR_MAINT_TRANS_CD','STR_MAINT_NUM','STR_MAINT_CD','STR_MAINT_CHAR_TXT','PRCS_CD','USER_ID','CRT_TS','PRCS_TS'])

        # copy out file from in
        df_trans_out = df_trans_in.copy()
        df_trans_out['STR_MAINT_NUM'] = 0
        p_out = date_1+':03:49:00 PM'
        df_trans_out['PRCS_TS'] = p_out

        # save files
        fp = program_folder + '/' + df_event.iloc[0,2]
        df_trans_in.to_csv('{} IN.txt'.format(fp), sep='\t', index=False)
        df_trans_out.to_csv('{} OUT.txt'.format(fp), sep='\t', index=False)
        message += '\nIN {}          OUT {}\n'.format(p_in, p_out)        
        message += '\n\nIn-file saved to\n   {} IN.txt\n   # of rows = {}'.format(fp,df_trans_in.shape[0])
        message += '\n\nOut-file saved to\n   {} OUT.txt\n   # of rows = {}'.format(fp,df_trans_out.shape[0])

    elif prog_size == 2:
        if date_1 == '' | date_2 == '':
            message += 'ENTER OUT DATE 1 (USE EVENING REMOVAL DATE)'
            print_message(message, False)
            return

        df_first_items_only = pd.read_excel(program_file, sheet_name='Items by Half', usecols='A:B')
        df_second_items_only = pd.read_excel(program_file, sheet_name='Items by Half', usecols='A:B')

        # join the stores and items where half
        df_trans_first_in = pd.merge(df_caps.loc[(df_caps['Sec_Cap']>0) & (df_caps['Half']==1)], df_filter, how='inner', left_on=['Division','Size'], right_on=['Div','BA_Filter'])
        # df_trans_first_out =
        # only_1 = df[df['half']==1]. merge(df[df['half']==2],how='left',on='item')
        # only_1 = only_1[only_1['half_y'].isna()]
        # df_trans_second_in = 
        df_trans_second_out = pd.merge(df_caps.loc[(df_caps['Sec_Cap']>0) & (df_caps['Half']==2)], df_filter, how='inner', left_on=['Division','Size'], right_on=['Div','BA_Filter'])
        
        # drop columns not needed in transmission file
        df_trans_in = df_trans_in.drop(['Half','Size','Division','Div','BA_Filter'], axis=1)

    else:
        message += '\nProgram size not 1 or 2. Prep this one manually.\n'

    print_message(message, False)

def get_date_1():
    global date_1
    date_1 = cal.get_date()
    out_label_1.config(text=date_1)
   
def get_date_2():
    global date_2
    date_2 = cal.get_date()
    out_label_2.config(text=date_2)

root = Tk()
root.title('Secondary Transaction Creator')
root.geometry('900x450')

left_frame = Frame(root)
left_frame.grid(row=0, column=0)

right_frame = Frame(root)
right_frame.grid(row=0, column=1)

right_up = Frame(right_frame)
right_up.grid(row=0, column=0)

right_down = Frame(right_frame)
right_down.grid(row=1, column=0)

cal = Calendar(left_frame, selectmode='day', date_pattern='yyyy/mm/dd', year=current_year, month=current_month, day=current_day)
cal.grid(row=0, column=0, columnspan=2)

butt_1 = Button(left_frame, text='Select Out Date - Half 1', command=get_date_1)
butt_1.grid(row=1, column=1)

butt_2 = Button(left_frame, text='Select Out Date - Half 2', command=get_date_2)
butt_2.grid(row=2, column=1)

out_label_1 = Label(left_frame, text='')
out_label_1.grid(row=1, column=0)

out_label_2 = Label(left_frame, text='')
out_label_2.grid(row=2, column=0)

files_txt = Text(right_up)
files_txt.pack()

load_button = Button(right_down, text='Select Secondary\nProgram File', command=load_program)
load_button.grid(row=0, column=0, sticky='nsew', padx=2)

pro_button = Button(right_down, text='Produce\nTransaction Files', command=produce_file)
pro_button.grid(row=0, column=1, sticky='nsew', padx=2)

root.mainloop()
