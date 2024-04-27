from app.gemini_funcs.init import model


def generate_recommendation(subject: str, goal: str) -> str:
    response = model.generate_content(
        f"Return a recommendation for someone interested learning more about {subject}. More specifically, their goal is: {goal}. Keep your response under 200 words.")
    return response.text


def generate_initial_questions(subject, goal):

    question_intial = f"""You are talking to someone interested in learning about {subject}. More specifically, their goal is {goal}. Your job is to help them get to their goal. However, first you must generate questions that help you guage their current understanding of the topic and use that to give them recommendations. Come up with a set of 5 questions that help you understand how much the person knows about what they're interested in learning about."""

    question_last = """Return a JSON object in the following format:
        {"questions": [{"question": "the question", "rationale": "rationale"}, {"question": "the question", "rationale": "rationale"}]]}"""

    question_combined = question_intial + question_last

    response = model.generate_content(question_combined)
    return response.text


def perform_analysis(input_string):
    response = model.generate_content(input_string)
    return response.text


def create_recommendations(goals):
    recommendations = {}
    for subject, goal in goals.items():
        recommendations[subject] = generate_recommendation(subject, goal)

    return recommendations


def generate_new_questions(subject_name, goal, old_questions, recommendation):
    input_string_first = f"""You are talking to someone interested in learning about {subject_name}. More specifically, their goal is {goal}. Your job is to help them get to their goal. They were previously asked the following questions: {old_questions}. Based on their answers, you gave them the following recommendation: {recommendation}. Now, come up with a set of 5 new questions that help you understand how much the person has learned from the previous questions and the recommendation you gave them."""

    input_string_last = """Return a JSON object in the following format:
        {"questions": [{"question": "the question", "rationale": "rationale"}, {"question": "the question", "rationale": "rationale"}]]}"""

    input_string = input_string_first + input_string_last

    response = model.generate_content(input_string)

    return response.text


def main():
    response = generate_initial_questions(
        "Python", "Programming in Python for Machine Learning")
    print(response)


if __name__ == "__main__":
    main()
