-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE DATABASE tournament;


\c tournament;

CREATE TABLE players(player_id SERIAL,
                     player_name VARCHAR,
                     player_wins_number INTEGER,
                     player_matches_number INTEGER);


CREATE TABLE matches(match_id SERIAL,
                     winner_id INTEGER,
                     loser_id INTEGER);
