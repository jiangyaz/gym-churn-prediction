from pandas import DataFrame, Series, read_csv
from utils import *
import pandas as pd
import numpy as np

user_checkins_1 = '../clubOne/data/05-08_05-09.txt'
user_checkins_2 = '../clubOne/data/06-09_to_05-10.txt'
user_checkins_3 = '../clubOne/data/06-10_to_05-11.txt'
user_checkins_4 = '../clubOne/data/06-11_to_05-12.txt'
user_checkins_5 = '../clubOne/data/06-12_to_05-13.txt'

column_names = ['Home club','Member number','Membership type','Membership status',
                'Member join date','Profile create date','Cancel date','Cancel reason',
                'Gender','Date of birth','Usage club','Usage date','Usage time','TID']
df_checkins1 = read_csv(user_checkins_1, names = column_names, 
                        dtype={'Member number': object,'Usage time': object}, skiprows = 1)
df_checkins2 = read_csv(user_checkins_2, names = column_names, 
                        dtype={'Member number': object,'Usage time': object}, skiprows = 1)
df_checkins3 = read_csv(user_checkins_3, names = column_names, 
                        dtype={'Member number': object,'Usage time': object}, skiprows = 1)
df_checkins4 = read_csv(user_checkins_4, names = column_names,
                        dtype={'Member number': object,'Usage time': object}, skiprows = 1)
df_checkins5 = read_csv(user_checkins_5, names = column_names, 
                        dtype={'Member number': object,'Usage time': object}, skiprows = 1)

# Combine all the 5 files to one dataframe (data range: May 2008 - May 2013)
df_checkins_raw = pd.concat([df_checkins1, df_checkins2, df_checkins3, df_checkins4, df_checkins5])

# Remove confusion/duplications for membership status and cancel reason column
df_checkins_cleaned = df_checkins_raw.replace({
                        'Membership status': {'a ': 'A', 'A ': 'A', 'C ': 'C', ' c': 'C', 'c ': 'C',
                                              'R ': 'R', 'L ': 'L', 'H ': 'H', 'P ': 'P', 'S ': 'S',
                                              'F ': 'F', 'V ': 'V'},
                        'Cancel reason': { 'mov': 'MOV', 'not': 'NOT', 'n/g': 'N/G', 'inc': 'INC', 
                                           'oth': 'OTH', 'dro': 'DRO', 'job': 'JOB', 'med': 'MED',
                                           'com': 'COM', '10D': '10d', 'fin': 'FIN', 'N/g': 'N/G',
                                           'err': 'ERR', 'tra': 'TRA', 'dis': 'DIS', 'zzZ': 'ZZZ',
                                           'zzz': 'ZZZ', 'Mov': 'MOV', 'hme': 'HME', 'DRo': 'DRO',
                                           'exp': 'EXP', 'tRA': 'TRA', 'T  ': 'TRA', 'emp': 'EMP',
                                           'OC ': 'OC',  'dec': 'DEC', 'coM': 'COM', 'TRa': 'TRA',
                                           'oTH': 'OTH', 'pen': 'PEN', 'Oth': 'OTH', 'bad': 'BAD',
                                           'lot': 'LOT', 'mil': 'MIL', 'EXp': 'EXP', 'drO': 'DRO',
                                           'cls': 'CLS', 'zZZ': 'ZZZ', 'dRO': 'DRO', 'n/G': 'N/G' }
                       })

remove = ['ACC', 'OC', 'PRF', 'N/C', 'XFR', 'LOT', 'CLS', 'MIL', 'BAD', 'EMP', 'PEN', 'DEC', 'ERR', '10d']
df_checkins = df_checkins_cleaned[~df_checkins_cleaned['Cancel reason'].isin(remove)]

print len(df_checkins_cleaned)
print len(df_checkins)

# Convert the member checkins info to member profile info.
df_grouped_member_num = df_checkins.groupby('Member number')
df_info = df_grouped_member_num.agg({ 	'Home club': lambda x: most_common_element(x), 
                                    	'Member number': lambda x: most_common_element(x),
                                    	'Membership type': lambda x: most_common_element(x),
                                    	'Membership status': lambda x: most_common_element(x),
                                    	'Member join date': lambda x: most_common_element(x),
                                    	'Profile create date': lambda x: most_common_element(x),
                                    	'Cancel date': lambda x: most_common_element(x),
                                    	'Cancel reason': lambda x: most_common_element(x),
                                    	'Gender': lambda x: most_common_element(x),
                                    	'Date of birth': lambda x: most_common_element(x),
                                    	'Usage date': lambda x: most_recent_date(x)
                                 	})

# Save both files to csv file.
df_info.to_csv('../clubOne/data/df_info_new.csv')
df_checkins.to_csv('../clubOne/data/df_checkins_new.csv')


