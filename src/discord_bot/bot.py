"""
This module defines the main Discord bot class for Athena.

It sets up the Discord client and runs the bot, connecting it to the agent
and handling the bot's lifecycle.
"""

import os

import discord

from src.agent.agent import Athena
from src.discord_bot.client import MyClient


class DiscordBot:
    """
    The main class for the Athena Discord bot.

    This class is responsible for initializing and running the Discord bot,
    connecting it with the Athena agent.
    """

    def __init__(self, agent: Athena):
        """
        Initializes the DiscordBot.

        Args:
            agent: An instance of the Athena agent.
        """
        self.agent = agent

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

        client = MyClient(self.agent, intents=intents)

        token = os.getenv("ATHENA_DISCORD_BOT_ACCESS_TOKEN")
        if not token:
            raise ValueError(
                "The ATHENA_DISCORD_BOT_ACCESS_TOKEN environment variable is not set. "
                "Please set it to your Discord bot's access token."
            )

        client.run(token)
