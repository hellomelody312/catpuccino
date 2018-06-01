import discord
import asyncio
from discord.ext import commands
#from .utils.dataIO import dataIO
import random
import os
import math
import requests
import json
#import schedule
import time

class Pets:
    """wwip"""

    def __init__(self, bot):
        self.bot = bot
        self.botownerid = "293041932542672896"
        self.owner_stats_url = requests.get("https://api.jsonbin.io/b/5b081b310fb4d74cdf23e613/latest")
        self.moves_url = requests.get("https://api.jsonbin.io/b/5b080ed07a973f4ce5784717/latest")
        self.pet_stats_url = requests.get("https://api.jsonbin.io/b/5b112f31c83f6d4cc734a41d/latest")
        self.owner_stats = self.owner_stats_url.json()
        #self.moves = self.moves_url.json()
        self.pet_stats = self.pet_stats_url.json()
        self.classes = ["all","pokemon","sakura","harrypotter","ffxv","sailormoon"]
        self.typelist = ["Normal","Fire","Fighting","Water","Flying","Grass","Poison","Electric","Ground","Psychic","Rock","Ice","Bug","Dragon","Ghost","Dark","Steel","Fairy"]

    def save_pet_stats(self):
        requests.put("https://api.jsonbin.io/b/5b112f31c83f6d4cc734a41d", json=self.pet_stats)

    def save_owner_stats(self):
        requests.put("https://api.jsonbin.io/b/5b081b310fb4d74cdf23e613", json=self.owner_stats)

