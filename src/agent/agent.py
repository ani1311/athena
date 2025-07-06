"""
This module defines the Athena agent, which uses the Google ADK to interact
with a generative AI model.
"""

import os

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from src.database.db import Database

# Define a constant for the application name to avoid repetition.
APP_NAME = "athena"


class Athena:
    """
    The Athena agent, responsible for processing user prompts and generating
    responses using a generative AI model.
    """

    def __init__(self, db: Database):
        """
        Initializes the Athena agent, setting up the ADK agent, session service,
        and runner. It retrieves the model ID from environment variables.
        """
        self.agent = Agent(
            model=os.environ.get("MODEL_ID"),
            name="athena_personal_assistant",
            instruction="""
You are a personal assistant named Athena. You respond to messages that will be
sent to you in a Discord channel, and you will respond with a discord formatted
message. Try to be generally helpful and friendly.
            """,
        )
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=self.agent,
            app_name=APP_NAME,
            session_service=self.session_service,
        )
        self._session_initialized = False

        self.db = db  # Store the database instance for later use

    async def _ensure_session(self):
        """
        Ensures that a session is created before the agent is run.

        This private method is called once to initialize the session with a
        hardcoded user and session ID. In a production environment, these
        should be made dynamic to handle multiple users.
        """
        if not self._session_initialized:
            # TODO: Replace hardcoded user_id and session_id with dynamic values
            # in a production environment.
            await self.session_service.create_session(
                app_name=APP_NAME, user_id="some_user", session_id="some_session_id"
            )
            self._session_initialized = True

    async def run_agent_and_get_response(self, prompt: str) -> str:
        """
        Sends a prompt to the ADK agent and returns the final response.

        Args:
            prompt: The user's message to send to the agent.

        Returns:
            The agent's final text response.
        """
        await self._ensure_session()

        content = types.Content(role="user", parts=[types.Part(text=prompt)])

        # run_async executes the agent and yields events. We iterate through
        # them to find the final response.
        async for event in self.runner.run_async(
            user_id="some_user", session_id="some_session_id", new_message=content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    return event.content.parts[0].text
                if event.actions and event.actions.escalate:
                    return f"Agent escalated: {event.error_message or 'No specific message.'}"
                break  # Stop processing once the final response is found.

        return "Agent did not produce a final response."

    async def get_response(self, author: str, message: str) -> str:
        """
        Formats the user's message and retrieves a response from the agent.

        Args:
            author: The author of the message.
            message: The content of the message.

        Returns:
            The agent's response to the message.
        """
        prompt = f"{author}: {message}"
        return await self.run_agent_and_get_response(prompt)
