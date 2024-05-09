
import pandas as pd
import numpy as np


# convert strings to numbers (for CC and C3PO data)
def parse_cap(s):
    try: 
        s2 = s.replace(" ", "").lower()
        return float(s2.split("cap+")[-1])
    except:
        return None

assert parse_cap("CAP +36") == 36.0
assert parse_cap("CAP+41") == 41.0


def parse_time(timestr):
    try:
        micro = 0.0
        if '.' in timestr:
            timestr, m = timestr.split('.')
            micro = int(m) / 10**len(m)
        tc = timestr.split(':')
        ftr = [3600, 60, 1]
        ftr = ftr[(3 - len(tc)):]
        return float(sum([a*b for a,b in zip(ftr, map(int, tc))]) + micro)
    except:
        return None

assert parse_time("1:15:59") == 60 * 60 + 15 * 60 + 59
assert parse_time("24:31.18") == 24 * 60 + 31 + .18
assert parse_time("02:52") == 2 * 60 + 52


# extrapolate caps
def parse_timecapped(df, fn_cap_transform, units, cols_s, cols_t):
    for i, unit in enumerate(units):
        if unit == "time":
            # get parse times
            finished = df.loc[pd.notnull(df[cols_t[i]]), cols_t[i]].values
            # use caps instead
            if len(finished) == 0:
                df[cols_t[i]] = df[cols_s[i]].apply(fn_cap_transform)
                continue
            # try to estimate TC and extrapolate              
            equidist = (np.max(finished) - np.min(finished)) / len(finished)
            timecap_estim = np.max(finished) + equidist
            timecap_estim = max(timecap_estim, 60 * (max(finished) // 60 + 1))  # TC estimated
            tmp = df[cols_s[i]].apply(fn_cap_transform)  # get cap reps
            estimated = (tmp.max() / tmp) * timecap_estim  # extrapolate

            df[cols_t[i]] = -df[cols_t[i]].fillna(estimated) # with "-" minus
            # mask = pd.isnull(df[cols_t[i]])
            # df.loc[mask, cols_t[i]] = estimated[mask]
            # df[cols_t[i]] = -df[cols_t[i]]
            
            # if the only "CAP", i.e. exactly the TC, then impute "timecap_estim"
            mask = df[cols_s[i]].str.upper() == "CAP"
            df.loc[mask, cols_t[i]] = -timecap_estim
    return df


# sport analytics
def zscore(x):
    z = (x - np.mean(x, axis=0)) / np.std(x, axis=0)
    return z


def small_number_adjustment(num: int):
    return min(1.0, np.sqrt(num / 30.))


def compscore(z):
    rho = np.corrcoef(z, rowvar=False)
    rhotl = np.tril(rho, -1)  # only i>j
    cs = 1.0 - np.abs(np.sum(rhotl) / np.prod(rho.size))
    return cs, rho
