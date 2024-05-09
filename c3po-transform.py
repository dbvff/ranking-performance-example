import glob
import os
import pandas as pd
# import numpy as np
from fn_transform import (
    parse_time, parse_cap, parse_timecapped,
    zscore, small_number_adjustment, compscore)


PATH_IN = "data/1-extracted/c3po"
PATH_OUT = "data/2-transform/c3po"

FILES = glob.glob(f"{PATH_IN}/*.csv")
os.makedirs(PATH_OUT, exist_ok=True)



# convert strings to numbers (for C3PO data)
def parse_rep(s):
    try:
        return float(s.split(" rep")[0])
    except:
        return None

assert parse_rep("7 rep") == 7.0
assert parse_rep("7 reps") == 7.0


def parse_rep_or_cap(s):
    x = parse_rep(s)
    if x is None:
        x = parse_cap(s)
    return x


def parse_lb(s):
    try:
        return float(s.lower().split(" lb")[0])
    except:
        return None

assert parse_lb("545 lb") == 545.0
assert parse_lb("545 lbs") == 545.0


def parse_kg(s):
    try:
        return float(s.lower().split(" kg")[0])
    except:
        return None



# loop over all files
for FILE in FILES:
    df = pd.read_csv(FILE, dtype=str)

    # skip empty files
    if len(df.index) == 0:
        print(f"No data in: {FILE}")
        continue
    # skip files with less than 4 rows!
    if len(df.index) < 4:
        print("field is too small: ", FILE)
        continue

    # get columns
    cols_s = [s for s in df.columns if "score_" in s]
    cols_r = [r for r in df.columns if "rank_" in r]

    # identify unit
    units = []
    for i in range(len(cols_s)):
        df[cols_r[i]] = df[cols_r[i]].astype(float)
        best = df.sort_values(by=cols_r[i]).iloc[0][cols_s[i]]
        if "rep" in best:
            units.append("rep")
            continue
        if "cap" in best.lower():
            units.append("allcap")
            continue
        if ":" in best:
            units.append("time")
            continue
        if "lb" in best:
            units.append("lb")
            continue
        if "kg" in best:
            units.append("kg")
            continue
        else:
            print("unknown unit!")
            units.append("unknown")

    # transform data
    cols_t = [f"trans_{i + 1}" for i in range(len(cols_s))]
    for i, unit in enumerate(units):
        if unit == "rep":
            df[cols_t[i]] = df[cols_s[i]].apply(parse_rep)
        elif unit == "allcap":
            df[cols_t[i]] = df[cols_s[i]].apply(parse_cap)
        elif unit == "time":
            df[cols_t[i]] = df[cols_s[i]].apply(parse_time)
        elif unit == "lb":
            df[cols_t[i]] = df[cols_s[i]].apply(parse_lb)
        elif unit == "kg":
            df[cols_t[i]] = df[cols_s[i]].apply(parse_kg)
        else:
            df[cols_t[i]] = df[cols_s[i]].astype(float)

    # time capped => look for "? reps" or "cap+?"
    df = parse_timecapped(df, parse_rep_or_cap, units, cols_s, cols_t)


    # compute z-scores        
    cols_z = [f"zscore_{i + 1}" for i in range(len(cols_t))]
    df[cols_z] = df[cols_t].apply(zscore)

    # small number adjustment factor
    smallnumadj = small_number_adjustment(len(df.index))
    df["small_num_adjust"] = smallnumadj

    # competition score
    cs, rho = compscore(df[cols_z].values)
    df["compscore"] = cs

    # ranking points
    df["avg-z_mul-sna_plus-cs"] = df[cols_z].mean(axis=1) * smallnumadj + cs

    # save files
    FILENAME = FILE.split("/")[-1].split(".")[0]
    df.to_csv(f"{PATH_OUT}/{FILENAME}.csv", index=False)



