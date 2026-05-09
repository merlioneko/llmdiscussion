from openai import OpenAI
from time import sleep

class Comment:
    def __init__(self, talker: str, message: str):
        self.talker = talker
        self.message = message

class Talker:
    def __init__(self, model: str, base_url: str, api_key: str,
                 topic: str = "Small talk"):
        self.model = model
        self.talker = OpenAI(base_url=base_url, api_key=api_key)
        self.rollplay = f"You are a helpful assistant. You talk about {topic}."

    def talk(self, history: list[str]) -> Comment:
        response = self.talker.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.rollplay},
                {"role": "user", "content": "\n".join(history)},
            ])
        return Comment(talker=self.model, message=response.choices[0].message.content or ".....")
    
class TalkHistory:
    def __init__(self):
        self.history: list[Comment] = []
    
    def add_comment(self, comment: Comment):
        self.history.append(comment)
    
    def to_prompt(self) -> list[dict[str, str]]:
        return [{"role": "user", "content": f"{comment.talker}: {comment.message}"} for comment in self.history]

topic = input("Enter the topic for the conversation: ")
talkerA = Talker(model="gpt-4o", base_url="https://api.openai.com/v1", api_key="your_api_key_for_model_A", topic=topic)
talkerB = Talker(model="gpt-4o", base_url="https://api.openai.com/v1", api_key="your_api_key_for_model_B", topic=topic)

talk_history = TalkHistory()
talk_history.add_comment(Comment(talker="Master", message=input("Enter the initial message for the conversation: ")))

response_A = Comment(talker=talkerA.model, message="")
response_B = Comment(talker=talkerB.model, message="")
while True:
    raw_response_A = talkerA.talk(talk_history)
    response_A = "Model_A: " + raw_response_A
    print(response_A)
    talk_history.add_comment(response_A)

    raw_response_B = talkerB.talk(talk_history)
    response_B = "Model_B: " + raw_response_B
    print(response_B)
    talk_history.add_comment(response_B)
    
