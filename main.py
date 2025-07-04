# main.py

from src.agent.agent import Agent
from src.database.db import Database
from src.discord_bot.bot import DiscordBot


def main():
    """
    The main function.
    """
    agent = Agent()
    db = Database()
    bot = DiscordBot(agent, db)
    bot.run()


if __name__ == "__main__":
    main()
