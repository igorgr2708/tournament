-- Deletes all previous created views, tables and databases
DROP DATABASE IF EXISTS tournament;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;
DROP VIEW IF EXISTS standings;


-- Creates the new database
CREATE DATABASE tournament;


-- To work with tournament database
\c tournament;


-- Creates table players
CREATE TABLE players(id SERIAL PRIMARY KEY ,
                     name VARCHAR);


-- Creates table matches
CREATE TABLE matches(match_id SERIAL PRIMARY KEY,
                     winner INTEGER REFERENCES players(id),
                     loser INTEGER REFERENCES players(id));


-- Creates view to retrieve player's standings in format (id, name, wins, matches)
CREATE VIEW standings AS
  select players.id,
    players.name,
    (select count(*) from matches where matches.winner=players.id) as wins,
    (select count(*) from matches where matches.winner=players.id or matches.loser=players.id) as matches_total
  from players order by wins desc;
