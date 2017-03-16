DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE player_tournament(
    p_id SERIAL PRIMARY KEY,
    name TEXT
); 

CREATE TABLE match_tournament(
    m_id SERIAL PRIMARY KEY,
    loser INTEGER,
    winner INTEGER
);

CREATE VIEW rankings AS SELECT p_id,name, (SELECT count(*) FROM match_tournament WHERE player_tournament.p_id = match_tournament.winner) AS wins, (SELECT count(*) FROM match_tournament WHERE player_tournament.p_id IN (match_tournament.loser,match_tournament.winner)) AS played FROM player_tournament ORDER BY wins DESC;
