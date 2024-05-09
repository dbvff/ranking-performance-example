import json
import glob
import csv
import os
import time
from fn_extract import name_to_hash


PATH_IN = "data/0-raw/cc"
PATH_OUT = "data/1-extracted/cc"

FILES = glob.glob(f"{PATH_IN}/*.json")
os.makedirs(PATH_OUT, exist_ok=True)


for JSONFILE in FILES:
    # Load file
    #JSONFILE = FILES[0]
    data = json.load(open(JSONFILE))

    # loop through all lines
    for subcatg in data:
        # get data for leaderboard
        workout_units = [d["caption"].lower() for d in subcatg["workouts"]]
        workout_keys = [d["key"] for d in subcatg["workouts"]]
        num_cols = len(workout_keys)
        #workout_units = [d["caption"].lower() for d in subcatg["workouts"]]

        # gender and division name
        gender = subcatg["scoringGroup"]["gender"]
        division = subcatg["scoringGroup"]["caption"].lower()
        if gender in ("female", "male"):
            gender = "F" if gender == "female" else "M"
            division = "".join([s for s in division if s in "0123456789+-"])
        else:
            gender = "NA"

        if len(division) < 3:
            division = subcatg["scoringGroup"]["caption"].replace(" ", "").replace("_", "-").strip() 


        # init CSV File
        FILENAME = JSONFILE.split("/")[-1].split(".")[0]
        CSVFILE = f"{PATH_OUT}/{FILENAME}_{gender}_{division}.csv"
        csv_fileptr = open(CSVFILE, "w")
        csv_writer = csv.writer(
            csv_fileptr, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(["hash", "name", "cty", "age"] \
                            + [f"rank_{i+1}" for i in range(num_cols)] \
                            + [f"score_{i+1}" for i in range(num_cols)] \
                            + workout_units)
        # loop over lines
        for row in subcatg["athletes"]:
            # start reading data
            name = row["name"].upper()
            cty = row["countryShortCode"] #.upper()
            ranks, scores = [], []
            for wkey in workout_keys:
                if row["workoutScores"][wkey]["res"].lower() in ('-', 'wd', 'cap +0', "dnf"):
                    scores.append( None )
                else:
                    scores.append( row["workoutScores"][wkey]["res"] )
                ranks.append( row["workoutScores"][wkey]["rankInnerValue"] )
            
            # skip all athletes/teams with incomplete scores (i.e. who withdraw is out)
            # it doesn't work for z-score/correlation calculation
            if any([x is None for x in scores]):
                #if not any([s in FILENAME for s in ("cfg-", )]):  # exceptions
                continue
            
            # write to csv
            csv_writer.writerow([name_to_hash(name), name, cty, None] + ranks + scores)

        csv_fileptr.close()
        time.sleep(0.5)
