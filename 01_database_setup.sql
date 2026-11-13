CREATE SCHEMA IF NOT EXISTS titanic_project;

CREATE TABLE IF NOT EXISTS titanic_project.titanic_staging (
    passengerid INTEGER,
    survived INTEGER,
    pclass INTEGER,
    name TEXT,
    sex VARCHAR(10),
    age DOUBLE PRECISION,
    sibsp INTEGER,
    parch INTEGER,
    ticket TEXT,
    fare DOUBLE PRECISION,
    cabin TEXT,
    embarked VARCHAR(5)
);

CREATE TABLE IF NOT EXISTS titanic_project.passengers (
    passengerid INTEGER PRIMARY KEY,
    survived INTEGER CHECK (survived IN (0,1)),
    pclass INTEGER,
    name TEXT,
    sex VARCHAR(10),
    age DOUBLE PRECISION,
    sibsp INTEGER,
    parch INTEGER,
    ticket TEXT,
    fare DOUBLE PRECISION,
    cabin TEXT,
    embarked VARCHAR(5)
);

-- After importing Titanic-Dataset.csv into titanic_staging, run this:
INSERT INTO titanic_project.passengers
SELECT passengerid, survived, pclass, name, sex, age, sibsp, parch,
       ticket, fare, cabin, embarked
FROM titanic_project.titanic_staging
ON CONFLICT (passengerid) DO UPDATE SET
    survived = EXCLUDED.survived,
    pclass = EXCLUDED.pclass,
    name = EXCLUDED.name,
    sex = EXCLUDED.sex,
    age = EXCLUDED.age,
    sibsp = EXCLUDED.sibsp,
    parch = EXCLUDED.parch,
    ticket = EXCLUDED.ticket,
    fare = EXCLUDED.fare,
    cabin = EXCLUDED.cabin,
    embarked = EXCLUDED.embarked;

-- Data validation
SELECT COUNT(*) AS total_passengers FROM titanic_project.passengers;

SELECT
    COUNT(*) AS total_records,
    COUNT(age) AS available_age,
    COUNT(*) - COUNT(age) AS missing_age,
    COUNT(embarked) AS available_embarked,
    COUNT(*) - COUNT(embarked) AS missing_embarked,
    COUNT(cabin) AS available_cabin,
    COUNT(*) - COUNT(cabin) AS missing_cabin
FROM titanic_project.passengers;

-- Analysis queries
SELECT survived, COUNT(*) AS passenger_count
FROM titanic_project.passengers
GROUP BY survived
ORDER BY survived;

SELECT sex, COUNT(*) AS total,
       SUM(survived) AS survivors,
       ROUND(100.0 * SUM(survived) / COUNT(*), 2) AS survival_percentage
FROM titanic_project.passengers
GROUP BY sex;

SELECT pclass, COUNT(*) AS total,
       SUM(survived) AS survivors,
       ROUND(100.0 * SUM(survived) / COUNT(*), 2) AS survival_percentage
FROM titanic_project.passengers
GROUP BY pclass
ORDER BY pclass;

SELECT embarked, COUNT(*) AS passenger_count
FROM titanic_project.passengers
GROUP BY embarked
ORDER BY embarked;

SELECT
    CASE
        WHEN age < 18 THEN 'Child'
        WHEN age < 60 THEN 'Adult'
        WHEN age >= 60 THEN 'Senior'
        ELSE 'Unknown'
    END AS age_group,
    COUNT(*) AS total,
    SUM(survived) AS survivors
FROM titanic_project.passengers
GROUP BY age_group
ORDER BY age_group;

SELECT pclass, ROUND(AVG(fare)::numeric, 2) AS average_fare
FROM titanic_project.passengers
GROUP BY pclass
ORDER BY pclass;
