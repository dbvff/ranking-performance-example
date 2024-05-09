import os
import pandas as pd
import numpy as np
from fn_ranking import get_compinfo, get_ranking_table


PATH_OUT = "data/4-results/example3"
os.makedirs(PATH_OUT, exist_ok=True)



competition_files = [
    # iF3 Teens/Juniors
    (75, 'cc', 'if3-masters-worlds-23_F_13-14.csv'),
    (75, 'cc', 'if3-masters-worlds-23_F_15-16.csv'),
    (75, 'cc', 'if3-masters-worlds-23_F_17-18.csv'),
    (75, 'cc', 'if3-masters-worlds-23_M_13-14.csv'),
    (75, 'cc', 'if3-masters-worlds-23_M_15-16.csv'),
    (75, 'cc', 'if3-masters-worlds-23_M_17-18.csv'),

    # CF Quarter'24 Teens/Juniors
    (50, 'c3po', 'cf-quarter-24_F_14-15.csv'),
    (50, 'c3po', 'cf-quarter-24_F_16-17.csv'),
    (50, 'c3po', 'cf-quarter-24_M_14-15.csv'),
    (50, 'c3po', 'cf-quarter-24_M_16-17.csv'),

]


# get competiton information
tmp = get_compinfo(competition_files)
tmp.to_csv(f"{PATH_OUT}/compinfo.csv", index=False)


# ranking table
tmp = get_ranking_table(competition_files, max_comps=2)
tmp.to_csv(f"{PATH_OUT}/ranking-table.csv", index=False)
