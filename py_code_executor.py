import sys
import json
import traceback
import re

class CodeExtractor:
    """Responsible for extracting code from a text response."""
    
    def __init__(self, language="python"):
        self.language = language
        self.code_pattern = re.compile(rf'```{self.language}(.*?)```', re.DOTALL)

    def extract(self, text):
        match = self.code_pattern.search(text)
        if match:
            return match.group(1).strip()
        else:
            return None

class CodeExecutor:
    """Responsible for executing the extracted code."""
    
    def __init__(self, extractor: CodeExtractor):
        self.extractor = extractor

    def execute(self, text):
        code = self.extractor.extract(text)
        if not code:
            return {"output": None, "error": "No Python code found in the text"}

        try:
            # Redirect stdout to capture print statements
            original_stdout = sys.stdout
            sys.stdout = open('output.txt', 'w')
            
            # Execute the code
            exec(code, {})
            
            # Reset stdout
            sys.stdout.close()
            sys.stdout = original_stdout
            
            # Read the output
            with open('output.txt', 'r') as file:
                output = file.read()
            
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": None, "error": traceback.format_exc()}

class Executor:
    """Handles the application flow."""
    
    def __init__(self):
        self.code_extractor = CodeExtractor()
        self.code_executor = CodeExecutor(self.code_extractor)

    def run(self, text):
        result = self.code_executor.execute(text)
        print(json.dumps(result))

if __name__ == "__main__":
    # Read the input text from the first command line argument
    input_text = sys.argv[1]
    
    # Create and run the application
    app = Executor()
    app.run(input_text)
