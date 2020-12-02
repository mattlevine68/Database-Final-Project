DROP TABLE IF EXISTS college CASCADE;
DROP TABLE IF EXISTS college_students CASCADE;
DROP TABLE IF EXISTS college_tuition CASCADE;
DROP TABLE IF EXISTS historical_tuition CASCADE;
DROP TABLE IF EXISTS college_salary CASCADE;
DROP TABLE IF EXISTS college_diversity CASCADE;


CREATE TABLE college(
    collegeid VARCHAR(127) PRIMARY KEY,
    state CHAR(2),
    type VARCHAR(31),
    applications INT,
    accepted INT,
    enrolled INT,
    professor_with_phd FLOAT,
    faculity_with_terminal FLOAT

);

CREATE TABLE college_students(
    collegeid VARCHAR(127) REFERENCES college,
    top10_students INT,
    top25_students INT,
    fulltime_undergrad INT,
    parttime_undergrad INT,
    grad_rate FLOAT,
    percent_stem FLOAT
);

CREATE TABLE college_tuition(
    collegeid VARCHAR(127) REFERENCES college,
    yearid INT,
    degree_length SMALLINT,
    room_board INT,
    books INT,
    personal INT,
    in_state INT,
    out_of_state INT,
    PRIMARY KEY(collegeid, yearid)
);

CREATE TABLE historical_tuition(
    college_type VARCHAR(127),
    yearid  INT,
    tuiton_type VARCHAR(127),
    tuition_cost INT
);

CREATE TABLE college_salary(
    collegeid VARCHAR(127) REFERENCES college,
    early_career INT,
    mid_career INT,
    making_a_difference FLOAT
);

CREATE TABLE college_diversity(
    collegeid VARCHAR(127) REFERENCES college,
    diverse_group VARCHAR(127),
    enrollment INT
);

GRANT ALL PRIVILEGES ON college, college_students, college_tuition, historical_tuition, college_salary, college_diversity TO project_user;