###background tasks
    #client = discord.Client()

    #async def bgloop():
    #    await client.wait_until_ready()
    #    while not client.is_closed:
    #        self.reduce_hunger()
    #        await asyncio.sleep(3600) # task runs every 60 seconds

    #client.loop.create_task(bgloop())
    #client.run(self.bot_settings["TOKEN"])


    def reduce_hunger(self):
        for userid in self.pet_stats:
            for petid in self.pet_stats[userid]:
                self.pet_stats[userid][petid]['hunger'] -= 10
                self.pet_stats[userid][petid]['happiness'] -= 1
        self.save_pet_stats()

    @commands.group(pass_context=True)
    async def pet(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("``Pet commands: \n;pet create to create your pet.\n;pet show to display stats.``")

    @pet.command(pass_context=True)
    async def show(self, ctx, petid:int=None):
        user = ctx.message.author
        if petid == None:
            petid = self.pet_stats[user.id]['current_pet']
        await self.output_pet_stats(user,petid)

    @pet.command(pass_context=True)
    async def feed(self, ctx, item=None):
        user = ctx.message.author
        petid = self.pet_stats[user.id]['current_pet']
        if item == None:
            await self.bot.say(self.pet_stats[user.id][petid]['nickname'] + "'s hunger is currently " + self.pet_stats[user.id][petid]['hunger']+". Would you like to feed it a biscuit for 20PMP? (30s) (next time type ;pet feed biscuit to skip this message.)")
            answer = await self.bot.wait_for_message(timeout=30, author=ctx.message.author)
            if answer is None:
                await self.bot.say('Purchase cancelled due to timeout.')
                return
            elif "yes" not in answer.content.lower():
                await self.bot.say('Well? Okay then.')
                return
            else:
                await self.feedbiscuit(user,petid)
        else:
            await self.feedbiscuit(user,petid)

    async def feedbiscuit(user,petid):
        self.pet_stats[user.id][petid]['hunger'] += 10
        self.pet_stats[user.id][petid]['happiness'] += 1
        self.owner_stats[user.id]['money'] -= 20
        self.save_pet_stats()
        self.save_owner_stats()
        await self.bot.say(user.display_name + " fed a biscuit to " + self.pet_stats[user.id][petid]['nickname'] +" for 20 PMP. Its happiness and hunger increased!\n"+self.pet_stats[user.id][petid]['nickname'] +"'s hunger is now" +self.pet_stats[user.id][petid]['hunger'] + "and its happiness is " + self.pet_stats[userid][petid]['happiness'] +".")


    @pet.command(pass_context=True)
    async def play(self, ctx,*, action:str=None):
        user = ctx.message.author
        petid = self.pet_stats[user.id]['current_pet']
        if action == None:
            msg0 = user.display_name + " played with " + self.pet_stats[user.id][petid]['nickname'] +"!\n"
            action = " played with " + user.display_name
        else:
            msg0 = user.display_name + " went to "+action+" with " + self.pet_stats[user.id][petid]['nickname'] +"!\n"
        embed=discord.Embed(title=msg0,color=user.color)
        embed.set_thumbnail(url=self.pet_stats[user.id][petid]['image'])
        reaction = random.choice(['superhappy','veryhappy','happy','normal','return','unhappy','veryunhappy'])
        if reaction == "superhappy":
            msg1 = self.pet_stats[user.id][petid]['nickname'] + " jumped at " +  user.display_name + " in complete joy!!"
            msg2 = "Its happiness increased by 10! " +user.display_name + " got 100 PMP!"
            self.owner_stats[user.id]['money'] += 100
            self.pet_stats[user.id][petid]['happiness'] += 20
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "veryhappy":
            pet_action = random.choice(['really liked it!','let out a big grin at {}!','appears very content!','\'s face lit up!'])
            msg1 =self.pet_stats[user.id][petid]['nickname'] +" " +  pet_action.format(user.display_name)
            msg2 = "Its happiness increased by 5! " + user.display_name + " got 30 PMP!"
            self.owner_stats[user.id]['money'] += 30
            self.pet_stats[user.id][petid]['happiness'] += 5
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "happy":
            pet_action = random.choice(['liked it!','smiled back at {}!','appears quite content.','lets out a small cry!'])
            msg1 =self.pet_stats[user.id][petid]['nickname'] +" "+  pet_action.format(user.display_name)
            msg2 = "Its happiness increased by 2! " + user.display_name + " got 10 PMP!"
            self.owner_stats[user.id]['money'] += 10
            self.pet_stats[user.id][petid]['happiness'] += 2
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "normal":
            pet_action = random.choice(['felt meh.','looked back at {} for 1 second in disinterest and turned away.','ignored {}.','had no reaction.'])
            msg1 =self.pet_stats[user.id][petid]['nickname'] +" " +  pet_action.format(user.display_name)
            msg2 = "" + user.display_name + " got 1 PMP."
            self.owner_stats[user.id]['money'] += 1
            #self.pet_stats[user.id][petid]['happiness'] += 2
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "unhappy":
            pet_action = random.choice(['did not like it.','turned away from {}.','appears quite distressed.','said no.','became sad for some reason.','sighed.'])
            msg1 =self.pet_stats[user.id][petid]['nickname'] + " "+ pet_action.format(user.display_name)
            msg2 =  "Its happiness decreased by 1!"
            #self.owner_stats[user.id]['money'] += 10
            self.pet_stats[user.id][petid]['happiness'] -= 1
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "veryunhappy":
            pet_action = random.choice(['got angry at {}!','frowned heavily at {}!','appeared very sad!','cried out in distress!'])
            msg1 =self.pet_stats[user.id][petid]['nickname'] + " " +  pet_action.format(user.display_name)
            msg2 = "Its happiness decreased by 5!"
            self.pet_stats[user.id][petid]['happiness'] -= 5
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "return":
            msg1 =self.pet_stats[user.id][petid]['nickname'] +  " decided to " + action + " with " + user.display_name + " back!"
            msg2 =  user.display_name + " got 50 PMP!"
            self.owner_stats[user.id]['money'] += 50
            #self.pet_stats[user.id][petid]['happiness'] -= 1
            embed.add_field(name=msg1,value=msg2,inline=False)
        await self.bot.say(embed=embed)
        self.pet_stats[user.id][petid]['exp'] += 10
        self.save_pet_stats()
        self.save_owner_stats()

    @pet.command(pass_context=True)
    async def select(self, ctx, number:int=None):
        user = ctx.message.author
        if number:
            if number > len(self.pet_stats[user.id])-1:
                await self.bot.say("No such pet.")
            else:
                self.pet_stats[user.id]['current_pet'] = str(number)
                await self.bot.say("Your current pet is " + self.pet_stats[user.id][str(number)]['nickname']+ ".")
        else:
            await self.bot.say("No number specified. You currently have " +str((len(self.pet_stats[user.id])-1))+ " pets.")


    @pet.command(pass_context=True)
    #@commands.cooldown(1, 36600, commands.BucketType.user)
    async def create(self, ctx):
        user = ctx.message.author
        if user.id not in self.pet_stats:
            self.pet_stats[user.id] = {"1": {"battle_stats": {"item": 0,"type1": "Fire","defe": 1,"spe": 1,"type2": "Ghost","win": 1,"hp": 1,"class": "all","atk": 1,
                                                              "buff": 0,"spd": 1,"lose": 0,"spa": 1,"bst": 400},"level": 1,"exp": 0,"hunger": 50,"happiness": 1,
                                                              "image": "","image_big": "","nickname": "","owner_name": ""},"current_pet":"1"}
            pet_current = "1"
        else:
            pet_current = str(len(self.pet_stats[user.id]))
            self.pet_stats[user.id][str(pet_current)] = {"battle_stats": {"item": 0,"type1": "Fire","defe": 1,"spe": 1,"type2": "Ghost","win": 1,"hp": 1,"class": "all","atk": 1,
                                                              "buff": 0,"spd": 1,"lose": 0,"spa": 1,"bst": 400},"level": 1,"exp": 0,"hunger": 100,"happiness": 1,
                                                              "image": "","image_big": "","nickname": "","owner_name": ""}
        await self.bot.say("Welcome to create-a-pet! You're creating your pet no. " + str(pet_current) + ". Type ``exit`` to quit anytime.\nFirst, let's give your pet a nickname:")
        nick = await self.bot.wait_for_message(author=ctx.message.author)
        if nick.content.lower() == 'exit':
            await self.bot.say("Pet creation cancelled.")
            return
        else:
            self.pet_stats[user.id][pet_current]['nickname'] = nick.content
        await self.bot.say("Your pet's name is **"+ self.pet_stats[user.id][pet_current]['nickname'] +"**.\nNext, let's have a thumbnail image for your pet! Give an url to a direct link of your pet's thumbnail.")
        imgurl = await self.bot.wait_for_message(author=ctx.message.author)
        imgg = str(imgurl.content)
        if imgg.lower() == 'exit':
            await self.bot.say("Pet creation cancelled.")
            return
        #while imgg[0:3] != 'http':
            #await self.bot.say("Not an url! Try again.")
            #imgurl = await self.bot.wait_for_message(author=ctx.message.author)
            #imgg = str(imgurl.content)
        self.pet_stats[user.id][pet_current]['image'] = imgg
        await self.bot.say("Next, set the types for your pet. It can be any 1 or 2 types from the Pokemon games. ex: fire fighting. Type ``random`` to randomly set types.")
        types = await self.bot.wait_for_message(author=ctx.message.author)
        if types.content == 'exit':
            await self.bot.say("Pet creation cancelled.")
            return
        elif types.content == 'random':
            self.pet_stats[user.id][pet_current]['battle_stats']['type1'] = random.choice(self.typelist)
            self.pet_stats[user.id][pet_current]['battle_stats']['type2'] = random.choice(self.typelist)
            type1 = self.pet_stats[user.id][pet_current]['battle_stats']['type1']
            type2 = self.pet_stats[user.id][pet_current]['battle_stats']['type2']
        else:
            while len(types.content.split()) > 2:
                await self.bot.say("Too many types! Try again.")
                types = await self.bot.wait_for_message(author=ctx.message.author)
            types_list = types.content.split()
            type1 = types_list[0][0].upper() + types_list[0][1:]
            if len(types_list) < 2:
                type2 = type1
            else:
                type2 = types_list[1][0].upper() + types_list[1][1:]
            for x in [type1,type2]:
                while x not in self.typelist:
                    await self.bot.say("Invalid type! Try again.")
                    types = await self.bot.wait_for_message(author=ctx.message.author)
                    types_list = types.content.split()
                    type1 = types_list[0][0].upper() + types_list[0][1:]
                    if len(types_list) < 2:
                        type2 = type1
                    else:
                        type2 = types_list[1][0].upper() + types_list[1][1:]
            self.pet_stats[user.id][pet_current]['battle_stats']['type1'] = type1
            self.pet_stats[user.id][pet_current]['battle_stats']['type2'] = type2
        await self.bot.say("You're about to create **" + self.pet_stats[user.id][pet_current]['nickname'] + "**, whose types are **" + type1 + "** and **" + type2 + "**. Are you sure? Type ``yes`` to confirm, others to exit.")
        cfm = await self.bot.wait_for_message(author=ctx.message.author)
        if cfm.content.lower() == 'yes':
            while True:
                self.pet_stats[user.id][pet_current]['battle_stats']['hp'] = random.randint(40,100)
                self.pet_stats[user.id][pet_current]['battle_stats']['atk'] = random.randint(30,100)
                self.pet_stats[user.id][pet_current]['battle_stats']['defe'] = random.randint(30,100)
                self.pet_stats[user.id][pet_current]['battle_stats']['spa'] = random.randint(30,100)
                self.pet_stats[user.id][pet_current]['battle_stats']['spd'] = random.randint(30,100)
                self.pet_stats[user.id][pet_current]['battle_stats']['spe'] = random.randint(30,100)
                bst0 = self.pet_stats[user.id][pet_current]['battle_stats']['hp'] + self.pet_stats[user.id][pet_current]['battle_stats']['atk'] +self.pet_stats[user.id][pet_current]['battle_stats']['defe'] +self.pet_stats[user.id][pet_current]['battle_stats']['spa']+self.pet_stats[user.id][pet_current]['battle_stats']['spd'] +self.pet_stats[user.id][pet_current]['battle_stats']['spe']
                if  self.pet_stats[user.id][pet_current]['battle_stats']['bst'] >= bst0 > (self.pet_stats[user.id][pet_current]['battle_stats']['bst']-(30)):
                    break
            self.pet_stats[user.id][pet_current]['battle_stats']['class'] = random.choice(self.classes)
            self.pet_stats[user.id][pet_current]['owner_name'] = user.display_name
            self.save_pet_stats()
            await self.bot.say("Congratulations on creating a new pet! It's been set as your active pet. Your pet's stats are generated as follows:")
            petid = pet_current
            self.pet_stats[user.id]['current_pet'] = str(pet_current)
            await self.output_pet_stats(user,petid)
        else:
            await self.bot.say("Pet creation cancelled. Feel free to try again.")

    async def output_pet_stats(self, user, petid):
        embed=discord.Embed(title=self.pet_stats[user.id][petid]['nickname'] + "\'s stats")
        embed.set_thumbnail(url=self.pet_stats[user.id][petid]['image'])
        embed.set_image(url=self.pet_stats[user.id][petid]['image'])
        embed.add_field(name="Name", value=self.pet_stats[user.id][petid]['nickname'], inline=True)
        embed.add_field(name="Happiness", value=self.pet_stats[user.id][petid]['happiness'], inline=True)
        embed.add_field(name="Hunger", value=self.pet_stats[user.id][petid]['hunger'], inline=True)
        embed.add_field(name="Owner", value=self.pet_stats[user.id][petid]['owner_name'], inline=True)
        embed.add_field(name="Class", value=self.pet_stats[user.id][petid]['battle_stats']['class'], inline=True)
        embed.add_field(name="HP", value=str(self.pet_stats[user.id][petid]['battle_stats']['hp']) + " (in battle aprox. "+ str(100+ round(self.pet_stats[user.id][petid]['battle_stats']['hp']*1.75)) +")", inline=True)
        embed.add_field(name="Physical Attack", value=self.pet_stats[user.id][petid]['battle_stats']['atk'], inline=True)
        embed.add_field(name="Physcial Defense", value=self.pet_stats[user.id][petid]['battle_stats']['defe'], inline=True)
        embed.add_field(name="Special Attack", value=self.pet_stats[user.id][petid]['battle_stats']['spa'], inline=True)
        embed.add_field(name="Special Defense", value=self.pet_stats[user.id][petid]['battle_stats']['spd'], inline=True)
        embed.add_field(name="Speed", value=self.pet_stats[user.id][petid]['battle_stats']['spe'], inline=True)
        embed.add_field(name="Buff Level", value=self.pet_stats[user.id][petid]['battle_stats']['buff'], inline=True)
        bst0 = self.pet_stats[user.id][petid]['battle_stats']['hp'] + self.pet_stats[user.id][petid]['battle_stats']['atk'] +self.pet_stats[user.id][petid]['battle_stats']['defe'] +self.pet_stats[user.id][petid]['battle_stats']['spa']+self.pet_stats[user.id][petid]['battle_stats']['spd'] +self.pet_stats[user.id][petid]['battle_stats']['spe']
        embed.add_field(name="Base Stat Total", value=bst0, inline=True)
        if self.pet_stats[user.id][petid]['battle_stats']['type1'] != self.pet_stats[user.id][petid]['battle_stats']['type2']:
            embed.add_field(name="Types", value=self.pet_stats[user.id][petid]['battle_stats']['type1'] + ", " + self.pet_stats[user.id][petid]['battle_stats']['type2'], inline=True)
        else:
            embed.add_field(name="Types", value=self.pet_stats[user.id][petid]['battle_stats']['type1'], inline=True)
        #embed.set_footer(text=".")
        await self.bot.say(embed=embed)



def setup(bot):
    n = Pets(bot)
    bot.add_cog(n)
