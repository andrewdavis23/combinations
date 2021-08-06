import pandas as pd

def standard_sec_logic(row):
    if row['CasePack'] == 1:
        return row['CasePack'] * 3
    elif row['CasePack'] * 2 > row['Capacity']:
        return row['CasePack']
    else:
        return row['CasePack'] * 2

# PROBLEM EXAMPLES
# FLOAT VS INT:      SS Cycle 8 Meat Rack - Secondary Capacities.xlsx
# TWO HALVES         SS EOS - Back to School Bargain Aisle - Secondary Capacities.xlsx

program_file = 'Y:/CAO/Bargain Aisle-Secondary Caps/2021/programs/SS EOS - Back to School Bargain Aisle - Secondary Capacities.xlsx'

df_filter = pd.read_excel(program_file, sheet_name='tbl_Master_Filter')
df_caps = pd.read_excel(program_file, sheet_name='tbl_Pog_Capacity')

# make sure key columns are same datatype prior to merge
# df_caps['Size'] = df_caps['Size'].astype(int)
# df_caps['Size'] = df_caps['Size'].str.upper()
df_caps['Size'] = df_caps['Size'].astype(str).str.upper()
# df_filter['BA_Filter'] = df_filter['BA_Filter'].astype(int)
# df_filter['BA_Filter'] = df_filter['BA_Filter'].str.upper()
df_filter['BA_Filter'] = df_filter['BA_Filter'].astype(str).str.upper()

if not(df_filter['Kraft_Filter'].isna().all()):
    message += '\nSTOP! Kraft_Filter is not null.\nDo this program manually.'
    print_message(message, False)
df_filter = df_filter.drop(['Kraft_Filter'], axis=1)

# clean data. Prepare for matching BA_Filter to Size.
df_filter = df_filter[df_filter['BA_Filter'] != 'NO']
df_filter = df_filter.dropna()

# calculate secondary capacity, then drop columns
df_caps['Sec_Cap'] = df_caps.apply(standard_sec_logic, axis=1)
df_caps = df_caps.drop(['Capacity','CasePack'], axis=1)

halves = pd.read_excel(program_file, sheet_name='Items by Half', usecols='A:B')
first_in = halves[(halves['Half']=='First') | (halves['Half']=='Both')]['ItemNum']
first_out = halves[halves['Half']=='First']['ItemNum']
second_in = halves[halves['Half']=='Second']['ItemNum']
second_out = halves[(halves['Half']=='Second') | (halves['Half']=='Both')]['ItemNum']

# join the stores and items where half
# EITHER MERGE, THEN SELECT ITEM OR VICE VERSA
df_trans_first_in = pd.merge(df_caps.loc[(df_caps['Sec_Cap']>0) & (df_caps['Half']==1)], df_filter, how='inner', left_on=['Division','Size'], right_on=['Div','BA_Filter'])
df_trans_first_out = pd.merge(df_caps.loc[(df_caps['Sec_Cap']>0) & (df_caps['Half']==1)], df_filter, how='inner', left_on=['Division','Size'], right_on=['Div','BA_Filter'])
df_trans_second_in = pd.merge(df_caps.loc[(df_caps['Sec_Cap']>0) & (df_caps['Half']==2)], df_filter, how='inner', left_on=['Division','Size'], right_on=['Div','BA_Filter'])
df_trans_second_out = pd.merge(df_caps.loc[(df_caps['Sec_Cap']>0) & (df_caps['Half']==2)], df_filter, how='inner', left_on=['Division','Size'], right_on=['Div','BA_Filter'])

print('{}\n{}\n{}\n{}\n'.format(df_trans_first_in.shape,df_trans_first_out.shape,df_trans_second_in.shape,df_trans_second_out.shape))

df_trans_first_in[df_trans_first_in['ItemNum'].isin(first_in)]
df_trans_first_out[df_trans_first_out['ItemNum'].isin(first_out)]
df_trans_second_in[df_trans_second_in['ItemNum'].isin(second_in)]
df_trans_second_out[df_trans_second_out['ItemNum'].isin(second_out)]

print('{}\n{}\n{}\n{}\n'.format(df_trans_first_in.shape,df_trans_first_out.shape,df_trans_second_in.shape,df_trans_second_out.shape))
print(df_trans_first_in.head())
# print('Total Rows',df_trans_first_in.shape[0] + df_trans_first_out.shape[0] + df_trans_second_in.shape[0] + df_trans_second_out.shape)