import pandas as pd
import numpy as np
import os.path


def get_compinfo(competition_files):
    compinfo = []
    for compweight, sourcename, filename in competition_files:
        # read file
        FILE = f"data/2-transform/{sourcename}/{filename}"
        if not os.path.isfile(FILE): print("file doesn't exit", FILE); continue
        df = pd.read_csv(FILE, dtype=str)
        # parse comp name from filename
        tmp = filename.split(".csv")[0].split("_")
        compname, gender, catg = None, None, None
        try:
            compname = tmp[0]
            gender = tmp[1]
            catg = tmp[2]
        except:
            print(filename)
        # save stats about the competition
        compinfo.append([
            compname, gender, catg,
            compweight,
            len([_ for _ in df.columns if "zscore_" in _]), # num tests
            len(df.index),  # num participants
            df['small_num_adjust'].iloc[0],
            df['compscore'].iloc[0],
        ])
    # done
    return pd.DataFrame(compinfo, columns=[
        "compname", "gender", "catg", "compweight", "num_tests", 
        "num_athletes", "small_num_adjust", "compscore"])


# for displaying the results
def places_by_points(pts):
    it = 1
    places = [it]
    last_pt = pts[0]
    for pt in pts[1:]:
        it += 1
        if pt == last_pt:
            places.append(places[-1])
        else:
            places.append(it)
            last_pt = pt
    return places



def get_ranking_table(competition_files, max_comps=3):
    # loop over athlete data
    athletes = {}
    for compweight, sourcename, filename in competition_files:
        # get comp name
        compname = filename.split(".csv")[0].replace("_", " ")

        # locked files
        if compweight == "locked":
            FILE = f"data/3-locked/{sourcename}/{filename}"
            if not os.path.isfile(FILE): print("file doesn't exit", FILE); continue
            df = pd.read_csv(FILE, dtype=str)
            df["rp"] = df["rp"].apply(float)
        else:
            # read file
            FILE = f"data/2-transform/{sourcename}/{filename}"
            if not os.path.isfile(FILE): print("file doesn't exit", FILE); continue
            df = pd.read_csv(FILE, dtype=str)
            # compute ranking points (normal case)
            df["rp"] = np.maximum(
                0, df["avg-z_mul-sna_plus-cs"].apply(float) * compweight)

        # save results for each athlete
        for hash, name, cty, age, rp in df[["hash", "name", "cty", "age", "rp"]].values.tolist():
            if rp <= 0.0:  # skip
                continue
            # if cty != "DE":  # skip
            #     continue
            if athletes.get(hash) is None:
                athletes[hash] = {"name": name, "cty": cty, "age": age, "data": []}
            athletes[hash]["data"].append({"rp": rp, "comp": compname})
            athletes[hash]["age"] = age if pd.isnull(athletes[hash]["age"]) else athletes[hash]["age"]  # find age
            athletes[hash]["cty"] = cty if pd.isnull(athletes[hash]["cty"]) else athletes[hash]["cty"]  # find country
            # print("age", age)

    # add the best 3 results "max_comps=3"
    for key in athletes.keys():
        tmp = athletes[key]["data"]
        athletes[key]["data"] = sorted(tmp, key=lambda x: -x["rp"])
        athletes[key]["total"] = np.flip([x["rp"] for x in tmp])[:max_comps].sum()
    # zu ordered list
    tmp = sorted(list(athletes.items()), key=lambda x: -x[1]["total"])
    ranking_table = []
    for key, val in tmp: # flatten table
        ranking_table.append([
            key, val["name"], val["cty"], val["age"],  
            val["total"], len(val["data"]), val["data"],
            ", ".join([f"{x['rp']:.1f}pts {x['comp']}" for x in val["data"]])
        ])
    # to dataframe
    tmp = pd.DataFrame(ranking_table, columns=[
        "hash", "name", "cty", "age", "total", "num_comps", "data", "data_display"])
    tmp["place"] = places_by_points(tmp["total"].values)
    tmp = tmp[["hash", "place", "total", "name", "cty", "age", "num_comps", "data_display", "data"]]
    return tmp
