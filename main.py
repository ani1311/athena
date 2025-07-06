"""Main entry point for the Athena personal assistant application."""

import asyncio
import src
from src.agent.agent import Athena
import src.database
from src.database.db import Database, Transactor
import src.database.models
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
    # transactor = Transactor(bot.agent.db.get_session())
    # goal = src.database.models.Goal(description="Test Goal")
    # transactor.add(goal)

    # goals = transactor.get_all(src.database.models.Goal)
    # for g in goals:
    #     print(f"Goal in the database: {g.description}")
    bot.run()


if __name__ == "__main__":
    run()
