import openai
from django.conf import settings

class ContentsService:
    def __init__():
        openai.api_key = settings.OPENAI_API_KEY
    
    def get_reply(messages):
        try:
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = messages,
            )
            reply = response["choices"][0]["message"]["content"]
        except openai.OpenAIError as err:
            reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"
        return reply
    
    def get_reply_s(messages):
        try:
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = messages,
                stream = True
            )
            for chunk in response:
                if 'content' in chunk['choices'][0]['delta']:
                    yield chunk["choices"][0]["delta"]["content"]
        except openai.OpenAIError as err:
            reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"