from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, create_tables

app = Flask(__name__)
app.secret_key = "your_secret_key_123"

# Create database tables
create_tables()


# ===========================
# Home
# ===========================
@app.route("/")
def home():
    return redirect(url_for("login"))


# ===========================
# Register
# ===========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        conn = get_db()

        existing = conn.execute(
            "SELECT * FROM users WHERE mobile=? OR email=?",
            (mobile, email)
        ).fetchone()

        if existing:
            conn.close()
            flash("Mobile number or Email already registered.", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn.execute(
            """
            INSERT INTO users(name, mobile, email, password)
            VALUES (?, ?, ?, ?)
            """,
            (name, mobile, email, hashed_password)
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


# ===========================
# Login
# ===========================
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

        flash("Invalid Mobile Number or Password!", "danger")

    return render_template("login.html")


# ===========================
# Dashboard
# ===========================
@app.route("/dashboard")
def dashboard():

    if "logged_in" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# ===========================
# Logout
# ===========================
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect(url_for("login"))


# ===========================
# Admin Login
# ===========================
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Change these credentials if needed
        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))

        flash("Invalid Admin Username or Password.", "danger")

    return render_template("admin_login.html")


# ===========================
# Admin Dashboard
# ===========================
@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_db()

    users = conn.execute(
        """
        SELECT id,
               name,
               mobile,
               email,
               created_at
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        users=users
    )


# ===========================
# Admin Logout
# ===========================
@app.route("/admin_logout")
def admin_logout():

    session.pop("admin", None)

    flash("Admin logged out successfully.", "success")

    return redirect(url_for("admin"))


# ===========================
# Run Application
# ===========================
if __name__ == "__main__":
    app.run(debug=True)
