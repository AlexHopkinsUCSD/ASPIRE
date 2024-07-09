import logging
import json

from app.app.errors.llm_response_error import LLMResponseError
from app.domain.models.question import QuestionCreate, AnswerPreCreate

logger = logging.getLogger(__name__)

async def format_questions(response, validator_status, params):
    try:
        questions = []
        for index, question in enumerate(response['questions']):
            question_obj = QuestionCreate(
                    **question, 
                    position=index+1, 
                    question_type="multiple_choice_question",
                    points_possible=5
                    )
            answer_obj = [AnswerPreCreate(**answer) for answer in question["answers"]]
            questions.append({"question": question_obj, "answers": answer_obj})

        return questions
    
    except Exception as e:
        logger.exception(msg="Failed to parse LLM response")
        raise LLMResponseError(
            message="Failed to parse LLM response.", 
            action="questions",
            status_code=500, 
            failed_validators=[str(validator) for validator in validator_status if validator.status == 'FAIL'], 
            llm_response=response
            )


async def check_answer(response, index, item):
    #TODO: Find a better way to do this, too many loops, too slow, I hate it - (the author of this atrocity)
    answer_list = item.get("answers")
    expected_answers = {"answer_text": str, "answer_weight": int}
    for a_index, answer in enumerate(answer_list):
        if all(expected_answers.get(key) == type(value) for key, value in answer.items()):
            continue
        elif len(answer.keys()) == 2:
            new_answer = {"answer_text" if type(v) == str else "answer_weight": v for v in answer.values()}
            response["questions"][index]["answers"][a_index] = new_answer
        else:
            response["questions"].pop(index)


async def check_contents_question_list(self, response, validator_status, prompt, action, params):
    """
    ---
    Validation Function 
    ---

    Checks each item of a list of objects assigned to the key: 'questions', validates that each item is a dictionary with the correct keys and values.
    
    ---
    Failure Conditions
    ---

    | Cause of Failure | Failure Mode | Outcome |
    | :--------------- | :----------: | :------ |
    | Response is not a dictionary with the key 'questions' | Safe | No Effect |
    | Value at key 'questions' is not a list | Safe | No Effect |
    | List is empty | Deadly | LLMResponseError |
    | List value not a dictionary | Safe | Checks if value is unprocessed JSON, processes if it is, otherwise it is removed |
    | Object is missing a required key | Safe | Adds the key and value either with an alternative value from the object not already assigned to a correct key or with a placeholder |
    """
    
    if not isinstance(response, dict) or 'questions' not in response.keys():
        self.error_response = f"Response not a dict with the key 'questions'. Received: {type(response['questions'])}"
        return "FAIL", response
    
    if not isinstance(response["questions"], list):
        self.error_response = f"Response value at key: 'questions' not a list. Received: {type(response['questions'])}"
        return "FAIL", response
    
    if not response['questions']:
        self.error_response = "Questions list empty"
        raise LLMResponseError(
            message="Response contains no values", 
            action="questions", 
            status_code=500, 
            llm_response=response, 
            failed_validators=[str(validator) for validator in validator_status if validator.status == 'FAIL']
            )
    
    expected_keys = {"question_name": str, "question_text": str, "correct_comments": str, "incorrect_comments": str, "neutral_comments": str, "answers": list}

    for index, item in enumerate(response['questions']):
        if type(item) != dict:
            try:
                item = json.loads(item)
                response[index] = item

            except TypeError:
                response["questions"].remove(item)

        dict_check = {key: expected_keys.get(key) == type(value) for key, value in item.items()}
        # If an item has all the expected keys with the correct value types and there are answers in the list, checks the answers then moves on to next loop
        if all(dict_check.values()):
            await check_answer(response=response, index=index, item=item)
            continue
        #TODO: Come up with a way to try and match values assigned to incorrect keys with the correct keys to fix LLM mistakes
        else:
            response["questions"].remove(item)

    return "PASS", response


async def check_has_key_questions(self, response, validator_status, prompt, action, params):
    """
    ---
    Validation Function 
    ---

    Checks if a llm response is a dictionary with only one key called 'questions'.
    
    ---
    Failure Conditions
    ---

    | Cause of Failure | Failure Mode | Outcome |
    | :--------------- | :----------: | :------ |
    | Response is not a dictionary | Safe | No Effect |
    | Response has no keys | Deadly | LLMResponseError |
    | Response has multiple keys | Safe | New response with all dict values packed in a list and assigned to the key 'questions' |
    | Response has one key != 'questions | Safe | Key reassigned to 'questions', value unchanged |
    """
    # if the response is not a dictionary this function cannot process it
    if not isinstance(response, dict):
        self.error_response = "Response not a dict"
        return "FAIL", response
    
    keys = list(response.keys())
    print(keys)
    key_length = len(keys)

    # If there are no keys the response must be empty and further processing is pointless
    if key_length < 1:
        self.error_response = "Response contains no values"
        raise LLMResponseError(
            message="Response contains no values", 
            action="questions", 
            status_code=500, 
            llm_response=response, 
            failed_validators=[str(validator) for validator in validator_status if validator.status == 'FAIL']
            )

    # multiple key handling
    if 0 < key_length > 1:
        new_response = []
        for val in response.values():
            if type(val) == list:
                new_response.extend(val)
            else:
                new_response.append(val)

        self.error_response = f"Expected LLM response with single key: 'questions'. Received multiple keys: {keys}. Reassigned response values to dict with key 'questions'"
        return "FAIL", {"questions": new_response}
    
    # single key handling
    if "questions" not in keys:
        self.error_response = f"Expected LLM response with single key: 'questions'. Received key: {keys[0]}. Reassigned to dict with key 'questions'"
        return "FAIL", {"questions": response[keys[0]]}
    
    # has the single key 'questions'
    return "PASS", response