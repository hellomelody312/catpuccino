import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from random import choice as randchoice
import os


class Insult:

    """Airenkun's Insult Cog"""
    def __init__(self, bot):
        self.bot = bot
        self.insults = fileIO("data/insult/insults.json","load")
        self.khens = fileIO("data/insult/insults2.json","load")

    @commands.command(pass_context=True, no_pm=True)
    async def insult(self, ctx, user : discord.Member=None):
        """Insults the user"""

        msg = ' '
        if user != None:
            if user.id == self.bot.user.id:
                user = ctx.message.author
                nem = str(user.nick)
                if nem == "None":
                   nem = str(user.name)
                msg = ", mày đần tới mức nghĩ chụy ngu mà tự chửi mình hả? Xem lại mình đi cái thứ não bò!"
                await self.bot.say(nem + msg)
            elif user.id == "293041932542672896":
                 msg = " Tao không chửi anh Mil yêu đâu ahihi"
                 await self.bot.say(msg)
            else:
                nem = str(user.nick)
                if nem == "None":
                   nem = str(user.name)
                await self.bot.say(nem + "," + msg + randchoice(self.insults))
        else:
            await self.bot.say(str(ctx.message.author.mention) + "," + msg + randchoice(self.insults))

    @commands.command(pass_context=True, no_pm=True)
    async def khen(self, ctx, user : discord.Member=None):
        """Khen ai đó"""

        msg = ' '
        if user != None:
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = "Khổ ghê, tui biết tui đẹp mà."
                await self.bot.say(msg)
            elif user.id == "293041932542672896":
                 msg = "Mil tuyệt vời nhứt quả đất luôn."
                 await self.bot.say(msg)
            else:
                nem = str(user.nick)
                if nem == "None":
                   nem = str(user.name)
                await self.bot.say(nem + "," + msg + randchoice(self.khens))
        else:
            await self.bot.say(ctx.message.author.mention + msg + randchoice(self.khens))

def check_folders():
    folders = ("data", "data/insult/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    """Moves the file from cogs to the data directory. Important -> Also changes the name to insults.json"""
    insults = {"You ugly as hell damn. Probably why most of your friends are online right?"}

    if not os.path.isfile("data/insult/insults.json"):
        if os.path.isfile("cogs/put_in_cogs_folder.json"):
            print("moving default insults.json...")
            os.rename("cogs/put_in_cogs_folder.json", "data/insult/insults.json")
        else:
            print("creating default insults.json...")
            fileIO("data/insult/insults.json", "save", insults)


def setup(bot):
    check_folders()
    check_files()
    n = Insult(bot)
    bot.add_cog(n)
