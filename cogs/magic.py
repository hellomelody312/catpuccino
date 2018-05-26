import discord
import asyncio
from discord.ext import commands
from .utils.dataIO import dataIO
import random
import os
import math
import requests
import json



class Magic:
    """wwip"""

    def __init__(self, bot):
        self.bot = bot
        self.ownerid = "293041932542672896"
        self.stats_url = requests.get("https://api.jsonbin.io/b/5b081b310fb4d74cdf23e613/latest")
        self.magic_url = requests.get("https://api.jsonbin.io/b/5b080ed07a973f4ce5784717/latest")
        self.stats = self.stats_url.json()
        self.magic = self.magic_url.json()
        self.moves = self.magic['Moves']
        self.types = self.magic['Types']
        self.typelist = ["Normal","Fire","Fighting","Water","Flying","Grass","Poison","Electric","Ground","Psychic","Rock","Ice","Bug","Dragon","Ghost","Dark","Steel","Fairy"]
        self.errornotexist = "One or both of you do not have stats in the database! Set your stats using ``;stat`` first."

    def save_stats(self):
        requests.put("https://api.jsonbin.io/b/5b081b310fb4d74cdf23e613", json=self.stats)


    @commands.command(pass_context=True)
    async def attack(self, ctx, target:discord.Member=None):
        user= ctx.message.author
        if not target:
            target = self.bot.user
        if str(user.id) not in self.stats or str(target.id) not in self.stats:
            #self.stats[user.id] = {'hp': 1, 'atk': 1, 'defe': 1, 'spa': 1, 'spd': 1, 'spe': 1, 'type1':"Normal",'type2':"Normal"}
            #self.save_stats()
            await self.bot.say(self.errornotexist)
        else:
            embed=discord.Embed(title=":sparkles: **Magic Battle** :sparkles:", color=0xe90169)
            userhp = 100+round(self.stats[user.id]['hp']*round(random.uniform(1.5,2), 2))
            targethp = 100+round(self.stats[target.id]['hp']*round(random.uniform(1.5,2), 2))
            userremaininghp = userhp
            targetremaininghp = targethp
            if self.stats[user.id]['spe'] < self.stats[target.id]['spe']:
                embed.add_field(name=user.display_name + " tries to attack!", value="*"+target.display_name + " goes first due to higher Speed!*", inline=True)
                user, target = target, user
                userhp, targethp = targethp, userhp
                userremaininghp, targetremaininghp = targetremaininghp, userremaininghp
            while targetremaininghp > 0:
                msg2 = ""
                if self.stats[user.id]['class'] == "all":
                    moveclass = random.choice(["harrypotter","sakura","pokemon"])
                else:
                    moveclass = self.stats[user.id]['class']
                moveid = str(random.randint(1,len(self.moves[moveclass])))
                msg1 = "**"+user.display_name + "** used **"+ self.moves[moveclass][moveid]['name']+"** " + self.types[self.moves[moveclass][moveid]['type']]['icon']
                if self.moves[moveclass][moveid]['effect']:
                    msg1 = msg1 +" to "+ self.moves[moveclass][moveid]['effect'] + "!\n"
                else:
                    msg1 = msg1 +"!\n"
                power = self.moves[moveclass][moveid]['power']
                if self.moves[moveclass][moveid]['category'] == "Physical":
                    atk = self.stats[user.id]['atk']
                    defe = self.stats[target.id]['defe']
                else:
                    atk = self.stats[user.id]['spa']
                    defe = self.stats[target.id]['spd']
                if self.moves[moveclass][moveid]['type'] in self.types[self.stats[target.id]['type1']]['supereffective']:
                    mul = 2
                elif self.moves[moveclass][moveid]['type'] in self.types[self.stats[target.id]['type1']]['notveryeffective']:
                    mul = 0.5
                elif self.moves[moveclass][moveid]['type'] in self.types[self.stats[target.id]['type1']]['noteffective']:
                    mul = 0
                else:
                    mul = 1
                if self.moves[moveclass][moveid]['type'] in self.types[self.stats[target.id]['type2']]['supereffective']:
                    mul = mul * 2
                elif self.moves[moveclass][moveid]['type'] in self.types[self.stats[target.id]['type2']]['notveryeffective']:
                    mul = mul * 0.5
                elif self.moves[moveclass][moveid]['type'] in self.types[self.stats[target.id]['type2']]['noteffective']:
                    mul = 0
                if self.moves[moveclass][moveid]['type'] == self.stats[user.id]['type1'] or self.moves[moveclass][moveid]['type'] == self.stats[user.id]['type2']:
                    power = power * 1.5
                if mul >1:
                    msg2 = msg2 + ":small_red_triangle: It's super effective! \n"
                elif 0 <mul <1:
                    msg2 = msg2 + ":small_red_triangle_down: It's not very effective... \n"
                elif 0 == mul:
                    msg2 = msg2 + ":x: It had no effect!\n"
                if mul > 0:
                    msg2 = msg2 + target.display_name + " took "
                    rand = 0.01*random.randint(75,115)
                    dmg = round(math.floor(math.floor(60 * power * atk / defe) / 50) + 2 * mul * rand)
                    targetremaininghp = targetremaininghp - dmg
                    msg2 = msg2 + str(dmg) + " damage! (" + str(round(dmg / (targethp)*100)) + "\%) ("+str(targetremaininghp)+"/"+str(targethp)+" HP)\n"
                    if targetremaininghp <= 0:
                        msg2 = msg2  + "\n***" + target.display_name + " has fainted!***"
                embed.add_field(name=msg1.replace("{}",target.display_name), value=msg2, inline=False)
                if targetremaininghp > 0:
                    user, target = target, user
                    userhp, targethp = targethp, userhp
                    userremaininghp, targetremaininghp = targetremaininghp, userremaininghp
            prize = random.randint(10,100)
            embed.set_footer(text=user.display_name + " received " + str(prize) + " PMP for winning! Congratulations!")
            self.stats[user.id]['money'] = self.stats[user.id]['money'] + prize
            self.stats[user.id]['win'] = self.stats[user.id]['win'] + 1
            self.stats[target.id]['lose'] = self.stats[target.id]['lose'] + 1
            self.save_stats()
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def pmp(self, ctx, target:discord.Member=None):
        if target:
            user = target
        else:
            user = ctx.message.author
        if str(user.id) not in self.stats:
            await self.bot.say(user.display_name + "\'s stats were not found.")
        else:
            await self.bot.say(user.display_name + " has "+ str(self.stats[user.id]['money']) +" PMP.")

    @commands.command(pass_context=True)
    async def givepmp(self, ctx, target:discord.Member=None, amount:int=0):
        user= ctx.message.author
        if target:
            if str(user.id) not in self.stats or str(target.id) not in self.stats:
                await self.bot.say(self.errornotexist)
            else:
                self.stats[user.id]['money']=self.stats[user.id]['money'] - amount
                self.stats[target.id]['money']=self.stats[target.id]['money'] + amount
                self.save_stats()
                await self.bot.say(embed=discord.Embed(title="Gave " + str(amount) + " PMP to " + target.display_name + ".",description="You now have " + str(self.stats[user.id]['money']) + " PMP.\n" + target.display_name + " now has " + str(self.stats[target.id]['money'])
                                                 + " PMP.", color=0xe90169))
        else:
            await self.bot.say("No one to give.")

    @commands.command(pass_context=True)
    async def setpmp(self, ctx, target:discord.Member=None, amount:int=0):
        user= ctx.message.author
        if user.id != self.ownerid:
            await self.bot.say("Not authorized to do this.")
        else:
            if target:
                if str(user.id) not in self.stats or str(target.id) not in self.stats:
                    await self.bot.say(self.errornotexist)
                else:
                    self.stats[target.id]['money']= amount
                    self.save_stats()
                    await self.bot.say(embed=discord.Embed(title="Set PMP",description= target.display_name + " now has " + str(self.stats[target.id]['money']) + " PMP.", color=0xe90169))
            else:
                await self.bot.say("No one to give.")

    @commands.group(pass_context=True)
    async def stat(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("``Magical duel commands: \n;stat random OR set hp atk def spA spD speed to set your stats.\n;settype type1 type2 to set your types.\n;stat show to show yours or someone else's stats.\nType ;attack @user to try attacking someone.``")


    @stat.command(pass_context=True)
    #async def _set(self, context, stat, num:integer = None):
    async def show(self, ctx, target:discord.Member =None):
        if target:
            user = target
        else:
            user= ctx.message.author
        if str(user.id) in self.stats:
            await self.output_stats(ctx,user)
        else:
            await self.bot.say(user.display_name + "\'s stats were not found!")

    @stat.command(pass_context=True)
    async def win(self, ctx, target:discord.Member =None):
        if target:
            user = target
        else:
            user= ctx.message.author
        if str(user.id) in self.stats:
            await self.bot.say("Wins: " + str(self.stats[user.id]['win']) + ", losses: " + str(self.stats[user.id]['lose']))
        else:
            await self.bot.say(user.display_name + "\'s stats were not found!")

    @stat.command(pass_context=True)
    async def reset(self,ctx):
        user = ctx.message.author
        self.stats[user.id] = {'hp': 60, 'atk': 60, 'defe': 60, 'spa': 60, 'spd': 60, 'spe': 60, 'class': "all", 'bst': 500, 'money': 0, 'item': 0,
                               'type1':"Normal",'type2':"Normal",'win':0,'lose':0}
        self.save_stats()
        await self.bot.say(user.display_name + "\'s stats were set all to 60 and your types to Normal.")

    @stat.command(pass_context=True)
    async def random(self, ctx, target:discord.Member=None):
        if target:
            user = target
        else:
            user = ctx.message.author
        if user.id not in self.stats:
             self.stats[user.id] = {'hp': 1, 'atk': 1, 'defe': 1, 'spa': 1, 'spd': 1, 'spe': 1, 'class': "all", 'bst': 450, 'money': 0, 'item': 0,
                                    'type1':"Normal",'type2':"Normal",'win':0,'lose':0}
        buff = ((self.stats[user.id]['bst']/50) - 9) * 10
        while True:
            self.stats[user.id]['hp'] = random.randint(65+buff,120+buff)
            self.stats[user.id]['atk'] = random.randint(50+buff,120+buff)
            self.stats[user.id]['defe'] = random.randint(50+buff,120+buff)
            self.stats[user.id]['spa'] = random.randint(50+buff,120+buff)
            self.stats[user.id]['spd'] = random.randint(50+buff,120+buff)
            self.stats[user.id]['spe'] = random.randint(50+buff,120+buff)
            bst0 = self.stats[user.id]['hp'] + self.stats[user.id]['atk'] +self.stats[user.id]['defe'] +self.stats[user.id]['spa']+self.stats[user.id]['spd'] +self.stats[user.id]['spe']
            if self.stats[user.id]['bst'] >= bst0:
                break
        self.stats[user.id]['class'] = "all"
        self.stats[user.id]['type1'] = random.choice(self.typelist)
        self.stats[user.id]['type2'] = random.choice(self.typelist)
        self.save_stats()
        await self.output_stats(ctx,user)


    @stat.command(pass_context=True)
    async def set(self, ctx, hp:int=1, atk:int=1, defe:int=1, spa:int=1, spd:int=1, spe:int=1, target:discord.Member=None):
        if target and user.id == "293041932542672896":
            user = target
        else:
            user= ctx.message.author
        if user.id not in self.stats:
            self.stats[user.id] = {'hp': 1, 'atk': 1, 'defe': 1, 'spa': 1, 'spd': 1, 'spe': 1,'class': "all", 'bst': 400, 'money': 0, 'item': 0, 'type1':"Normal",'type2':"Normal"}
            self.save_stats()
        if atk + defe +spa +spd +spe +hp >550:
            await self.bot.say("Too OP! BST should be no more than 550.")
        else:
            name = user.display_name
            self.stats[user.id]['hp'] = hp
            self.stats[user.id]['atk'] = atk
            self.stats[user.id]['defe'] = defe
            self.stats[user.id]['spa'] = spa
            self.stats[user.id]['spd'] = spd
            self.stats[user.id]['spe'] = spe
            self.save_stats()
            await self.output_stats(ctx,user)


    async def output_stats(self, ctx, user):
        embed=discord.Embed(title=user.display_name + "\'s stats")
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Class", value=self.stats[user.id]['class'], inline=True)
        embed.add_field(name="HP", value=str(self.stats[user.id]['hp']) + " (in battle aprox. "+ str(100+ round(self.stats[user.id]['hp']*1.75)) +")", inline=True)
        embed.add_field(name="Physical Attack", value=self.stats[user.id]['atk'], inline=True)
        embed.add_field(name="Physcial Defense", value=self.stats[user.id]['defe'], inline=True)
        embed.add_field(name="Special Attack", value=self.stats[user.id]['spa'], inline=True)
        embed.add_field(name="Special Defense", value=self.stats[user.id]['spd'], inline=True)
        embed.add_field(name="Speed", value=self.stats[user.id]['spe'], inline=True)
        if self.stats[user.id]['type1'] != self.stats[user.id]['type2']:
            embed.add_field(name="Types", value=self.stats[user.id]['type1'] + ", " + self.stats[user.id]['type2'], inline=True)
        else:
            embed.add_field(name="Types", value=self.stats[user.id]['type1'], inline=True)
        #embed.set_footer(text=".")
        await self.bot.say(content=user.display_name + "\'s stats are:", embed=embed)

    @commands.command(pass_context=True)
    async def settype(self, ctx, type1:str=None, type2:str=None):
        user= ctx.message.author
        if not type1:
            await self.bot.say("No type specified.")
        elif not type2:
            type2 = type1
        if type1[0].upper() + type1[1:] not in self.types or type2[0].upper() + type2[1:] not in self.types:
            await self.bot.say("Invalid type specified.")
        else:
            self.stats[user.id]['type1'] =type1[0].upper() + type1[1:]
            self.stats[user.id]['type2'] =type2[0].upper() + type2[1:]
            self.save_stats()
            if type2 != type1:
                msg = user.display_name + "\'s types have been set to " + self.stats[user.id]['type1'] +" and " + self.stats[user.id]['type2'] + "."
            else:
                msg = user.display_name + "\'s type has been set to " + self.stats[user.id]['type1']+ "."
            await self.bot.say(msg)

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
