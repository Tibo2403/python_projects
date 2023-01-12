# SQLITE : CREATION DE LA TABLE

import sqlite3

# connexion = "albums2.db"
# executer / curseur
# commit
# fermer

connexion = sqlite3.connect("albums2.db")

sql_table_artiste = """CREATE TABLE artiste (
    artiste_id INTEGER NOT NULL PRIMARY KEY, 
    nom VARCHAR);"""

# con.execute(sql_table_artiste)
curseur = connexion.cursor()
curseur.execute(sql_table_artiste)
curseur.execute("""CREATE TABLE album (
    album_id INTEGER NOT NULL PRIMARY KEY,
    artiste_id INTEGER REFERENCES artiste,
    titre VARCHAR,
    annee_sortie INTEGER);""")

connexion.commit()
connexion.close()