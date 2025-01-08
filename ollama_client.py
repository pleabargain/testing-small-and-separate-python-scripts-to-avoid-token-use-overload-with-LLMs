import ollama
from datetime import datetime
from logger_config import setup_logger
from typing import Generator, Dict

# Set up logger for Ollama client operations
logger = setup_logger('ollama_client', 'ollama_client.log')

class OllamaClient:
    def __init__(self, model="llama3.2"):
        self.model = model
        logger.debug(f"Initialized OllamaClient with model: {model}")

    def generate_response_stream(self, prompt: str, conversation_history: list = None) -> Generator[str, None, Dict]:
        """Generate a streaming response from Ollama for the given prompt
        Args:
            prompt (str): The current user prompt
            conversation_history (list, optional): List of previous conversations to use as context
        """
        try:
            logger.debug(f"Generating streaming response for prompt: {prompt[:50]}...")
            
            # Format conversation history into messages
            messages = []
            if conversation_history:
                for conv in conversation_history:
                    messages.append({"role": "user", "content": conv["user_input"]})
                    if isinstance(conv["llm_response"], dict) and "response" in conv["llm_response"]:
                        messages.append({"role": "assistant", "content": conv["llm_response"]["response"]})
                    elif isinstance(conv["llm_response"], str):
                        messages.append({"role": "assistant", "content": conv["llm_response"]})
            
            # Add current prompt
            messages.append({"role": "user", "content": prompt})
            stream = ollama.chat(model=self.model, messages=messages, stream=True)
            
            full_response = ""
            for chunk in stream:
                content = chunk['message']['content']
                full_response += content
                yield content
            
            logger.info("Successfully completed streaming response from Ollama")
            
            # Return the final response data for storage
            return {
                "model": self.model,
                "response": full_response,
                "response_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Error during streaming: {str(e)}"
            logger.error(error_msg, exc_info=True)
            yield f"Error: {error_msg}"
            return self._create_error_response(error_msg)

    def _create_error_response(self, error_message: str) -> Dict:
        """Create a formatted error response"""
        return {
            "model": self.model,
            "response": f"Error: {error_message}",
            "response_timestamp": datetime.utcnow().isoformat()
        }

    def check_server_status(self) -> bool:
        """Check if the Ollama server is running and accessible"""
        try:
            logger.debug("Checking Ollama server status")
            ollama.list()
            logger.info("Ollama server is running and accessible")
            return True
        except Exception as e:
            logger.error(f"Ollama server check failed: {str(e)}", exc_info=True)
            return False
