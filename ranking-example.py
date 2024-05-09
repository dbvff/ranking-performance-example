import os
import pandas as pd
import numpy as np
from fn_ranking import get_compinfo, get_ranking_table


PATH_OUT = "data/4-results/example"
os.makedirs(PATH_OUT, exist_ok=True)



competition_files = [
    # iF3 Euros '23
    (25, 'cc', 'if3-euros-23_F_IndividualWomenPrelims.csv'),
    (75, 'cc', 'if3-euros-23_F_IndividualWomenFinal.csv'),
    (25, 'cc', 'if3-euros-23_M_IndividualMenPrelims.csv'),
    (75, 'cc', 'if3-euros-23_M_IndividualMenFinal.csv'),
    
    # CF Quarter'24 
    # (50, 'c3po', 'cf-quarter-24_F.csv'),
    # (50, 'c3po', 'cf-quarter-24_M.csv'),

    # CF Semi '23, 
    (75, 'c3po', 'cf-semi-africa-23_F.csv'),
    (75, 'c3po', 'cf-semi-africa-23_M.csv'),
    (75, 'c3po', 'cf-semi-asia-23_F.csv'),
    (75, 'c3po', 'cf-semi-asia-23_M.csv'),
    (75, 'c3po', 'cf-semi-europe-23_F.csv'),
    (75, 'c3po', 'cf-semi-europe-23_M.csv'),
    (75, 'c3po', 'cf-semi-na-east-23_F.csv'),
    (75, 'c3po', 'cf-semi-na-east-23_M.csv'),
    (75, 'c3po', 'cf-semi-na-west-23_F.csv'),
    (75, 'c3po', 'cf-semi-na-west-23_M.csv'),
    (75, 'c3po', 'cf-semi-oceania-23_F.csv'),
    (75, 'c3po', 'cf-semi-oceania-23_M.csv'),
    (75, 'c3po', 'cf-semi-south-am-23_F.csv'),
    (75, 'c3po', 'cf-semi-south-am-23_M.csv'),

    # CFG, is precomputed due to Cuts
    ('locked', 'c3po', 'cfg-23_M.csv'),  # The field "ranking_points" is precomputed!
    ('locked', 'c3po', 'cfg-23_F.csv'),
]


# get competiton information
tmp = get_compinfo(competition_files)
tmp.to_csv(f"{PATH_OUT}/compinfo.csv", index=False)


# ranking table
tmp = get_ranking_table(competition_files, max_comps=2)
tmp.to_csv(f"{PATH_OUT}/ranking-table.csv", index=False)
