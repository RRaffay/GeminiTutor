from app.firebase_funcs.init import db
from app.gemini_funcs.init import model, model_pro


def get_recommendation(uid, subject_name):
    """
    Generate a string of recommendations for a user.

    Args:
        uid (str): Unique identifier for the user.
        subject_name (str): Name of the subject.

    Returns:
        str: String of recommendation.
    """
    doc_ref = db.collection('users').document(uid)
    user_data = doc_ref.get().to_dict()
    # Get the goal for the subject from user data
    goal = user_data['goals'].get(subject_name, '')
    university = user_data['university']
    course_description = user_data['course_descriptions'].get(
        subject_name, f'Course by {university}')

    # Generate the string with questions, rationales, and answers
    qa_string = "\n".join(
        f"Question: {q['question']}\nRationale: {q['rationale']}\nAnswer: {q.get('answer', '')}\n"
        for q in user_data['current_questions'][subject_name]['questions']
    )

    input_string = f"""Generate recommendations for a user taking {subject_name}. 

    The course description: {course_description}.

    More specifically, the user's goal is: {goal}. Below is a set of questions asked to the user to gauge their understanding about the topic of interest. They are in the format questions, rationale for asking question, answer by users.\n\n{qa_string}"""

    try:
        response = model_pro.generate_content(input_string)
    except Exception as e:
        print(e)
        print("Using the base model")
        response = model.generate_content(input_string)

    return response.text


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


def generate_new_questions(subject_name, goal, old_questions, recommendation):
    input_string_first = f"""You are talking to someone interested in learning about {subject_name}. More specifically, their goal is {goal}. Your job is to help them get to their goal. They were previously asked the following questions: {old_questions}. Based on their answers, you gave them the following recommendation: {recommendation}. Now, come up with a set of 5 new questions that help you understand how much the person has learned from the previous questions and the recommendation you gave them."""

    input_string_last = """Return a JSON object in the following format:
        {"questions": [{"question": "the question", "rationale": "rationale"}, {"question": "the question", "rationale": "rationale"}]]}"""

    input_string = input_string_first + input_string_last

    response = model.generate_content(input_string)

    return response.text
