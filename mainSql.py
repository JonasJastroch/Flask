import sqlite3

verbindung = sqlite3.connect("datenbank/test.db")
zeiger = verbindung.cursor()

#zeiger.execute("CREATE TABLE test2(vorname TEXT, nachname TEXT, geburtstag DATE)")
#zeiger.execute("DELETE FROM test2")
#zeiger.execute("""INSERT INTO test VALUES (?,?,?)""", ("Felix", "Förster", "09.05.2004"))

zeiger.execute("SELECT * FROM test")
inhalt = zeiger.fetchall()
print(inhalt)

verbindung.commit()
verbindung.close()