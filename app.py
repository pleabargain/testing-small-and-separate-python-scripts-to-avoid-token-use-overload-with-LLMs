import streamlit as st
from ollama_client import OllamaClient
from data_storage import ConversationStorage
from logger_config import setup_logger

# Set up logger for Streamlit app
logger = setup_logger('streamlit_app', 'streamlit_app.log')

# Initialize the clients (only once)
ollama_client = None
storage = None

def get_clients():
    global ollama_client, storage
    if ollama_client is None or storage is None:
        logger.debug("Initializing OllamaClient and ConversationStorage")
        ollama_client = OllamaClient()
        storage = ConversationStorage()
    return ollama_client, storage

def initialize_session_state():
    """Initialize session state variables"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        logger.debug("Initialized empty chat history in session state")

def main():
    try:
        # Get or initialize clients
        ollama_client, storage = get_clients()
        
        # Set up the Streamlit page
        st.title("Chat with Llama")
        
        # Add custom styling
        st.markdown("""
        <style>
        .stChatMessage {
            min-height: 100px;
            padding: 15px;
            margin: 5px 0;
        }
        .stChatMessage p {
            margin: 0;
            padding: 0;
            white-space: pre-wrap;
            overflow-wrap: break-word;
            word-wrap: break-word;
        }
        .element-container {
            width: 100%;
        }
        .stMarkdown {
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)
        
        logger.debug("Streamlit app started")

        # Initialize session state
        initialize_session_state()

        # Check Ollama server status
        if not ollama_client.check_server_status():
            st.error("⚠️ Ollama server is not accessible. Please ensure it's running.")
            logger.error("Ollama server check failed")
            return

        # Create the input area
        user_input = st.text_input("Enter your message:", key="user_input")
        submit_button = st.button("Send")

        # Handle user input (support both button and ctrl+enter)
        if (submit_button or user_input) and user_input:
            input_text = user_input  # Store input before clearing
            logger.debug(f"Processing user input: {input_text[:50]}...")
            
            # Add user message to chat history
            st.session_state.chat_history.append({"user": input_text, "assistant": ""})
            
            try:
                # Display assistant response with streaming
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    
                    # Get last 5 conversations for context
                    conversation_history = storage.get_conversations(limit=5)
                    logger.debug(f"Retrieved {len(conversation_history)} previous conversations for context")
                    
                    # Stream the response with conversation history
                    for chunk in ollama_client.generate_response_stream(input_text, conversation_history):
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    
                    # Final response without cursor
                    message_placeholder.markdown(full_response)
                    response = full_response
                    
                    # Save the conversation
                    if storage.save_conversation(input_text, {"response": response}):
                        logger.info("Successfully saved conversation")
                    else:
                        logger.error("Failed to save conversation")
                        st.warning("Failed to save conversation")
                    
                    # Update chat history with complete response
                    st.session_state.chat_history[-1]["assistant"] = response
                    logger.debug("Updated chat history in session state")
                    
            except Exception as e:
                error_msg = f"Error during streaming: {str(e)}"
                logger.error(error_msg, exc_info=True)
                st.error(error_msg)

        # Display chat history (excluding the current streaming message)
        for i, chat in enumerate(st.session_state.chat_history[:-1] if submit_button else st.session_state.chat_history):
            with st.chat_message("user"):
                st.markdown(chat["user"])
            with st.chat_message("assistant"):
                st.markdown(chat["assistant"])

    except Exception as e:
        error_msg = f"Unexpected error in Streamlit app: {str(e)}"
        logger.error(error_msg, exc_info=True)
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
