from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import json
import re
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI()


@router.get("/generate-questions")
async def generate_questions(topic: str):
    # Challenge 1.a - Write a prompt as in requirement document. Use {topic} variable to include the topic in the prompt
    prompt = f"""
    Generate 3 questions related to the topic "{topic}" with the following properties:
    - Each question should have "Id", "Question", and "ExpectedAnswer".
    - Provide the output in JSON format as shown below:
    [
      {{
        "Id": 1,
        "Question": "____",
        "ExpectedAnswer": "____"
      }},
      {{
        "Id": 2,
        "Question": "____",
        "ExpectedAnswer": "____"
      }},
      {{
        "Id": 3,
        "Question": "____",
        "ExpectedAnswer": "____"
      }}
    ]
    - Each answer should be 2 or 3 sentences long.
    - DO NOT USE STRUCTURED OUTPUT feature of OpenAI.
    """

    # Challenge 1.b - Call OpenAI API to generate questions using prompt variable
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates descriptive questions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    # Extract the generated text and convert it to JSON
    questions_text = response.choices[0].message.content

    # Challenge 1.c - Remove extra characters from response if present
    questions_json_str = re.sub(r"[\r\n]+", "", questions_text).strip()

    # Load the questions as JSON object from the text 
    questions_json = json.loads(questions_json_str)

    # Return the questions as a JSON response
    return JSONResponse(content={"questions": questions_json})


@router.post("/submitdescriptivequestions")
async def submit_descriptive_questions(request: Request):
    data = await request.json()
    user_message = json.dumps(data['questions'])
    #output = user_message.json()
    output = json.loads(user_message)


    # Challenge 2.a - Write prompt to evaluate the question and answer
    prompt = f"""You are a technical interviewer. Evaluate the following question and answer pair:
    here you need to evaluate the question and answer pair for 3 questions.
    The question and answer pair is as follows:
    {output} has the following question and answer pair:
    1. Question: {data['questions'][0]['Question']}
    Expected Answer is in : {data['questions'][0]['ExpectedAnswer']}
    the candidate has answered as : {data['questions'][0]['CandidateAnswer']}
    2. Question: {data['questions'][1]['Question']}
    Expected Answer is in : {data['questions'][1]['ExpectedAnswer']}
    the candidate has answered as : {data['questions'][1]['CandidateAnswer']}
    3. Question: {data['questions'][2]['Question']}
    Expected Answer is in : {data['questions'][2]['ExpectedAnswer']}
    the candidate has answered as : {data['questions'][2]['CandidateAnswer']}

You need to evaluate the candidate's answer based on the following criteria:
1. Whether the answer is correct or incorrect.
    2. If the answer is incorrect, provide the correct answer.
    3. Provide a score from 0 to 10 based on the quality of the answer.
    4. Provide a detailed explanation of the answer.
    5. Provide a list of keywords that are relevant to the question and answer.

                        """

    # Challenge 2.b - Call the OpenAI API and get the response
    feedback_response = {}
    feedback_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates descriptive questions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )


    # Extract the generated text
    feedback_text = feedback_response.choices[0].message.content

    # Return the feedback as a JSON response
    return JSONResponse(content={"feedback": feedback_text})
