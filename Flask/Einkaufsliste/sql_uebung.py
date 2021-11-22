import sqlite3 
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly' 

@app.route("/")

@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == '__main__':  
    app.run(debug=True)

# def create():

#     connection = sqlite3.connect('database.db') 
    
#     with open('schema.sql') as file: 
#         connection.executescript(file.read()) 
    
#     connection.commit() 
#     connection.close() 

# create()


# def einfügen(Name, Anzahl):
#     connection = sqlite3.connect('database.db')
#     cur = connection.cursor()
#     cur.execute("INSERT INTO einkaufsliste (name, anzahl) VALUES (?,?)", (Name, Anzahl))
#     connection.commit() 
#     connection.close() 

# einfügen("Äpfel", 12)
# einfügen("Toast", 1)
# einfügen("Schokolade", 3)
# einfügen("Rotwein", 10)
# einfügen("Vodka", 2)
# einfügen("RedBull", 1)

# def ausgabe():
#     connection = sqlite3.connect('database.db')
#     cur = connection.cursor()
#     rows = cur.execute("SELECT name, anzahl FROM einkaufsliste").fetchall()

#     for row in rows:
#         print(row)

#     connection.commit()
#     connection.close()

# ausgabe()