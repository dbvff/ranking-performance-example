import json
import requests
import os

os.makedirs("data/0-raw/c3po/", exist_ok=True)

def download(url, file):
    try:
        # download first page
        req = requests.get(f"{url}")
        data = req.json()
        page_count = data['pagination']['totalPages']
        # loop over all pages
        pages = []
        for i in range(1, page_count+1):
            req = requests.get(f"{url}&page={i}")
            pages.append(req.json())
        # save
        json.dump(pages, open(file, "w"))
    except Exception as err:
        print(err)



# CF Semifinals
semis = [
    ("africa", 215),
    ("asia", 217),
    ("europe", 218),
    ("na-east", 219),
    ("na-west", 220),
    ("oceania", 221),
    ("south-am", 222),
]

year = 23
for cname, did in semis:
    # CF Semi '23, M
    url = f"https://c3po.crossfit.com/api/competitions/v2/competitions/semifinals/20{year}/leaderboards?semifinal={did}&division=1&sort=0"
    download(url, f"data/0-raw/c3po/cf-semi-{cname.lower()}-{year}_M.json")
    # CF Semi '23, M
    url = f"https://c3po.crossfit.com/api/competitions/v2/competitions/semifinals/20{year}/leaderboards?semifinal={did}&division=2&sort=0"
    download(url, f"data/0-raw/c3po/cf-semi-{cname.lower()}-{year}_F.json")
    # CF Semi '23, MMFF
    # url = f"https://c3po.crossfit.com/api/competitions/v2/competitions/semifinals/20{year}/leaderboards?semifinal={did}&division=11&sort=0"
    # download(url, "data/0-raw/c3po/cf-semi-{cname.lower()}-{year}_MMFF.json")



# CFG'23 M
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/games/2023/leaderboards?division=1&sort=0'
download(url, "data/0-raw/c3po/cfg-23_M.json")
# CFG'23 F
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/games/2023/leaderboards?division=2&sort=0'
download(url, "data/0-raw/c3po/cfg-23_F.json")
# CFG'23 MMFF 
# url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/games/2023/leaderboards?division=11&sort=0'
# download(url, "data/0-raw/c3po/cfg-23_MMFF.json")
# Masters & Teens hatte sich niemand qualifiziert


# CF Quarter '24, M
# url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=229&division=1&region=0&sort=0'
# download(url, "data/0-raw/c3po/cf-quarter-24_M.json")
# # CF Quarter '24, F
# url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=229&division=2&region=0&sort=0'
# download(url, "data/0-raw/c3po/cf-quarter-24_F.json")
# CF Quarter '24, Team
# url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=231&division=11&region=0&sort=0'
# download(url, "data/0-raw/c3po/cf-quarter-24_MMFF.json")


# # CF Open'24, M (too much data)
# url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/open/2024/leaderboards?division=1&region=0&sort=0'
# download(url, "data/0-raw/c3po/cf-open-24_M.json")

# # CF Open'24, F (too much data)
# url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/open/2024/leaderboards?division=2&region=0&sort=0'
# download(url, "data/0-raw/c3po/cf-open-24_F.json")

# # CF Open'24, MMFF (pointless because it's just Indy score and not actual team scores)
# url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/open/2024/leaderboards?division=11&region=0&sort=0'
# download(url, "data/0-raw/c3po/cf-open-24_MMFF.json")




# CF Quarter '24, M, 35-39
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=18&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_M_35-39.json")
# CF Quarter '24, M, 40-44
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=12&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_M_40-44.json")
# CF Quarter '24, M, 45-49
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=3&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_M_45-49.json")
# CF Quarter '24, M, 50-54
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=5&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_M_50-54.json")
# CF Quarter '24, M, 55-59
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=7&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_M_55-59.json")
# CF Quarter '24, M, 60-64
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=36&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_M_60-64.json")
# CF Quarter '24, M, 65+
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=38&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_M_65+.json")
# CF Quarter '24, M, 16-17
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=16&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_M_16-17.json")
# CF Quarter '24, M, 14-15
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=14&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_M_14-15.json")

# CF Quarter '24, F, 35-39
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=19&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_F_35-39.json")
# CF Quarter '24, F, 40-44
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=13&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_F_40-44.json")
# CF Quarter '24, F, 45-49
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=4&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_F_45-49.json")
# CF Quarter '24, F, 50-54
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=6&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_F_50-54.json")
# CF Quarter '24, F, 55-59
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=8&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_F_55-59.json")
# CF Quarter '24, F, 60-64
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=37&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_F_60-64.json")
# CF Quarter '24, F, 65+
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=39&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_F_65+.json")
# CF Quarter '24, F, 16-17
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=17&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_F_16-17.json")
# CF Quarter '24, F, 14-15
url = 'https://c3po.crossfit.com/api/competitions/v2/competitions/quarterfinals/2024/leaderboards?quarterfinal=230&division=15&region=0&sort=0'
download(url, "data/0-raw/c3po/cf-quarter-24_F_14-15.json")

