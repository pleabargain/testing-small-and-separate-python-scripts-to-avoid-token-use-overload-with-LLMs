import json
from datetime import datetime
import uuid
from logger_config import setup_logger

# Set up logger for data storage operations
logger = setup_logger('data_storage', 'data_storage.log')

class ConversationStorage:
    def __init__(self, filename="conversations.json"):
        self.filename = filename
        logger.debug(f"Initialized ConversationStorage with filename: {filename}")

    def save_conversation(self, user_input, llm_response):
        """Save a conversation with timestamps to JSON file"""
        try:
            logger.debug("Attempting to save new conversation")
            conversation = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "user_input": user_input,
                "llm_response": llm_response
            }
            
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    logger.debug("Successfully loaded existing conversation file")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logger.warning(f"Could not load existing file: {str(e)}. Creating new data structure.")
                data = {"conversations": []}
            
            data["conversations"].append(conversation)
            
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Successfully saved conversation with ID: {conversation['id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}", exc_info=True)
            return False

    def get_conversations(self):
        """Retrieve all conversations from the JSON file"""
        try:
            logger.debug("Attempting to retrieve conversations")
            with open(self.filename, 'r') as f:
                data = json.load(f)
            logger.info("Successfully retrieved conversations")
            return data.get("conversations", [])
        except FileNotFoundError:
            logger.warning("No conversation file found")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding conversation file: {str(e)}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Unexpected error retrieving conversations: {str(e)}", exc_info=True)
            return []
