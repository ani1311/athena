"""_summary_

Raises:
    ValueError: _description_
"""

import os
import discord

from src.agent.agent import Athena
from src.database.db import Database
from src.discord_bot.client import MyClient


class DiscordBot:
    """
    The Discord bot.
    """

    def __init__(self, agent: Athena, db: Database):
        self.agent = agent
        self.db = db

    def run(self):
        """
        Runs the Discord bot.
        """
        print("Discord bot is running...")

        intents = discord.Intents.default()
        intents.message_content = True

        client = MyClient(self.agent, intents=intents)

        # Read token from environment variable
        token = os.getenv("ATHENA_DISCORD_BOT_ACCESS_TOKEN")
        if not token:
            raise ValueError(
                "ATHENA_DISCORD_BOT_ACCESS_TOKEN environment variable is not set"
            )

        client.run(token)
