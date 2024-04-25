from app.gemini_funcs.initial_rec import generate_initial_questions, perform_analysis, generate_new_questions
from app.firebase_funcs.database import get_user_data, update_goal_and_recommendations, update_user_data, add_answers_to_user_data, get_recommendation_string, update_recommendation, move_questions_to_old_questions, get_input_string_new_questions
from app.utils.data_parsing import parse_questions
from flask import session


def handle_initial_questions(uid, subject_name, goal):
    """
    Handles the initial questions for a user.

    Args:
        uid (str): The user ID.
        subject_name (str): The name of the subject.
        goal (str): The user's goal.

    Returns:
        list: The parsed questions.

    Raises:
        Exception: If an error occurs while parsing the questions.
    """
    initial_questions = generate_initial_questions(subject_name, goal)

    try:
        parsed_questions = parse_questions(initial_questions)
    except Exception as e:
        print(e)
        parsed_questions = None

    firebase_questions = parsed_questions

    update_user_data(uid, {
        f'first_visit.{subject_name}': True,
        f'current_questions.{subject_name}': firebase_questions
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
