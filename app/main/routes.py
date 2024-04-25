from flask import Blueprint, render_template, session, redirect, url_for, request
from app.firebase_funcs.database import get_user_data, update_goal_and_recommendations, update_user_data, add_answers_to_user_data, get_recommendation_string, update_recommendation
from app.utils.markdown_conversion import convert_markdown_to_html
from flask import jsonify
from app.main.controller import handle_initial_questions, process_answers_controller
from app.main.controller import handle_initial_questions, process_answers_controller, get_current_questions

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
        user_data = get_user_data(session['user_id'])
        if user_data:
            return render_template('home.html', user=user_data)
        else:
            print("User data not found.")
            return "<p>User data not found.</p>", 404
    return redirect(url_for('auth.login'))


@main.route("/subject/<subject_name>")
def subject_page(subject_name):
    """
    Render the subject page for a given subject name.

    Args:
        subject_name (str): The name of the subject.

    Returns:
        flask.Response: The rendered HTML template for the subject page.

    Raises:
        None

    """
    if 'user_id' in session:
        user_data = get_user_data(session['user_id'])
        if user_data:
            goal = user_data['goals'].get(subject_name, '')
            first_visit = user_data['first_visit'].get(subject_name, False)
            if first_visit:
                parsed_questions = handle_initial_questions(
                    session['user_id'], subject_name, goal)
                return render_template('subject_page.html', subject_name=subject_name, goal=goal, first_visit=first_visit, questions=parsed_questions['questions'])
            else:
                recommendation = user_data['recommendations'].get(
                    subject_name, '')
                html_recommendation = convert_markdown_to_html(recommendation)
                return render_template('subject_page.html', subject_name=subject_name, goal=goal, first_visit=first_visit, recommendation=html_recommendation)
    return redirect(url_for('auth.login'))


@main.route("/subject/<subject_name>/update_goal", methods=['POST'])
def update_goal(subject_name):
    """
    Update the goal for a specific subject.

    Args:
        subject_name (str): The name of the subject for which the goal is being updated.

    Returns:
        tuple: A tuple containing an empty string and the HTTP status code 200.

    Raises:
        None

    """
    if 'user_id' in session:
        uid = session['user_id']
        new_goal = request.json['goal']
        update_goal_and_recommendations(uid, subject_name, new_goal)
        return "", 200
    return redirect(url_for('auth.login'))


@main.route("/subject/<subject_name>/process_answers", methods=['POST'])
def process_answers(subject_name):
    """
    Process the answers submitted by the user for a specific subject.

    Args:
        subject_name (str): The name of the subject for which the answers are being processed.

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
            user_id, subject_name, questions, answers)

        return jsonify({'recommendation': recommendation})
    return redirect(url_for('auth.login'))


@main.route("/subject/<subject_name>/fetch_questions", methods=['POST'])
def fetch_questions(subject_name):
    if 'user_id' in session:
        user_id = session['user_id']
        current_questions = get_current_questions(
            subject_name=subject_name, user_id=user_id)
        return jsonify({'questions': current_questions})
