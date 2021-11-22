from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)

title = "Login-Test"
text = ""
user = ""

def set_unlogged():
    print("Ausloggen...")
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    zeiger = conn.cursor()

    zeiger.execute("UPDATE login SET logged=? WHERE logged=?", ("0", "1"))

    conn.commit()
    conn.close()

def get_status():
    conn = sqlite3.connect("data.db")
    zeiger = conn.cursor()

    username = zeiger.execute("SELECT benutzername FROM login WHERE logged=?", ("1")).fetchone()
    conn.close()
    if username == None or "<" in username:
        return "nicht angemeldet"
    else:
        username = username[0]
        return username




set_unlogged()

@app.route("/")

@app.route("/index")
def index():
    return render_template("index.html", title=title, user=get_status())

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST" or request.method == "GET":
        if get_status() != "nicht angemeldet":
            set_unlogged()
            text = "Erfolgreich ausgeloggt!"
            return render_template("indexcreate.html", title=title, text=text, user=get_status()) 
        else:
            text = "Abmeldung nicht möglich!"
            return render_template("indexwrong.html", title=title, text=text, user=get_status())

@app.route("/login", methods=['POST', 'GET'])
def login():

    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    zeiger = conn.cursor()

    benutzername = ""
    passwort = ""

    if request.method == "POST" or request.method == "GET":
        benutzername = request.form["username"]
        passwort = request.form["password"]
    else:
        return "Etwas ist schiefgelaufen!"

    if benutzername == "" or passwort == "":
        text = "Alle Felder müssen ausgefüllt sein!"
        
        return render_template("indexwrong.html", text=text, title=title, user=get_status)

    try:
        password = zeiger.execute("SELECT passwort FROM login WHERE benutzername = ?", (benutzername,)).fetchone()["passwort"]
    except:
        return "Das Konto existiert nicht!"

    if passwort == password:
        text = "Erfolgreich eingeloggt!"
        if get_status() != "nicht angemeldet":
            zeiger.execute("UPDATE login SET logged=? WHERE benutzername=?", ("0", str(get_status())))
                
        zeiger.execute("UPDATE login SET logged=? WHERE benutzername=?", ("1", benutzername))
        conn.commit()
        conn.close()
        return render_template("indexcreate.html", text=text, title=title, user=get_status())
    else:
        text = "Benutzername oder Passwort stimmt nicht!"
        return render_template("indexwrong.html", text=text, title=title, user=get_status())


@app.route("/forget")
def forget():
    return render_template("forget.html", title=title, user=get_status())

@app.route("/register")
def register():
    return render_template("register.html", title=title, user=get_status())

@app.route("/reset", methods=['POST', 'GET'])
def reset():

    newpw = str(random.randint(1,9)) + "" + str(random.randint(1,9)) + "" + str(random.randint(1,9))

    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    zeiger = conn.cursor()

    benutzername = ""
    username = ""

    if request.method == "POST" or request.method == "GET":
        benutzername = request.form["username"]
        print(1)

    try:
        username = zeiger.execute("SELECT benutzername FROM login WHERE benutzername=?", (benutzername,)).fetchone()["benutzername"]
        print(2)
    except:
        text = "Diesen Benutzer gibt es nicht!"
        return render_template("forgetwrong.html", text=text, title=title, user=get_status())
        print(3)

    if benutzername != "":
        zeiger.execute("UPDATE login SET passwort=? WHERE benutzername=?", (newpw, benutzername))
        print(4)
    else:
        text = "Ein Benutzername muss angegeben werden!"
        return render_template("forgetwrong.html", text=text, title=title, user=get_status())
        print(5)

    conn.commit()
    conn.close()
    print(6)

    text = "Passwort wurde erfolgreich zurückgesetzt auf: " + newpw
    return render_template("indexcreate.html", text=text, title=title, user=get_status())

@app.route("/create", methods=['POST', 'GET'])
def create():

    benutzername = ""
    passwort = ""
    passwort2 = ""
    username = ""

    if request.method == "POST" or request.method == "GET":
        benutzername = request.form["username"]
        passwort = request.form["password"]
        passwort2 = request.form["password2"]

        if passwort != passwort2:
            text = "Beide Passwörter müssen identisch sein!"
            return render_template("registerwrong.html", text=text, title=title, user=get_status())
        elif benutzername == "" or passwort == "" or passwort2 == "":
            text = "Alle Felder müssen ausgefüllt sein!"
            return render_template("registerwrong.html", text=text, title=title, user=get_status())


    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    zeiger = conn.cursor()

    exc = """
    CREATE TABLE IF NOT EXISTS login (
        benutzername TEXT,
        passwort TEXT
    );"""

    conn.execute(exc)

    if benutzername != "":
        try:
            username = zeiger.execute("SELECT benutzername FROM login WHERE benutzername = ?", (benutzername,)).fetchone()["benutzername"]
        except:
            zeiger.execute("INSERT INTO login (benutzername, passwort) VALUES (?, ?)", (benutzername, passwort))

            if get_status() != "nicht angemeldet":
                zeiger.execute("UPDATE login SET logged=? WHERE benutzername=?", ("0", str(get_status())))
                
            zeiger.execute("UPDATE login SET logged=? WHERE benutzername=?", ("1", benutzername))

            conn.commit()
            conn.close()  
            text = "Neues Konto wurde erfolgreich erstellt!"
            return render_template("indexcreate.html", title=title, text=text, user=get_status())

    if username == benutzername and username != "":
        text = "Dieser Benutzername ist schon vergebeben!"
        return render_template("registerwrong.html", text=text, title=title, user=get_status())
    


    conn.commit()
    conn.close()    
    

if __name__ == '__main__':  
    app.run(debug=True)