# OKC Player Stats Backend

Backend scripts to load basketball player statistics into a PostgreSQL database, calculate player summaries, and rank player stats.

---

## Project Overview

This project implements a complete backend system for basketball player statistics, demonstrating backend engineering, data aggregation, and database management skills.

**Key features:**
- Loads raw CSV data into a normalized PostgreSQL database
- Ensures repeated runs do not duplicate data
- Calculates player summary statistics (shots, passes, turnovers) across different halfcourt actions
- Computes ranks for each stat relative to all players
- Prepares data for API consumption and frontend integration (frontend not included)

---

## Setup Instructions

1. **Install prerequisites**
   - Python 3.10+
   - PostgreSQL

2. **Create database and user**
createuser okcapplicant --createdb
createdb okc

3. **Load the exported database (optional)**
psql -U okcapplicant okc < backend/scripts/dbexport.psql

4. **Install Python dependencies**
pip install -r backend/requirements.txt

5. **Run the data loading and aggregation scripts**
python backend/scripts/load_data.py

6. **Verify tables and summaries in PostgreSQL**
psql -U okcapplicant okc
\dt
SELECT * FROM players LIMIT 5;
SELECT * FROM stats LIMIT 5;

