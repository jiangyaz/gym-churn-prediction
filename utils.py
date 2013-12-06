from pandas import DataFrame, Series, read_csv
from datetime import datetime
from datetime import timedelta
from collections import Counter

def load_info_file(index):
    df_info_file     = '../clubOne/data/info/p' + str(index) + '_info.csv'
    col_info = [ 'index', 'Member number','Cancel reason','DOB','Cancel date','Join date','Last Active',
                'Home club','Profile create', 'M/F', 'Type', 'Status']
    df_info = read_csv(df_info_file, index_col = 0, names = col_info, dtype={'Member number': object}, skiprows = 1)
    df_info = df_info.set_index(['Member number'])
    return df_info

def load_checkins_file(index):
    df_checkins_file = '../clubOne/data/info/p' + str(index) + '_checkins.csv'
    col_checkins = ['Home club','Member number','Membership type','Membership status',
                    'Member join date','Profile create date','Cancel date','Cancel reason',
                    'Gender','Date of birth','Usage club','Usage date','Usage time','TID']
    df_checkins = read_csv(df_checkins_file, index_col = 0, names = col_checkins, dtype={'Member number': object}, skiprows = 1)
    return df_checkins

def most_common_element(list):
    count = Counter(list)
    return count.most_common(1)[0][0]

def most_recent_date(list):
    most_recent = datetime(1900, 1, 1)
    for i in range(0, len(list)):
        date = datetime.strptime(list.iloc[i], '%m/%d/%Y')
        if most_recent < date:
            most_recent = date
    return most_recent.strftime('%m/%d/%Y')

def normalize(number, max):
	if number > max:
		return 1.0
	else: 
		return float(number)/max

def empty_date_table():
    date_keys = []
    for i in range(2008, 2014):
        for j in range(1, 53):
            key = str(i) + str(j).zfill(2)
            date_keys.append(key)
    return Series([0] * len(date_keys), index = date_keys)

def get_year_week(date):
    return str(date.isocalendar()[0]) + str(date.isocalendar()[1]).zfill(2)  
