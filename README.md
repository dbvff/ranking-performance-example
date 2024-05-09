# Ranking system based on competition performance data 
The is a example to demonstrate the performance-based ranking system

## Installation (How to run it?)

```sh
# Installation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# C3PO: extract and feature engineering
python c3po-download.py
python c3po-extract.py
python c3po-transform.py
python data/3-locked/c3po/compute-cfg23.py

# CC: extract and feature engineering
python cc-extract.py
python cc-transform.py

# compute z-scores, correlations, ranking points
python ranking-example.py
```


## Folder Structure
The datasets are **not** of this software library (principle: seperate software from data).

- `data/` 
    - `0-raw` - raw data files, e.g. C3PO API dump, CC JSON files
    - `1-extracted` - CSV files hashed names, ranks and scores as columns
    - `2-transform` - CSV files with Z-scores, adjustment factors, competitiveness scores
    - `3-locked` - manually edited CSV files, e.g. CFG'23 to make the cuts work, different hashes for surname changes.
    - `4-results` - ranking tables, overview with competitiveness scores
