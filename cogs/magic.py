import discord
import asyncio
from discord.ext import commands
from .utils.dataIO import dataIO
import random
import os
import math





class Magic:
    """wwip"""

    def __init__(self, bot):
        self.bot = bot
        self.statspath = "data/magic/stats.json"
        self.stats = dataIO.load_json(self.statspath)
        self.magic = dataIO.load_json("data/magic/magic.json")
        self.moves = self.magic['Moves']
        self.types = self.magic['Types']
        self.typelist = ["Normal","Fire","Fighting","Water","Flying","Grass","Poison","Electric","Ground","Psychic","Rock","Ice","Bug","Dragon","Ghost","Dark","Steel","Fairy"]

    def save_stats(self):
        dataIO.save_json(self.statspath, self.stats)
        dataIO.is_valid_json("data/magic/stats.json")

    @commands.command(pass_context=True)
    async def attack(self, ctx, target:discord.Member=None):
        user= ctx.message.author
        if not target:
            target = user
        if user.id not in self.stats or target.id not in self.stats:
            #self.stats[user.id] = {'hp': 1, 'atk': 1, 'defe': 1, 'spa': 1, 'spd': 1, 'spe': 1, 'type1':"Normal",'type2':"Normal"}
            #self.save_stats()
            await self.bot.say("One or both of you do not have stats in the database! Set your stats using ``;magic setstats`` first.")
        else:
            moveid = str(random.randint(1,16))
            msg = user.name + " used "+ self.moves[moveid]['name'] +" on " + target.name + "! "
            if self.moves[moveid]['hits'] == 0:
                msg = msg + user.name + self.moves[moveid]['effect'] + "It's an OHKO! " + target.name + " has fainted!"
                await self.bot.say(msg)
            else:
                power = self.moves[moveid]['power']
                if self.moves[moveid]['category'] == "Physical":
                    atk = self.stats[user.id]['atk']
                    defe = self.stats[target.id]['defe']
                else:
                    atk = self.stats[user.id]['spa']
                    defe = self.stats[target.id]['spd']
                if self.moves[moveid]['type'] in self.types[self.stats[target.id]['type1']]['supereffective']:
                    mul = 2
                elif self.moves[moveid]['type'] in self.types[self.stats[target.id]['type1']]['notveryeffective']:
                    mul = 0.5
                elif self.moves[moveid]['type'] in self.types[self.stats[target.id]['type1']]['noteffective']:
                    mul = 0
                else:
                    mul = 1
                if self.moves[moveid]['type'] in self.types[self.stats[target.id]['type2']]['supereffective']:
                    mul = mul * 2
                elif self.moves[moveid]['type'] in self.types[self.stats[target.id]['type2']]['notveryeffective']:
                    mul = mul * 0.5
                elif self.moves[moveid]['type'] in self.types[self.stats[target.id]['type2']]['noteffective']:
                    mul = 0
                if self.moves[moveid]['type'] == self.stats[user.id]['type1'] or self.moves[moveid]['type'] == self.stats[user.id]['type2']:
                    power = power * 1.5
                if mul >1:
                    msg = msg + "It's super effective! \n"
                elif 0 <mul <1:
                    msg = msg + "It's not very effective... \n"
                if self.moves[moveid]['effect']:
                    msg = msg + user.name + self.moves[moveid]['effect']
                totaldmg = 0
                for x in range(0, self.moves[moveid]['hits']):
                    rand = random.randint(85,100)
                    dmg = round(math.floor(math.floor(100 * power * atk / defe) / 50) + 2 * mul * (0.01*rand))
                    totaldmg = totaldmg + dmg
                    msg = msg + "It does " + str(dmg) + " damage. (" + str(round(dmg / (self.stats[target.id]['hp']*3)*100)) + "\% of " + target.name + "\'s health)\n"
                    if self.stats[target.id]['hp']*3 <= totaldmg:
                        break
                if totaldmg >= self.stats[target.id]['hp']*3:
                    msg = msg + " " + target.name + " has fainted!"
                await self.bot.say(msg)

    @commands.group(pass_context=True)
    async def stat(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("Magic commands: \n;stat set random OR hp atk def spA spD speed to set your stats.\n;set type to set your types.\n;stat show to show yours or someone else's stats.\nType ;attack @user to try attacking someone.")


    @stat.command(pass_context=True)
    #async def _set(self, context, stat, num:integer = None):
    async def show(self, ctx, target:discord.Member =None):
        if target:
            user = target
        else:
            user= ctx.message.author
        if user.id in self.stats:
            await self.output_stats(ctx,user)
        else:
            self.stats[user.id] = {'hp': 1, 'atk': 1, 'defe': 1, 'spa': 1, 'spd': 1, 'spe': 1, 'type1':"Normal",'type2':"Normal"}
            self.save_stats()
            await self.bot.say(user.name + "\'s stats were not found and have been set all to 1.")

    @stat.command(pass_context=True)
    async def reset(self,ctx):
        user = ctx.message.author
        self.stats[user.id] = {'hp': 1, 'atk': 1, 'defe': 1, 'spa': 1, 'spd': 1, 'spe': 1, 'type1':"Normal",'type2':"Normal"}
        self.save_stats()
        await self.bot.say(user.name + "\'s stats were set all to 1 and your types to Normal.")

    @stat.command(pass_context=True)
    async def random(self, ctx):
        user = ctx.message.author
        self.stats[user.id] = {'hp': 1, 'atk': 1, 'defe': 1, 'spa': 1, 'spd': 1, 'spe': 1, 'type1':"Normal",'type2':"Normal"}
        self.stats[user.id]['hp'] = random.randint(60,120)
        self.stats[user.id]['atk'] = random.randint(60,120)
        self.stats[user.id]['defe'] = random.randint(60,120)
        self.stats[user.id]['spa'] = random.randint(60,120)
        self.stats[user.id]['spd'] = random.randint(60,120)
        self.stats[user.id]['spe'] = random.randint(60,120)
        self.stats[user.id]['type1'] = random.choice(self.typelist)
        self.stats[user.id]['type2'] = random.choice(self.typelist)
        self.save_stats()
        self.bot.say(user.name + "\'s stats and types were randomized!")
        await self.output_stats(ctx,user)

    @stat.command(pass_context=True)
    async def set(self, ctx, hp:int=1, atk:int=1, defe:int=1, spa:int=1, spd:int=1, spe:int=1, target:discord.Member=None):
        if target:
            user = target
        else:
            user= ctx.message.author
        if user.id not in self.stats:
            self.stats[user.id] = {'hp': 1, 'atk': 1, 'defe': 1, 'spa': 1, 'spd': 1, 'spe': 1, 'type1':"Normal",'type2':"Normal"}
            self.save_stats()
        if atk + defe +spa +spd +spe +hp >500:
            await self.bot.say("Too OP! BST should be no more than 500.")
        else:
            name = user.name
            self.stats[user.id]['hp'] = hp
            self.stats[user.id]['atk'] = atk
            self.stats[user.id]['defe'] = defe
            self.stats[user.id]['spa'] = spa
            self.stats[user.id]['spd'] = spd
            self.stats[user.id]['spe'] = spe
            self.save_stats()
            await self.output_stats(ctx,user)


    async def output_stats(self, ctx, user):
        embed=discord.Embed(title=user.name + "\'s stats")
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="HP", value=self.stats[user.id]['hp'], inline=True)
        embed.add_field(name="Physical Attack", value=self.stats[user.id]['atk'], inline=True)
        embed.add_field(name="Physcial Defense", value=self.stats[user.id]['defe'], inline=True)
        embed.add_field(name="Special Attack", value=self.stats[user.id]['spa'], inline=True)
        embed.add_field(name="Special Defense", value=self.stats[user.id]['spd'], inline=True)
        embed.add_field(name="Speed", value=self.stats[user.id]['spe'], inline=True)
        embed.add_field(name="Types", value=self.stats[user.id]['type1'] + ", " + self.stats[user.id]['type2'], inline=True)
        embed.set_footer(text=".")
        await self.bot.say(content=user.name + "\'s stats are:", embed=embed)

    @commands.command(pass_context=True)
    async def settype(self, ctx, type1:str="Normal", type2:str="Normal"):
        user= ctx.message.author
        if type1 not in self.types or type2 not in self.types:
            await self.bot.say("Invalid type specified.")
        else:
            self.stats[user.id]['type1'] =type1
            self.stats[user.id]['type2'] =type2
            self.save_stats()
            await self.bot.say(user.name + "\'s types have been set to: " + self.stats[user.id]['type1'] +" and " + self.stats[user.id]['type2'] + ".")

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
