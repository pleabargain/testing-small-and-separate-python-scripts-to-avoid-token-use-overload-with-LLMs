# Streamlit Ollama Chat Interface

#repo
https://github.com/pleabargain/testing-small-and-separate-python-scripts-to-avoid-token-use-overload-with-LLMs


A Streamlit-based chat interface that interacts with a local Ollama LLM server. This project demonstrates modular Python development with comprehensive logging and error handling.

It'll hold the last 5 conversations in memory.

# this is a local instance of the streamlit app
I am using the llama3.2 model

I'm using the python-json-logger package to log the messages to a file.

#goal
I'm trying to get the number of files that need to be edited when working with cline to as few as possible. This might help in keeping the code clean and easy to maintain. As well, to help the coding assistants from spiraling into crazy town.


## Project Structure

- `app.py` - Main Streamlit application with user interface
- `ollama_client.py` - Handles communication with Ollama server
- `data_storage.py` - Manages conversation storage in JSON format
- `logger_config.py` - Configures logging for all components
- `schema.json` - Defines the JSON schema for conversation storage
- `logs/` - Directory containing component-specific log files
  - `streamlit_app.log` - Streamlit application logs
  - `ollama_client.log` - Ollama client interaction logs
  - `data_storage.log` - Data storage operation logs

## Features

- Text input interface with send button
- Real-time chat with Ollama LLM
- Persistent conversation storage in JSON format
- Comprehensive error handling and logging
- Server status monitoring
- Chat history display

## Prerequisites

- Python 3.8+
- Ollama server running locally with llama3.2 model
- Ollama server accessible at http://localhost:11434/

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure Ollama server is running with llama3.2 model
2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open your browser at http://localhost:8501

## Logging

The application uses comprehensive logging with different log files for each component:

- All logs include timestamp, component name, and log level
- Debug mode is enabled by default
- Logs are stored in the `logs/` directory
- Each component has its own log file for easier debugging

## Data Storage

Conversations are stored in `conversations.json` following the schema defined in `schema.json`. Each entry includes:

- Unique conversation ID
- Timestamp
- User input
- LLM response with model information

## Error Handling

The application includes robust error handling:

- Ollama server connectivity checks
- JSON file operations with fallbacks
- Input validation
- Comprehensive error logging
- User-friendly error messages in UI

## Development

The project is structured to separate concerns:

- UI logic in Streamlit app
- LLM interaction in dedicated client
- Data persistence in storage module
- Centralized logging configuration

This modular approach makes the code more maintainable and easier to test.
