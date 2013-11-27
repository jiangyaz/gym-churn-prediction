from pandas import DataFrame, Series
from collections import Counter
from datetime import datetime
from datetime import timedelta

start_date = datetime(2012, 6, 1)
end_date   = datetime(2013, 3, 1)

start_date_60d = end_date - timedelta(60)
start_date_90d = end_date - timedelta(90)
end_date_14d   = end_date + timedelta(14)
end_date_30d   = end_date + timedelta(30)
end_date_60d   = end_date + timedelta(60)
end_date_90d   = end_date + timedelta(90)

def most_common_element(list):
    count = Counter(list)
    return count.most_common(1)[0][0]

def user_health(group):
    member_num = most_common_element(group['Member number'])
    member_cancel = most_common_element(group['Cancel date']).strip()
    member_join = most_common_element(group['Member join date']).strip()
    usage_dates = group['Usage date']

    thre_unhealthy = 3
    cancel_14d = 0
    cancel_30d = 0
    cancel_60d = 0
    cancel_90d = 0
    unhealthy_14d = 0
    unhealthy_30d = 0
    unhealthy_60d = 0
    unhealthy_90d = 0
    
    if len(member_join) == 10 and datetime.strptime(member_join,'%m/%d/%Y') <= (end_date - timedelta(90)):
        if len(member_cancel) == 10 and datetime.strptime(member_cancel,'%m/%d/%Y') <= end_date:
            # member already cancelled 
            healthy_now = 0
        else:
            # check if the user has cancelled in next 14d, 30d, 60d, 90d
            if len(member_cancel) == 10:
                cancel_date = datetime.strptime(member_cancel,'%m/%d/%Y')
                if cancel_date <= (end_date + timedelta(14)):
                    cancel_14d = 1
                if cancel_date <= (end_date + timedelta(30)):
                    cancel_30d = 1
                if cancel_date <= (end_date + timedelta(60)):
                    cancel_60d = 1
                if cancel_date <= (end_date + timedelta(90)):
                    cancel_90d = 1
            
            use_count_0d = 0
            use_count_14d = 0
            use_count_30d = 0
            use_count_60d = 0
            use_count_90d = 0
            
            for i in range(0, len(usage_dates)):
                usage_date_str = usage_dates.iloc[i]
                usage_date_str = usage_date_str.strip()
                usage_date = datetime.strptime(usage_date_str, '%m/%d/%Y')
                # check if the user is healthy now
                if usage_date <= end_date and usage_date >= (end_date - timedelta(60)):
                    use_count_0d = use_count_0d + 1
                # check if the user's usage will be unhealthy in 14d, 30d, 60d, 90d
                if usage_date <= end_date_14d and usage_date >= (end_date_14d  - timedelta(60)):
                    use_count_14d = use_count_14d + 1
                if usage_date <= end_date_30d and usage_date >= (end_date_30d  - timedelta(60)):
                    use_count_30d = use_count_30d + 1
                if usage_date <= end_date_60d and usage_date >= (end_date_60d  - timedelta(60)):
                    use_count_60d = use_count_60d + 1
                if usage_date <= end_date_90d and usage_date >= (end_date_90d  - timedelta(60)):
                    use_count_90d = use_count_90d + 1
                    
            # print member_num + ' join:' + member_join + ' 0d:' + str(use_count_0d) + ' 14d:' + str(use_count_14d) + ' 30d:' + str(use_count_30d) \
            #       + ' 60d:' + str(use_count_60d) + ' 90d:' + str(use_count_90d)
            if use_count_0d > thre_unhealthy:
                healthy_now = 1
            else: 
                healthy_now = 0
                
            if use_count_14d <= thre_unhealthy:
                unhealthy_14d = 1
            if use_count_30d <= thre_unhealthy:
                unhealthy_30d = 1 
            if use_count_60d <= thre_unhealthy:
                unhealthy_60d = 1 
            if use_count_90d <= thre_unhealthy:
                unhealthy_90d = 1 
    else:
        # not enough data 
        healthy_now = 0

    return Series([healthy_now, cancel_14d, cancel_30d, cancel_60d, cancel_90d, unhealthy_14d, unhealthy_30d, unhealthy_60d, unhealthy_90d], 
                  index = ['healthy_now', 'cancel_14d', 'cancel_30d', 'cancel_60d', 'cancel_90d', 'unhealthy_14d', 'unhealthy_30d', 'unhealthy_60d', 'unhealthy_90d'])


    