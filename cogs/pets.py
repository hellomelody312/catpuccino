import discord
import asyncio
from discord.ext import commands
from .utils.dataIO import dataIO
import random
import os
import math
import requests
import json
#import schedule
import time
from copy import deepcopy


class Pets:
    """wwip"""

    def __init__(self, bot):
        self.bot = bot
        self.botownerid = "293041932542672896"
        self.owner_stats_url = requests.get("https://api.jsonbin.io/b/5b081b310fb4d74cdf23e613/latest")
        self.moves_url = requests.get("https://api.jsonbin.io/b/5b080ed07a973f4ce5784717/latest")
        self.pet_stats_url = requests.get("https://api.jsonbin.io/b/5b112f31c83f6d4cc734a41d/latest")
        self.bosses_url = requests.get("https://api.jsonbin.io/b/5b1463390fb4d74cdf23f0af/latest")
        self.owner_stats = self.owner_stats_url.json()
        self.errornotexist = "One or both of you do not have pets in the database!"
        ##for duels
        self.bosses = self.bosses_url.json()
        self.types = dataIO.load_json('data/magic/types.json')
        self.typelist = ["Light","Normal","Fire","Fighting","Water","Flying","Grass","Poison","Electric","Ground","Psychic","Rock","Ice","Bug","Dragon","Ghost","Dark","Steel","Fairy"]
        self.moves = self.moves_url.json()
        self.p1_buffs ={"atk":1,"defe":1,"spa":1,"spd":1,"acc":1,"statused":0,"status":"none","turns":0,"protected":0,"reflected":0}
        self.p2_buffs ={"atk":1,"defe":1,"spa":1,"spd":1,"acc":1,"statused":0,"status":"none","turns":0,"protected":0,"reflected":0}
        self.statuses = ["poison","burn","flinch","confused","reflect","protect","freeze","para","sleep"]
        self.stat_names = {"atk":"Attack","defe":"Defense","spa":"Special Attack","spd":"Special Defense","acc":"Accuracy"}
        self.pet_stats = self.pet_stats_url.json()
        self.classes = ["all","pokemon","sakura","harrypotter","ffxv","sailormoon"]
        self.moodnames = {'love':'In Love','happy2':'Very Happy','happy1':'Happy','bored':'Bored','sad':'Sad','angry':'Angry','shy':'Embarrassed','asleep':'Sleeping'}


    def save_pet_stats(self):
        requests.put("https://api.jsonbin.io/b/5b112f31c83f6d4cc734a41d", json=self.pet_stats)

    def save_owner_stats(self):
        requests.put("https://api.jsonbin.io/b/5b081b310fb4d74cdf23e613", json=self.owner_stats)

    def save_boss_stats(self):
        requests.put("https://api.jsonbin.io/b/5b1463390fb4d74cdf23f0af", json=self.bosses)

###background tasks
#    async def bgloop():
#        await self.bot.wait_until_ready()
#        while not self.bot.is_closed:
#            self.reduce_hunger()
#            await asyncio.sleep(216000) # task runs every 60 seconds

