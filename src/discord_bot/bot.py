"""
This module defines the main Discord bot class for Athena.

It sets up the Discord client and runs the bot, connecting it to the agent
and handling the bot's lifecycle.
"""

import asyncio
import os

import discord

from src.agent.agent import Athena
from src.database.db import Database
from src.discord_bot.client import MyClient
from src.discord_bot.cog import PeriodicMessageCog


class DiscordBot:
    """
    The main class for the Athena Discord bot.

    This class is responsible for initializing and running the Discord bot,
    connecting it with the Athena agent.
    """

    def __init__(self, agent: Athena, db: Database, periodic_channel_name: str = None):
        """
        Initializes the DiscordBot.

        Args:
            agent: An instance of the Athena agent.
            db: An instance of the Database.
            periodic_channel_name: Optional channel ID for periodic messages.
        """
        self.agent = agent
        self.db = db
        self.periodic_channel_name = periodic_channel_name

    def run(self):
        """
        Runs the Discord bot.

        This method sets up the Discord client, reads the bot token from an
        environment variable, and starts the bot. It raises a ValueError if the
        bot token is not found.
        """
        print("Discord bot is running...")

        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        client = MyClient(agent=self.agent, command_prefix="!", intents=intents)

        token = os.getenv("ATHENA_DISCORD_BOT_ACCESS_TOKEN")
        if not token:
            raise ValueError(
                "The ATHENA_DISCORD_BOT_ACCESS_TOKEN environment variable is not set. "
                "Please set it to your Discord bot's access token."
            )

        async def start_bot():
            """
            Starts the bot and adds the cog if a periodic channel is specified.
            """
            async with client:
                if self.periodic_channel_name:
                    await client.add_cog(
                        PeriodicMessageCog(client, self.periodic_channel_name)
                    )
                await client.start(token)

        asyncio.run(start_bot())
