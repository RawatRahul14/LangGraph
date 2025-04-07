# Importing RunnableWithMessageHistory to wrap an LLM with memory support
from langchain_core.runnables.history import RunnableWithMessageHistory

# Importing in-memory storage for chat history and base class for flexibility in history storage types
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory

# Importing the Runnable class which represents a callable LLM or chain
from langchain_core.runnables import Runnable

# Class to manage memory for different chat sessions
class MemoryManager:

    def __init__(self):

        # Dictionary to store chat histories for different session_ids
        self.store = {}

    # Returns the chat history object for a specific session_id
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:

        # If there's no history for the given session_id, create a new in-memory chat history
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()

        # Return the stored or newly created chat history
        return self.store[session_id]
    
# Class to handle conversation logic using LLM and session-based memory
class ConversationModel:
    def __init__(self,
                 llm: Runnable,
                 memory_manager: MemoryManager):
        
        # Save the LLM (Runnable type - can be a chain, a prompt + model, etc.)
        self.llm = llm

        # Save the memory manager that handles session histories
        self.memory_manager = memory_manager

        # Wrap the LLM with memory support by integrating it with the session-based chat history
        self.model_with_history = RunnableWithMessageHistory(self.llm,
                                                             self.memory_manager.get_session_history)

    # Sends a message to the LLM for a specific session and returns the response 
    def send_message(self,
                     message: str,
                     session_id: str):
        
        # Configuration object to pass session_id for history tracking
        config = {
            "configurable": {
                "session_id": session_id
            }
        }

        response = self.model_with_history.invoke(message, config = config)

        return response.content