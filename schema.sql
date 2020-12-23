DROP SCHEMA IF EXISTS testing CASCADE;
CREATE SCHEMA testing;

DROP TABLE IF EXISTS college CASCADE;
DROP TABLE IF EXISTS college_statistics CASCADE;
DROP TABLE IF EXISTS college_students CASCADE;
DROP TABLE IF EXISTS college_tuition CASCADE;
DROP TABLE IF EXISTS historical_tuition CASCADE;
DROP TABLE IF EXISTS college_salary CASCADE;
DROP TABLE IF EXISTS college_diversity CASCADE;


CREATE TABLE college(
    collegeid VARCHAR(127) PRIMARY KEY,
    state VARCHAR(63)
);

CREATE TABLE college_statistics(
  collegeid VARCHAR(127) REFERENCES college,
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
    in_state INT,
    out_of_state INT,
    PRIMARY KEY(collegeid, yearid)
);

CREATE TABLE historical_tuition(
    college_type VARCHAR(127),
    yearid  INT,
    tuiton_type VARCHAR(127),
    tuition_cost INT,
    PRIMARY KEY(college_type, yearid, tuiton_type)
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
    enrollment INT,
    PRIMARY KEY(collegeid, diverse_group)
);

GRANT ALL PRIVILEGES ON college, college_students, college_statistics, college_tuition, 
                        historical_tuition, college_salary, college_diversity TO project_user;

DROP FUNCTION IF EXISTS verify_college;
DROP FUNCTION IF EXISTS verify_new_college;
DROP FUNCTION IF EXISTS verify_new_student;
DROP FUNCTION IF EXISTS verify_new_statistics;
DROP FUNCTION IF EXISTS verify_new_tuition;
DROP FUNCTION IF EXISTS verify_new_historical;
DROP FUNCTION IF EXISTS verify_new_salary;
DROP FUNCTION IF EXISTS verify_new_diversity;

CREATE FUNCTION verify_college() RETURNS TRIGGER
AS $$
BEGIN
  IF EXISTS (SELECT collegeid FROM college WHERE collegeid = NEW.collegeid)
    THEN RETURN NEW;
    ELSE INSERT INTO college VALUES(NEW.collegeid, NULL);
         RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION verify_new_college() RETURNS TRIGGER
AS $$
BEGIN
  IF EXISTS (SELECT collegeid FROM college WHERE collegeid = NEW.collegeid)
    THEN RETURN NULL;
    ELSE RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION verify_new_student() RETURNS TRIGGER
AS $$
BEGIN
  IF EXISTS (SELECT collegeid FROM college_students WHERE collegeid = NEW.collegeid)
    THEN RETURN NULL;
    ELSE RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION verify_new_statistics() RETURNS TRIGGER
AS $$
BEGIN
  IF EXISTS (SELECT collegeid FROM college_statistics WHERE collegeid = NEW.collegeid)
    THEN RETURN NULL;
    ELSE RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION verify_new_tuition() RETURNS TRIGGER
AS $$
BEGIN
  IF EXISTS (SELECT collegeid FROM college_tuition WHERE collegeid = NEW.collegeid)
    THEN RETURN NULL;
    ELSE RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION verify_new_historical() RETURNS TRIGGER
AS $$
BEGIN
  IF EXISTS (SELECT college_type
            FROM historical_tuition
            WHERE college_type = NEW.college_type
            AND yearid = NEW.yearid
            AND tuiton_type = NEW.tuiton_type)

    THEN RETURN NULL;
    ELSE RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION verify_new_salary() RETURNS TRIGGER
AS $$
BEGIN
  IF EXISTS (SELECT collegeid FROM college_salary WHERE collegeid = NEW.collegeid)
    THEN RETURN NULL;
    ELSE RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION verify_new_diversity() RETURNS TRIGGER
AS $$
BEGIN
  IF EXISTS (SELECT collegeid FROM college_diversity WHERE collegeid = NEW.collegeid AND diverse_group = NEW.diverse_group)
    THEN RETURN NULL;
    ELSE RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER verify_college_student_trigger
BEFORE INSERT ON college_students
FOR EACH ROW
EXECUTE PROCEDURE verify_college();

CREATE TRIGGER verify_college_statistic_trigger
BEFORE INSERT ON college_statistics
FOR EACH ROW
EXECUTE PROCEDURE verify_college();

CREATE TRIGGER verify_college_tuition_trigger
BEFORE INSERT ON college_tuition
FOR EACH ROW
EXECUTE PROCEDURE verify_college();

CREATE TRIGGER verify_college_salary_trigger
BEFORE INSERT ON college_salary
FOR EACH ROW
EXECUTE PROCEDURE verify_college();

CREATE TRIGGER verify_college_diversity_trigger
BEFORE INSERT ON college_diversity
FOR EACH ROW
EXECUTE PROCEDURE verify_college();


CREATE TRIGGER duplicate_college
BEFORE INSERT ON college
FOR EACH ROW
EXECUTE PROCEDURE verify_new_college();

CREATE TRIGGER duplicate_college_student_trigger
BEFORE INSERT ON college_students
FOR EACH ROW
EXECUTE PROCEDURE verify_new_student();

CREATE TRIGGER duplicate_college_statistic_trigger
BEFORE INSERT ON college_statistics
FOR EACH ROW
EXECUTE PROCEDURE verify_new_statistics();

CREATE TRIGGER duplicate_college_tuition_trigger
BEFORE INSERT ON college_tuition
FOR EACH ROW
EXECUTE PROCEDURE verify_new_tuition();

CREATE TRIGGER duplicate_college_historical_trigger
BEFORE INSERT ON historical_tuition
FOR EACH ROW
EXECUTE PROCEDURE verify_new_historical();

CREATE TRIGGER duplicate_college_salary_trigger
BEFORE INSERT ON college_salary
FOR EACH ROW
EXECUTE PROCEDURE verify_new_salary();

CREATE TRIGGER duplicate_college_diversity_trigger
BEFORE INSERT ON college_diversity
FOR EACH ROW
EXECUTE PROCEDURE verify_new_diversity();
