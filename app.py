from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, create_tables

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Create database
create_tables()


# ===========================
# Home
# ===========================
@app.route("/")
def home():
    return redirect(url_for("login"))


# ===========================
# User Registration
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
            flash("User already exists.", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn.execute(
            """
            INSERT INTO users(name,mobile,email,password)
            VALUES(?,?,?,?)
            """,
            (name, mobile, email, hashed_password)
        )

        conn.commit()
        conn.close()

        flash("Registration Successful. Please Login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ===========================
# User Login
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

            session["user"] = True
            session["id"] = user["id"]
            session["name"] = user["name"]
            session["mobile"] = user["mobile"]
            session["email"] = user["email"]

            return redirect(url_for("dashboard"))

        flash("Invalid Mobile Number or Password", "danger")

    return render_template("login.html")


# ===========================
# User Dashboard
# ===========================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# ===========================
# User Logout
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

        if username == "UMESH1106" and password == "8919":

            session["admin"] = True

            return redirect(url_for("admin_dashboard"))

        flash("Invalid Username or Password", "danger")

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
        SELECT
            id,
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

    flash("Admin Logged Out", "success")

    return redirect(url_for("admin"))


# ===========================
# Run
# ===========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
