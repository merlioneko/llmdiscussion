from openai import OpenAI
from time import sleep

model_A = "gpt-3.5-turbo"
model_B = "gpt-3.5-turbo"

talker_A = OpenAI(base_url="http://localhost:8000/v1", api_key="test")
talker_B = OpenAI(base_url="http://localhost:8001/v1", api_key="test")

talk_history = []
talk_history.append("Master: " + input("Enter the initial message for the conversation: "))

response_A = ""
response_B = ""
while True:
    raw_response_A = talker_A.chat.completions.create(
        model=model_A,
        messages=[
            {"role": "system", "content": "You are a kindly assistant. You talk to another assistant Model_B."},
            {"role": "user", "content": "\n".join(talk_history)},
        ])
    response_A = "Model_A: " + raw_response_A.choices[0].message.content
    print(response_A)
    talk_history.append(response_A)

    raw_response_B = talker_B.chat.completions.create(
        model=model_B,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You talk to another assistant Model_A."},
            {"role": "user", "content": "\n".join(talk_history)},
        ])
    response_B = "Model_B: " + raw_response_B.choices[0].message.content
    print(response_B)
    talk_history.append(response_B)

def history_to_prompt(history: list[str]):
    """履歴をmessage配列に直す"""
    prompt = []
