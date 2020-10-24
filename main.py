import requests
import pandas as pd
import covid_requests
import seaborn as sb
from covid_requests import get_total_tests, get_confirmed_cases
import datetime
from math import ceil

from matplotlib import pyplot as plt

tests = get_total_tests()
cases = get_confirmed_cases()

# Total tests performed, convert json array to dataframe
df_tests = pd.DataFrame(tests)
# Total cases confirmed, convert json array to dataframe
df_cases = pd.DataFrame(cases)

# merge dataframes on date column
df = pd.merge(df_tests, df_cases, on='date')

pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 200)

# df.fillna(0, inplace=True)

df['avg3'] = df.tests.rolling(3, center=True, min_periods=1).mean()
df['avg5'] = df.tests.rolling(5, center=True, min_periods=1).mean()

# Replace NaN values on the 'tests' column with the corresponding computed value in 'avg5' column
# df.loc[df.tests.isna(), 'tests'] = df.loc[df.tests.isna(), 'avg']
#
# compute extra columns,
# 'confirmed_per_day', 'rapid_tests_per_day', 'tests_per_day', 'total_tests_per_day'
df['rapid_tests_per_day'] = df['rapid-tests'].diff()
df['tests_per_day'] = df['tests'].diff()
df['confirmed_per_day'] = df['confirmed'].diff()
df['total_tests_per_day'] = df.rapid_tests_per_day + df.tests_per_day
df['cases_per_test'] = df.confirmed_per_day / df.total_tests_per_day

df.fillna(0)

df['datetime'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
df['month'] = df['datetime'].apply(lambda x: x.month)

# cells with 'inf' or 'NaN' value are set to 0
df.loc[df.cases_per_test.isin([np.inf, np.nan]), 'cases_per_test'] = 0
df['cases_per_test'] = df['cases_per_test'].apply(lambda x: ceil(x*1000)/1000)


# rows where tests number is 0
# df.loc[df.tests == 0]

# df.loc[(df.datetime > datetime.date(2020, 4, 16)) & (df.datetime < datetime.date(2020, 4, 22))]
df = df.loc[df.datetime >= datetime.date(2020, 2, 26)]

df.tests[df.tests.isna()] = df.avg5[df.tests.isna()]



# sb.lmplot(x='confirmed_per_day', y='total_tests_per_day', data=df)
# sb.lmplot(y='confirmed_per_day', x='total_tests_per_day', data=df, hue='month', fit_reg=False)