from .init import db
from app.gemini_funcs.initial_rec import create_recommendations


def create_user_document(uid, first_name, last_name, email, university, classes, goals):
    """
    Creates a new user document in the 'users' collection of the Firestore database.

    Args:
        uid (str): The unique identifier for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        university (str): The university the user is associated with.
        classes (list): A list of classes the user is enrolled in.
        goals (list): A list of goals the user has set.

    Returns:
        None
    """
    # Get a reference to the document
    doc_ref = db.collection('users').document(uid)

    doc_info = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'university': university,
        'classes': classes,
        'first_visit': {course: True for course in classes},
        'goals': goals
    }
    doc_ref.set(doc_info)


def get_user_data(uid):
    """
    Retrieve a user's data from the Firestore database.

    Args:
        uid (str): Unique identifier for the user.

    Returns:
        dict: User's data if exists, None otherwise.
    """
    doc_ref = db.collection('users').document(uid)
    user_data = doc_ref.get()
    if user_data.exists:
        return user_data.to_dict()
    return None


def update_user_data(uid, update_dict, collection='users'):
    """
    Update a user's data in the Firestore database.

    Args:
        uid (str): Unique identifier for the user.
        update_dict (dict): Dictionary of fields to update.
        collection (str): Collection name in the Firestore database.
    """
    doc_ref = db.collection(collection).document(uid)
    doc_ref.update(update_dict)


def add_questions_to_user_data(uid, subject_name, questions):
    """
    Add questions to a user's data in the Firestore database.

    Args:
        uid (str): Unique identifier for the user.
        subject_name (str): Name of the subject.
        questions (list): List of questions.
    """
    doc_ref = db.collection('users').document(uid)
    user_data = doc_ref.get().to_dict()

    user_data['questions'][subject_name] = {
        'questions': questions
    }

    doc_ref.update(user_data)


def add_answers_to_user_data(uid, subject_name, questions, answers):
    """
    Add user's answers to their data in the Firestore database.

    Args:
        uid (str): Unique identifier for the user.
        subject_name (str): Name of the subject.
        questions (dict): Dictionary of questions.
        answers (dict): Dictionary of answers.
    """
    doc_ref = db.collection('users').document(uid)
    user_data = doc_ref.get().to_dict()

    for question_text, answer_text in zip(questions.values(), answers.values()):
        # Find the question reference from user_data['questions'][subject_name]['questions']
        question_ref = next(
            (q for q in user_data['current_questions'][subject_name]
             ['questions'] if q['question'] == question_text),
            None
        )

        if question_ref is not None:
            # Update the question with the answer
            question_ref['answer'] = answer_text
        else:
            print(f"Question not found: {question_text}")

    # Update the user document with the modified data
    doc_ref.update(user_data)


def get_recommendation_string(uid, subject_name):
    """
    Generate a string of recommendations for a user.

    Args:
        uid (str): Unique identifier for the user.
        subject_name (str): Name of the subject.

    Returns:
        str: String of recommendations.
    """
    doc_ref = db.collection('users').document(uid)
    user_data = doc_ref.get().to_dict()
    # Get the goal for the subject from user data
    goal = user_data['goals'].get(subject_name, '')

    # Generate the string with questions, rationales, and answers
    qa_string = "\n".join(
        f"Question: {q['question']}\nRationale: {q['rationale']}\nAnswer: {q.get('answer', '')}\n"
        for q in user_data['current_questions'][subject_name]['questions']
    )

    return f"Generate recommendations for user interested in {subject_name}. More specifically, {goal}. Below is a set of questions asked to the user to gauge their understanding about the topic of interest. They are in the format questions, rationale for asking question, answer by users.\n\n{qa_string}"


def get_input_string_new_questions(uid, subject_name):
    """
    Generate an input string for generating new questions for a user.

    Args:
        uid (str): Unique identifier for the user.
        subject_name (str): Name of the subject.

    Returns:
        str: Input string for generating new questions.
    """
    doc_ref = db.collection('users').document(uid)
    user_data = doc_ref.get().to_dict()

    # Generate the string with old questions and recommendation
    qa_string = "\n".join(
        f"Question: {q['question']}\nRationale: {q['rationale']}\nAnswer: {q.get('answer', '')}\n"
        for q in user_data['old_questions'][subject_name]['questions']
    )

    return qa_string


def update_recommendation(uid, subject_name, recommendation):
    """
    Update a user's recommendation in the Firestore database.

    Args:
        uid (str): Unique identifier for the user.
        subject_name (str): Name of the subject.
        recommendation (str): New recommendation.
    """
    user_data = get_user_data(uid)
    if not user_data.get('recommendations'):
        user_data['recommendations'] = {}
    user_data['recommendations'][subject_name] = recommendation
    update_user_data(uid, user_data)


def move_questions_to_old_questions(uid, subject_name):
    """
    Move the current questions to old questions in the Firestore database.

    Args:
        uid (str): Unique identifier for the user.
        subject_name (str): Name of the subject.
    """
    doc_ref = db.collection('users').document(uid)
    user_data = doc_ref.get().to_dict()

    if 'old_questions' not in user_data:
        user_data['old_questions'] = {}

    user_data['old_questions'][subject_name] = user_data['current_questions'][subject_name]
    user_data['current_questions'][subject_name] = []

    doc_ref.update(user_data)


def update_goal_and_recommendations(uid, subject_name, new_goal):
    """
    Update a user's goal and recommendations in the Firestore database.

    Args:
        uid (str): Unique identifier for the user.
        subject_name (str): Name of the subject.
        new_goal (str): New goal for the subject.
    """
    doc_ref = db.collection('users').document(uid)
    doc_ref.update({f'goals.{subject_name}': new_goal})

    new_recommendations = create_recommendations({subject_name: new_goal})
    doc_ref.update(
        {f'recommendations.{subject_name}': new_recommendations[subject_name]})
