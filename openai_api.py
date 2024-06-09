from openai import OpenAI
from py_code_executorv0 import execute_code,extract_code

class ChatWithLLM:
    chat_history=list()
    last_response=""
    def __init__(self,model_name) -> None:
        self.ModelName=model_name

    def setContext(self,context):
        return "No model formatting set!"
        
    def sendPrompt(self,prompt):
        return "No model specific api call set!"

    def readResponse(self):
        return self.last_response
    
    def showChatHistroy(self):
        return self.chat_history
    
class ChatWithGPT(ChatWithLLM):
    def __init__(self, model_name='gpt-3.5-turbo') -> None:
        super().__init__(model_name)
        self.client=OpenAI()

    def setContext(self, context):
        self.chat_history.append({
            "role": "system",
            "content": context
        })
        print("Context Set Succesfully!")
    
    def sendPrompt(self, prompt):
        #Adding prompt to chat history to retail context from ongoing chat
        self.chat_history.append({
                "role":"user",
                "content":prompt
            })
        
        #Sending the prompt to API and receiving respose
        self.last_response = self.client.chat.completions.create(
            model=self.ModelName,
            messages=self.chat_history)
        
        #Maintaining chat History
        self.chat_history.append({
            "role":"assistant",
            "content":self.last_response.choices[0].message.content
        })
        return self.last_response.choices[0].message.content
    
    def readResponse(self):
        return self.last_response.choices[0].message.content
    
class GPTwithSandbox(ChatWithGPT):
    def __init__(self, model_name='gpt-3.5-turbo') -> None:
        super().__init__(model_name)

    def sendPrompt(self, prompt, role="user"):
        #Adding prompt to chat history to retail context from ongoing chat
        if role != "user":
            print(f"role ={role} and in code format")
            self.chat_history.append({
                    "role":"user",
                    "content": f"Response by Function: {prompt}"
                })
        else:
            print(f"role ={role} and in noncode format")
            self.chat_history.append({
                    "role":role,
                    "content":prompt
                })
        
        #Sending the prompt to API and receiving respose
        self.last_response = self.client.chat.completions.create(
            model=self.ModelName,
            messages=self.chat_history)
        
        #Maintaining chat History
        self.chat_history.append({
            "role":"assistant",
            "content":self.last_response.choices[0].message.content
        })
        return self.last_response.choices[0].message.content
    
    def checkForCode(self,gpt_response):
        if not bool(extract_code(gpt_response)):
            print("code Not Found")
            return False
        else:
            print("Code Found")
            code_output=execute_code(gpt_response)
            return self.sendPrompt(code_output,role="function")