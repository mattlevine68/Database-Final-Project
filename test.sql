SELECT ce.collegeid AS college, c.state, ce.enrollment_total AS minorities_enrolled, ct.in_state, ct.out_of_state
FROM college c, (SELECT collegeid, SUM(enrollment) AS enrollment_total
                 FROM college_diversity cd
                 GROUP BY cd.collegeid) AS ce
JOIN college_tuition ct ON ct.collegeid = ce.collegeid
WHERE ce.collegeid = c.collegeid
ORDER BY ce.enrollment_total DESC
LIMIT 10;




-- CREATE TABLE college(
--     collegeid VARCHAR(127) PRIMARY KEY,
--     state VARCHAR(63)
-- );
--
-- CREATE TABLE college_diversity(
--     collegeid VARCHAR(127) REFERENCES college,
--     diverse_group VARCHAR(127),
--     enrollment INT
-- );
--
-- CREATE TABLE college_tuition(
--     collegeid VARCHAR(127) REFERENCES college,
--     yearid INT,
--     degree_length SMALLINT,
--     room_board INT,
--     in_state INT,
--     out_of_state INT,
--     PRIMARY KEY(collegeid, yearid)
-- );
