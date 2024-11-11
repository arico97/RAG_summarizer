from typing import List, Dict
from io import BytesIO

# Type definition for chat entries
ChatEntry = Dict[str, str]

class ChatTextGenerator:
    """
    A class to create a text document simulating a chat conversation.
    """

    def __init__(self) -> None:
        """Initialize the ChatTextGenerator."""
        self.text_output = BytesIO()

    def add_chat_message(self, speaker: str, message: str) -> None:
        """
        Add a chat message to the text document.

        Parameters:
        ----------
        speaker : str
            The name or identifier of the message sender (e.g., "User", "ChatGPT").
        message : str
            The text content of the message to display in the chat format.
        """
        # Format each message with the speaker name and message
        formatted_message = f"{speaker}: {message}\n\n"
        self.text_output.write(formatted_message.encode("utf-8"))

    def generate_chat_text(self, chat_history: List[ChatEntry]) -> BytesIO:
        """
        Generate a text file simulating a chat conversation and return it as a BytesIO object.

        Parameters:
        ----------
        chat_history : List[ChatEntry]
            A list of dictionaries representing chat entries with 'prompt' and 'answer' keys.

        Returns:
        --------
        BytesIO
            A BytesIO object containing the generated text data.
        """
        # Add each chat message
        for chat in chat_history:
            # User message
            self.add_chat_message("User", chat["prompt"])
            # ChatGPT response
            self.add_chat_message("Chat", chat["answer"])

        # Reset the pointer to the beginning of the BytesIO object
        self.text_output.seek(0)
        return self.text_output
