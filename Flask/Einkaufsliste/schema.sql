DROP TABLE IF EXISTS einkaufsliste; 
 
CREATE TABLE einkaufsliste( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    anzahl INTEGER NOT NULL 
);