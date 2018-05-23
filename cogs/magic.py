import discord
import asyncio
from discord.ext import commands
from .utils.dataIO import dataIO
import random
import os






class Magic:
    """wwip"""

    def __init__(self, bot):
        self.bot = bot
        self.statspath = "data/magic/stats.json"
        self.stats = dataIO.load_json(self.statspath)

    def save_stats(self):
        dataIO.save_json(self.statspath, self.stats)
        dataIO.is_valid_json("data/magic/stats.json")

    @commands.group(pass_context=True)
    async def magic(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('bla bla')

    @magic.command(pass_context=True)
    #async def _set(self, context, stat, num:integer = None):
    async def showstats(self, ctx, target:discord.Member =None):
        if target:
            user = target
        else:
            user= ctx.message.author
        if user.id in self.stats:
            await self.bot.say(user.name + '\'s stats are: ' + str(self.stats[user.id]))
        else:
            self.stats[user.id] = {'hp': 0, 'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0}
            self.save_stats()
            await self.bot.say(user.name + '\'s stats are: ' + str(self.stats[user.id]))

    @magic.command(pass_context=True)
    async def setstats(self, ctx, hp:int=0, atk:int=0, defe:int=0, spa:int=0, spd:int=0, spe:int=0):
        user= ctx.message.author
        self.stats[user.id] = {'hp': hp, 'atk': atk, 'def': defe, 'spa': spa, 'spd': spd, 'spe': spe}
        self.save_stats()
        await self.bot.say(user.name + '\'s stats are: ' + str(self.stats[user.id]))

def check_folders():
    folders = ("data", "data/magic/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    """Moves the file from cogs to the data directory. Important -> Also changes the name to insults.json"""
    insults = {"You ugly as hell damn. Probably why most of your friends are online right?"}

    if not os.path.isfile("data/magic/stats.json"):
        if os.path.isfile("cogs/put_in_cogs_folder.json"):
            print("moving default insults.json...")
            os.rename("cogs/put_in_cogs_folder.json", "data/insult/insults.json")
        else:
            print("creating default insults.json...")
            fileIO("data/insult/insults.json", "save", insults)


def setup(bot):
    check_folders()
    check_files()
    n = Magic(bot)
    bot.add_cog(n)
