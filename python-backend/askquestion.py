from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import json
from openai import OpenAI
import os

router = APIRouter()

@router.get("/ask-question")
async def generate_question(topic: str):
    # Challenge 1.a - Write the prompt
    prompt = f"""
    You are an AI assistant that generates questions based on a given topic.
    The questions should be clear, concise, and easy to understand.
    The topic is: {topic}
    Please generate a a question based on the topic.
    """
   
    client = OpenAI()

    # Challenge 1.b - Call OpenAI API to generate questions
    response = {}
    response = client.chat.completions.create(
    model="gpt-4o",
    n=1,
    temperature=0.2,
    messages=[
        {"role": "developer", "content": "You are an expert in technical interviews. "
        "generting questions with concise 1-2 sentences answers"},
        {
            "role": "user",
            "content": prompt,
        },
    ],
)
  
    # Extract the generated text
    questions_text = response.choices[0].message.content

    # Return the questions as a JSON response
    return JSONResponse(content={"question": questions_text})

@router.post("/question-feedback")
async def submit_descriptive_questions(request: Request):
    # Request parameter includes both question and answer provided by user.
    data = await request.json()
    question = data['question']['question']
    answer = data['question']['CandidateAnswer']
    
    #Challenge 2.a - Write Prompt to evaluate the question and answer
    #Use question and answer variable to generate the prompt
    prompt = f""" 
    This is a question and answer evaluation task.
    You are given a question and an answer. Your task is to evaluate the answer based on the question and provide feedback.
    The feedback should include the following:
    1. Whether the answer is correct or incorrect.
    2. If the answer is incorrect, provide the correct answer.
    3. Provide a score from 0 to 10 based on the quality of the answer.
    4. Provide a detailed explanation of the answer.
    5. Provide a list of keywords that are relevant to the question and answer.
    here is the question and answer:
    Question: {question}
    Answer: {answer}
                      """

    # OpenAI Call to generate feedback
    header_name = os.getenv('GATEWAY_HEADER_NAME')
    header_value = os.getenv('GATEWAY_HEADER_VALUE')
    headers = {
        header_name: header_value
    }
    client = OpenAI(default_headers=headers)

    #Challenge 2.b - Call the OpenAI API and get the resopnse
    response = {}
    response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.2,
    messages=[
        {"role": "developer", "content": "you are an expert in technical interviews. "},
        {
            "role": "user",
            "content": prompt,
        },
    ],
    )

    # Extract the generated text
    feedback_text = response.choices[0].message.content

    # Return the feedback as a JSON response
    return JSONResponse(content={"feedback": feedback_text})
