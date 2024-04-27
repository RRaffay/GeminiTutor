from app.gemini_funcs.init import model, model_pro


def generate_recommendation(subject: str, goal: str) -> str:
    response = model.generate_content(
        f"Return a recommendation for someone interested learning more about {subject}. More specifically, their goal is: {goal}. Keep your response under 200 words.")
    return response.text


def generate_initial_questions(course_description, goal):

    question_intial = f"""You are talking to someone taking a course. More specifically, their class is {course_description}.
    
    Their goal is {goal}. 
    
    Your job is to help them get to their goal. However, first you must generate questions that help you guage their current understanding of the topic and use that to give them recommendations. Come up with a set of 5 questions that help you understand how much the person knows about what they're interested in learning about."""

    question_last = """Return a JSON object in the following format:
        {"questions": [{"question": "the question", "rationale": "rationale"}, {"question": "the question", "rationale": "rationale"}]]}"""

    question_combined = question_intial + question_last

    try:
        response = model_pro.generate_content(question_combined)
    except Exception as e:
        print(e)
        print("Using the base model")
        response = model.generate_content(question_combined)
    return response.text


def create_recommendations(goals):
    recommendations = {}
    for subject, goal in goals.items():
        recommendations[subject] = generate_recommendation(subject, goal)

    return recommendations


def main():
    response = generate_initial_questions(
        "Python", "Programming in Python for Machine Learning")
    print(response)


if __name__ == "__main__":
    main()
