from flask import Blueprint, request, render_template, redirect, url_for, session
from app.firebase_funcs.auth import create_user, verify_user

auth = Blueprint('auth', __name__)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register a new user.

    If the request method is POST, the function retrieves the user's information from the request form,
    creates a new user using the provided information, and redirects the user to the home page.
    If the request method is GET, the function renders the registration form.

    Returns:
        If the request method is POST, it redirects the user to the home page.
        If the request method is GET, it renders the registration form.
    """
    if request.method == 'POST':
        # Retrieving all form fields
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        university = request.form['university']
        # New way to retrieve class names as they are now sent as a list of inputs
        # Adjusted to handle multiple inputs
        classes = request.form.getlist('class_names[]')
        # Clean up and filter out empty entries
        classes = [cls.replace(" ", "") for cls in classes if cls.strip()]

        # Construct goals dictionary based on the classes
        goals = {cls: request.form.get(
            f'goal_{cls}', '').strip() for cls in classes}

        # Assuming create_user handles the logic of storing classes and goals
        user = create_user(email, password, first_name,
                           last_name, university, classes, goals)
        session['user_id'] = user.uid
        return redirect(url_for('main.home'))

    return render_template('register.html')


@auth.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handle the login functionality.

    This function handles the login process when the user submits the login form.
    It retrieves the email and password from the form, verifies the user's credentials,
    and sets the user's ID in the session if the credentials are valid.

    Returns:
        If the login is successful, it redirects the user to the home page.
        If the login fails, it returns an error message with a status code of 403.

    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = verify_user(email, password)
            session['user_id'] = user.uid
            return redirect(url_for('main.home'))
        except Exception as e:
            return str(e), 403
    return render_template('login.html')


@auth.route("/logout")
def logout():
    """
    Log out the current user by removing the 'user_id' from the session.

    Returns:
        A redirect response to the login page.
    """
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))
