# start from main folder so that the paths work
import pandas as pd
import os
import sys
sys.path.append(os.getcwd())
from fn_transform import (small_number_adjustment, compscore)


for FILENAME in ("cfg-23_M.csv", "cfg-23_F.csv"):

    df = pd.read_csv(f"data/2-transform/c3po/{FILENAME}")

    cols1 = ['zscore_1', 'zscore_2', 'zscore_3', 'zscore_4', 'zscore_5', 'zscore_6']
    cols2 = ['zscore_7', 'zscore_8', 'zscore_9']
    cols3 = ['zscore_10', 'zscore_11', 'zscore_12']

    tmp = df[cols1].dropna()
    df["sna1"] = small_number_adjustment(len(tmp.index))
    df["cs1"], _ = compscore(tmp.values)
    df["rp1"] = 100.0 * (df["sna1"] * tmp.mean(axis=1) + df["cs1"]) 

    tmp = df[cols2].dropna()
    df["sna2"] = small_number_adjustment(len(tmp.index))
    df["cs2"], _ = compscore(tmp.values)
    df["rp2"] = 50.0 * (df["sna2"] * tmp.mean(axis=1) + df["cs2"]) 

    tmp = df[cols3].dropna()
    df["sna3"] = small_number_adjustment(len(tmp.index))
    df["cs3"], _ = compscore(tmp.values)
    df["rp3"] = 50.0 * (df["sna3"] * tmp.mean(axis=1) + df["cs3"]) 

    df["rp"] = df[["rp1", "rp2", "rp3"]].fillna(0.0).sum(axis=1)

    os.makedirs("data/3-locked/c3po/", exist_ok=True)
    df.to_csv(f"data/3-locked/c3po/{FILENAME}")
