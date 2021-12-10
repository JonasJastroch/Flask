from flask import Flask, render_template, request
import sqlite3
import random
import datetime

app = Flask(__name__)

title = "PUPLYC"
text = ""
user = ""
visibility = "opacity-0"
alert = ""

conn = sqlite3.connect("data.db")
conn.row_factory = sqlite3.Row
zeiger = conn.cursor()

exc = """
CREATE TABLE IF NOT EXISTS login (
    benutzername TEXT,
    passwort TEXT,
    chats TEXT
);"""

zeiger.execute(exc)

conn.commit()
conn.close()

def get_messages(user1, user2):
    conn = sqlite3.connect("data.db")
    zeiger = conn.cursor()

    try:
        name = str(f"{user1}chat{user2}")
        m = []

        ids = zeiger.execute(f"SELECT COUNT(id) FROM {name}").fetchone()
        ids = ids[0]

        for e in range(ids):
            ms = zeiger.execute(f"SELECT * FROM {name} WHERE id=?", (e+1,)).fetchone()
            m.append(ms)

        conn.close()

    except:
        name = str(f"{user2}chat{user1}")
        m = []

        ids = zeiger.execute(f"SELECT COUNT(id) FROM {name}").fetchone()
        ids = ids[0]

        for e in range(ids):
            ms = zeiger.execute(f"SELECT * FROM {name} WHERE id=?", (e+1,)).fetchone()
            m.append(ms)

        conn.close()

    return m

def new_message(user1, user2, message):
    conn = sqlite3.connect("data.db")
    zeiger = conn.cursor()

    try:
        name = str(f"{user1}chat{user2}")

        date = datetime.date.today()
        date = str(date).split("-")
        date = f"{date[2]}.{date[1]}.{date[0]}"

        time = datetime.datetime.now().strftime('%H:%M')
        time = time + " Uhr"

        zeiger.execute(f"INSERT INTO {name} (user1, user2, message, time, date) VALUES (?,?,?,?,?)", (user1, user2, message, date, time))

        conn.commit()
        conn.close()
    except:
        name = str(f"{user2}chat{user1}")

        date = datetime.date.today()
        date = str(date).split("-")
        date = f"{date[2]}.{date[1]}.{date[0]}"

        time = datetime.datetime.now().strftime('%H:%M')
        time = time + " Uhr"

        zeiger.execute(f"INSERT INTO {name} (user1, user2, message, time, date) VALUES (?,?,?,?,?)", (user1, user2, message, date, time))

        conn.commit()
        conn.close()


def get_chats(user1):
    conn = sqlite3.connect("data.db")
    zeiger = conn.cursor()

    chats = zeiger.execute(f"SELECT chats FROM login WHERE benutzername=?", (user1,)).fetchall()
    chats = chats[0][0]

    if chats != None:
        print("a")
        users = str(chats).replace("chat", "")
        users = users.replace(user1, "")
        if "and" in users:
            users = users.split("and")
        else:
            usrs = []
            usrs.append(users)
            return usrs
    else:
        users = ""

    print(users)

    conn.close()

    return users

def add_chat(user1, user2):
    conn = sqlite3.connect("data.db")
    zeiger = conn.cursor()

    name = str(f"{user1}chat{user2}")

    c = zeiger.execute(f"SELECT chats FROM login WHERE benutzername=?", (user1,)).fetchall()
    c = c[0][0]

    print(c)

    if c != None:
        print("b")
        chats = c + "and" + name
    else:
        print("c")
        chats = name
    zeiger.execute(f"UPDATE login SET chats=? WHERE benutzername=?", (chats, user1))


    c = zeiger.execute(f"SELECT chats FROM login WHERE benutzername=?", (user2,)).fetchall()
    c = c[0][0]

    print(c)

    if c != None:
        print("b")
        chats = c + "and" + name
    else:
        print("c")
        chats = name
    zeiger.execute(f"UPDATE login SET chats=? WHERE benutzername=?", (chats, user2))
    

    conn.commit()
    conn.close()

