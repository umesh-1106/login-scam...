from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"


# ==========================
# Database Connection
# ==========================

def get_db():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# Create Database
# ==========================

def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mobile TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()


init_db()


# ==========================
# Home
# ==========================

@app.route("/")
def home():
    return redirect(url_for("login"))


# ==========================
# Register
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE mobile=? OR email=?",
            (mobile, email)
        ).fetchone()

        if user:
            flash("Mobile number or Email already exists!", "danger")
            conn.close()
            return redirect(url_for("register"))

        hashed = generate_password_hash(password)

        conn.execute(
            """
            INSERT INTO users(name,mobile,email,password)
            VALUES(?,?,?,?)
            """,
            (name, mobile, email, hashed)
        )

        conn.commit()

        user = conn.execute(
            "SELECT * FROM users WHERE mobile=?",
            (mobile,)
        ).fetchone()

        conn.close()

        session["logged_in"] = True
        session["user_id"] = user["id"]
        session["name"] = user["name"]
        session["mobile"] = user["mobile"]
        session["email"] = user["email"]

        flash("Registration Successful!", "success")

        return redirect(url_for("dashboard"))

    return render_template("register.html")


# ==========================
# Login
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        mobile = request.form["mobile"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE mobile=?",
            (mobile,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["logged_in"] = True
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["mobile"] = user["mobile"]
            session["email"] = user["email"]

            return redirect(url_for("dashboard"))

        flash("Invalid Mobile Number or Password", "danger")

    return render_template("login.html")


# ==========================
# Dashboard
# ==========================

@app.route("/dashboard")
def dashboard():

    if "logged_in" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# ==========================
# Logout
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully", "success")

    return redirect(url_for("login"))


# ==========================
# Admin Login
# ==========================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["admin"] = True

            return redirect(url_for("admin_dashboard"))

        flash("Invalid Admin Credentials", "danger")

    return render_template("admin_login.html")


# ==========================
# Admin Dashboard
# ==========================

@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_db()

    users = conn.execute(
        "SELECT * FROM users ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        users=users
    )


# ==========================
# Admin Logout
# ==========================

@app.route("/admin_logout")
def admin_logout():

    session.pop("admin", None)

    return redirect(url_for("admin"))


# ==========================
# Run
# ==========================

if __name__ == "__main__":
    app.run(debug=True)
