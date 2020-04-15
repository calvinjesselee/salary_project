#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 10:41:19 2020

@author: calvinlee
"""


import pandas as pd
df = pd.read_csv('glassdoor_jobs.csv')

# Salary parsing

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

df = df [ df['Salary Estimate']  != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0] ).to_frame()
salary = salary [ salary['Salary Estimate']  != ''].iloc[:,0]

minus_k = salary.apply(lambda x: x.replace('K', '').replace('$',''))
min_hr = minus_k.apply(lambda x: x.lower().replace('per hour', '').replace('employer provided salary:', ''))

df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1].replace(" ", "")))
df['avg_salary'] = (df.min_salary + df.max_salary) / 2

df = df.dropna(subset = ['min_salary'])

# Company Name text only
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1)

# state field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df['job_state'] = df['job_state'].apply(lambda x: x.upper().replace('LOS ANGELES', 'LA'))

df.job_state.value_counts()

df['job&hq_same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)

# age of company
df['company_age'] = df.Founded.apply(lambda x: x if x <1 else 2020 -x)

# parsing of job description (python, etc.)
# python
df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
# matlab
df['matlab'] = df['Job Description'].apply(lambda x: 1 if 'matlab' in x.lower() else 0)
# c++
df['cpp'] = df['Job Description'].apply(lambda x: 1 if 'c++' in x.lower() else 0)
# sql
df['sql'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)
# java
df['java'] = df['Job Description'].apply(lambda x: 1 if 'java' in x.lower() else 0)
# signal processing
df['dsp'] = df['Job Description'].apply(lambda x: 1 if 'signal processing' in x.lower() else 0)
# power
df['power'] = df['Job Description'].apply(lambda x: 1 if 'power' in x.lower() else 0)
# machine learning
df['ML'] = df['Job Description'].apply(lambda x: 1 if 'machine learning' in x.lower() or 'deep learning' in x.lower()
                                       or 'neural network' in x.lower() or 'rnn' in x.lower() 
                                       or 'cnn' in x.lower() or 'lstm' in x.lower() or 'artificial intelligence' in x.lower() else 0)
# entry lvl
df['entry_lvl'] = df['Job Title'].apply(lambda x: 1 if 'entry' in x.lower() or 'associate' in x.lower() else 0)
df['entry_lvl1'] = df['Job Description'].apply(lambda x: 1 if 'entry' in x.lower() else 0)
df['entry_lvl'] = (df.entry_lvl + df.entry_lvl1).apply(lambda x: 1 if x> 0 else 0)

# senior_lvl
df['senior_lvl'] = df['Job Title'].apply(lambda x: 1 if 'senior' in x.lower() or 'sr.' in x.lower() 
                                         or 'sr' in x.lower() or 'principal' in x.lower()
                                         or 'manager' in x.lower() else 0)

df['senior_lvl1'] = df['Job Description'].apply(lambda x: 1 if 'senior' in x.lower() or 'principal' in x.lower()  else 0)
df['senior_lvl'] = (df.senior_lvl + df.senior_lvl1).apply(lambda x: 1 if x> 0 else 0)

# Delete
del df['senior_lvl1']
del df['entry_lvl1'] 

df.to_csv('salary_data_cleaned.csv', index = False)


# Count
df.python.value_counts()
df.matlab.value_counts()
df.cpp.value_counts()
df.sql.value_counts()
df.java.value_counts()
df.dsp.value_counts()
df.power.value_counts()
df.ML.value_counts()
df.entry_lvl.value_counts()
df.senior_lvl.value_counts()