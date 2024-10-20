"""Custom exceptions for the app."""

# pylint: disable=too-few-public-methods
class InappropriatePromptException(Exception):
    """Raised when the prompt is inappropriate."""
    def __init__(self, message="Error: Inappropriate Prompt"):
        self.message = message
        super().__init__(self.message)
