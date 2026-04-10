1. Clone the repo
2. Log into MySQL and manually create the database
   1. mysql -u root -p
   2. CREATE DATABASE IF NOT EXISTS gamecafe;
3. cd into the cloned repo
4. mysql -u root -p < db_proof/schema.sql mysql -u root -p < db_proof/data.sql
5. Activate virtual environment: source venv/bin/activate
6. pip install -r requirements.txt