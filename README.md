# Database Final Project

# Order to run code:
  1. Get requirements from requirements.txt downloaded
  2. db-setup.sql
  3. load_data.py
  4. application.py

# Steps for each file:
  ## requirements.txt:
    - run in terminal pip install -r requirements.txt in terminal

  ## db-setup.sql
    - run in terminal psql -U postgres postgres < db-setup.sql

  ## load_data.py:
      - run in terminal python load_data.py or python3 load_data.py if that's how its setup
        - if mongodb is set up differently might be a problem, I don't really know I haven't used it too much

  ## application.py:
      - run in terminal python application.py or python3 application.py if that's how its setup
        - results will show in terminal, if it is hard to read make terminal window bigger


# Descriptions of Queries in application.py:
  ## Career Stem Query:
    - Options for input (Limit, State)
    - Return the college, state, percent of students in stem and how much students make early career where we have 
      data for percent of students in stem. Users have the option to get total result or results of a specific state
      and can limit how many results they see.

  ## Diversity Query:
    - Options for input (Limit)
    - Returns the college, state, how many minorities are enrolled in a school, in state tuition and 
      out of state tuition. Users have an option to limit the results they see.

  ## Grad Rate Query:
    - Options for input (Min Samples)
    - Returns the state, average grad rate for the state, average full time undergrads for the state, 
      average in state tuition, average out of state tuition and the average percent of people believing 
      they made a difference. Users have the option to have a minimum amount of colleges for each state.

  ## Winning Enrolled Query:
    - Options for input (Win Percent, Enrolled)
    - First returns the schools that have a win percent greater than a user inputed number for either 
      football or basketball (using MongoDB). The next query returns the college, state, how many 
      students are enrolled and if the school is public or private for schools that fulfilled the first
      queries. Users can choose what the win percent the sports team have to be greater than and what 
      the number of students enrolled has to be greater than

  ## Winning Tech Query:
    - Options for input (Limit, Power Rating, Offensive Rank)
    - First returns the schools that have a Power Rating (How likely to beat a d1 team) and made the playoffs, 
      or have a football team that has more wins than losses but have a certain offensive ranking. The next query 
      returns the college, state, percent of professors with PhDs and the percent of students in stem for schools
      that fulfill the first queries. The user has the option to limit the results, choose the power rating 
      and choose the offensive ranking.


# Challenges Faced:
  - Learned about MongoDB in class but I never used before so I don't think my queries are the best
    - Had to do the intersection of two Mongodb queries in Python because of that
  - Never made a widget before so not the neatest
  - Gave a lot of flexibility to the users but probably could've did a better job in writing out my code in database.py

# Requirements:
  - PSQL
  - MongoDB (I used 4.4 in case a problem arises)
