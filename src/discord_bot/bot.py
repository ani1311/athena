# src/discord_bot/bot.py

from src.agent.agent import Agent
from src.database.db import Database

import discord
import asyncio
import os


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.testing_channel = None

    async def on_ready(self):
        channels = self.get_all_channels()
        for channel in channels:
            print(channel.name, channel.id)
            if channel.name == "testing":
                self.testing_channel = channel

        if self.testing_channel:
            await self.testing_channel.send("Hello my master, I am ready to serve you!")
            # Start the background task for sending test messages
            self.loop.create_task(self.send_test_messages())

    async def send_test_messages(self):
        """
        Send a test message every 30 seconds to the testing channel.
        """
        await self.wait_until_ready()  # Ensure the bot is fully ready
        while not self.is_closed():
            if self.testing_channel:
                await self.testing_channel.send("Test message - sent every 30 seconds!")
            await asyncio.sleep(30)  # Wait 30 seconds

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")


class DiscordBot:
    """
    The Discord bot.
    """

    def __init__(self, agent: Agent, db: Database):
        self.agent = agent
        self.db = db

    def run(self):
        """
        Runs the Discord bot.
        """
        print("Discord bot is running...")

        intents = discord.Intents.default()
        intents.message_content = True

        client = MyClient(intents=intents)

        # Read token from environment variable
        token = os.getenv("ATHENA_DISCORD_BOT_ACCESS_TOKEN")
        if not token:
            raise ValueError(
                "ATHENA_DISCORD_BOT_ACCESS_TOKEN environment variable is not set"
            )

        client.run(token)
