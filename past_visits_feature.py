from pandas import DataFrame, Series, read_csv
from utils import *
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

end_date = 0

def days_after_last_active(group, df_info):
    member_num = most_common_element(group['Member number'])
    usage_dates = group['Usage date']
    
    last_active = df_info[df_info['Member number'] == member_num ]['Last Active'].iloc[0]
    last_active = last_active.strip()
    if len(last_active) == 10:
        last_active_date =  datetime.strptime(last_active, '%m/%d/%Y')
        num_days = 9999
        for i in range(0, len(usage_dates)):
            usage_date_str = usage_dates.iloc[i]
            usage_date_str = usage_date_str.strip()
            if len(usage_date_str) < 10:
                continue
            else:
                usage_date = datetime.strptime(usage_date_str, '%m/%d/%Y')
                if usage_date <= end_date:
                    length = np.math.floor((end_date - usage_date).total_seconds()/(60*60*24))
                    if num_days > length:
                        num_days = length

        num_days_norm = 1.0 - normalize(num_days, 20.0)
        return Series([num_days_norm], index =['days_after_last_active'])
    else:
        return Series([0.0], index =['days_after_last_active'])

def past_visits_num(group):
    member_num = most_common_element(group['Member number'])
    usage_dates = group['Usage date']
        
    start_date_7d = end_date - timedelta(7)
    start_date_14d = end_date - timedelta(14) 
    start_date_30d = end_date - timedelta(30)
    start_date_60d = end_date - timedelta(60)
    start_date_90d = end_date - timedelta(90)

    count_7d = 0
    count_14d = 0
    count_30d = 0
    count_60d = 0
    count_90d = 0
    
    for i in range(0, len(usage_dates)):
        usage_date_str = usage_dates.iloc[i]
        usage_date_str = usage_date_str.strip()
        if len(usage_date_str) < 8:
            continue
        else:
            usage_date = datetime.strptime(usage_date_str, '%m/%d/%Y')
        if usage_date >= start_date_7d and usage_date <= end_date:
            count_7d = count_7d + 1
        if usage_date >= start_date_14d and usage_date <= end_date:
            count_14d = count_14d + 1
        if usage_date >= start_date_30d and usage_date <= end_date:
            count_30d = count_30d + 1
        if usage_date >= start_date_60d and usage_date <= end_date:
            count_60d = count_60d + 1
        if usage_date >= start_date_90d and usage_date <= end_date:
            count_90d = count_90d + 1 

        f_7d = normalize(count_7d, 4.0)
        f_14d = normalize(count_14d, 7.0)
        f_30d = normalize(count_30d, 15.0)
        f_60d = normalize(count_60d, 30.0)
        f_90d = normalize(count_90d, 45.0)

    return Series([f_7d, f_14d, f_30d, f_60d, f_90d], 
                  index = ['visits_07d', 'visits_14d', 'visits_30d', 'visits_60d', 'visits_90d'])


def f_club_regularity(group):
    member_num = most_common_element(group['Member number'])
    clubs = [11, 12, 13, 15, 19, 20, 23, 25, 41, 50, 84, 93]
    club_dict = {11:0, 12:0, 13:0, 15:0, 19:0, 20:0, 23:0, 25:0, 41:0, 50:0, 84:0, 93:0, -1:0}
    
    usage_clubs = group['Usage club']
    for i in range(1, len(usage_clubs)):
        club_num = usage_clubs.iloc[i]
        if club_num in clubs:
            club_dict[club_num] = club_dict[club_num] + 1
        else:
            club_dict[-1] = club_dict[-1] + 1
     
    values = club_dict.values()
    total_visits = sum(values)
    entropy = 0
    for k in range(1, len(values)):
        if values[k] > 0:
            p = float(values[k])/total_visits
            entropy = entropy - np.log2(p) * p
    regularity = 1.0 - normalize(entropy, 0.5)
    return Series([regularity], index =['club_regularity'])  


def load_past_visits_feature(index):
    df_info = load_info_file(index)
    df_checkins = load_checkins_file(index)

    global end_date
    end_date = datetime(2008 + index, 3, 1)

    df_grouped_member_num = df_checkins.groupby('Member number')
    df_visits = df_grouped_member_num.apply(past_visits_num)
    df_visits.to_csv('../clubOne/data/features/p'+ str(index) +'_f_past_visits.csv', index=False)


def load_day_num_last_visit_feature(index):
    df_info = load_info_file(index)
    df_checkins = load_checkins_file(index)

    global end_date
    end_date = datetime(2008 + index, 3, 1)
    df_grouped_member_num = df_checkins.groupby('Member number')
    df_last_visit = df_grouped_member_num.apply(days_after_last_active, df_info)
    df_last_visit.to_csv('../clubOne/data/features/p'+ str(index) +'_f_num_days_last_active.csv', index=False)


def load_club_regularity_feature(index):
    df_info = load_info_file(index)
    df_checkins = load_checkins_file(index)

    df_grouped_member_num = df_checkins.groupby('Member number')
    df_club_regularity = df_grouped_member_num.apply(f_club_regularity)
    df_club_regularity.to_csv('../clubOne/data/features/p'+ str(index) +'_f_club_regularity.csv', index=False)





