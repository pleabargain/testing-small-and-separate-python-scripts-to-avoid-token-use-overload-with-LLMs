goal: test ollama locally with a streamlit app where the functionality is separated into separate python scripts. Find out if this will make Cline e development more efficient.

Create a streamlit app

create a separate python script that accesses ollama locally and returns a response to the user
activate full debug mode
log all errors to a log file specifically for this function
ollama is a local LLM server
ollama is running on http://localhost:11434/
llama3.2 is the model
model="llama3.2"


streamlit app should have a text input and a button
activate full debug mode
log all errors to a log file specifically for this function
when user hits ctrl+enter, the input is saved to a JSON file and passed to the ollama function that returns a response in the streamlit app
the user input is saved with a timestamp in a JSON file
the user input is passed to the streamlit user interface
the user input text field is cleared after the input is saved to the JSON file and waits for the next input



create a separate python script that saves the input and ollama response to a JSON file
activate full debug mode
log all errors to a log file specifically for this function
the input is saved with a timestamp in a JSON file
the input is passed to the ollama function that returns a response in the streamlit app
the ollama response is streamed to the user in the streamlit app and saved with a timestamp in a JSON file with the input

create a JSON schema for the input and output from user and the ollama response


create a requirements.txt file
- do not number the python files
create a readme.md file and update as necessary



