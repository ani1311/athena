"""
This module defines the Discord client for Athena, which handles all
interactions with the Discord API.
"""

import discord

from src.agent.agent import Athena

# Discord's maximum message length.
MAX_MESSAGE_LENGTH = 2000


class MyClient(discord.Client):
    """
    The customized Discord client for the Athena bot.

    This class handles Discord events, such as when the bot is ready and when a
    message is received.
    """

    def __init__(self, agent: Athena, *args, **kwargs):
        """
        Initializes the Discord client.

        Args:
            agent: An instance of the Athena agent.
            *args: Variable length argument list for the parent class.
            **kwargs: Arbitrary keyword arguments for the parent class.
        """
        super().__init__(*args, **kwargs)
        self.agent = agent

    async def on_ready(self):
        """
        Handles the event when the bot has successfully connected to Discord.
        """
        print(f"Bot '{self.user.name}' (ID: {self.user.id}) is ready!")

    def _split_response(self, response: str) -> list[str]:
        """
        Splits a response string into chunks that are within Discord's
        message length limit.

        Args:
            response: The string to split.

        Returns:
            A list of response chunks.
        """
        return [
            response[i : i + MAX_MESSAGE_LENGTH]
            for i in range(0, len(response), MAX_MESSAGE_LENGTH)
        ]

    async def on_message(self, message: discord.Message):
        """
        Handles the event when a message is sent in a channel the bot can see.

        Args:
            message: The message object from Discord.
        """
        # Ignore messages sent by the bot itself.
        if message.author == self.user:
            return

        print(
            f"Message from {message.author}: {message.content}, "
            f"Type: {message.type}, In thread: {isinstance(message.channel, discord.Thread)}"
        )

        # Get a response from the Athena agent.
        agent_response = await self.agent.get_response(
            str(message.author), message.content
        )

        if not agent_response:
            return

        # Split the response into chunks to adhere to Discord's message limit.
        chunks = self._split_response(agent_response)

        # If the original message is in a thread, reply in the same thread.
        # Otherwise, create a new thread for the response.
        response_channel = message.channel
        if not isinstance(message.channel, discord.Thread):
            # Use the message content as the thread name, truncated if necessary
            thread_name = message.content[:100] if message.content else "Response"
            response_channel = await message.create_thread(name=thread_name)

        for chunk in chunks:
            await response_channel.send(chunk)
