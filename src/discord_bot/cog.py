import discord
from discord.ext import tasks, commands

class PeriodicMessageCog(commands.Cog):
    def __init__(self, bot, channel_name):
        self.bot = bot
        self.channel_name = channel_name
        self.channel = None
        if self.channel_name:
            self.periodic_message_task.start()

    def cog_unload(self):
        self.periodic_message_task.cancel()

    @tasks.loop(seconds=10)
    async def periodic_message_task(self):
        if self.channel:
            message = "🤖 Periodic check-in! How can I help you today?"
            await self.channel.send(message)
            print(f"Sent periodic message to channel {self.channel.name}")

    @periodic_message_task.before_loop
    async def before_periodic_message_task(self):
        await self.bot.wait_until_ready()
        if self.channel_name:
            for channel in self.bot.get_all_channels():
                if channel.name == self.channel_name:
                    self.channel = channel
                    print(f"Periodic message channel set to {channel.name} (ID: {channel.id})")
                    return
            print(f"Channel '{self.channel_name}' not found for periodic messages.")
