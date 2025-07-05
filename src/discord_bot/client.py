"""_
summary_
"""

import asyncio
import discord

from src.agent.agent import Athena


class MyClient(discord.Client):
    """_summary_

    Args:
        discord (_type_): _description_
    """

    def __init__(self, agent: Athena, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent = agent
        self.testing_channel = None

    async def on_ready(self):
        """
        Called when the bot is ready.
        """
        print(f"Bot '{self.user.name}' (ID: {self.user.id}) is ready!")

        channels = self.get_all_channels()
        for channel in channels:
            print(channel.name, channel.id)
            if channel.name == "testing":
                self.testing_channel = channel

        # if self.testing_channel:
        #     await self.testing_channel.send("Hello my master, I am ready to serve you!")
        #     Start the background task for sending test messages
        #     self.loop.create_task(self.send_test_messages())

    async def send_test_messages(self):
        """
        Send a test message every 30 seconds to the testing channel.
        """
        await self.wait_until_ready()  # Ensure the bot is fully ready
        while not self.is_closed():
            if self.testing_channel:
                await self.testing_channel.send("Test message - sent every 30 seconds!")
            await asyncio.sleep(30)  # Wait 30 seconds

    async def on_message(self, message: discord.Message):
        """
        Called when a message is sent in a channel the bot can see.
        """
        # Don't respond to the bot's own messages
        if message.author == self.user:
            return

        # Check if the message is in a thread
        is_in_thread = isinstance(message.channel, discord.Thread)

        print(
            f"Message from {message.author}: {message.content}, Type: {message.type}, In thread: {is_in_thread}"
        )

        # Get response from agent
        resp = await self.agent.get_response(message.author, message.content)

        # Split response into chunks if it's too long (Discord limit is 4000 characters)
        max_length = 2000
        if len(resp) <= max_length:
            chunks = [resp]
        else:
            chunks = []
            for i in range(0, len(resp), max_length):
                chunks.append(resp[i : i + max_length])

        if is_in_thread:
            # If already in a thread, just reply in the same thread
            for chunk in chunks:
                await message.channel.send(chunk)
        else:
            # If not in a thread, create a new thread and send response there
            thread = await message.create_thread(name="Response")
            for chunk in chunks:
                await thread.send(chunk)
