import sys
import subprocess
import json
import traceback
import re

sandbox_fileName="sandbox.py"

def extract_code(text):
    """
    Extracts Python code from a text response. Assumes that code is enclosed in triple backticks.
    """
    code_pattern = re.compile(r'```python(.*?)```', re.DOTALL)
    match = code_pattern.search(text)
    if match:
        return match.group(1).strip()
    else:
        return None

def write_python_file(filename, code):
    with open(filename, 'w') as file:
        file.write(code)

def run_python_file(filename):
    try:
        result = subprocess.run(
            ['python', filename],
            text=True,
            capture_output=True,
            check=True
        )
        return {"Output": result.stdout.strip(), "Error": None}
    except subprocess.CalledProcessError as e:
        return {"Output": e.stdout.strip(), "Error": e.stderr.strip()}


def execute_code(text):
    code = extract_code(text)
    write_python_file(filename=sandbox_fileName,code=code)
    return run_python_file(filename=sandbox_fileName)

if __name__ == "__main__":
    # Read the input text from the first command line argument
    text = sys.argv[1]
    
    # Execute the code
    result = execute_code(text=text)
    
    # Print the result as JSON
    print(json.dumps(result))
