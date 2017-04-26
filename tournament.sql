DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;


CREATE TABLE playertournament(
    p_id SERIAL PRIMARY KEY,
    name TEXT
); 

CREATE TABLE matchtournament(
    m_id SERIAL PRIMARY KEY,
    loser INTEGER,
    winner INTEGER,
    FOREIGN KEY(winner) REFERENCES playertournament(p_id),
    FOREIGN KEY(loser) REFERENCES playertournament(p_id)
);

CREATE VIEW rankings AS SELECT p_id,name, (SELECT count(*) FROM matchtournament WHERE playertournament.p_id = matchtournament.winner) AS wins, (SELECT count(*) FROM matchtournament WHERE playertournament.p_id IN (matchtournament.loser,matchtournament.winner)) AS played FROM playertournament ORDER BY wins DESC;
