"""Main entry point for the Athena personal assistant application."""

import asyncio
from src.agent.agent import Athena
from src.database.db import Database
from src.discord_bot.bot import DiscordBot


async def setup():
    """
    The main function.
    """
    db = Database()
    agent = Athena(db)
    bot = DiscordBot(agent, db=db, periodic_channel_name="testing")
    return bot


def run():
    """
    The main entry point for the application.
    """
    bot = asyncio.run(setup())
    bot.run()


if __name__ == "__main__":
    run()
