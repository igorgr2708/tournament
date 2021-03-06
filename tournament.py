#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

# Method returns the connection object to Database


def connect():
    """Returns connection and cursor objects."""
    conn = psycopg2.connect("dbname=tournament")
    cursor = conn.cursor()
    return conn, cursor

def commit(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()


# Method cleans the code against SQL injection.


def clean_sql(dirty_sql):
    """Method cleans the code against SQL injection.
       Args:
           dirty_sql: initial sql code to be cleaned.
    """
    return bleach.clean(dirty_sql, tags=['>'],)


# Method deletes all the matches from 'matches' table and
# sets to zero matches and wins in 'players' table.


def deleteMatches():
    """Method deletes all the matches from 'matches' table and
       sets to zero matches and wins in 'players' table.
    """
    conn, cursor = connect()
    cursor.execute(clean_sql("DELETE FROM matches;"))
    commit(conn, cursor)


# Method deletes all players records from 'players' table.
def deletePlayers():
    """Method deletes all players records from 'players' table."""
    conn, cursor = connect()
    cursor.execute(clean_sql("DELETE FROM players;"))
    commit(conn, cursor)


# Method returns the number of currently registered players.
def countPlayers():
    """Method returns the number of currently registered players."""
    conn, cursor = connect()
    cursor.execute(clean_sql("SELECT count(*) FROM players;"))
    count = cursor.fetchone()[0]
    commit(conn, cursor)
    return count


# Method inserts the new player record in the 'players' table.
def registerPlayer(name):
    """Method inserts the new player record in the 'players' table.
       Args:
           name: Username
    """
    conn, cursor = connect()

    SQL = clean_sql("INSERT INTO players(name) VALUES(%s)")
    data = (clean_sql(name),)
    cursor.execute(SQL, data)
    commit(conn, cursor)


# Method returns the list of players with their wins and matches data.
def playerStandings():
    """Method returns the list of players with their wins and matches data."""
    conn, cursor = connect()
    cursor.execute(
        clean_sql("select * from standings;"))
    list_of_players = cursor.fetchall()
    commit(conn, cursor)
    return list_of_players


# Method updates the 'matches' table and players' wins and matches records.
def reportMatch(winner, loser):
    """Method updates the 'matches' table and players' wins and matches records.
       Args:
           winner: player_id of the winner
           loser : player_id of the loser
    """
    conn, cursor = connect()

    SQL = clean_sql("INSERT INTO matches(winner, loser) VALUES(%s, %s)")
    data = (clean_sql(winner), clean_sql(loser),)

    cursor.execute(SQL, data)
    commit(conn, cursor)

# Method returns the list of tuples for next round of Swiss system.


def swissPairings():
    """Method returns the list of tuples for next round of Swiss system."""
    conn, cursor = connect()
    cursor.execute("SELECT * FROM standings;")
    list_of_players = cursor.fetchall()

    pairs = []

    for i in range(0, len(list_of_players)):
        if i % 2 == 0:
            pair = (list_of_players[i][0], list_of_players[i][1],
                    list_of_players[i + 1][0], list_of_players[i + 1][1])

            pairs.append(pair)
    commit(conn, cursor)
    return pairs

# Method cleans the code against SQL injection.
def clean_sql(dirty_sql):
    """Method cleans the code against SQL injection.
       Args:
           dirty_sql: initial sql code to be cleaned.
    """
    return bleach.clean(dirty_sql, tags=['>'],)
