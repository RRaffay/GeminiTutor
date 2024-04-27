from app.gemini_funcs.initial_rec import generate_initial_questions
from app.gemini_funcs.drivers import class_details
from app.firebase_funcs.database import get_user_data, update_goal_and_recommendations, update_user_data, add_answers_to_user_data, update_recommendation, move_questions_to_old_questions
from app.utils.data_parsing import parse_questions
from flask import session
from app.gemini_funcs.rec_logic import get_recommendation_string, perform_analysis, get_input_string_new_questions, generate_new_questions


def handle_initial_questions(uid, course_name, goal):
    """
    Handles the initial questions for a user.

    Args:
        uid (str): The user ID.
        course_name (str): The name of the subject.
        goal (str): The user's goal.

    Returns:
        list: The parsed questions.

    Raises:
        Exception: If an error occurs while parsing the questions.
    """
    user_data = get_user_data(uid)
    university_name = user_data['university']

    course_description = class_details(course_name, university_name)

    if 'course_descriptions' not in user_data:
        user_data['course_descriptions'] = {}
    user_data['course_descriptions'][course_name] = course_description
    update_user_data(uid, user_data)

    initial_questions = generate_initial_questions(course_description, goal)

    try:
        parsed_questions = parse_questions(initial_questions)
    except Exception as e:
        print(e)
        parsed_questions = None

    firebase_questions = parsed_questions

    update_user_data(uid, {
        f'first_visit.{course_name}': False,
        f'current_questions.{course_name}': firebase_questions
    })

    return parsed_questions


def process_answers_controller(user_id, subject_name, questions, answers):
    """
    Process the answers provided by a user for a specific subject.

    Args:
        user_id (int): The ID of the user.
        subject_name (str): The name of the subject.
        questions (list): A list of questions related to the subject.
        answers (list): A list of answers corresponding to the questions.

    Returns:
        str: The recommendation generated based on the user's answers.
    """
    add_answers_to_user_data(user_id, subject_name, questions, answers)

    rec_input_string = get_recommendation_string(user_id, subject_name)

    recommendation = perform_analysis(rec_input_string)

    move_questions_to_old_questions(user_id, subject_name)

    user_data = get_user_data(user_id)
    user_goal = user_data['goals'][subject_name]

    old_question_string = get_input_string_new_questions(user_id, subject_name)

    new_questions = generate_new_questions(
        subject_name, user_goal, old_question_string, recommendation)

    try:
        parsed_questions = parse_questions(new_questions)
    except Exception as e:
        print(e)
        parsed_questions = None

    update_user_data(user_id, {
        f'current_questions.{subject_name}': parsed_questions
    })

    update_recommendation(user_id, subject_name, recommendation)
    return recommendation


def get_current_questions(subject_name, user_id):
    """
    Get the current questions for a specific subject.
    Args:
        subject_name (str): The name of the subject.
        user_id (str): The user ID.
    Returns:
        list: The current questions for the subject.
    Raises:
        Exception: If an error occurs while retrieving the questions.
    """
    user_data = get_user_data(user_id)
    current_questions = user_data['current_questions'].get(subject_name, None)

    if current_questions is None:
        return None

    print(current_questions)
    return current_questions


def get_home_page(user_id):
    """
    Get the home page for a user.

    Args:
        user_id (str): The user ID.

    Returns:
        dict: The user data.

    Raises:
        Exception: If an error occurs while retrieving the user data.
    """
    user_data = get_user_data(user_id)

    if user_data is None:
        return None

    home_page = {
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'classes': user_data['classes'],
    }

    return home_page
