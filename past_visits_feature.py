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

def calculate_last_visits(group, final_date):
    usage_dates = group['Usage date']  
    start_date_7d = final_date - timedelta(7)
    start_date_14d = final_date - timedelta(14) 
    start_date_30d = final_date - timedelta(30)
    start_date_60d = final_date - timedelta(60)
    start_date_90d = final_date - timedelta(90)

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
        if usage_date >= start_date_7d and usage_date <= final_date:
            count_7d = count_7d + 1
        if usage_date >= start_date_14d and usage_date <= final_date:
            count_14d = count_14d + 1
        if usage_date >= start_date_30d and usage_date <= final_date:
            count_30d = count_30d + 1
        if usage_date >= start_date_60d and usage_date <= final_date:
            count_60d = count_60d + 1
        if usage_date >= start_date_90d and usage_date <= final_date:
            count_90d = count_90d + 1 
        
        f_7d  = normalize(count_7d,   4.0)
        f_14d = normalize(count_14d,  7.0)
        f_30d = normalize(count_30d, 15.0)
        f_60d = normalize(count_60d, 30.0)
        f_90d = normalize(count_90d, 45.0)
        
    return [f_7d, f_14d, f_30d, f_60d, f_90d]

    
def past_visits_num(group):
    end_date_7d = end_date - timedelta(7)
    end_date_14d = end_date - timedelta(14)
    end_date_30d = end_date - timedelta(30)
    
    past_count =  calculate_last_visits(group, end_date)
    past_count_7d =  calculate_last_visits(group, end_date_7d)
    past_count_14d =  calculate_last_visits(group, end_date_14d)
    past_count_30d =  calculate_last_visits(group, end_date_30d)
    
    index_b0 = ['visits_07d', 'visits_14d', 'visits_30d', 'visits_60d', 'visits_90d']
    index_b7 = ['visits_07d_b7', 'visits_14d_b7', 'visits_30d_b7', 'visits_60d_b7', 'visits_90d_b7']
    index_b14 = ['visits_07d_b14', 'visits_14d_b14', 'visits_30d_b14', 'visits_60d_b14', 'visits_90d_b14']
    index_b30 = ['visits_07d_b30', 'visits_14d_b30', 'visits_30d_b30', 'visits_60d_b30', 'visits_90d_b30']
    
    return Series(past_count + past_count_7d + past_count_14d + past_count_30d, \
                  index = index_b0 + index_b7 + index_b14 + index_b30)


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


def absent_week_percent(week_stats):
    if len(week_stats) == 0:
        return 0
    else: 
        non_absent_week = sum(x > 0 for x in week_stats)
        return float(non_absent_week)/len(week_stats)


def average_usage(week_stats):
    if len(week_stats) == 0:
        return 0
    else:
        used_weeks = [x for x in week_stats if x > 0]
        avg_usage = np.mean(used_weeks)
        return normalize(avg_usage, 5.0)
  

def consec_no_use(week_stats):
    # print week_stats
    data = week_stats + [1]
    L = len(week_stats)
    if L == 0:
        return 0
    else:
        nonusage = []
        flag = False
        count = 0
        for i in range(0, L):
            val = data[L-1-i]
            if val == 0 and flag is True:
                count +=1
            elif val == 0 and flag is False:
                count +=1
                flag = True
            elif val > 0 and flag is True:
                nonusage.append([i+1 - count, count])
                count = 0
                flag = False
        
        score = 0
        for k in range(0, len(nonusage)):
            score = score + nonusage[k][1] * np.exp(-0.05 * nonusage[k][0])
        return 1.0 - normalize(score, 10)


def weekly_stats(group):
    member_num = most_common_element(group['Member number'])
    member_type = most_common_element(group['Membership status'])
    cancel_date_str = most_common_element(group['Cancel date']).strip()
    join_date_str = most_common_element(group['Member join date']).strip()
    
    year_weeks = group['Year week']
    
    if len(cancel_date_str) == 10:
        cancel_date = datetime.strptime(cancel_date_str, '%m/%d/%Y')
        if cancel_date < end_date:
            print 'Err: this member ' + str(member_num) + ' already cancelled!'
        
    # compute the start date
    if len(join_date_str) < 10:
        return []
    else:
        start_date = datetime.strptime(join_date_str, '%m/%d/%Y')
        if start_date < datetime(2008, 5, 1):
            start_date = datetime(2008, 5, 1)
            
    # check if the start date is earlier than end date
    if start_date > end_date:
        return []
    
    start_year_week = get_year_week(start_date)
    end_year_week = get_year_week(end_date)
    counts = year_weeks.value_counts()
    
    date_table = empty_date_table()
    for i in range(0, len(counts)):
        if counts.index[i] in date_table.index:
            date_table.ix[counts.index[i]] = counts.values[i]
    date_table_select = date_table[start_year_week:end_year_week]
    
    return list(date_table_select.values)

def checkins_year_week(row):
    usage_date_str = row['Usage date'].strip()
    if len(usage_date_str) < 10:
        return '-'
    else:
        usage_date = datetime.strptime(usage_date_str, '%m/%d/%Y')
        return str(usage_date.isocalendar()[0]) + str(usage_date.isocalendar()[1]).zfill(2)  


def load_past_visits_feature(index):
    global end_date
    end_date = datetime(2008 + index, 3, 1)

    df_info = load_info_file(index)
    df_checkins = load_checkins_file(index)

    df_grouped_member_num = df_checkins.groupby('Member number')
    df_visits = df_grouped_member_num.apply(past_visits_num)
    df_visits.to_csv('../clubOne/data/features/p'+ str(index) +'_f_past_visits.csv', index=False)


def load_day_num_last_visit_feature(index):
    global end_date
    end_date = datetime(2008 + index, 3, 1)

    df_info = load_info_file(index)
    df_checkins = load_checkins_file(index)

    df_grouped_member_num = df_checkins.groupby('Member number')
    df_last_visit = df_grouped_member_num.apply(days_after_last_active, df_info)
    df_last_visit.to_csv('../clubOne/data/features/p'+ str(index) +'_f_num_days_last_active.csv', index=False)


def load_club_regularity_feature(index):
    df_info = load_info_file(index)
    df_checkins = load_checkins_file(index)

    df_grouped_member_num = df_checkins.groupby('Member number')
    df_club_regularity = df_grouped_member_num.apply(f_club_regularity)
    df_club_regularity.to_csv('../clubOne/data/features/p'+ str(index) +'_f_club_regularity.csv', index=False)


def load_weekly_visit_feature(index):
    global end_date
    end_date = datetime(2008 + index, 3, 1)

    df_info = load_info_file(index)
    df_checkins = load_checkins_file(index)
    df_checkins['Year week'] = df_checkins.apply(checkins_year_week, axis = 1)
    
    gp_checkins_id = df_checkins.groupby(['Member number'])
    df_info['weekly visits'] = gp_checkins_id.apply(weekly_stats)

    absent_percent = df_info['weekly visits'].apply(absent_week_percent)
    avg_usage = df_info['weekly visits'].apply(average_usage)
    no_use = df_info['weekly visits'].apply(consec_no_use)

    df_f_week_stats = DataFrame({   'Absent percentage': absent_percent, \
                                    'Average active usage' : avg_usage, \
                                    'Consecutive nonusage': no_use })

    df_f_week_stats.to_csv('../clubOne/data/features/p'+ str(index) +'_f_week_stats.csv', index=False)











