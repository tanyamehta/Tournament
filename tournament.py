
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        database_name = 'tournament'
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")



def deleteMatches():
    """Remove all the match records from the database."""
    DB, cursor = connect()
    q = "TRUNCATE " + "match_tournament"
    cursor.execute(q)
    DB.commit()
    cursor.close()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB, cursor = connect()
    q = "TRUNCATE " + "player_tournament"
    cursor.execute(q)
    DB.commit()
    cursor.close()
    DB.close()
    

def countPlayers():
    """Returns the number of player_tournament currently registered."""
    query = """SELECT count(*) FROM player_tournament"""
    r = select(query)
    return int(r[0][0])


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    if name:
        q = "INSERT INTO player_tournament(name) VALUES(%s)"
        DB, cursor = connect()
        cursor.execute(q, (name,))
        DB.commit()
        cursor.close()
        DB.close()
    else:
        return False


def playerStandings():
    """Returns a list of the player_tournament and their win records, sorted by wins.
    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, match_tournament):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of match_tournament the player has won
        match_tournament: the number of match_tournament the player has played
    """
    q = "SELECT p_id,name,wins,played FROM rankings"
    return select(q)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two player_tournament.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, cursor = connect()
    query = "INSERT INTO match_tournament(winner,loser) VALUES(%s,%s)"
    cursor.execute(query, (winner, loser))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of player_tournament for the next round of a match.
    Assuming that there are an even number of player_tournament registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB, cursor = connect()
    pairList = []
    totalPairs = countPlayers()
    for pair in xrange(0, totalPairs, 2):
        query = """SELECT p_id,name FROM rankings ORDER BY wins
        LIMIT 2 OFFSET """ + str(pair)
        cursor.execute(query)
        result = cursor.fetchall()
        result = select(query)
        result = (result[0]+result[1])
        pairList.append(result)
    return pairList