#    Pets.bot.loop.create_task(self.bgloop())


    def reduce_hunger(self):
        for userid in self.pet_stats:
            for petid in self.pet_stats[userid]['pets']:
                if self.pet_stats[userid]['pets'][petid]['hunger'] > 0:
                    self.pet_stats[userid]['pets'][petid]['hunger'] -= 2
                #self.pet_stats[userid]['pets'][petid]['affection'] -= 1
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
            await self.bot.say(self.pet_stats[user.id]['pets'][petid]['name'] + "'s hunger is currently " + str(self.pet_stats[user.id]['pets'][petid]['hunger'])+". Would you like to feed it a biscuit for 20PMP? (30s) (next time type ;pet feed biscuit to skip this message.)")
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

    async def feedbiscuit(self,user,petid):
        self.pet_stats[user.id]['pets'][petid]['hunger'] += 10
        self.pet_stats[user.id]['pets'][petid]['affection'] += 1
        self.owner_stats[user.id]['money'] -= 20
        self.save_pet_stats()
        self.save_owner_stats()
        await self.bot.say(user.display_name + " fed a biscuit to " + self.pet_stats[user.id]['pets'][petid]['name'] +" for 20 PMP. Its affection and hunger increased!\n"+self.pet_stats[user.id]['pets'][petid]['name'] +"'s hunger is now " +str(self.pet_stats[user.id]['pets'][petid]['hunger']) + " and its affection is " + str(self.pet_stats[user.id]['pets'][petid]['affection']) +".")

    @pet.command(pass_context=True)
    async def moodsetup(self, ctx):
        user = ctx.message.author
        petid = self.pet_stats[user.id]['current_pet']
        await self.bot.say("Welcome to Mood Setup. Here you can provide different image links for your pet's different moods aside from default. If you don't have an image for a specific mood, type ``skip`` and you will move to the next one. There are currently 8 moods in total.\nYou will be setting up moods for "+self.pet_stats[user.id]['pets'][petid]['name']+". Type ``next`` to begin. At any time you can type ``exit`` to quit.")
        cfm = await self.bot.wait_for_message(author=ctx.message.author)
        if cfm.content != 'next':
            await self.bot.say("Mood setup cancelled.")
            return
        else:
            step = 0
            for mood in ['love','happy2','happy1','bored','sad','angry','shy','asleep']:
                step +=1
                await self.bot.say("Provide an url for the **" + self.moodnames[mood] + "** mood. (" + str(step) + "/8)")
                imgurl = await self.bot.wait_for_message(author=ctx.message.author)
                imgg = str(imgurl.content)
                while imgg[0:4] != 'http' and imgg.lower() not in ['exit','skip'] :
                    await self.bot.say("Not an url! Try again.")
                    imgurl = await self.bot.wait_for_message(author=ctx.message.author)
                    imgg = str(imgurl.content)
                if imgg.lower() == 'exit':
                    await self.bot.say("Mood setup cancelled. Any changes already made will be saved.")
                    break
                if imgg.lower() == 'skip':
                    #await self.bot.say("Skipped the current mood.")
                    continue
                self.pet_stats[user.id]['pets'][petid]['images'][mood] = imgg
            await self.bot.say("Thank you for completing Mood Setup.")
            self.save_pet_stats()

    @pet.command(pass_context=True)
    async def play(self, ctx,*, action:str=None):
        user = ctx.message.author
        petid = self.pet_stats[user.id]['current_pet']
        if action == None:
            msg0 = user.display_name + " played with " + self.pet_stats[user.id]['pets'][petid]['name'] +"!\n"
            action = " play "
        else:
            msg0 = user.display_name + " went to "+action+" with " + self.pet_stats[user.id]['pets'][petid]['name'] +"!\n"
        embed=discord.Embed(title=msg0,color=user.color)
        reaction = random.choice(['love','happy2','happy1','bored','return','sad','angry','shy'])
        if reaction != 'return':
            if self.pet_stats[user.id]['pets'][petid]['images'][reaction] != "":
                mood_url = self.pet_stats[user.id]['pets'][petid]['images'][reaction]
            elif reaction in ['love','happy2'] and self.pet_stats[user.id]['pets'][petid]['images']['happy1'] != "":
                mood_url = self.pet_stats[user.id]['pets'][petid]['images']['happy1']
            elif reaction in ['angry','bored'] and self.pet_stats[user.id]['pets'][petid]['images']['sad'] != "":
                mood_url = self.pet_stats[user.id]['pets'][petid]['images']['sad']
            else:
                mood_url = self.pet_stats[user.id]['pets'][petid]['images']['default']
        else:
            mood_url = self.pet_stats[user.id]['pets'][petid]['images']['default']
        embed.set_thumbnail(url=mood_url)
        if reaction == "love":
            pet_action = random.choice(['loved it!','jumped at {} in affection!','ran to hug {}!','became super duper happy!','was elated!','was esctatic about it!'])
            msg1 =self.pet_stats[user.id]['pets'][petid]['name'] +" "+  pet_action.format(user.display_name)
            msg2 = "Its affection increased by 20! " +user.display_name + " got 200 PMP!"
            self.owner_stats[user.id]['money'] += 200
            self.pet_stats[user.id]['pets'][petid]['affection'] += 20
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "happy2":
            pet_action = random.choice(['really liked it!','let out a big grin at {}!','appears very content!','became really happy!','\'s face lit up!'])
            msg1 =self.pet_stats[user.id]['pets'][petid]['name'] +" " +  pet_action.format(user.display_name)
            msg2 = "Its affection increased by 5! " + user.display_name + " got 50 PMP!"
            self.owner_stats[user.id]['money'] += 50
            self.pet_stats[user.id]['pets'][petid]['affection'] += 5
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "happy1":
            pet_action = random.choice(['liked it!','smiled back at {}!','appears quite content.','became happy!','lets out a small cry of joy!'])
            msg1 =self.pet_stats[user.id]['pets'][petid]['name'] +" "+  pet_action.format(user.display_name)
            msg2 = "Its affection increased by 2! " + user.display_name + " got 25 PMP!"
            self.owner_stats[user.id]['money'] += 25
            self.pet_stats[user.id]['pets'][petid]['affection'] += 2
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "bored":
            pet_action = random.choice(['felt meh.','looked back at {} for 1 second in disinterest and turned away.','ignored {}.','had no reaction.','would rather do something more interesting.'])
            msg1 =self.pet_stats[user.id]['pets'][petid]['name'] +" " +  pet_action.format(user.display_name)
            msg2 = "" + user.display_name + " got 1 PMP."
            self.owner_stats[user.id]['money'] += 1
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "sad":
            pet_action = random.choice(['did not like it.','turned away from {}.','appears quite down.','said no.','became sad for some reason.','did not quite enjoy that.'])
            msg1 =self.pet_stats[user.id]['pets'][petid]['name'] + " "+ pet_action.format(user.display_name)
            msg2 =  "Its affection decreased by 1!"
            self.pet_stats[user.id]['pets'][petid]['affection'] -= 1
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "shy":
            pet_action = random.choice(['blushed for some reason...','looked at {} with a certain degree of shyness...','became embarrassed somehow...','tried to hide its blushing...','turned all red for some reason...','did not know how to react properly...'])
            msg1 =self.pet_stats[user.id]['pets'][petid]['name'] + " "+ pet_action.format(user.display_name)
            msg2 =  "Its affection changed by some random amount! \n"
            msg3 =  user.display_name + " got 40 PMP!"
            embrn = random.randint(-3,4)
            self.pet_stats[user.id]['pets'][petid]['affection'] += embrn
            self.owner_stats[user.id]['money'] += 40
            embed.add_field(name=msg1,value=msg2+msg3,inline=False)
        elif reaction == "angry":
            pet_action = random.choice(['got angry at {}!','frowned heavily at {}!','appeared very irritated!','cried out in distress!'])
            msg1 =self.pet_stats[user.id]['pets'][petid]['name'] + " " +  pet_action.format(user.display_name)
            msg2 = "Its affection decreased by 5!"
            self.pet_stats[user.id]['pets'][petid]['affection'] -= 5
            embed.add_field(name=msg1,value=msg2,inline=False)
        elif reaction == "return":
            msg1 =self.pet_stats[user.id]['pets'][petid]['name'] +  " decided to " + action + " with " + user.display_name + " back!"
            msg2 =  user.display_name + " got 75 PMP!"
            self.owner_stats[user.id]['money'] += 75
            embed.add_field(name=msg1,value=msg2,inline=False)
        await self.bot.say(embed=embed)
        self.pet_stats[user.id]['pets'][petid]['exp'] += 10
        self.save_pet_stats()
        self.save_owner_stats()

    @pet.command(pass_context=True)
    async def avatar(self, ctx, imgg:str=None):
        user = ctx.message.author
        await self.bot.say("Specify a new avatar url for **"+ self.pet_stats[user.id][self.pet_stats[user.id]['current_pet']]['name'] +"**. (exit to cancel.)")
        imgurl = await self.bot.wait_for_message(author=ctx.message.author)
        imgg = str(imgurl.content)
        while imgg[0:4] != 'http' and imgg.lower() != 'exit':
            await self.bot.say(imgg[0:7]+"Not an url! Try again.")
            imgurl = await self.bot.wait_for_message(author=ctx.message.author)
            imgg = str(imgurl.content)
        if imgg.lower() == 'exit':
            await self.bot.say("Avatar change cancelled.")
            return
        else:
            self.pet_stats[user.id][self.pet_stats[user.id]['current_pet']]['image'] = imgg
            self.save_pet_stats()
            await self.bot.say("Avatar changed.")

    @pet.command(pass_context=True)
    async def name(self, ctx, imgg:str=None):
        user = ctx.message.author
        await self.bot.say("Specify a new name for **"+ self.pet_stats[user.id][self.pet_stats[user.id]['current_pet']]['name'] +"**. (exit to cancel.)")
        imgurl = await self.bot.wait_for_message(author=ctx.message.author)
        imgg = str(imgurl.content)
        if imgg.lower() == 'exit':
            await self.bot.say("Avatar change cancelled.")
            return
        else:
            self.pet_stats[user.id][self.pet_stats[user.id]['current_pet']]['name'] = imgg
            self.save_pet_stats()
            await self.bot.say("Name changed.")

    @pet.command(pass_context=True)
    async def select(self, ctx, number:int=None):
        user = ctx.message.author
        if number:
            if number > len(self.pet_stats[user.id]['pets']):
                await self.bot.say("No such pet.")
            else:
                self.pet_stats[user.id]['current_pet'] = str(number)
                await self.bot.say("Your current pet is " + self.pet_stats[user.id]['pets'][str(number)]['name']+ ".")
                self.save_pet_stats()
        else:
            embed=discord.Embed(title="Available pets:",color=user.color)
            for each in self.pet_stats[user.id]['pets']:
                msg = str(each) + " - " +  self.pet_stats[user.id]['pets'][each]['name']
                embed.add_field(name=msg, value="Affection: " + str(self.pet_stats[user.id]['pets'][each]['affection']))
            await self.bot.say(embed=embed)

    @pet.command(pass_context=True)
    async def settings(self, ctx):
        '''Edit settings for your pet.'''
        if ctx.invoked_subcommand is None:
            await self.bot.say("``Pet settings: \n;pet settings image to setup different emotions images.\n;pet settings  to be added.``")


    @pet.command(pass_context=True)
    #@commands.cooldown(1, 36600, commands.BucketType.user)
    async def create(self, ctx):
        user = ctx.message.author
        if user.id not in self.pet_stats:
            self.pet_stats[user.id] = {"pets":{"1": {"stats": {"item": 0,"type1": "","defe": 1,"spe": 1,"type2": "","win": 0,"hp": 1,"class": "all","atk": 1,
                                                              "buff": 0,"spd": 1,"lose": 0,"spa": 1},"level": 1,"exp": 0,"hunger": 50,"affection": 1,
                                                              "images": {"default":"","love": "","happy2": "","happy1": "","sad": "","angry": "","shy": "","bored": "","asleep": ""},
                                                              "name": ""}},"current_pet":"1"}
            pet_current = "1"
        else:
            pet_current = str(len(self.pet_stats[user.id]['pets'])+1)
            self.pet_stats[user.id]['pets'][pet_current] = {"stats": {"item": 0,"type1": "","defe": 1,"spe": 1,"type2": "","win": 0,"hp": 1,"class": "all","atk": 1,
                                                              "buff": 0,"spd": 1,"lose": 0,"spa": 1},"level": 1,"exp": 0,"hunger": 50,"affection": 1,
                                                              "images": {"default":"","love": "","happy2": "","happy1": "","sad": "","angry": "","shy": "","bored": "","asleep": ""},
                                                              "name": ""}
        await self.bot.say("Welcome to create-a-pet! You're creating your pet no. " + str(pet_current) + ". Type ``exit`` to quit anytime.\nFirst, let's give your pet a name:")
        nick = await self.bot.wait_for_message(author=ctx.message.author)
        if nick.content.lower() == 'exit':
            await self.bot.say("Pet creation cancelled.")
            return
        else:
            self.pet_stats[user.id]['pets'][pet_current]['name'] = nick.content
        await self.bot.say("Your pet's name is **"+ self.pet_stats[user.id]['pets'][pet_current]['name'] +"**.\nNext, let's have an image for your pet! Give a **direct** link of your pet's default image.")
        imgurl = await self.bot.wait_for_message(author=ctx.message.author)
        imgg = str(imgurl.content)
        while imgg[0:4] != 'http' and imgg.lower() != 'exit':
            await self.bot.say("Not an url! Try again.")
            imgurl = await self.bot.wait_for_message(author=ctx.message.author)
            imgg = str(imgurl.content)
        if imgg.lower() == 'exit':
            await self.bot.say("Pet creation cancelled.")
            return
        self.pet_stats[user.id]['pets'][pet_current]['image'] = imgg
        await self.bot.say("Done. Later you can use ;pet moodsetup to set more images of your pet like happy, sad, bored, angry, etc. if you want.\nNext, set the types for your pet. It can be any 1 or 2 types from the Pokemon games. ex: fire fighting. Type ``random`` to randomly set types.")
        types = await self.bot.wait_for_message(author=ctx.message.author)
        if types.content == 'exit':
            await self.bot.say("Pet creation cancelled.")
            return
        elif types.content == 'random':
            self.pet_stats[user.id]['pets'][pet_current]['stats']['type1'] = random.choice(self.typelist)
            self.pet_stats[user.id]['pets'][pet_current]['stats']['type2'] = random.choice(self.typelist)
            type1 = self.pet_stats[user.id]['pets'][pet_current]['stats']['type1']
            type2 = self.pet_stats[user.id]['pets'][pet_current]['stats']['type2']
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
            while type1 not in self.typelist or type2 not in self.typelist:
                await self.bot.say("Invalid type! Try again.")
                types = await self.bot.wait_for_message(author=ctx.message.author)
                types_list = types.content.split()
                type1 = types_list[0][0].upper() + types_list[0][1:]
                if len(types_list) < 2:
                    type2 = type1
                else:
                    type2 = types_list[1][0].upper() + types_list[1][1:]
            self.pet_stats[user.id]['pets'][pet_current]['stats']['type1'] = type1
            self.pet_stats[user.id]['pets'][pet_current]['stats']['type2'] = type2
        if type1 != type2:
            ty = "types are **" + type1 + "** and **" + type2
        else:
            ty = "type is **" + type1
        await self.bot.say("You're about to create **" + self.pet_stats[user.id]['pets'][pet_current]['name'] + "**, whose " + ty + "**. Are you sure? Type ``yes`` to confirm, others to exit.")
        cfm = await self.bot.wait_for_message(author=ctx.message.author)
        if cfm.content.lower() == 'yes':
            while True:
                bufflv = self.pet_stats[user.id]['pets'][pet_current]['stats']['buff']
                maxbst = 400 + bufflv*50
                self.pet_stats[user.id]['pets'][pet_current]['stats']['hp'] = random.randint(40+bufflv*5,110+bufflv*10)
                self.pet_stats[user.id]['pets'][pet_current]['stats']['atk'] = random.randint(30+bufflv*50,100+bufflv*10)
                self.pet_stats[user.id]['pets'][pet_current]['stats']['defe'] = random.randint(30+bufflv*50,100+bufflv*10)
                self.pet_stats[user.id]['pets'][pet_current]['stats']['spa'] = random.randint(30+bufflv*50,100+bufflv*10)
                self.pet_stats[user.id]['pets'][pet_current]['stats']['spd'] = random.randint(30+bufflv*50,100+bufflv*10)
                self.pet_stats[user.id]['pets'][pet_current]['stats']['spe'] = random.randint(30+bufflv*50,100+bufflv*10)
                bst0 = self.pet_stats[user.id]['pets'][pet_current]['stats']['hp'] + self.pet_stats[user.id]['pets'][pet_current]['stats']['atk'] +self.pet_stats[user.id]['pets'][pet_current]['stats']['defe'] +self.pet_stats[user.id]['pets'][pet_current]['stats']['spa']+self.pet_stats[user.id]['pets'][pet_current]['stats']['spd'] +self.pet_stats[user.id]['pets'][pet_current]['stats']['spe']
                if  maxbst >= bst0 > (maxbst-(30)):
                    break
            self.pet_stats[user.id]['pets'][pet_current]['stats']['class'] = random.choice(self.classes)
            self.save_pet_stats()
            await self.bot.say("Congratulations on creating a new pet! It's been set as your active pet. Your pet's stats are generated as follows:")
            petid = pet_current
            self.pet_stats[user.id]['current_pet'] = str(pet_current)
            await self.output_pet_stats(user,petid)
        else:
            await self.bot.say("Pet creation cancelled. Feel free to try again.")


