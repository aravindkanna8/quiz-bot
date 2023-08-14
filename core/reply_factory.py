
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id is None:
        return False, "No current question to answer."

    # Validate and store the answer in the session
    if current_question_id < len(PYTHON_QUESTION_LIST):
        correct_answer = PYTHON_QUESTION_LIST[current_question_id]
        session_answers = session.get("answers", {})
        session_answers[current_question_id] = answer

        # Optionally, you can check if the user's answer is correct
        if answer == correct_answer:
            # Update user's score or perform other actions if needed
            session["score"] = session.get("score", 0) + 1

        session["answers"] = session_answers
        return True, ""
    else:
        return False, "Invalid question ID"

def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_question_id], next_question_id
    else:
        return None, None

def generate_final_response(session):
    total_questions = len(PYTHON_QUESTION_LIST)
    total_correct = session.get("score", 0)  # Retrieve user's total correct answers

    score_percentage = (total_correct / total_questions) * 100
    final_response = f"Your final score is: {score_percentage:.2f}%"

    return final_response
