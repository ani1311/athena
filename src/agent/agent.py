# src/agent/agent.py

class Agent:
    """
    A mock ADK agent that returns a constant string.
    """

    def get_response(self, message: str) -> str:
        """
        Returns a constant string response.
        """
        return f"You said: {message}"
