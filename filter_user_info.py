from pandas import DataFrame, Series, read_csv
from user_health import *
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

def load_user_info(file_name, col_name):
	df_info = read_csv(file_name, names = col_name, dtype={'Member number': object}, skiprows = 1)
	df_info = df_info.drop('Member number dup', 1)
	return df_info

def load_user_checkins(file_name, col_name):
	df_checkins = read_csv(file_name, names = col_name, 
                        dtype={'Member number': object,'Usage time': object}, skiprows = 1)

	df_checkins_cleaned = df_checkins.replace({
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
	df_checkins_out = df_checkins_cleaned[~df_checkins_cleaned['Cancel reason'].isin(remove)]
	return df_checkins_out


user_info_file   = '../clubOne/data/df_info.csv'
user_checkins_p1 = '../clubOne/data/05-08_05-09.txt'
user_checkins_p2 = '../clubOne/data/06-09_to_05-10.txt'
user_checkins_p3 = '../clubOne/data/06-10_to_05-11.txt'
user_checkins_p4 = '../clubOne/data/06-11_to_05-12.txt'
user_checkins_p5 = '../clubOne/data/06-12_to_05-13.txt'

col_name_checkins = [	'Home club','Member number','Membership type','Membership status',
                      	'Member join date','Profile create date','Cancel date','Cancel reason',
                      	'Gender','Date of birth','Usage club','Usage date','Usage time','TID']

col_name_info = [	'Member number','Cancel reason','Date of birth','Cancel date','Member join date','Last Active',
             		'Home club', 'Member number dup','Profile create date', 'Gender', 'Membership type', 'Membership status']

# load member profile and checkin info
df_info = load_user_info(user_info_file, col_name_info)
df_checkins = load_user_checkins(user_checkins_p5, col_name_checkins)

# group checkin info based on member number and analyze user health
df_grouped_member_num = df_checkins.groupby('Member number')
df_visits = df_grouped_member_num.apply(user_health)

# filter out the healthy member profile, checkins and cancel/inactive info
df_healthy = df_visits[df_visits['healthy_now'] == 1]
filtered_id = set(df_healthy.index)
df_future_info = df_healthy.drop('healthy_now', 1)
df_user_info_h = df_info[df_info['Member number'].isin(filtered_id)]
df_user_checkins_h = df_checkins[df_checkins['Member number'].isin(filtered_id)]

print len(filtered_id)

# save the information to csv file
df_user_info_h.to_csv('../clubOne/data/out/p5_info.csv')
df_user_checkins_h.to_csv('../clubOne/data/out/p5_checkins.csv')
df_future_info.to_csv('../clubOne/data/out/p5_y.csv') 

