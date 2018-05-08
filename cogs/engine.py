from discord.ext import commands
from random import randint
from random import choice

class Engine:
    """leavin you in the dust!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def vroom(self, ctx):
        """You don't need no instruction manual to be free!!"""
        await self.bot.say("VROOM VROOM!")

    @commands.command(pass_context=True, no_pm=True, name='rate')
    async def rate(self, ctx, *, rate:str = None):
        """Đánh giá thứ gì đó theo thang điểm 100."""
        if rate != None:
            await self.bot.say(rate + ": " + str(randint(0,101)) + "/100.")
        else:
            if ctx.message.author.nick:
                nem = ctx.message.author.nick
            else:
                nem = ctx.message.author.name
            await self.bot.say(nem + ": " + str(randint(0,101)) + "/100.")


def setup(bot):
    bot.add_cog(Engine(bot))
