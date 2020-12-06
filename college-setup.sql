DROP DATABASE IF EXISTS final_project;
CREATE DATABASE final_project;

DROP USER IF EXISTS project_user;
CREATE USER project_user WITH PASSWORD 'goodGrades';

GRANT ALL PRIVILEGES ON DATABASE final_project TO project_user;
ALTER USER project_user SET search_path = testing;
