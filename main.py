# Import the OpenAI chat model from LangChain. This provides a wrapper for models like GPT-3.5.
from langchain.chat_models import ChatOpenAI

# Import the custom memory manager and conversation handler you defined
from src.components.memory_chat_manager import MemoryManager, ConversationModel

# ---------------- Step 1: Initialize the LLM and memory system ---------------- #

# Create an instance of ChatOpenAI with specified parameters
# model_name: Specifies the OpenAI model to use
# temperature: Controls randomness; 0.7 gives moderately creative responses
llm = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature = 0.0)

# Create a memory manager instance to manage session-based chat histories
memory_manager = MemoryManager()

# Create a conversation model that wraps the LLM with memory support
conversation = ConversationModel(llm, memory_manager)

# ---------------- Step 2: Define two user sessions ---------------- #

# Define a unique session ID for user Rahul
session_id_1 = "rahul-session"

# Define a unique session ID for user Alice
session_id_2 = "alice-session"

# ---------------- Step 3: Simulate conversation with user Rahul ---------------- #

# First message from Rahul - this will be stored in memory under 'rahul-session'
print(conversation.send_message("Hi, I'm Rahul!", session_id_1))

# Since the name was shared earlier in the same session, the model can now reference it
print(conversation.send_message("What's my name?", session_id_1))

# ---------------- Step 4: Simulate conversation with user Alice ---------------- #

# First message from Alice - stored under a different session
print(conversation.send_message("Hello! I'm Alice.", session_id_2))

# Because Alice also mentioned her name earlier in her session, the model should recall it
print(conversation.send_message("Do you remember my name?", session_id_2))