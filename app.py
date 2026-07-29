from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret Key
app.secret_key = "your_secret_key"

# ===============================
# MySQL Configuration
# ===============================
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "attendance_system"

mysql = MySQL(app)

# ===============================
# Home
# ===============================
@app.route("/")
def home():
    return redirect(url_for("login"))

# ===============================
# Register
# ===============================
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

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE mobile=%s OR email=%s",
            (mobile, email)
        )

        account = cursor.fetchone()

        if account:
            flash("Mobile Number or Email already exists!", "danger")
            cursor.close()
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users(name,mobile,email,password)
            VALUES(%s,%s,%s,%s)
            """,
            (name, mobile, email, hashed_password)
        )

        mysql.connection.commit()
        cursor.close()

        flash("Registration Successful. Please Login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# ===============================
# Login
# ===============================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        mobile = request.form["mobile"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE mobile=%s",
            (mobile,)
        )

        user = cursor.fetchone()
        cursor.close()

        if user:

            # Table Order
            # 0=id
            # 1=name
            # 2=mobile
            # 3=email
            # 4=password

            if check_password_hash(user[4], password):

                session["logged_in"] = True
                session["user_id"] = user[0]
                session["name"] = user[1]
                session["mobile"] = user[2]
                session["email"] = user[3]

                return redirect(url_for("dashboard"))

        flash("Invalid Mobile Number or Password", "danger")

    return render_template("login.html")

# ===============================
# User Dashboard
# ===============================
@app.route("/dashboard")
def dashboard():

    if "logged_in" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")

# ===============================
# Logout
# ===============================
@app.route("/logout")
def logout():

    session.clear()
    flash("Logged Out Successfully.", "success")

    return redirect(url_for("login"))

# ===============================
# Admin Login
# ===============================
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

# ===============================
# Admin Dashboard
# ===============================
@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin"))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
        id,
        name,
        mobile,
        email,
        created_at
        FROM users
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    cursor.close()

    return render_template(
        "admin_dashboard.html",
        users=users
    )

# ===============================
# Admin Logout
# ===============================
@app.route("/admin_logout")
def admin_logout():

    session.pop("admin", None)

    return redirect(url_for("admin"))

# ===============================
# Run
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
