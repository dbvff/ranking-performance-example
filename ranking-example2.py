import os
import pandas as pd
import numpy as np
from fn_ranking import get_compinfo, get_ranking_table


PATH_OUT = "data/4-results/example2"
os.makedirs(PATH_OUT, exist_ok=True)



competition_files = [
    # iF3 Masters
    (75, 'cc', 'if3-masters-worlds-23_F_30-34.csv'),
    (75, 'cc', 'if3-masters-worlds-23_F_35-39.csv'),
    (75, 'cc', 'if3-masters-worlds-23_F_40-44.csv'),
    (75, 'cc', 'if3-masters-worlds-23_F_45-49.csv'),
    (75, 'cc', 'if3-masters-worlds-23_F_50-54.csv'),
    (75, 'cc', 'if3-masters-worlds-23_F_55-59.csv'),
    (75, 'cc', 'if3-masters-worlds-23_F_60-64.csv'),
    (75, 'cc', 'if3-masters-worlds-23_F_65+.csv'),
    (75, 'cc', 'if3-masters-worlds-23_M_30-34.csv'),
    (75, 'cc', 'if3-masters-worlds-23_M_35-39.csv'),
    (75, 'cc', 'if3-masters-worlds-23_M_40-44.csv'),
    (75, 'cc', 'if3-masters-worlds-23_M_45-49.csv'),
    (75, 'cc', 'if3-masters-worlds-23_M_50-54.csv'),
    (75, 'cc', 'if3-masters-worlds-23_M_55-59.csv'),
    (75, 'cc', 'if3-masters-worlds-23_M_60-64.csv'),
    (75, 'cc', 'if3-masters-worlds-23_M_65+.csv'),

    # CF Quarter'24 Masters
    (50, 'c3po', 'cf-quarter-24_F_35-39.csv'),
    (50, 'c3po', 'cf-quarter-24_F_40-44.csv'),
    (50, 'c3po', 'cf-quarter-24_F_45-49.csv'),
    (50, 'c3po', 'cf-quarter-24_F_50-54.csv'),
    (50, 'c3po', 'cf-quarter-24_F_55-59.csv'),
    (50, 'c3po', 'cf-quarter-24_F_60-64.csv'),
    (50, 'c3po', 'cf-quarter-24_F_65+.csv'),
    (50, 'c3po', 'cf-quarter-24_M_35-39.csv'),
    (50, 'c3po', 'cf-quarter-24_M_40-44.csv'),
    (50, 'c3po', 'cf-quarter-24_M_45-49.csv'),
    (50, 'c3po', 'cf-quarter-24_M_50-54.csv'),
    (50, 'c3po', 'cf-quarter-24_M_55-59.csv'),
    (50, 'c3po', 'cf-quarter-24_M_60-64.csv'),
    (50, 'c3po', 'cf-quarter-24_M_65+.csv'),

]


# get competiton information
tmp = get_compinfo(competition_files)
tmp.to_csv(f"{PATH_OUT}/compinfo.csv", index=False)


# ranking table
tmp = get_ranking_table(competition_files, max_comps=2)
tmp.to_csv(f"{PATH_OUT}/ranking-table.csv", index=False)