def set_alert(alert):
    a = alert
    return a


@app.route("/")

@app.route("/index")
def load():
    return render_template("load.html", user="nicht angemeldet")

@app.route("/<usr>/index")
def index(usr):
    user1 = str(usr).replace("usr=", "")
    return render_template("index.html", title=title, user=user1, visibility="opacity-0")

@app.route("/<usr>/chatadd", methods=["POST", "GET"])
def add(usr):

    benutzername = ""

    if request.method == "POST" or request.method == "GET":
        benutzername = request.form["username"]
    else:
        return "Etwas ist schiefgelaufen!"

    conn = sqlite3.connect("data.db")
    zeiger = conn.cursor()

    user1 = str(usr).replace("usr=", "")
    user2 = benutzername

    name = str(f"{user1}chat{benutzername}")

    add_chat(user1, user2)

    zeiger.execute(f"CREATE TABLE IF NOT EXISTS {name} (id INTEGER PRIMARY KEY AUTOINCREMENT, user1 TEXT, user2 TEXT, message TEXT, time TEXT, date TEXT);")

    conn.commit()
    conn.close()

    return render_template("chat.html", title=title, user=user1, users=get_chats(user1), visibility=visibility)

@app.route("/<usr>/clicked/<chat>", methods=["POST", "GET"])
def clicked(usr, chat):

    user1 = str(usr).replace("usr=", "")

    if request.method == "POST" or request.method == "GET":
        try:
            user2 = request.form["user"]
        except:
            user2 = str(chat).replace("chat=", "")
    else:
        return "Etwas ist schiefgelaufen!"

    return render_template("chat.html", title=title, user=user1, chat=user2, users=get_chats(user1), visibility="opacity-100", message=get_messages(user1, user2))

@app.route('/<usr>/send/<chat>', methods=('GET', 'POST'))
def send(usr, chat):

    if request.method == "POST" or request.method == "GET":
        message = request.form["message"]
    else:
        return "Etwas ist schiefgelaufen!"

    user1 = str(usr).replace("usr=", "")
    user2 = str(chat).replace("chat=", "")

    new_message(user1, user2, message)

    #return render_template("chat.html", title=title, user=user1, chat=user2, users=get_chats(user1), visibility="opacity-100", message=get_messages(user1, user2))
    return render_template("clickedrefresh.html", user=user1, chat=user2)

@app.route("/<usr>/logout", methods=["GET", "POST"])
def logout(usr):
    user1 = str(usr).replace("usr=", "")
    if request.method == "POST" or request.method == "GET":
        if user1 != "nicht angemeldet":
            text = "Erfolgreich ausgeloggt!"
            return render_template("load.html", user="nicht angemeldet") 
        else:
            text = "Abmeldung nicht möglich!"
            return render_template("index.html", title=title, text=text, user=user1, alert=set_alert("danger"), visibility="opacity-100")

@app.route("/<usr>/chat")
def chat(usr):
    user1 = str(usr).replace("usr=", "")
    return render_template("chat.html", title=title, user=user1, users=get_chats(user1), visibility=visibility, chat="")

@app.route("/<usr>/login", methods=['POST', 'GET'])
def login(usr):

    user1 = str(usr).replace("usr=", "")

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
        
        return render_template("index.html", text=text, title=title, user=user1, alert=set_alert("danger"), visibility="opacity-100")

    try:
        password = zeiger.execute("SELECT passwort FROM login WHERE benutzername=?", (benutzername,)).fetchone()["passwort"]
    except:
        return "Das Konto existiert nicht!"

    if passwort == password:
        text = "Erfolgreich eingeloggt!"
        # if user1 != "nicht angemeldet":
        #     zeiger.execute("UPDATE login SET logged=? WHERE benutzername=?", ("0", user1))
                
        # zeiger.execute("UPDATE login SET logged=? WHERE benutzername=?", ("1", benutzername))
        conn.commit()
        conn.close()

        return render_template("refresh.html", user=benutzername)
    else:
        text = "Benutzername oder Passwort stimmt nicht!"
        return render_template("index.html", text=text, title=title, user=user1, alert=set_alert("danger"), visibility="opacity-100")


