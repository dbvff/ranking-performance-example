import glob
import os
import pandas as pd
# import numpy as np
from fn_transform import (
    parse_time, parse_cap, parse_timecapped,
    zscore, small_number_adjustment, compscore)


PATH_IN = "data/1-extracted/cc"
PATH_OUT = "data/2-transform/cc"

FILES = glob.glob(f"{PATH_IN}/*.csv")
os.makedirs(PATH_OUT, exist_ok=True)


# convert strings to numbers (for C3PO data)
def parse_remove_tiebreaks(s):
    return s.split("+")[0].strip()


def parse_number(s):
    s2 = parse_remove_tiebreaks(s)
    try:
        return float(s2)
    except:
        return None

def parse_cap_notiebreak(s):
    s2 = s.split(" (")[0].strip()
    return parse_cap(s2)

def parse_time_notiebreak(s):
    s2 = s.split(" (")[0].strip()
    return parse_time(s2)

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
    units = [s.split(".")[0] for s in df.columns[-len(cols_r):]]
    df = df[df.columns[:-len(cols_r)]]

    # transform data
    cols_t = [f"trans_{i + 1}" for i in range(len(cols_s))]
    for i, unit in enumerate(units):
        if unit in ("kg", "lb", "reps", "calories", "meters"):
            df[cols_t[i]] = df[cols_s[i]].apply(parse_number)
        elif unit in ("seconds"):
            df[cols_t[i]] = -df[cols_s[i]].apply(parse_number)  # with "-" minus
        elif unit in ("time"): 
            df[cols_t[i]] = df[cols_s[i]].apply(parse_time_notiebreak)
        else:
            df[cols_t[i]] = None

    # time capped => look for "cap+ ?"
    df = parse_timecapped(df, parse_cap_notiebreak, units, cols_s, cols_t)

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
