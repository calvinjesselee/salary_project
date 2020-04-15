#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 09:15:27 2020

@author: calvinlee
"""


import glassdoor_scraper as gs
import pandas as pd

path = "/home/calvinlee/Documents/salary_project/chromedriver"
slp_time = 5
df = gs.get_jobs('electrical engineer', 10000,False, path, slp_time)
df.to_csv('glassdoor_jobs.csv', index = False)