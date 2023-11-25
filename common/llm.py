import os
from openai import OpenAI

client = OpenAI(os.environ['OPENAI_KEY'])

def get_response(messages):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response = response.choices[0].message.content
    return response
