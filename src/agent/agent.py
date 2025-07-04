"""
Athena ADK Agent
"""

import asyncio
import os

from google.adk.agents import Agent
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.runners import Runner

from google.genai import types


class Athena:
    """
    A mock ADK agent that returns a constant string.
    """

    def __init__(self):
        """
        Initializes the Agent.
        """
        self.agent = Agent(
            model=os.environ.get("MODEL_ID"),
            name="athena_personal_assistant",
            instruction="""
You are a personal assistant named Athena. You respond to messages that will be sent to you in a Discord channel,
and you will respond with a discord formatted message. Try to be generally helpful and friendly.
            """,
        )
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=self.agent,
            app_name="athena",
            session_service=self.session_service,
        )
        self._session_initialized = False

    async def _ensure_session(self):
        """
        Ensures the session is created (only called once).
        """
        if not self._session_initialized:
            await self.session_service.create_session(
                app_name="athena", user_id="some_user", session_id="some_session_id"
            )
            self._session_initialized = True

    async def run_agent_and_get_response(self, prompt: str) -> str:
        """
        Sends a query to the agent and prints the final response.
        """
        # Ensure session is created before running
        await self._ensure_session()

        # Prepare the user's message in ADK format
        content = types.Content(role="user", parts=[types.Part(text=prompt)])

        final_response_text = "Agent did not produce a final response."  # Default

        # Key Concept: run_async executes the agent logic and yields Events.
        # We iterate through events to find the final answer.
        async for event in self.runner.run_async(
            user_id="some_user", session_id="some_session_id", new_message=content
        ):
            # You can uncomment the line below to see *all* events during execution
            # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

            # Key Concept: is_final_response() marks the concluding message for the turn.
            if event.is_final_response():
                if event.content and event.content.parts:
                    # Assuming text response in the first part
                    final_response_text = event.content.parts[0].text
                elif (
                    event.actions and event.actions.escalate
                ):  # Handle potential errors/escalations
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                # Add more checks here if needed (e.g., specific error codes)
                break  # Stop processing events once the final response is found

        return final_response_text

    async def get_response(self, author: str, message: str) -> str:
        """
        Returns a constant string response.
        """
        resp = await self.run_agent_and_get_response(f"{author}: {message}")
        return resp