#### PET DUEL COMMANDS

    @pet.command(pass_context=True)
    async def duel(self, ctx, *,target:discord.Member=None):
        if not target:
            await self.bot.say("Please specify target.")
        elif str(ctx.message.author.id) not in self.pet_stats or str(target.id) not in self.pet_stats:
            await self.bot.say(self.errornotexist)
        else:
            mode = "petvspet"
            p1 = ctx.message.author
            p1_color = ctx.message.author.color
            p1_stats = self.pet_stats[ctx.message.author.id]['pets'][self.pet_stats[ctx.message.author.id]['current_pet']]['stats']
            p1_name = self.pet_stats[ctx.message.author.id]['pets'][self.pet_stats[ctx.message.author.id]['current_pet']]['name']
            p2 = target
            p2_stats = self.pet_stats[target.id]['pets'][self.pet_stats[target.id]['current_pet']]['stats']
            p2_color = target.color
            p2_name = self.pet_stats[target.id]['pets'][self.pet_stats[target.id]['current_pet']]['name']
            await self.duelscript(p1,p2,p1_name,p1_color,p1_stats,p2_name,p2_color,p2_stats,mode)

    @pet.command(pass_context=True)
    async def attack(self, ctx, *,target:discord.Member=None):
        if not target:
            await self.bot.say("Please specify target.")
        elif str(ctx.message.author.id) not in self.pet_stats or str(target.id) not in self.pet_stats:
            await self.bot.say(self.errornotexist)
        else:
            mode = "petvshuman"
            p1 = ctx.message.author
            p1_color = ctx.message.author.color
            p1_stats = self.pet_stats[ctx.message.author.id]['pets'][self.pet_stats[ctx.message.author.id]['current_pet']]['stats']
            p1_name = self.pet_stats[ctx.message.author.id]['pets'][self.pet_stats[ctx.message.author.id]['current_pet']]['name']
            p2 = target
            p2_color = target.color
            p2_name = target.display_name
            p2_stats = self.owner_stats[target.id]
            await self.duelscript(p1,p2,p1_name,p1_color,p1_stats,p2_name,p2_color,p2_stats,mode)

    @pet.command(pass_context=True)
    async def duelboss(self, ctx, *,target:str=None):
        if not target:
            await self.bot.say("List of available bosses: " + str(list(self.bosses)).strip('[]'))
        elif str(ctx.message.author.id) not in self.pet_stats or target not in self.bosses:
            await self.bot.say(self.errornotexist)
        else:
            mode = "petvsboss"
            p1 = ctx.message.author
            p1_color = ctx.message.author.color
            p1_stats = self.pet_stats[ctx.message.author.id]['pets'][self.pet_stats[ctx.message.author.id]['current_pet']]['stats']
            p1_name = self.pet_stats[ctx.message.author.id]['pets'][self.pet_stats[ctx.message.author.id]['current_pet']]['name']
            p2 = target
            p2_stats = self.bosses[target]
            p2_name = p2_stats['displayname']
            p2_color = p2_stats['color']
            await self.duelscript(p1,p2,p1_name,p1_color,p1_stats,p2_name,p2_color,p2_stats,mode)

    async def duelscript(self,p1,p2,p1_name,p1_color,p1_stats,p2_name,p2_color,p2_stats,mode):
        embed=discord.Embed(title="**"+p1_name+ self.types[p1_stats['type1']]['icon'] +self.types[p1_stats['type2']]['icon']+" vs. " + p2_name + self.types[p2_stats['type1']]['icon'] +self.types[p2_stats['type2']]['icon']+"**", color=0xe90169) #start battle
        p1_hp = 100+round(p1_stats['hp']*round(random.uniform(1.5,2), 2))
        p2_hp = 100+round(p2_stats['hp']*round(random.uniform(1.5,2), 2))
        p1_remaininghp = p1_hp
        p2_remaininghp = p2_hp
        current_buffs_p1 = dict(self.p1_buffs)
        current_buffs_p2 = dict(self.p2_buffs)
        #user_status
        if p1_stats['spe'] < p2_stats['spe']:
            embed.add_field(name=p1_name + " tries to attack!", value="*"+p2_name + " goes first due to higher Speed!*", inline=True)
            p1, p2 = p2, p1
            p1_hp, p2_hp = p2_hp, p1_hp
            p1_name, p2_name = p2_name, p1_name
            p1_remaininghp, p2_remaininghp = p2_remaininghp, p1_remaininghp
            p1_color, p2_color = p2_color, p1_color
            p1_stats,p2_stats = p2_stats, p1_stats
        await self.bot.say(embed=embed)
        while p2_remaininghp > 0 and p1_remaininghp > 0:
            try:
                msg2 = ""
                msg1 = ""
                swapped = 0
                canattack = True
                if current_buffs_p1['status'] not in ["none","burn","poison"]: ##check pre-move status conditions
                    if current_buffs_p1['status'] == "freeze":
                        if current_buffs_p1['turns'] == 0:
                            embed2=discord.Embed(description=p1_name + " thawed out! :sweat_drops:",color=p1_color)
                            await self.bot.say(embed=embed2)
                            current_buffs_p1['status'] = "none"
                            current_buffs_p1['statused'] = 0
                        else:
                            embed2=discord.Embed(description=p1_name + " is frozen solid! :snowflake:",color=p1_color)
                            await self.bot.say(embed=embed2)
                            canattack = False
                    if current_buffs_p1['status'] == "flinch":
                        canattack = False
                        embed2=discord.Embed(description=p1_name + " flinched from the attack! ",color=p1_color)
                        await self.bot.say(embed=embed2)
                        current_buffs_p1['status'] = "none"
                        current_buffs_p1['statused'] = 0
                    if current_buffs_p1['status'] == "confuse":
                        if current_buffs_p1['turns'] == 0:
                            embed2=discord.Embed(description=p1_name + " snapped out of confusion!",color=p1_color)
                            await self.bot.say(embed=embed2)
                            current_buffs_p1['status'] = "none"
                            current_buffs_p1['statused'] = 0
                        else:
                            embed2=discord.Embed(description=p1_name + " is confused! :dizzy:",color=p1_color)
                            await self.bot.say(embed=embed2)
                            q = random.randint(1,100)
                            if q < 33:
                                canattack = False
                                confuse_dmg = round(math.floor(math.floor(50  * 50 * p1_stats['atk'] / p1_stats['defe']) / 50) + 2)
                                p1_remaininghp -= confuse_dmg
                                embed3=discord.Embed(description=p1_name + " hurt themselves in confusion! :boom: (" + str(round(dmg / (p1_hp)*100)) + "\%) ("+str(p1_remaininghp)+"/"+str(p1_hp)+" HP)",color=p1_color)
                                await self.bot.say(embed=embed3)
                            else:
                                canattack = True
                    if current_buffs_p1['status'] == "para":
                        q = random.randint(1,100)
                        if q < 40:
                            canattack = False
                            embed2=discord.Embed(description=p1_name + " can't move due to paralysis! :zap:",color=p1_color)
                            await self.bot.say(embed=embed2)
                        else:
                            canattack = True
                    if current_buffs_p1['status'] == "sleep":
                        if current_buffs_p1['turns'] == 0:
                            embed2=discord.Embed(description=p1_name + " woke up! ",color=p1_color)
                            await self.bot.say(embed=embed2)
                            current_buffs_p1['status'] = "none"
                            current_buffs_p1['statused'] = 0
                        else:
                            canattack = False
                            embed2=discord.Embed(description=p1_name + " is fast asleep. :zzz:",color=p1_color)
                            await self.bot.say(embed=embed2)
                    if current_buffs_p1['turns'] > 0:
                        current_buffs_p1['turns'] -= 1
                    await asyncio.sleep(1)
                if canattack == True:
                    embed=discord.Embed(color=p1_color) #initialize panel
                    if p1_stats['class'] == "all": #detect class
                        moveclass = random.choice(["pokemon","sakura","harrypotter","ffxv","sailormoon","test"])
                    else:
                        moveclass = p1_stats['class']
                    moveid = random.choice(list(self.moves[moveclass])) #choose move
                    if moveclass == "harrypotter" or moveclass == "sakura": #change the verb
                        verb = "cast"
                    else:
                        verb = "used"
                    msg1 += "**"+p1_name + "** "+ verb +" **"+ self.moves[moveclass][moveid]['name']+"** " + self.types[self.moves[moveclass][moveid]['type']]['icon']
                    if self.moves[moveclass][moveid]['text']:
                        msg1 = msg1 +" to "+ self.moves[moveclass][moveid]['text'] + "!\n"
                    else:
                        msg1 = msg1 +"!\n" # write used move to do sth
                    hit = 1
                    if self.moves[moveclass][moveid]['acc'] > 0:
                        hit_chance = random.randint(1,100) #accuracy check
                        if hit_chance >  self.moves[moveclass][moveid]['acc']*current_buffs_p1['acc']:
                            hit = 0
                            msg2 += "The attack missed!"
                    if hit == 1: #if the move hits
                        if self.moves[moveclass][moveid]['category'] == "Status":
                            if current_buffs_p2['protected'] == 1 and self.moves[moveclass][moveid]['effect'] not in ["heal","protect","reflect","refresh","stat_self"]:
                                current_buffs_p2['protected'] = 0
                                msg2 += p2_name + " protected themselves from the attack!"
                            elif  self.moves[moveclass][moveid]['effect'] == "protect":
                                current_buffs_p1['protected'] = 1
                                msg2 += p1_name + " protected themselves!"
                            elif  self.moves[moveclass][moveid]['effect'] == "reflect":
                                current_buffs_p1['reflected'] = 1
                                msg2 += p1_name + " is ready to reflect the next attack!"
                            else:
                                msg2,current_buffs_p1,current_buffs_p2,p1_remaininghp = self.check_if_cause_status(moveclass,moveid,msg2,current_buffs_p1,current_buffs_p2,p1_name,p2_name,p1_remaininghp,p1_hp)
                        else:
                            if current_buffs_p2['protected'] == 1:
                                current_buffs_p2['protected'] = 0
                                msg2 += p2_name + " protected themselves from the attack!"
                            else:
                                power = abs(random.randint(self.moves[moveclass][moveid]['power']-self.moves[moveclass][moveid]['random'],self.moves[moveclass][moveid]['power']+self.moves[moveclass][moveid]['random']))
                                if current_buffs_p2['reflected'] == 1:
                                    swapped = 1
                                    current_buffs_p2['reflected'] = 0
                                    msg2 += p2_name + " reflected the attack!\n"
                                    p3 = p2
                                    p2 = p1
                                    p3_hp = p2_hp
                                    p2_hp = p1_hp
                                    p3_name = p2_name
                                    p2_name = p1_name
                                    p3_remaininghp = p2_remaininghp
                                    p2_remaininghp = p1_remaininghp
                                    p1_stats,p2_stats = p2_stats, p1_stats
                                    current_buffs_p2temp = {}
                                    current_buffs_p2temp = deepcopy(current_buffs_p2)
                                    current_buffs_p2.clear()
                                    current_buffs_p2 = deepcopy(current_buffs_p1)
                                    current_buffs_p1.clear()
                                    current_buffs_p1 = deepcopy(current_buffs_p2temp)
                                if self.moves[moveclass][moveid]['category'] == "Physical":
                                    if current_buffs_p1['status'][0] == "burn":
                                        atk = p1_stats['atk']*0.5*current_buffs_p1['atk']
                                    else:
                                        atk = p1_stats['atk']*current_buffs_p1['atk']
                                    defe = p2_stats['defe']*current_buffs_p2['defe']
                                else:
                                    atk = p1_stats['spa']*current_buffs_p1['spa']
                                    defe = p2_stats['spd']*current_buffs_p2['spd']
                                mul = 1
                                for typy in ['type1','type2']: #check type effectiveness
                                    if self.moves[moveclass][moveid]['type'] in self.types[p2_stats[typy]]['supereffective']:
                                        mul *= 2
                                    elif self.moves[moveclass][moveid]['type'] in self.types[p2_stats[typy]]['notveryeffective']:
                                        mul *= 0.5
                                    elif self.moves[moveclass][moveid]['type'] in self.types[p2_stats[typy]]['noteffective']:
                                        mul *= 0
                                if self.moves[moveclass][moveid]['type'] in [p1_stats['type1'],p1_stats['type2']]: #check STAB
                                    power *= 1.5
                                if mul >1:
                                    msg2 = msg2 + ":small_red_triangle: It's super effective! \n"
                                elif 0 <mul <1:
                                    msg2 = msg2 + ":small_red_triangle_down: It's not very effective... \n"
                                elif 0 == mul:
                                    msg2 = msg2 + ":x: It had no effect!\n"
                                if mul > 0:
                                    rand = 0.01*random.randint(85,115)
                                    dmg = round(math.floor(math.floor(64  * power * atk / defe) / 50) + 2 * mul * rand)
                                    critchance = random.randint(1,100)
                                    if critchance <= self.moves[moveclass][moveid]['crit']:
                                        dmg *+ 1.5
                                        msg2 += "**A critical hit!**\n"
                                    p2_remaininghp = round(p2_remaininghp - dmg)
                                    msg2 += p2_name + " took " + str(dmg) + " damage! (" + str(round(dmg / (p2_hp)*100)) + "\%) ("+str(p2_remaininghp)+"/"+str(p2_hp)+" HP)\n"
                                    if p2_remaininghp <= 0:
                                        msg2 = msg2  + "\n***" + p2_name + " has fainted!***"
                                    else:
                                        if self.moves[moveclass][moveid]['effect'] == "recoil":
                                            recoil_dmg =  round(dmg *self.moves[moveclass][moveid]['affected_stat'][1]/100)
                                            p1_remaininghp -= recoil_dmg
                                            msg2 += p1_name + " took " + str(recoil_dmg) + " recoil damage! (" + str(round(recoil_dmg / (p1_hp)*100)) + "\%) ("+str(p1_remaininghp)+"/"+str(p1_hp)+" HP)\n"
                                            if p1_remaininghp <=0:
                                                msg2 += "\n***" + p1_name + " has fainted!***"
                                        elif self.moves[moveclass][moveid]['effect'] == "drain":
                                            drain_dmg =  round(dmg *self.moves[moveclass][moveid]['affected_stat'][1]/100)
                                            p1_remaininghp += drain_dmg
                                            msg2 += p1_name + " drained " + str(drain_dmg) + " HP! (" + str(round(drain_dmg / (p1_hp)*100)) + "\%) ("+str(p1_remaininghp)+"/"+str(p1_hp)+" HP)\n"
                                        else:
                                            msg2,current_buffs_p1,current_buffs_p2,p1_remaininghp = self.check_if_cause_status(moveclass,moveid,msg2,current_buffs_p1,current_buffs_p2,p1_name,p2_name,p1_remaininghp,p1_hp)

                                if swapped == 1: #swaps back after reflection
                                    swapped = 0
                                    p1_remaininghp = p2_remaininghp
                                    p2 = p3
                                    p2_hp = p3_hp
                                    p2_name = p3_name
                                    p2_remaininghp = p3_remaininghp
                                    p1_stats,p2_stats = p2_stats, p1_stats
                                    current_buffs_p2temp = {}
                                    current_buffs_p2temp = deepcopy(current_buffs_p2)
                                    current_buffs_p2.clear()
                                    current_buffs_p2 = deepcopy(current_buffs_p1)
                                    current_buffs_p1.clear()
                                    current_buffs_p1 = deepcopy(current_buffs_p2temp)

                    if p2_remaininghp > 0: #if p2 is not fainted yet, check if p1 is burned or poisoned, then hceck if p1 fainted, then switch p1 and p2
                        if current_buffs_p1['statused'] == 1:
                            if current_buffs_p1['status'] == "burn":
                                burn_dmg = round(p1_hp/16)
                                p1_remaininghp -= burn_dmg
                                msg2 += "\n*"+p1_name + " lost " + str(burn_dmg) + " HP from the burn!* :fire: (" + str(round(burn_dmg / (p1_hp)*100)) + "\%) ("+str(p1_remaininghp)+"/"+str(p1_hp)+" HP)"
                            elif current_buffs_p1['status'] == "poison":
                                poison_dmg = round(p1_hp/8)
                                p1_remaininghp -= poison_dmg
                                msg2 += "\n*"+p1_name + " lost " + str(poison_dmg) + " HP from poison!* :skull_crossbones: (" + str(round(poison_dmg / (p1_hp)*100)) + "\%) ("+str(p1_remaininghp)+"/"+str(p1_hp)+" HP)"
                            if p1_remaininghp <=0:
                                msg2 += "\n***" + p1_name + " has fainted!***"

                    embed.add_field(name=msg1.replace("{}",p2_name), value=msg2, inline=False)
                    await self.bot.say(embed=embed)
                    await asyncio.sleep(2)

                if p2_remaininghp >0:
                    p1, p2 = p2, p1
                    p1_hp, p2_hp = p2_hp, p1_hp
                    p1_remaininghp, p2_remaininghp = p2_remaininghp, p1_remaininghp
                    p1_name, p2_name = p2_name, p1_name
                    p1_color, p2_color = p2_color, p1_color
                    p1_stats,p2_stats = p2_stats, p1_stats
                    current_buffs_p2temp = {}
                    current_buffs_p2temp = deepcopy(current_buffs_p2)
                    current_buffs_p2.clear()
                    current_buffs_p2 = deepcopy(current_buffs_p1)
                    current_buffs_p1.clear()
                    current_buffs_p1 = deepcopy(current_buffs_p2temp)

            except discord.errors.HTTPException:
                embed4=discord.Embed(description="Discord is being a bitch again and is throwing HTTP400 errors. \nThis battle may be bugged for the rest of its duration.")
                await self.bot.say(embed=embed4)
        if p2 == p1:
            embed = discord.Embed(color=p1_color,title=p1_name + " well played themselves! Congratulations!")
        else:
            prize = random.randint(50,200)
            p1_stats['win'] = p1_stats['win'] + 1
            p2_stats['lose'] = p2_stats['lose'] + 1
            if p2_stats['buff']-p1_stats['buff'] > 0:
                prize += int(1500*(p2_stats['buff']-p1_stats['buff']))
            if mode == "petvspet":
                embed = discord.Embed(color=p1_color,title=p1_name + " received " + str(prize) + " PMP for winning! Congratulations!\nThe PMP has been transferred to its owner.")
                self.owner_stats[p1.id]['money'] += prize
            if mode == "petvsboss":
                if p1 in self.bosses:
                    self.bosses[p1]['money'] += prize
                    embed = discord.Embed(color=p1_color,title=p1_name + " received " + str(prize) + " PMP for winning.")
                else:
                    prize += 1000
                    self.owner_stats[p1.id]['money'] += prize
                    embed = discord.Embed(color=p1_color,title=p1_name + " did well against a boss! It received an extra 1000 PMP for a total of " + str(prize) + " PMP for winning! Congratulations!\nThe PMP has been transferred to its owner.")
                self.save_boss_stats()
            if mode == "petvshuman":
                if p1_name == p1.display_name:
                    embed = discord.Embed(color=p1_color,title=p1_name + " received " + str(prize) + " PMP for winning! Congratulations!")
                else:
                    prize += 500
                    embed = discord.Embed(color=p1_color,title=p1_name + " did well against a human! It received an extra 500 PMP for a total of " + str(prize) + " PMP for winning! Congratulations!\nThe PMP has been transferred to its owner.")
                self.owner_stats[p1.id]['money'] += prize
            self.save_pet_stats()
            self.save_owner_stats()
        await self.bot.say(embed=embed)

    def check_if_cause_status(self,moveclass,moveid,msg2,current_buffs_p1,current_buffs_p2,p1_name,p2_name,p1_remaininghp,p1_hp):
        if self.moves[moveclass][moveid]['effect'] == "stat_self":
            raise_chance = random.randint(1,100)
            if raise_chance <= self.moves[moveclass][moveid]['affected_stat'][2]:
                current_buffs_p1[self.moves[moveclass][moveid]['affected_stat'][0]] += self.moves[moveclass][moveid]['affected_stat'][1]/100
                if current_buffs_p1[self.moves[moveclass][moveid]['affected_stat'][0]] == 0:
                    current_buffs_p1[self.moves[moveclass][moveid]['affected_stat'][0]] += 0.1
                if self.moves[moveclass][moveid]['affected_stat'][1] < 0:
                    veve = [":arrow_down: *"," fell by " ]
                else:
                    veve = [":arrow_up: *"," increased by "]
                msg2 += veve[0] + p1_name + "\'s " + self.stat_names[self.moves[moveclass][moveid]['affected_stat'][0]] + veve[1] + str(abs(self.moves[moveclass][moveid]['affected_stat'][1])) + "%!*"
        elif self.moves[moveclass][moveid]['effect'] == "stat_enemy":
            fall_chance = random.randint(1,100)
            if fall_chance <= self.moves[moveclass][moveid]['affected_stat'][2]:
                if self.moves[moveclass][moveid]['affected_stat'][1] < 0:
                    veve = [":arrow_down: *"," fell by "]
                else:
                    veve = [":arrow_up: *"," increased by "]
                current_buffs_p2[self.moves[moveclass][moveid]['affected_stat'][0]] += self.moves[moveclass][moveid]['affected_stat'][1]/100
                if current_buffs_p2[self.moves[moveclass][moveid]['affected_stat'][0]] == 0:
                    current_buffs_p2[self.moves[moveclass][moveid]['affected_stat'][0]] += 0.1
                msg2 += veve[0] + p2_name + "\'s " + self.stat_names[self.moves[moveclass][moveid]['affected_stat'][0]] + veve[1] + str(abs(self.moves[moveclass][moveid]['affected_stat'][1])) + "%!*"
        elif self.moves[moveclass][moveid]['effect'] == "cause_status":
            if current_buffs_p2['statused'] == 0: #check if move causes status
                status_chance = random.randint(1,100)
                if status_chance <= self.moves[moveclass][moveid]['status'][1]:
                    current_buffs_p2['statused'] = 1
                    current_buffs_p2['status'] = self.moves[moveclass][moveid]['status'][0]
                    if self.moves[moveclass][moveid]['status'][0] in ["confuse","sleep","freeze"]:
                        turns = random.randint(1,3)
                        current_buffs_p2['turns'] = turns
                    if current_buffs_p2['status'] == "confuse":
                        msg2 += "\n**"+ p2_name + " became confused!** :dizzy:"
                    elif current_buffs_p2['status'] == "poison":
                        msg2 += "\n**"+ p2_name + " was poisoned!** :skull_crossbones:"
                    elif current_buffs_p2['status'] == "burn":
                        msg2 +="\n**"+  p2_name + " was burned! **:fire:"
                    elif current_buffs_p2['status'] == "freeze":
                        msg2 += "\n**"+ p2_name + " was frozen solid! **:snowflake:"
                    elif current_buffs_p2['status'] == "para":
                        msg2 += "\n**"+  p2_name + " became paralysed! **:zap:"
                    elif current_buffs_p2['status'] == "sleep":
                        msg2 += "\n**"+  p2_name + " fell asleep! **:zzz:"
            else:
                msg2 += "It failed to inflict a status!"
        elif  self.moves[moveclass][moveid]['effect'] == "refresh":
            current_buffs_p1['status'] = "none"
            current_buffs_p1['statused'] = 0
            current_buffs_p1['turns'] = 0
            msg2 += p1_name + " healed their status conditions!"
        elif self.moves[moveclass][moveid]['effect'] == "heal":
            if p1_remaininghp == p1_hp:
                msg2 += p1_name + "\'s HP is full!"
            else:
                healed_hp = round(math.floor(self.moves[moveclass][moveid]['affected_stat'][1]*p1_hp/100))
                p1_remaininghp += healed_hp
                if p1_remaininghp > p1_hp:
                     p1_remaininghp = p1_hp
                msg2 += p1_name + " restored " + str(healed_hp) + " HP! (" + str(self.moves[moveclass][moveid]['affected_stat'][1]) + "%) ("+str(p1_remaininghp)+"/"+str(p1_hp)+" HP)\n"
        if self.moves[moveclass][moveid]['effect2'] == "stat_self":
            raise_chance = random.randint(1,100)
            if raise_chance <= self.moves[moveclass][moveid]['affected_stat'][5]:
                current_buffs_p1[self.moves[moveclass][moveid]['affected_stat'][3]] += self.moves[moveclass][moveid]['affected_stat'][4]/100
                if current_buffs_p1[self.moves[moveclass][moveid]['affected_stat'][3]] == 0:
                    current_buffs_p1[self.moves[moveclass][moveid]['affected_stat'][3]] += 0.1
                if self.moves[moveclass][moveid]['affected_stat'][4] < 0:
                    veve = ["\n:arrow_down: *"," fell by " ]
                else:
                    veve = ["\n:arrow_up: *"," increased by "]
                msg2 += veve[0] + p1_name + "\'s " + self.stat_names[self.moves[moveclass][moveid]['affected_stat'][3]] + veve[1] + str(abs(self.moves[moveclass][moveid]['affected_stat'][4])) + "%!*"
        elif self.moves[moveclass][moveid]['effect2'] == "stat_enemy":
            fall_chance = random.randint(1,100)
            if fall_chance <= self.moves[moveclass][moveid]['affected_stat'][5]:
                if self.moves[moveclass][moveid]['affected_stat'][4] < 0:
                    veve = [":arrow_down: *"," fell by "]
                else:
                    veve = [":arrow_up: *"," increased by "]
                current_buffs_p2[self.moves[moveclass][moveid]['affected_stat'][3]] += self.moves[moveclass][moveid]['affected_stat'][4]/100
                if current_buffs_p2[self.moves[moveclass][moveid]['affected_stat'][3]] == 0:
                    current_buffs_p2[self.moves[moveclass][moveid]['affected_stat'][3]] += 0.1
                msg2 += veve[0] + p2_name + "\'s " + self.stat_names[self.moves[moveclass][moveid]['affected_stat'][3]] + veve[1] + str(abs(self.moves[moveclass][moveid]['affected_stat'][4])) + "%!*"
        return msg2,current_buffs_p1,current_buffs_p2,p1_remaininghp

