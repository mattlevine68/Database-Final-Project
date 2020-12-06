-- Which state has the worst grad rate but the highest tuition and whats there fulltime_undergrad
SELECT c.collegeid AS college, c.state, cs.grad_rate, cs.fulltime_undergrad, ct.in_state, ct.out_of_state, csa.making_a_difference
FROM college c, (SELECT c.state, SUM(grad_rate), SUM(fulltime_undergrad)
                 FROM college_students
                 WHERE c.collegeid = college_students.collegeid
                 GROUP BY c.state) AS cs



      SELECT c.state, ROUND(AVG(CAST(cs.grad_rate AS NUMERIC)),2) AS grad_rate_avg, ROUND(AVG(CAST(cs.fulltime_undergrad AS NUMERIC)),2) AS fulltime_undergrad_AVG,
      ROUND(AVG(CAST(ct.in_state AS NUMERIC)),2) AS in_state_avg, ROUND(AVG(CAST(ct.out_of_state AS NUMERIC)),2) AS out_of_state_avg,
      ROUND(AVG(CAST(csa.making_a_difference AS NUMERIC)),2) AS making_a_difference_avg
      FROM college_students cs, college c, college_tuition ct, college_salary csa
      WHERE c.collegeid = cs.collegeid
      AND c.collegeid = ct.collegeid
      AND c.collegeid = csa.collegeid
      GROUP BY c.state
      ORDER BY grad_rate_avg ASC;


CREATE TABLE college(
    collegeid VARCHAR(127) PRIMARY KEY,
    state VARCHAR(63)
);

CREATE TABLE college_tuition(
    collegeid VARCHAR(127) REFERENCES college,
    yearid INT,
    degree_length SMALLINT,
    room_board INT,
    in_state INT,
    out_of_state INT,
    PRIMARY KEY(collegeid, yearid)
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

CREATE TABLE college_salary(
    collegeid VARCHAR(127) REFERENCES college,
    early_career INT,
    mid_career INT,
    making_a_difference FLOAT
);
