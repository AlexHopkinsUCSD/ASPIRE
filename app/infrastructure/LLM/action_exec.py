import os
import fitz
import shutil 
from openai import OpenAI

from typing import Optional, List, Union, Dict
from fastapi import UploadFile, Depends

from app.infrastructure.decorators.register import Register
from app.domain.models.llm_agent import ContextCollection
from app.domain.models.errors import ErrorResponse
from app.domain.protocols.services.concept import ConceptService as ConceptServiceProtocol
from app.domain.services.concept import ConceptService
import json

from langchain_community.chat_models.openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

register = Register()

class ActionExecutor:

    async def executePrompt(self, base_prompt, context_prompt, action_prompt, model_name):
        # model_name = "gemini-1.5-pro-latest"
        model_name = model_name
        if 'gpt' in model_name:
            chain_gpt = ChatOpenAI(model=model_name, openai_api_key=os.getenv("OPENAI_API_KEY"), model_kwargs={"response_format": {"type": "json_object"}})
            chain = chain_gpt
            messages=[
                {"role": "system", "content": base_prompt},
                {"role": "assistant", "content": context_prompt},
                {"role": "user", "content": action_prompt}
            ]
            result = await chain.ainvoke(messages)
            return result.content

        elif 'gemini' in model_name:    
            chain_gemini = ChatGoogleGenerativeAI(model=model_name, google_api_key=os.getenv("GOOGLE_API_KEY"))
            chain = chain_gemini
            messages=[
                # SystemMessage(content= f"{base_prompt}+{context_prompt}"),
                HumanMessage(content= f"{action_prompt}+ Please perform the action based on the base prompt: {base_prompt}+ context_prompt{context_prompt}")
            ]
            result=await chain.ainvoke(messages)
            res = result.content
            start_index = res.find('{')
            end_index = res.rfind('}')
            res = res[start_index:end_index+1]
            res = res.strip()
            return res
        else:
            raise ValueError("Unsupported AI provider")

    @register.add(action="summarize")
    async def summarize_contents(self, context:Union[ContextCollection, ErrorResponse], params = Dict):
        """
        Generates a summary of the teaching materials provided in the context.
        Inputs:
            context (ContextCollection): Contains the base prompt and file contents.
            params (dict, optional): Additional parameters (not currently used).
        Output:
            str: JSON-formatted summary of the teaching materials.
        """
        if isinstance(context, ErrorResponse):
            print(f"Error: {context}")
            return
        model_name = params.get('model_name')
        base_prompt = context.base_prompt
        context_prompt = f"The following is context related to the course being taught. These are the materials being taught: {context.file_contents}"      
        # TODO: Give a template to follow for the action prompt
        action_prompt = "Analyze and summarize the provided course materials. Extract key concepts, major topics, and any essential details that contribute to understanding the course's scope. Return the summary as a JSON string formatted as a single paragraph under the 'summary' key."
        result = await self.executePrompt(base_prompt, context_prompt, action_prompt, model_name)
        built_prompt = f"{base_prompt}\n{context_prompt}\n{action_prompt}"
        # print(built_prompt)
        return built_prompt, result

    @register.add(action="domain-concepts")
    async def domain_concepts(self, context:Union[ContextCollection, ErrorResponse], params = Dict):
        """
        Identifies and lists domain concepts from the provided teaching materials and existing database concepts.
        Inputs:
            context (ContextCollection): Includes the base prompt, file contents, and context concepts.
            params (dict, optional): Additional parameters (not currently used).
        Output:
            str: JSON-formatted list of identified domain concepts from the teaching materials.
        """
        if isinstance(context, ErrorResponse):
        # Handle the error here. You might want to log the error and return.
            print(f"Error: {context}")
            return
        model_name = params.get('model_name')
        base_prompt = context.base_prompt
        context_prompt = f"The following is context related to the course being taught. These are the materials being taught: {context.file_contents}, These are the concepts in the database already: {context.context_concepts}" 
        # TODO: Give a template to follow for the action prompt and improve the prompt
        action_prompt = "Based on the given context, Create a JSON structure representing a list of concepts. Please use 'concepts' as a key. Then, declare an array under this key to hold the list of concepts. Populate the array with individual concepts as strings. Ensure that the structure maintains hierarchy, with the key as the parent and the array as its child. Consider including terms relevant to the topic or subject matter and make sure there are no duplicates."
        result = await self.executePrompt(base_prompt, context_prompt, action_prompt, model_name)
        # print(result)
        built_prompt = f"{base_prompt}\n{context_prompt}\n{action_prompt}"
        return built_prompt, result

    @register.add(action="module-concepts")
    async def module_concepts(self, context:Union[ContextCollection, ErrorResponse], params = Dict):
        """
        Extracts module concepts from the teaching materials, compares them with existing database concepts, and handles potential format errors.
        Inputs:
            context (ContextCollection): Includes the base prompt, file contents, and context concepts.
            params (dict, optional): Additional parameters (not currently used).
        Output:
            tuple: Contains prerequisites for the identified module concepts and the module concepts themselves, both typically in JSON format. Also handles and returns errors if the concepts are not in the proper format.
        """
        if isinstance(context, ErrorResponse):
        # Handle the error here. You might want to log the error and return.
            print(f"Error: {context}")
            return
        model_name = params.get('model_name')
        base_prompt = context.base_prompt
        context_prompt = f"The following is context related to the course being taught. These are the materials being taught: {context.file_contents}, These are the concepts in the database already: {context.context_concepts}" 
        # TODO: Give a template to follow for the action prompt and improve the prompt
        action_prompt = "Based on the given context, Create a JSON structure representing a list of concepts. Please use 'concepts' as a key. Then, declare an array under this key to hold the list of concepts. Populate the array with individual concepts as strings. Ensure that the structure maintains hierarchy, with the key as the parent and the array as its child. Consider including terms relevant to the topic or subject matter and make sure there are no duplicates."   
        module_concepts = await self.executePrompt(base_prompt, context_prompt, action_prompt, model_name)
        # print("The module concepts are", module_concepts)
        try:
            module_concepts_dict = json.loads(module_concepts)
        except Exception as e:
            print(e)
            return ErrorResponse(code=404, type="ValidationError", message="The module concepts were not returned in the proper format.")
        # TODO: Add module concepts to context_concepts and focus_concepts and make sure duplicates are not added
        if context.context_concepts is None:
            context.context_concepts = []
        context.context_concepts.append(module_concepts_dict)
        if context.focus_concepts is None:
            context.focus_concepts = []
        context.focus_concepts.append(module_concepts_dict) 
        # print("The focus concepts are", context.focus_concepts)
        context_prompt = context_prompt + f"The following are the concepts that we are focusing on: {context.focus_concepts}"
        # TODO: Improve the prompt by specifying the role of each peice of context in relation to the aciton
        action_prompt = """ Generate a JSON structure representing the prerequisites for each concept covered in a lecture on control flow and loops in programming. The lecture is aimed at students with weak computer science backgrounds. 
        The lecture covers various topics, each with subtopics. Provide the following structure:
        1. Start by creating a top-level object with curly braces {}.
        2. Inside the top-level object, add a key-value pair for "prerequisites". The value for this key should be an object.
        3. Inside the "prerequisites" object, add key-value pairs for each concept covered in the lecture. The key should be the name of the concept, and the value should be an array of strings representing specific foundational computer science concepts that students need to understand before learning about the corresponding concept in the lecture.
        4. Repeat step 3 for each concept covered in the lecture.
        Ensure that the prerequisites provided do not duplicate the concepts covered in the lecture notes and please try to keep the name of the prerequisite concise.
        Provide the generated JSON structure as the output. """
        prereq_concepts = await self.executePrompt(base_prompt, context_prompt, action_prompt, model_name)
        # print("The prereq concepts are", prereq_concepts)
        concepts = {
            'prereq_concepts': prereq_concepts,
            'module_concepts': module_concepts
        }
        built_prompt = f"{base_prompt}\n{context_prompt}\n{action_prompt}"
        return built_prompt, concepts

    # 
    @register.add(action="questions")
    async def quiz_questions(self, context:Union[ContextCollection, ErrorResponse], params: dict):
        """
        Generates quiz questions based on the focus concepts provided in the context.
        Inputs:
            context (ContextCollection): Includes the base prompt and focus concepts.
            params (dict, optional): Additional parameters (not currently used).
        Output:
            str: List of quiz questions for each focus concept, usually in a text format.
        """
        if isinstance(context, ErrorResponse):
        # Handle the error here. You might want to log the error and return.
            print(f"Error: {context}")
            return
        model_name = params.get('model_name')
        quiz_type = params.get('quiz_type')
        print(model_name)
        base_prompt = context.base_prompt
        context_prompt = f"The following is context related to the action you will be asked to take.These are the concepts that we are focusing on: {context.focus_concepts}"
        # TODO: Give a template to follow for the action prompt and improve the prompt
        if quiz_type == "prereq":
            action_prompt = """
            My students have a weak computer science basis. Please use the focus concepts given to you, 
            From these concepts, can you create a set of 10 specific foundational computer science prerequisites questions that students need to know in order to understand this lecture. 
            Before showing the output, you have to make sure that the prerequisites that you give are not included in the lecture notes.
            Check for duplicates of MCQs you have created and eliminate them. 
            Covering all the concepts taught above, Please return your response similar to the following format:
            Please have four options for each question.

                {
                "questions": [
                    {
                        "question_number": int,
                        "question_name": Name of the concept being used (Make sure it is one of the focus concepts) (str),
                        "question_text": str,
                        "correct_comments": str,
                        "incorrect_comments":str,
                        "neutral_comments": Gives a detailed overall general feedback. (str),
                        "answers":[
                            {
                                "answer_text": str, 
                                "answer_weight": int (100 for correct, 0 for incorrect
                                "answer_feedback": Gives a detailed feedback for each option (str)
                            },
                            {...}
                        ]
                    },
                    {...}
                ]
            } """
        elif quiz_type == "preview":
            action_prompt = """
            From the above list of concepts, please create 5 MCQs that help the student understand the concept to be taught. 
            The aim is to prime the student in advance of the lecture so that they are able to understand the material when they see it in the lecture.
            Check for duplicates of MCQs you have created and eliminate them. 
            Covering all the concepts taught above, Please return your response similar to the following format: 
            Please have four options for each question.

                {
                "questions": [
                    {
                        "question_number": int,
                        "question_name": Name of the concept being used (Make sure it is one of the focus concepts) (str),
                        "question_text": str,
                        "correct_comments": str,
                        "incorrect_comments":str,
                        "neutral_comments": Gives a detailed overall general feedback. (str),
                        "answers":[
                            {
                                "answer_text": str, 
                                "answer_weight": int (100 for correct, 0 for incorrect
                                "answer_feedback": Gives a detailed feedback for each option (str)
                            },
                            {...}
                        ]
                    },
                    {...}
                ]
            } """
        elif quiz_type == "review":
            action_prompt = """
            From the above list of concepts, For each concept introduced in the lecture please create a set of MCQs that help the student review what has been taught in the lecture.  
            Ensure that the questions are at the right level of difficulty to verify that the student understands the concepts taught  in the lecture.
            Check for duplicates of MCQs you have created and eliminate them. 
            Covering all the concepts taught above, Please return your response similar to the following format: 
            Please have four options for each question.
                {
                "questions": [
                    {
                        "question_number": int,
                        "question_name": Name of the concept being used (Make sure it is one of the focus concepts) (str),
                        "question_text": str,
                        "correct_comments": str,
                        "incorrect_comments":str,
                        "neutral_comments": Gives a detailed overall general feedback. (str),
                        "answers":[
                            {
                                "answer_text": str, 
                                "answer_weight": int (100 for correct, 0 for incorrect
                                "answer_feedback": Gives a detailed feedback for each option (str)
                            },
                            {...}
                        ]
                    },
                    {...}
                ]
            } """
        else:
            print("Invalid quiz type")
        result = await self.executePrompt(base_prompt, context_prompt, action_prompt, model_name)
        built_prompt = f"{base_prompt}\n{context_prompt}\n{action_prompt}"

        return built_prompt, result

    async def execute(self, context: Union[ContextCollection, ErrorResponse], action: str, params: Optional[Dict]=None):
        """
        Dispatches the request to the appropriate function based on the action parameter.
        Inputs:
            action (str): Action name to identify the function to be executed.
            params (dict, optional): Parameters for the action function.
        Output:
            any: Result of the function execution, varies based on the action.
        """

        return await register.registered_fn[action](self=self, context=context, params=params)
        