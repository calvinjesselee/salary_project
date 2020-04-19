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

# hourly wage to annual
df['min_salary'] = df.apply(lambda x: x.min_salary*2.08 if x.hourly == 1 else x.min_salary, axis = 1)
df['max_salary'] = df.apply(lambda x: x.max_salary*2.08 if x.hourly == 1 else x.max_salary, axis = 1)

df['avg_salary'] = (df.min_salary + df.max_salary) / 2

df = df.dropna(subset = ['min_salary'])


# Company Name text only
df['company_txt'] = df.apply(lambda x: x['Company Name'].replace('\n', '') if x['Rating'] < 0 else x['Company Name'][:-3].replace('\n', ''), axis = 1)

# state field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df['job_state'] = df['job_state'].apply(lambda x: x.upper().replace('LOS ANGELES', 'LA'))

df.job_state.value_counts()

df['hq_same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)

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

# Embedded System
df['Embedded_System'] = df['Job Description'].apply(lambda x: 1 if 'embedded' in x.lower() else 0)

# machine learning
df['ML'] = df['Job Description'].apply(lambda x: 1 if 'machine learning' in x.lower() or 'deep learning' in x.lower()
                                       or 'neural network' in x.lower() or 'rnn' in x.lower() 
                                       or 'cnn' in x.lower() or 'lstm' in x.lower() or 'artificial intelligence' in x.lower() else 0)
# Position Senority
def seniority(title):
    if 'sr' in title.lower() or 'sr.' in title.lower() or 'manager'in title.lower() or 'senior' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
        return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower() or 'junior' in title.lower():
        return 'junior'
    elif 'entry' in title.lower() or 'associate' in title.lower():
        return 'entry'
    else:
        return 'na'
df['seniority'] = df['Job Title'].apply(seniority)


# Job description length
df['desc_len'] = df['Job Description'].apply(lambda x: len(x))


# Competitor count
df['Num_Competitors'] = df['Competitors'].apply(lambda x: len(x.split(',')) if x != '-1' else 0)


df.to_csv('salary_data_cleaned.csv', index = False)
df1 = pd.read_csv('salary_data_cleaned.csv')

# Count
df.python.value_counts()
df.matlab.value_counts()
df.cpp.value_counts()
df.sql.value_counts()
df.java.value_counts()
df.dsp.value_counts()
df.power.value_counts()
df.ML.value_counts()
df.seniority.value_counts()