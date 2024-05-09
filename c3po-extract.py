import json
import glob
import csv
import os
import time
from fn_extract import name_to_hash


PATH_IN = "data/0-raw/c3po"
PATH_OUT = "data/1-extracted/c3po"

FILES = glob.glob(f"{PATH_IN}/*.json")
os.makedirs(PATH_OUT, exist_ok=True)


for JSONFILE in FILES:
    # Load file
    #JSONFILE = FILES[0]
    data = json.load(open(JSONFILE))

    # find number of columns
    num_cols = None
    for page in data:
        for row in page["leaderboardRows"]:
            num_cols = len(row["scores"])
            break
        break

    # init CSV File
    FILENAME = JSONFILE.split("/")[-1].split(".")[0]
    CSVFILE = f"{PATH_OUT}/{FILENAME}.csv"
    csv_fileptr = open(CSVFILE, "w")
    csv_writer = csv.writer(
        csv_fileptr, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(["hash", "name", "cty", "age"] \
                        + [f"rank_{i+1}" for i in range(num_cols)] \
                        + [f"score_{i+1}" for i in range(num_cols)])

    # loop through all lines
    for page in data:
        for row in page["leaderboardRows"]:
            # start reading data
            #cid = row["entrant"]["competitorId"]
            name = row["entrant"]["competitorName"].upper()
            cty = row["entrant"]["countryOfOriginCode"] #.upper()
            age = row["entrant"]["age"]
            ranks, scores = [], []
            # for workout in sorted(row["scores"], key=lambda x: x["ordinal"]):
            for workout in row["scores"]:
                if workout["scoreDisplay"].lower() in ("", "0 reps", "wd", "dnf"):
                    scores.append(None)
                else:
                    scores.append(workout["scoreDisplay"])
                ranks.append(workout["rank"])

            # skip all athletes/teams with incomplete scores (i.e. who withdraw is out)
            # it doesn't work for z-score/correlation calculation
            if any([x is None for x in scores]):
                if not any([s in FILENAME for s in ("cfg-", )]):  # exceptions
                    continue

            # write to csv
            csv_writer.writerow([name_to_hash(name), name, cty, age] + ranks + scores)

    csv_fileptr.close()
    time.sleep(0.5)
