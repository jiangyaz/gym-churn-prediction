from pandas import DataFrame, Series, read_csv
from basic_feature import *
from past_visits_feature import *

import pandas as pd
import numpy as np

data_seg_num = 5

for i in range(1, data_seg_num + 1):
	print 'Start loading data part ' + str(i) + '...'
	
	# load_basic_feature(i)
	# load_past_visits_feature(i)

	# print 'Loading feature: "# days since last visit" ...'
	# load_day_num_last_visit_feature(i)

	# print 'Loading feature: "membership type" ...'
	# load_member_type_feature(i)

	# print 'Loading feature: "club regularity" ...'
	# load_club_regularity_feature(i)

	load_weekly_visit_feature(i)
	
	print 'Loading complete. \n'
