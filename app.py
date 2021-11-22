from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")

@app.route("/index") 
def index(): 
    title = "Testseite"
    return render_template("index.html", title=title)

@app.route("/login")
def login():
    print("Du wurdest erfolgreich eingeloggt!")
    return "Deine Logindaten wurden erfolgreich gespeichert!"

if __name__ == "__main__":
    app.run(debug=True)