FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app
# Copying all data to the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exposing container to Internet
EXPOSE 8000

# Define environment variable for OpenAI API Key
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Run the application
CMD ["chainlit", "run", "chainlit_app.py"]
