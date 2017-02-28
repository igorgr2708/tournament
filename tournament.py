#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

# Method returns the connection object to Database


def connect():
    """Returns connection object."""
    return psycopg2.connect("dbname=tournament")

# Method deletes all the matches from 'matches' table and
# sets to zero matches and wins in 'players' table.


def deleteMatches():
    """Method deletes all the matches from 'matches' table and
       sets to zero matches and wins in 'players' table.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(clean_sql("DELETE FROM matches;"))
    cursor.execute(clean_sql("UPDATE players SET player_matches_number = 0;"))
    cursor.execute(clean_sql("UPDATE players SET player_wins_number = 0;"))
    conn.commit()
    cursor.close()
    conn.close()


# Method deletes all players records from 'players' table.
def deletePlayers():
    """Method deletes all players records from 'players' table."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(clean_sql("DELETE FROM players;"))
    conn.commit()
    cursor.close()
    conn.close()


# Method returns the number of currently registered players.
def countPlayers():
    """Method returns the number of currently registered players."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(clean_sql("SELECT count(*) FROM players;"))
    return cursor.fetchone()[0]


# Method inserts the new player record in the 'players' table.
def registerPlayer(name):
    """Method inserts the new player record in the 'players' table.
       Args:
           name: Username
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(clean_sql("INSERT INTO "
                             "players(player_name,player_matches_number,"
                             "player_wins_number) VALUES(%s, 0, 0)"), (name,))
    conn.commit()
    cursor.close()
    conn.close()


# Method returns the list of players with their wins and matches data.
def playerStandings():
    """Method returns the list of players with their wins and matches data."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        clean_sql("SELECT * FROM players ORDER BY player_wins_number DESC;"))
    list_of_players = cursor.fetchall()
    cursor.close()
    conn.close()
    return list_of_players


# Method updates the 'matches' table and players' wins and matches records.
def reportMatch(winner, loser):
    """Method updates the 'matches' table and players' wins and matches records.
       Args:
           winner: player_id of the winner
           loser : player_id of the loser
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        clean_sql("INSERT INTO matches(winner_id, loser_id) VALUES(%s, %s)"),
        (winner, loser,))

    cursor.execute(clean_sql("UPDATE PLAYERS SET player_matches_number = "
                             "player_matches_number + 1 "
                             "WHERE player_id=%d;" % winner))
    cursor.execute(
        clean_sql("UPDATE PLAYERS SET "
                  "player_wins_number = player_wins_number + 1 "
                  "WHERE player_id=%d;" % winner))
    cursor.execute(
        clean_sql("UPDATE PLAYERS SET "
                  "player_matches_number = player_matches_number + 1 "
                  "WHERE player_id=%d;" % loser))

    conn.commit()
    cursor.close()
    conn.close()

# Method returns the list of tuples for next round of Swiss system.


def swissPairings():
    """Method returns the list of tuples for next round of Swiss system."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(clean_sql("SELECT player_id, player_name FROM players"
                             " ORDER BY player_wins_number DESC;"))
    list_of_players = cursor.fetchall()

    pairs = []

    for i in range(0, len(list_of_players)):
        if i % 2 == 0:
            pair = (list_of_players[i][0], list_of_players[i][1],
                    list_of_players[i+1][0], list_of_players[i+1][1])

            pairs.append(pair)

    cursor.close()
    conn.close()
    return pairs

# Method cleans the code against SQL injection.


def clean_sql(dirty_sql):
    """Method cleans the code against SQL injection.
       Args:
           dirty_sql: initial sql code to be cleaned.
    """
    return bleach.clean(dirty_sql, tags=[],)
