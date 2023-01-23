import functools
from flask import (
    Flask,
    session,
    render_template,
    request,
    abort,
    flash,
    redirect,
    url_for,
)
from passlib.hash import pbkdf2_sha256

# This code is a Python script that creates a web application using the Flask library.
# The application includes routes for a home page, a protected page, a login page, and a signup page.
# The script uses the Passlib library to securely hash and verify passwords for user accounts.
# When a user attempts to access the protected page, the code checks if the user is logged in
# by looking at a "session" variable that is set when a user logs in.
# If the user is not logged in, they are redirected to the login page.
# The script also has a custom error handler for when a user tries to access the protected page without being logged in.
# Additionally, the script uses a decorator function to make a route only accessible to logged-in users.
# This decorator uses the session variable to check if the user is logged in and the users dictionary to check if
# the email provided is registered or not.

# Create a new Flask application
app = Flask(__name__)

# Secret key generated with secrets.token_urlsafe()
app.secret_key = "lkaQT-kAb6aIvqWETVcCQ28F-j-rP_PSEaCDdTynkXA"

# A dictionary to store registered users and their hashed passwords
users = {}


# A decorator function to make a route only accessible to logged in users

# This is a decorator function that you can use to make a route only accessible to logged in users.
# When a function is decorated with this login_required decorator, it will only be accessible to logged-in users.
# If a user is not logged in, they will be redirected to the login page.
# The decorator function uses the session variable to check if the user is logged in and the users dictionary
# to check if the email provided is registered or not. It also uses functools.wraps(route) utility function to keep
# the original name and docstring of the wrapped function.
def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        # Check if the user is logged in by checking the session variable
        email = session.get("email")
        if email or email not in users:
            # If not logged in, redirect to the login page
            return redirect(url_for("login"))
        # If logged in, call the original route function
        return route(*args, **kwargs)

    return route_wrapper


# A route for the home page
@app.get("/")
def home():
    return render_template("home.html", email=session.get("email"))


# A route for a protected page
@app.get("/protected")
# Apply the login_required decorator to this route
@login_required
def protected():
    return render_template("protected.html")


# A route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    email = ""

    # Check if the request is a POST request (submitting a form)
    if request.method == "POST":
        # Get the email and password from the form
        email = request.form.get("email")
        password = request.form.get("password")

        # Verify the email and password using the hashed password stored in the users dictionary
        if pbkdf2_sha256.verify(password, users.get(email)):
            session["email"] = email
            return redirect(url_for("protected"))
        # If the email or password is incorrect, flash a message
        flash("Incorrect e-mail or password")
    return render_template("login.html", email=email)


# A route for the signup page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Check if the request is a POST request (submitting a form)
    if request.method == "POST":
        # Get the email and password from the form
        email = request.form.get("email")
        password = request.form.get("password")

        # Hash the password and store it in the users dictionary
        users[email] = pbkdf2_sha256.hash(password)
        print(users)
        # session["email"] = email
        # - Setting the session here would be okay if you
        # - want users to be logged in immediately after
        # - signing up.
        flash("Successfully signed up.")
        return redirect(url_for("login"))
    return render_template("signup.html")


# custom error handler for 401 (unauthorized) errors
@app.errorhandler(401)
def auth_error():
    return "Not authorized"