### END OF PET DUEL
    async def output_pet_stats(self, user, petid):
        embed=discord.Embed(title=self.pet_stats[user.id]['pets'][petid]['name'] + "\'s stats")
        embed.set_thumbnail(url=self.pet_stats[user.id]['pets'][petid]['image'])
        embed.set_image(url=self.pet_stats[user.id]['pets'][petid]['image'])
        embed.add_field(name="Name", value=self.pet_stats[user.id]['pets'][petid]['name'], inline=True)
        embed.add_field(name="Affection", value=self.pet_stats[user.id]['pets'][petid]['affection'], inline=True)
        embed.add_field(name="Hunger", value=self.pet_stats[user.id]['pets'][petid]['hunger'], inline=True)
        embed.add_field(name="Owner", value=user.display_name, inline=True)
        embed.add_field(name="Class", value=self.pet_stats[user.id]['pets'][petid]['stats']['class'], inline=True)
        embed.add_field(name="HP", value=str(self.pet_stats[user.id]['pets'][petid]['stats']['hp']) + " (in battle aprox. "+ str(100+ round(self.pet_stats[user.id]['pets'][petid]['stats']['hp']*1.75)) +")", inline=True)
        embed.add_field(name="Physical Attack", value=self.pet_stats[user.id]['pets'][petid]['stats']['atk'], inline=True)
        embed.add_field(name="Physcial Defense", value=self.pet_stats[user.id]['pets'][petid]['stats']['defe'], inline=True)
        embed.add_field(name="Special Attack", value=self.pet_stats[user.id]['pets'][petid]['stats']['spa'], inline=True)
        embed.add_field(name="Special Defense", value=self.pet_stats[user.id]['pets'][petid]['stats']['spd'], inline=True)
        embed.add_field(name="Speed", value=self.pet_stats[user.id]['pets'][petid]['stats']['spe'], inline=True)
        embed.add_field(name="Buff Level", value=self.pet_stats[user.id]['pets'][petid]['stats']['buff'], inline=True)
        bst0 = self.pet_stats[user.id]['pets'][petid]['stats']['hp'] + self.pet_stats[user.id]['pets'][petid]['stats']['atk'] +self.pet_stats[user.id]['pets'][petid]['stats']['defe'] +self.pet_stats[user.id]['pets'][petid]['stats']['spa']+self.pet_stats[user.id]['pets'][petid]['stats']['spd'] +self.pet_stats[user.id]['pets'][petid]['stats']['spe']
        embed.add_field(name="Base Stat Total", value=bst0, inline=True)
        if self.pet_stats[user.id]['pets'][petid]['stats']['type1'] != self.pet_stats[user.id]['pets'][petid]['stats']['type2']:
            embed.add_field(name="Types", value=self.pet_stats[user.id]['pets'][petid]['stats']['type1'] + ", " + self.pet_stats[user.id]['pets'][petid]['stats']['type2'], inline=True)
        else:
            embed.add_field(name="Types", value=self.pet_stats[user.id]['pets'][petid]['stats']['type1'], inline=True)
        cmtfot = random.choice(['Được nâng niu như nâng trứng.','Dễ thương thuộc top quả đất.','Lúc nào cũng đói.'])
        embed.set_footer(text=cmtfot)
        await self.bot.say(embed=embed)


def setup(bot):
    n = Pets(bot)
    bot.add_cog(n)
