# Swiss System Application

## Installation Instructions
1. Install Python from https://www.python.org/downloads/

2. Install PostgreSQL database from https://www.postgresql.org/download/

3. Verify that everything is installed properly :
    * In command line run :
        ``` python --version ```
    * If you can see the python version - everything is ok
    * In command line run
          ``` psql --version```
    * If you can see the PostgreSQL version - everything is ok

4. In command line go to tournament folder and run:
    * ```psql``` to enter the database
    * ```\i tournament.sql``` - this will install the schema in database
    
    
5. Now to make a test run of the program, write in command line:
    ``` python tournament_test.py ```
    * If all the test pass and you receive the following message :
    * ``` Success!  All tests pass! ```

    * That means that everything works properly!



          
## Project Structure
    * tournament.sql - SQL Schema installation file. Use it to install the required database and the tables within it.
    * tournament.py - Main application file, contains methods to manipulate the players and matches.
    * tournament_test.py - Test file. Used to check that everything works properly.
    * README.md - This file with instructions.
