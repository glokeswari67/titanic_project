TITANIC DATA ANALYSIS PROJECT
PostgreSQL + Python + Pandas + Streamlit

IMPORTANT:
The ZIP contains the complete project code and SQL. The Titanic CSV is not embedded.
Download it from:
https://raw.githubusercontent.com/dsindy/kaggle-titanic/master/data/train.csv

Save the file as Titanic-Dataset.csv inside this project folder.
The expected CSV has 891 data rows and these 12 columns:
PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked

STEP 1 - Create the database
Open pgAdmin 4.
Right-click Databases > Create > Database.
Database name: titanic_db
Save.

STEP 2 - Create tables
Open Query Tool for titanic_db.
Open and execute 01_database_setup.sql.
The script creates schema and tables. The INSERT section can be run after CSV import.

STEP 3 - Import CSV
In pgAdmin expand:
titanic_db > Schemas > titanic_project > Tables
Right-click titanic_staging > Import/Export Data.
Choose Import.
Filename: browse to Titanic-Dataset.csv
Format: csv
Encoding: UTF8
Header: Yes
Delimiter: ,
Quote: "
Click OK.

STEP 4 - Copy staging rows into final table
In Query Tool run:
INSERT INTO titanic_project.passengers
SELECT * FROM titanic_project.titanic_staging
ON CONFLICT (passengerid) DO NOTHING;

If you already ran the INSERT statement inside 01_database_setup.sql, do not run it again.
Check:
SELECT COUNT(*) FROM titanic_project.passengers;
Expected: 891

STEP 5 - Install Python packages
Open this project folder in VS Code.
Open Terminal > New Terminal.
Run:
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt

If PowerShell blocks activation, run this once in the same terminal:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
Then activate again.

STEP 6 - Set PostgreSQL password
In the same VS Code terminal, run:
$env:PGPASSWORD="YOUR_POSTGRES_PASSWORD"

Replace YOUR_POSTGRES_PASSWORD with the password you created for PostgreSQL.
Optional if your PostgreSQL settings differ:
$env:PGHOST="localhost"
$env:PGPORT="5432"
$env:PGDATABASE="titanic_db"
$env:PGUSER="postgres"

STEP 7 - Run the app
streamlit run app.py

The app should open in your browser.

FILES
01_database_setup.sql - schema, staging/final tables and analysis queries
db.py - PostgreSQL connection and pandas query helper
app.py - Streamlit dashboard, data explorer, SQL practice and quiz
requirements.txt - required Python packages

TROUBLESHOOTING
1. password authentication failed: set the correct PGPASSWORD in the terminal.
2. relation passengers does not exist: run the SQL setup and data-copy steps.
3. no rows shown: check that CSV import completed and passengers has 891 rows.
4. streamlit is not recognized: activate venv and run py -m pip install -r requirements.txt.
5. Import column error: ensure the CSV header and order match the 12 columns listed above.

Submit the project folder/ZIP plus screenshots of the running dashboard and SQL validation if your instructor asks for them.