@app.route("/<usr>/forget")
def forget(usr):
    user1 = str(usr).replace("usr=", "")
    return render_template("forget.html", title=title, user=user1, visibility="opacity-0")

@app.route("/<usr>/register")
def register(usr):
    user1 = str(usr).replace("usr=", "")
    return render_template("register.html", title=title, user=user1, visibility="opacity-0")

@app.route("/<usr>/reset", methods=['POST', 'GET'])
def reset(usr):

    user1 = str(usr).replace("usr=", "")

    newpw = str(random.randint(1,9)) + "" + str(random.randint(1,9)) + "" + str(random.randint(1,9))

    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    zeiger = conn.cursor()

    benutzername = ""

    if request.method == "POST" or request.method == "GET":
        benutzername = request.form["username"]

    try:
        username = zeiger.execute("SELECT benutzername FROM login WHERE benutzername=?", (benutzername,)).fetchone()["benutzername"]
    except:
        text = "Diesen Benutzer gibt es nicht!"
        return render_template("forget.html", text=text, title=title, user=user1, alert=set_alert("danger"), visibility="opacity-100")

    if benutzername != "":
        zeiger.execute("UPDATE login SET passwort=? WHERE benutzername=?", (newpw, benutzername))
    else:
        text = "Ein Benutzername muss angegeben werden!"
        return render_template("forget.html", text=text, title=title, user=user1, alert=set_alert("danger"), visibility="opacity-100")

    conn.commit()
    conn.close()

    text = "Passwort wurde erfolgreich zurückgesetzt auf: " + newpw
    return render_template("index.html", text=text, title=title, user=user1, alert=set_alert("success"), visibility="opacity-100")

@app.route("/<usr>/create", methods=['POST', 'GET'])
def create(usr):

    user1 = str(usr).replace("usr=", "")

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
            return render_template("register.html", text=text, title=title, user=user1, alert=set_alert("danger"), visibility="opacity-100")
        elif benutzername == "" or passwort == "" or passwort2 == "":
            text = "Alle Felder müssen ausgefüllt sein!"
            return render_template("register.html", text=text, title=title, user=user1, alert=set_alert("danger"), visibility="opacity-100")


    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    zeiger = conn.cursor()

    exc = """
    CREATE TABLE IF NOT EXISTS login (
        benutzername TEXT,
        passwort TEXT,
        chats TEXT
    );"""

    conn.execute(exc)

    if benutzername != "":
        try:
            username = zeiger.execute("SELECT benutzername FROM login WHERE benutzername = ?", (benutzername,)).fetchone()["benutzername"]
        except:
            zeiger.execute("INSERT INTO login (benutzername, passwort) VALUES (?, ?)", (benutzername, passwort))

            # if user1 != "nicht angemeldet":
            #     zeiger.execute("UPDATE login SET logged=? WHERE benutzername=?", ("0", user1))
                
            # zeiger.execute("UPDATE login SET logged=? WHERE benutzername=?", ("1", benutzername))

            conn.commit()
            conn.close()  
            text = "Neues Konto wurde erfolgreich erstellt!"
            return render_template("load.html", user=benutzername)

    if username == benutzername and username != "":
        text = "Dieser Benutzername ist schon vergebeben!"
        return render_template("register.html", text=text, title=title, user=user1, alert=set_alert("danger"), visibility="opacity-100")
    


    conn.commit()
    conn.close()    
    

if __name__ == '__main__':  
    app.run(debug=True)