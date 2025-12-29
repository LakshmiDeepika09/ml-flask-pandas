from flask import Flask, render_template, request, redirect, session
import mysql.connector
import matplotlib.pyplot as plt
from model import train_and_predict
import os

app = Flask(__name__)
app.secret_key = "secret"

UPLOAD_FOLDER = "uploads"
GRAPH_PATH = "static/graph.png"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lakshmigt@09",
    database="ml_appp"
)
cursor = db.cursor(buffered=True)

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (u, p))
        user = cursor.fetchone()

        if user:
            session["user"] = u
            return redirect("/upload")
    return render_template("login.html")

# ---------------- CSV UPLOAD ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        file = request.files["file"]
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        session["csv"] = file.filename
        return redirect("/dashboard")

    return render_template("upload.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    salary = None

    if request.method == "POST":
        exp = float(request.form["experience"])
        csv_path = os.path.join(UPLOAD_FOLDER, session["csv"])

        salary, X, y, model = train_and_predict(csv_path, exp)

        cursor.execute("INSERT INTO predictions (experience, salary) VALUES (%s,%s)", (exp, salary))
        db.commit()

        # Graph
        plt.scatter(X, y)
        plt.plot(X, model.predict(X))
        plt.xlabel("Experience")
        plt.ylabel("Salary")
        plt.savefig(GRAPH_PATH)
        plt.close()

    return render_template("dashboard.html", salary=salary)

app.run(debug=True)