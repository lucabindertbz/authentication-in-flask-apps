# authentication-in-flask-apps

This project is a simple web application written in Python using the Flask web framework. The application allows users to sign up, log in, and access a protected page.

The first line imports the functools module, which is used later to wrap a function.
The next lines import various modules from the Flask library, which is used to handle routing, templates, and form handling for the web application.
The passlib.hash module is used to hash and verify passwords.

An instance of the Flask class is created, and a secret key is set for the application to use with sessions. A dictionary users is also created to store registered user's email and hashed password.

The login_required function is a decorator that checks if a user is logged in before allowing access to a route. If the user is not logged in, they will be redirected to the login page.

The home() function handles the root route '/' and renders the home.html template.

The protected() function handles the '/protected' route and is decorated with the login_required decorator, which means a user has to be logged in to access this route. If a user is not logged in, they will be redirected to the login page.

The login() function handles the '/login' route, it can handle both GET and POST requests. When a user submits a login form, the function checks if the email and password match one of the registered users. If they match, the user's email is saved in the session, and the user is redirected to the protected page.

The signup() function handles the '/signup' route, it can handle both GET and POST requests. When a user submits the signup form, their email and password are hashed and saved in the users dictionary. The user is then redirected to the login page.

The auth_error() function handles the 401 error, which is raised when a user tries to access a protected route without being logged in.
