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
        self.moves_url = requests.get("https://api.jsonbin.io/b/5b080ed07a973f4ce5784717/latest")
        self.stats = self.stats_url.json()
        self.moves = self.moves_url.json()
        self.types = dataIO.load_json('data/magic/types.json')
        self.typelist = ["Light","Normal","Fire","Fighting","Water","Flying","Grass","Poison","Electric","Ground","Psychic","Rock","Ice","Bug","Dragon","Ghost","Dark","Steel","Fairy"]
        self.errornotexist = "One or both of you do not have stats in the database! Set your stats using ``;stat`` first."
        self.classes = ["all","pokemon","sakura","harrypotter","new","sailormoon"]

    def save_stats(self):
        requests.put("https://api.jsonbin.io/b/5b081b310fb4d74cdf23e613", json=self.stats)


    @commands.command(pass_context=True)
    async def attack(self, ctx, *,target=None):
        if not target:
            await self.bot.say("Please specify target.")
        elif target.strip('<>@!') not in self.stats:
             await self.bot.say("Invalid opponent.")
        elif target.strip('<>@!') == ctx.message.author.id:
            await self.bot.say("Trying to cheat PMP??")
        elif str(ctx.message.author.id) not in self.stats or target.strip('<>@!') not in self.stats:
            await self.bot.say(self.errornotexist)
        else:
            p1 = ctx.message.author.id
            p1_name = ctx.message.author.display_name
            p1_color = ctx.message.author.color
            if target[0] != '<':
                p2 = target
                p2_name = self.stats[p2]['displayname']
                p2_color = 0xbd1540
            else:
                #server = discord.Client.get_server(id="378799662557036546")
                p2u = ctx.message.author.server.get_member(target.strip('<>@!'))
                p2 = str(p2u.id)
                p2_color = p2u.color
                p2_name = p2u.display_name
            embed=discord.Embed(title=":sparkles: **Magical Duel Starts** :sparkles:", color=0xe90169) #start battle
            p1_hp = 100+round(self.stats[p1]['hp']*round(random.uniform(1.5,2), 2))
            p2_hp = 100+round(self.stats[p2]['hp']*round(random.uniform(1.5,2), 2))
            p1_remaininghp = p1_hp
            p2_remaininghp = p2_hp
            #user_status
            if self.stats[p1]['spe'] < self.stats[p2]['spe']:
                embed.add_field(name=p1_name + " tries to attack!", value="*"+p2_name + " goes first due to higher Speed!*", inline=True)
                p1, p2 = p2, p1
                p1_hp, p2_hp = p2_hp, p1_hp
                p1_name, p2_name = p2_name, p1_name
                p1_remaininghp, p2_remaininghp = p2_remaininghp, p1_remaininghp
                p1_color, p2_color = p2_color, p1_color
            await self.bot.say(embed=embed)
            while p2_remaininghp > 0:
                embed=discord.Embed(color=p1_color)
                msg2 = ""
                if self.stats[p1]['class'] == "all":
                    moveclass = random.choice(["pokemon","sakura","harrypotter","new","sailormoon"])
                else:
                    moveclass = self.stats[p1]['class']
                moveid = str(random.randint(1,len(self.moves[moveclass])))
                if moveclass == "harrypotter" or moveclass == "sakura":
                    verb = "cast"
                else:
                    verb = "used"
                msg1 = "**"+p1_name + "** "+ verb +" **"+ self.moves[moveclass][moveid]['name']+"** " + self.types[self.moves[moveclass][moveid]['type']]['icon']
                if self.moves[moveclass][moveid]['effect']:
                    msg1 = msg1 +" to "+ self.moves[moveclass][moveid]['effect'] + "!\n"
                else:
                    msg1 = msg1 +"!\n"
                power = random.randint(self.moves[moveclass][moveid]['power']-self.moves[moveclass][moveid]['random'],self.moves[moveclass][moveid]['power']+self.moves[moveclass][moveid]['random'])
                if self.moves[moveclass][moveid]['category'] == "Physical":
                    atk = self.stats[p1]['atk']
                    defe = self.stats[p2]['defe']
                else:
                    atk = self.stats[p1]['spa']
                    defe = self.stats[p2]['spd']
                if self.moves[moveclass][moveid]['type'] in self.types[self.stats[p2]['type1']]['supereffective']:
                    mul = 2
                elif self.moves[moveclass][moveid]['type'] in self.types[self.stats[p2]['type1']]['notveryeffective']:
                    mul = 0.5
                elif self.moves[moveclass][moveid]['type'] in self.types[self.stats[p2]['type1']]['noteffective']:
                    mul = 0
                else:
                    mul = 1
                if self.moves[moveclass][moveid]['type'] in self.types[self.stats[p2]['type2']]['supereffective']:
                    mul = mul * 2
                elif self.moves[moveclass][moveid]['type'] in self.types[self.stats[p2]['type2']]['notveryeffective']:
                    mul = mul * 0.5
                elif self.moves[moveclass][moveid]['type'] in self.types[self.stats[p2]['type2']]['noteffective']:
                    mul = 0
                if self.moves[moveclass][moveid]['type'] == self.stats[p1]['type1'] or self.moves[moveclass][moveid]['type'] == self.stats[p1]['type2']:
                    power = power * 1.5
                if mul >1:
                    msg2 = msg2 + ":small_red_triangle: It's super effective! \n"
                elif 0 <mul <1:
                    msg2 = msg2 + ":small_red_triangle_down: It's not very effective... \n"
                elif 0 == mul:
                    msg2 = msg2 + ":x: It had no effect!\n"
                if mul > 0:
                    msg2 = msg2 + p2_name + " took "
                    rand = 0.01*random.randint(75,115)
                    dmg = round(math.floor(math.floor(75  * power * atk / defe) / 50) + 2 * mul * rand)
                    p2_remaininghp = p2_remaininghp - dmg
                    msg2 = msg2 + str(dmg) + " damage! (" + str(round(dmg / (p2_hp)*100)) + "\%) ("+str(p2_remaininghp)+"/"+str(p2_hp)+" HP)\n"
                    if p2_remaininghp <= 0:
                        msg2 = msg2  + "\n***" + p2_name + " has fainted!***"
                embed.add_field(name=msg1.replace("{}",p2_name), value=msg2, inline=False)
                if p2_remaininghp > 0:
                    p1, p2 = p2, p1
                    p1_hp, p2_hp = p2_hp, p1_hp
                    p1_remaininghp, p2_remaininghp = p2_remaininghp, p1_remaininghp
                    p1_name, p2_name = p2_name, p1_name
                    p1_color, p2_color = p2_color, p1_color
                await self.bot.say(embed=embed)
                await asyncio.sleep(2)
            prize = random.randint(50,200)
            if self.stats[p2]['buff']-self.stats[p1]['buff'] > 0:
                prize += int(1500*(self.stats[p2]['buff']-self.stats[p1]['buff']))
            embed = discord.Embed(color=p1_color,title=p1_name + " received " + str(prize) + " PMP for winning! Congratulations!")
            self.stats[p1]['money'] = self.stats[p1]['money'] + prize
            self.stats[p1]['win'] = self.stats[p1]['win'] + 1
            self.stats[p2]['lose'] = self.stats[p2]['lose'] + 1
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
    async def showboss(self, ctx, *,target=None):
        if target:
            if target in self.stats:
                user = target
                await self.output_stats_nonmember(user)
            else:
                await self.bot.say("Stats were not found!")
        else:
            await self.bot.say("No bosses specified")

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
        self.stats[user.id] = {'hp': 60, 'atk': 60, 'defe': 60, 'spa': 60, 'spd': 60, 'spe': 60, 'class': "all", 'bst': 450, 'money': 0, 'item': 0,
                               'type1':"Normal",'type2':"Normal",'win':0,'lose':0, 'buff':0}
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
                                    'type1':"Normal",'type2':"Normal",'win':0,'lose':0, 'buff':0}
        buff = self.stats[user.id]['buff'] * 10
        while True:
            self.stats[user.id]['hp'] = random.randint(40+buff/2,120+buff)
            self.stats[user.id]['atk'] = random.randint(30+buff/2,120+buff)
            self.stats[user.id]['defe'] = random.randint(30+buff/2,120+buff)
            self.stats[user.id]['spa'] = random.randint(30+buff/2,120+buff)
            self.stats[user.id]['spd'] = random.randint(30+buff/2,120+buff)
            self.stats[user.id]['spe'] = random.randint(30+buff/2,120+buff)
            bst0 = self.stats[user.id]['hp'] + self.stats[user.id]['atk'] +self.stats[user.id]['defe'] +self.stats[user.id]['spa']+self.stats[user.id]['spd'] +self.stats[user.id]['spe']
            if  self.stats[user.id]['bst'] >= bst0 > (self.stats[user.id]['bst']-(30+buff)):
                break
        self.stats[user.id]['class'] = random.choice(self.classes)
        self.stats[user.id]['type1'] = random.choice(self.typelist)
        self.stats[user.id]['type2'] = random.choice(self.typelist)
        self.save_stats()
        await self.output_stats(ctx,user)


    @stat.command(pass_context=True)
    async def set(self, ctx, hp:int=1, atk:int=1, defe:int=1, spa:int=1, spd:int=1, spe:int=1, target:discord.Member=None):
        user= ctx.message.author
        limit = 140+self.stats[user.id]['buff']*10
        if target:
            if user.id != self.ownerid:
                await self.bot.say("Not authorized to do this.")
        else:
            if user.id not in self.stats:
                self.stats[user.id] = {'hp': 1, 'atk': 1, 'defe': 1, 'spa': 1, 'spd': 1, 'spe': 1,'class': "all", 'bst': 400, 'money': 0, 'item': 0, 'type1':"Normal",'type2':"Normal"}
                self.save_stats()
            if atk + defe +spa +spd +spe +hp > self.stats[user.id]['bst']:
                await self.bot.say("Too OP! BST should be no more than your max BST of " + str(self.stats[user.id]['bst']) + ".")
            elif atk > limit or defe > limit or spa > limit or spd > limit or spe > limit or hp > limit:
                await self.bot.say("Too OP! Any  one stat should be no more than " + str(limit) + ".")
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
        embed.add_field(name="Buff Level", value=self.stats[user.id]['buff'], inline=True)
        bst0 = self.stats[user.id]['hp'] + self.stats[user.id]['atk'] +self.stats[user.id]['defe'] +self.stats[user.id]['spa']+self.stats[user.id]['spd'] +self.stats[user.id]['spe']
        embed.add_field(name="Base Stat Total", value=bst0, inline=True)
        if self.stats[user.id]['type1'] != self.stats[user.id]['type2']:
            embed.add_field(name="Types", value=self.stats[user.id]['type1'] + ", " + self.stats[user.id]['type2'], inline=True)
        else:
            embed.add_field(name="Types", value=self.stats[user.id]['type1'], inline=True)
        #embed.set_footer(text=".")
        await self.bot.say(content=user.display_name + "\'s stats are:", embed=embed)

    async def output_stats_nonmember(self, user):
        embed=discord.Embed(title=self.stats[user]['displayname'] + "\'s stats")
        #embed.set_thumbnail(url=self.stats[user]['pic'])
        embed.add_field(name="Class", value=self.stats[user]['class'], inline=True)
        embed.add_field(name="HP", value=str(self.stats[user]['hp']) + " (in battle aprox. "+ str(100+ round(self.stats[user]['hp']*1.75)) +")", inline=True)
        embed.add_field(name="Physical Attack", value=self.stats[user]['atk'], inline=True)
        embed.add_field(name="Physcial Defense", value=self.stats[user]['defe'], inline=True)
        embed.add_field(name="Special Attack", value=self.stats[user]['spa'], inline=True)
        embed.add_field(name="Special Defense", value=self.stats[user]['spd'], inline=True)
        embed.add_field(name="Speed", value=self.stats[user]['spe'], inline=True)
        embed.add_field(name="Buff Level", value=self.stats[user]['buff'], inline=True)
        bst0 = self.stats[user]['hp'] + self.stats[user]['atk'] +self.stats[user]['defe'] +self.stats[user]['spa']+self.stats[user]['spd'] +self.stats[user]['spe']
        embed.add_field(name="Base Stat Total", value=bst0, inline=True)
        if self.stats[user]['type1'] != self.stats[user]['type2']:
            embed.add_field(name="Types", value=self.stats[user]['type1'] + ", " + self.stats[user]['type2'], inline=True)
        else:
            embed.add_field(name="Types", value=self.stats[user]['type1'], inline=True)
        #embed.set_footer(text=".")
        await self.bot.say(content=self.stats[user]['displayname'] + "\'s stats are:", embed=embed)

    @commands.command(pass_context=True)
    async def upgrade(self, ctx):
        user = ctx.message.author
        price = 50 + (self.stats[user.id]['buff']**2)*2500
        await self.bot.say("You currently have buff **level " + str(self.stats[user.id]['buff']) +"** with a max BST of **" + str(self.stats[user.id]['bst']) + "**. Would you like to purchase a buff for **" + str(price) + "** PMP?\n"
                            + "A buff will increase your BST by **50**, and min and max stat random value by **5** and **10**. Type *yes* to confirm. (30s)")
        answer = await self.bot.wait_for_message(timeout=30, author=ctx.message.author)
        if answer is None:
            await self.bot.say('Purchase cancelled due to timeout.')
            return
        elif "yes" not in answer.content.lower():
            await self.bot.say('Well? Okay then.')
            return
        else:
            if self.stats[user.id]['money'] < price:
                await self.bot.say("You don't have enough PMP!")
            else:
                self.stats[user.id]['buff'] = self.stats[user.id]['buff'] + 1
                self.stats[user.id]['bst'] = self.stats[user.id]['bst'] +50
                self.stats[user.id]['money'] = self.stats[user.id]['money'] - price
                self.save_stats()
                await self.bot.say("Purchase success. You now have buff level **" + str(self.stats[user.id]['buff']) +"** with a max BST of **" + str(self.stats[user.id]['bst']) + "**.\n"
                                   + "Your random value has been increased to **min " + str(30+self.stats[user.id]['buff']*5) + ", max " + str((120+self.stats[user.id]['buff']*10)) + "**.")

    @commands.command(pass_context=True)
    async def moveinfo(self, ctx, *, move:str=None):
        if move:
            found = 0
            for i in self.moves: #for every class
                for j in self.moves[i]: #for every move j in class i
                    if self.moves[i][j]['name'].lower() == move.lower(): #compare
                        found = 1
                        embed=discord.Embed(title=self.moves[i][j]['name'] + "\'s info")
                        #embed.set_thumbnail(url=user.avatar_url) #to be edited
                        embed.add_field(name="Class", value=str(i), inline=True)
                        embed.add_field(name="Category", value=self.moves[i][j]['category'], inline=True)
                        if self.moves[i][j]['random'] > 0:
                            rara = " ± " + str(self.moves[i][j]['random'])
                        else:
                            rara = ""
                        embed.add_field(name="Power", value=str(self.moves[i][j]['power']) + rara, inline=True)
                        #embed.add_field(name="Accuracy", value=str(self.moves[i][j]['acc']), inline=True) TBA
                        embed.add_field(name="Type", value=self.moves[i][j]['type'] + " " + self.types[self.moves[i][j]['type']]['icon'], inline=True)
                        embed.add_field(name="Origin", value=self.moves[i][j]['origin'], inline=True)
                        #embed.add_field(name="Speed", value=self.stats[user.id]['spe'], inline=True) unuused
                        await self.bot.say(embed=embed)
            if found == 0:
                await self.bot.say("No such move.")
        else:
            await self.bot.say("No move specified.")
#self.moves[moveclass][moveid]['power']

    @commands.command(pass_context=True)
    async def setclass(self, ctx):
        user= ctx.message.author
        await self.bot.say('Currently available classes are and the following: ' + str(self.classes) + ". Type a class name to change to.")
        answer = await self.bot.wait_for_message(timeout=30, author=ctx.message.author)
        if answer is None:
            await self.bot.say('Purchase cancelled due to timeout.')
            return
        elif answer.content.lower() not in self.classes:
            await self.bot.say('Invalid class.')
            return
        else:
            self.stats[user.id]['class'] = str(answer.content)
            self.save_stats()
            await self.bot.say('Successfully changed class.')

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
