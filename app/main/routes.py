from flask import Blueprint, render_template, session, redirect, url_for, request
from app.firebase_funcs.database import get_user_data, update_goal_and_recommendations, add_class_to_user, delete_class_from_user
from app.utils.markdown_conversion import convert_markdown_to_html
from flask import jsonify
from app.main.controller import handle_initial_questions, process_answers_controller, get_current_questions, get_home_page


main = Blueprint('main', __name__)


@main.route("/")
def home():
    """
    Renders the home page.

    If the 'user_id' is present in the session, it retrieves the user data using the 'user_id' and renders the home.html template with the user data.
    If the user data is not found, it prints a message and returns a 404 error response.
    If the 'user_id' is not present in the session, it redirects to the login page.

    Returns:
        If the user data is found, it returns the rendered home.html template with the user data.
        If the user data is not found, it returns a 404 error response.
        If the 'user_id' is not present in the session, it redirects to the login page.
    """
    if 'user_id' in session:
        home_page_data = get_home_page(session['user_id'])
        if home_page_data:
            return render_template('home.html', data=home_page_data)
        else:
            print("User data not found.")
            return "<p>User data not found.</p>", 404
    return redirect(url_for('auth.login'))


@main.route("/class/<class_name>")
def class_page(class_name):
    """
    Render the class page for a given class name.

    Args:
        subject_name (str): The name of the class.

    Returns:
        flask.Response: The rendered HTML template for the subject page.

    Raises:
        None

    """
    if 'user_id' in session:
        user_data = get_user_data(session['user_id'])
        if user_data:
            goal = user_data['goals'].get(class_name, '')
            first_visit = user_data['first_visit'].get(class_name, False)
            if first_visit:
                parsed_questions = handle_initial_questions(
                    session['user_id'], class_name, goal)
                return render_template('subject_page.html', class_name=class_name, goal=goal, first_visit=first_visit, questions=parsed_questions['questions'])
            else:
                if 'recommendations' not in user_data:
                    user_data['recommendations'] = {}
                recommendation = user_data['recommendations'].get(
                    class_name, '')
                html_recommendation = convert_markdown_to_html(recommendation)
                return render_template('subject_page.html', class_name=class_name, goal=goal, first_visit=first_visit, recommendation=html_recommendation)
    return redirect(url_for('auth.login'))


@main.route("/class/<class_name>/update_goal", methods=['POST'])
def update_goal(class_name):
    """
    Update the goal for a specific class.

    Args:
        class_name (str): The name of the subject for which the goal is being updated.

    Returns:
        tuple: A tuple containing an empty string and the HTTP status code 200.

    Raises:
        None

    """
    if 'user_id' in session:
        uid = session['user_id']
        new_goal = request.json['goal']
        update_goal_and_recommendations(uid, class_name, new_goal)
        return "", 200
    return redirect(url_for('auth.login'))


@main.route("/class/<class_name>/process_answers", methods=['POST'])
def process_answers(class_name):
    """
    Process the answers submitted by the user for a specific subject.

    Args:
        class_name (str): The name of the subject for which the answers are being processed.

    Returns:
        If the user is logged in, it returns a JSON response containing the recommendation for the user.
        If the user is not logged in, it redirects to the login page.
    """
    if 'user_id' in session:
        user_id = session['user_id']
        form_data = request.form.to_dict()
        questions = {k: form_data[k]
                     for k in form_data if k.startswith('question')}
        answers = {k: form_data[k]
                   for k in form_data if k.startswith('answer')}

        recommendation = process_answers_controller(
            user_id, class_name, questions, answers)

        return jsonify({'recommendation': recommendation})
    return redirect(url_for('auth.login'))


@main.route("/class/<class_name>/fetch_questions", methods=['POST'])
def fetch_questions(class_name):
    if 'user_id' in session:
        user_id = session['user_id']
        current_questions = get_current_questions(
            subject_name=class_name, user_id=user_id)
        return jsonify({'questions': current_questions})


@main.route("/add_class", methods=['POST'])
def add_class():
    """
    Add a class to the user's profile.

    Returns:
        tuple: A tuple containing an empty string and the HTTP status code 200.

    Raises:
        None

    """
    if 'user_id' in session:
        uid = session['user_id']
        class_name = request.json['class_name']
        goal = request.json['goal']
        success = add_class_to_user(uid, class_name=class_name, goal=goal)

        if success:
            return jsonify({"success": True, "message": "Class added successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to add class"}), 500
    return jsonify({"success": False, "message": "User not logged in"}), 401


@main.route("/delete_class/<class_name>", methods=['POST'])
def delete_class(class_name):
    """
    Delete a class from the user's profile.
    """
    if 'user_id' in session:
        uid = session['user_id']
        # Call the function to delete the class
        delete_class_from_user(uid, class_name)
        return "", 200  # Return an HTTP 200 OK response
    return redirect(url_for('auth.login'))
