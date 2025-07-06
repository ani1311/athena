"""
Cog for sending periodic messages in a Discord channel.
"""

from discord.ext import tasks, commands


class PeriodicMessageCog(commands.Cog):
    """
    A cog that sends periodic messages to a specified channel.
    """

    def __init__(self, bot, channel_name):
        self.bot = bot
        self.channel_name = channel_name
        self.channel = None
        if self.channel_name:
            self.periodic_message_task.start()

    async def cog_unload(self):
        self.periodic_message_task.cancel()

    @tasks.loop(minutes=10)
    async def periodic_message_task(self):
        """
        Sends a periodic message to the specified channel every 10 seconds.
        """
        if self.channel:
            message = "🤖 Periodic check-in! How can I help you today?"
            await self.channel.send(message)
            print(f"Sent periodic message to channel {self.channel.name}")

    @periodic_message_task.before_loop
    async def before_periodic_message_task(self):
        """
        Waits until the bot is ready and sets the channel for periodic messages.
        k"""
        await self.bot.wait_until_ready()
        if self.channel_name:
            for channel in self.bot.get_all_channels():
                if channel.name == self.channel_name:
                    self.channel = channel
                    print(
                        f"Periodic message channel set to {channel.name} (ID: {channel.id})"
                    )
                    return
            print(f"Channel '{self.channel_name}' not found for periodic messages.")
