from pandas import DataFrame, Series, read_csv
from utils import *
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from collections import Counter

ref_date = 0

def f_gender(gender):
    if gender == 'M':
        return Series([1], index =['gender'])
    else: 
        return Series([0], index =['gender'])
    
def f_age(birth_date):
    birth_date = birth_date.strip()
    if len(birth_date) == 10:
        dob = datetime.strptime(birth_date, '%m/%d/%Y')
        diff = ref_date - dob
        age = np.math.floor(diff.total_seconds()/(60*60*24*365))
        if age <= 22:
            return Series([1,0,0,0],index=['age0-22', 'age23-40', 'age41-55', 'age56+'])
        elif age <= 40:
            return Series([0,1,0,0],index=['age0-22', 'age23-40', 'age41-55', 'age56+'])
        elif age <= 55:
            return Series([0,0,1,0],index=['age0-22', 'age23-40', 'age41-55', 'age56+'])
        else:
            return Series([0,0,0,1],index=['age0-22', 'age23-40', 'age41-55', 'age56+'])
    else:
        return Series([0,0,0,0], index=['age0-22', 'age23-40', 'age41-55', 'age56+'])
        
def f_member_length(join_date):
    join_date = join_date.strip()
    if len(join_date) == 10:
        join = datetime.strptime(join_date, '%m/%d/%Y')
        diff = ref_date - join
        length = diff.total_seconds()/(60*60*24*30)
        if length > 60:
            return Series([1.0], index =['length'])
        else: 
            return Series([length/60.0], index =['length']) 
    else:
        return Series([0.0], index =['length'])
        
def f_club(home_club):
    if home_club == 11:
        return Series([1,0,0,0,0,0,0,0,0,0,0,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    elif home_club == 12:
        return Series([0,1,0,0,0,0,0,0,0,0,0,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    elif home_club == 13:
        return Series([0,0,1,0,0,0,0,0,0,0,0,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    elif home_club == 15:
        return Series([0,0,0,1,0,0,0,0,0,0,0,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    elif home_club == 19:
        return Series([0,0,0,0,1,0,0,0,0,0,0,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    elif home_club == 20:
        return Series([0,0,0,0,0,1,0,0,0,0,0,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    elif home_club == 23:
        return Series([0,0,0,0,0,0,1,0,0,0,0,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    elif home_club == 25:
        return Series([0,0,0,0,0,0,0,1,0,0,0,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    elif home_club == 41:
        return Series([0,0,0,0,0,0,0,0,1,0,0,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    elif home_club == 50:
        return Series([0,0,0,0,0,0,0,0,0,1,0,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    elif home_club == 84:
        return Series([0,0,0,0,0,0,0,0,0,0,1,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    elif home_club == 93:
        return Series([0,0,0,0,0,0,0,0,0,0,0,1],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
    else:
        return Series([0,0,0,0,0,0,0,0,0,0,0,0],index=['c11','c12','c13','c15','c19','c20','c23','c25','c41','c50','c84','c93'])
 

def load_basic_feature(index):
    df_info = load_info_file(index)
    df_checkins = load_checkins_file(index)	
    
    global ref_date
    ref_date = datetime(2008+index, 3, 1)

    info_gender = df_info['M/F'].apply(f_gender)
    info_age    = df_info['DOB'].apply(f_age)
    info_length = df_info['Join date'].apply(f_member_length)
    info_club   = df_info['Home club'].apply(f_club)

    info_length.to_csv('../clubOne/data/features/p'+ str(index) +'_f_length.csv', index=False)
    info_age.to_csv('../clubOne/data/features/p' + str(index) + '_f_age.csv', index=False)
    info_gender.to_csv('../clubOne/data/features/p' + str(index) + '_f_gender.csv', index=False)
    info_club.to_csv('../clubOne/data/features/p' + str(index) + '_f_club.csv', index=False)

def f_types(types):
    member_types=['CRP', 'SNR', 'N/C', 'STD', 'CPA', 'NM ', 'CAP', 'STA', 'SNA', 'STU', 'YTA', 'PEN', 'SUA', 'YTH', 'CHA']
    if types == 'CRP':
        return Series([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], index = member_types)
    elif types == 'SNR':
        return Series([0,1,0,0,0,0,0,0,0,0,0,0,0,0,0], index = member_types)
    elif types == 'N/C':
        return Series([0,0,1,0,0,0,0,0,0,0,0,0,0,0,0], index = member_types)
    elif types == 'STD':
        return Series([0,0,0,1,0,0,0,0,0,0,0,0,0,0,0], index = member_types)
    elif types == 'CPA':
        return Series([0,0,0,0,1,0,0,0,0,0,0,0,0,0,0], index = member_types)
    elif types == 'NM':
        return Series([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0], index = member_types)
    elif types == 'CAP':
        return Series([0,0,0,0,0,0,1,0,0,0,0,0,0,0,0], index = member_types)
    elif types == 'STA':
        return Series([0,0,0,0,0,0,0,1,0,0,0,0,0,0,0], index = member_types)
    elif types == 'SNA':
        return Series([0,0,0,0,0,0,0,0,1,0,0,0,0,0,0], index = member_types)
    elif types == 'STU':
        return Series([0,0,0,0,0,0,0,0,0,1,0,0,0,0,0], index = member_types)
    elif types == 'YTA':
        return Series([0,0,0,0,0,0,0,0,0,0,1,0,0,0,0], index = member_types)
    elif types == 'PEN':
        return Series([0,0,0,0,0,0,0,0,0,0,0,1,0,0,0], index = member_types)
    elif types == 'SUA':
        return Series([0,0,0,0,0,0,0,0,0,0,0,0,1,0,0], index = member_types)
    elif types == 'YTH':
        return Series([0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], index = member_types)
    elif types == 'CHA':
        return Series([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], index = member_types)
    else:
        return Series([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], index = member_types)


def load_member_type_feature(index):
    df_info = load_info_file(index)
    df_checkins = load_checkins_file(index)

    info_type = df_info['Type'].apply(f_types)
    info_type.to_csv('../clubOne/data/features/p' + str(index) + '_f_type.csv', index=False)

   



