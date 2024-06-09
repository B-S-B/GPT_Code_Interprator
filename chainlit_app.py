import chainlit as cl
from file_handeling import CSV
from openai_api import GPTwithSandbox

context="Act as a Data Scientis who writes accurate and error free code. I have enabled python sandbox like function that can extract code from your response, execute it and respond with the output and errors The syntax of respose will be in format: Response by Function: {'output': the_output, 'error': error_discription}. Hence always respond with complete code and in a single code section and always generte final output through a print function."

chat_instance=GPTwithSandbox()
chat_instance.setContext(context=context)

@cl.on_message
async def handle_message(message):
    if message.elements:
        # Handle file upload
        files =[ file for file in message.elements if "text/csv" in file.mime]
        if not files:
            await cl.Message(content="Only CSV files supported!\n Please retry").send()
        else:
            csv_file=CSV(files[0].name,files[0].path)
            user_instruction = message.content
            response=chat_instance.sendPrompt(f"{user_instruction}. Following is the sample dataframe of the attached csv file with {csv_file}. {csv_file.getCsvSample(5)}")
            await cl.Message(response).send()
            code_execution_response=chat_instance.checkForCode(response)
            if bool(code_execution_response):
                await cl.Message(f"Code Runner response: {code_execution_response}").send()
    else:
        # Handle general chit-chat
        response=chat_instance.sendPrompt(message.content)
        await cl.Message(response).send()
        code_execution_response=chat_instance.checkForCode(response)
        if bool(code_execution_response):
            await cl.Message(f"{code_execution_response}").send()