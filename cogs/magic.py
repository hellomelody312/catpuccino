import discord
import asyncio
from discord.ext import commands
from .utils.dataIO import dataIO
import random
import os
import math
import requests
import json
from copy import deepcopy


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
        self.classes = ["all","pokemon","sakura","harrypotter","ffxv","sailormoon","test2","test1","test3"]
        self.p1_buffs ={"atk":1,"defe":1,"spa":1,"spd":1,"acc":1,"statused":0,"status":"none","turns":0,"protected":0,"reflected":0}
        self.p2_buffs ={"atk":1,"defe":1,"spa":1,"spd":1,"acc":1,"statused":0,"status":"none","turns":0,"protected":0,"reflected":0}
        self.statuses = ["poison","burn","flinch","confused","reflect","protect","freeze","para","sleep"]
        self.stat_names = {"atk":"Attack","defe":"Defense","spa":"Special Attack","spd":"Special Defense","acc":"Accuracy"}


    def save_stats(self):
        requests.put("https://api.jsonbin.io/b/5b081b310fb4d74cdf23e613", json=self.stats)


    @commands.command(pass_context=True)
    async def duel(self, ctx, *,target=None):
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
                p2_color = self.stats[p2]['color']
            else:
                p2u = ctx.message.author.server.get_member(target.strip('<>@!'))
                p2 = str(p2u.id)
                p2_color = p2u.color
                p2_name = p2u.display_name
            embed=discord.Embed(title=":sparkles: **Magical Duel Starts** :sparkles:", color=0xe90169) #start battle
            p1_hp = 100+round(self.stats[p1]['hp']*round(random.uniform(1.5,2), 2))
            p2_hp = 100+round(self.stats[p2]['hp']*round(random.uniform(1.5,2), 2))
            p1_remaininghp = p1_hp
            p2_remaininghp = p2_hp
            current_buffs_p1 = dict(self.p1_buffs)
            current_buffs_p2 = dict(self.p2_buffs)
            #user_status
            if self.stats[p1]['spe'] < self.stats[p2]['spe']:
                embed.add_field(name=p1_name + " tries to attack!", value="*"+p2_name + " goes first due to higher Speed!*", inline=True)
                p1, p2 = p2, p1
                p1_hp, p2_hp = p2_hp, p1_hp
                p1_name, p2_name = p2_name, p1_name
                p1_remaininghp, p2_remaininghp = p2_remaininghp, p1_remaininghp
                p1_color, p2_color = p2_color, p1_color
            await self.bot.say(embed=embed)
            while p2_remaininghp > 0 and p1_remaininghp > 0:
                try:

                    msg2 = ""
                    msg1 = ""
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
                                    confuse_dmg = round(math.floor(math.floor(50  * 50 * self.stats[p1]['atk'] / self.stats[p1]['defe']) / 50) + 2)
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
                        if self.stats[p1]['class'] == "all": #detect class
                            moveclass = random.choice(["pokemon","sakura","harrypotter","ffxv","sailormoon","test"])
                        else:
                            moveclass = self.stats[p1]['class']
                        moveid = str(random.randint(1,len(self.moves[moveclass]))) #choose move
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
                                if  self.moves[moveclass][moveid]['effect'] == "protect":
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
                                        #swapped = 1
                                        msg2 += p2_name + " reflected the attack!\n"
                                        p3 = p2
                                        p2 = p1
                                        p3_hp = p2_hp
                                        p2_hp = p1_hp
                                        p3_name = p2_name
                                        p2_name = p1_name
                                        p3_remaininghp = p2_remaininghp
                                        p2_remaininghp = p1_remaininghp
                                        current_buffs_p2temp = {}
                                        current_buffs_p2temp = deepcopy(current_buffs_p2)
                                        current_buffs_p2.clear()
                                        current_buffs_p2 = deepcopy(current_buffs_p1)
                                        current_buffs_p1.clear()
                                        current_buffs_p1 = deepcopy(current_buffs_p2temp)
                                    if self.moves[moveclass][moveid]['category'] == "Physical":
                                        if current_buffs_p1['status'][0] == "burn":
                                            atk = self.stats[p1]['atk']*0.5*current_buffs_p1['atk']
                                        else:
                                            atk = self.stats[p1]['atk']*current_buffs_p1['atk']
                                        defe = self.stats[p2]['defe']*current_buffs_p2['defe']
                                    else:
                                        atk = self.stats[p1]['spa']*current_buffs_p1['spa']
                                        defe = self.stats[p2]['spd']*current_buffs_p2['spd']
                                    mul = 1
                                    for typy in ['type1','type2']: #check type effectiveness
                                        if self.moves[moveclass][moveid]['type'] in self.types[self.stats[p2][typy]]['supereffective']:
                                            mul *= 2
                                        elif self.moves[moveclass][moveid]['type'] in self.types[self.stats[p2][typy]]['notveryeffective']:
                                            mul *= 0.5
                                        elif self.moves[moveclass][moveid]['type'] in self.types[self.stats[p2][typy]]['noteffective']:
                                            mul *= 0
                                    if self.moves[moveclass][moveid]['type'] in [self.stats[p1]['type1'],self.stats[p1]['type2']]: #check STAB
                                        power *= 1.5
                                    if mul >1:
                                        msg2 = msg2 + ":small_red_triangle: It's super effective! \n"
                                    elif 0 <mul <1:
                                        msg2 = msg2 + ":small_red_triangle_down: It's not very effective... \n"
                                    elif 0 == mul:
                                        msg2 = msg2 + ":x: It had no effect!\n"
                                    if mul > 0:
                                        rand = 0.01*random.randint(85,115)
                                        dmg = round(math.floor(math.floor(90  * power * atk / defe) / 50) + 2 * mul * rand)
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
                                            elif self.moves[moveclass][moveid]['effect'] == "drain":
                                                drain_dmg =  round(dmg *self.moves[moveclass][moveid]['affected_stat'][1]/100)
                                                p1_remaininghp += drain_dmg
                                                msg2 += p1_name + " drained " + str(drain_dmg) + " HP! (" + str(round(drain_dmg / (p1_hp)*100)) + "\%) ("+str(p1_remaininghp)+"/"+str(p1_hp)+" HP)\n"
                                            else:
                                                msg2,current_buffs_p1,current_buffs_p2,p1_remaininghp = self.check_if_cause_status(moveclass,moveid,msg2,current_buffs_p1,current_buffs_p2,p1_name,p2_name,p1_remaininghp,p1_hp)

                                    if current_buffs_p2['reflected'] == 1: #swaps back after reflection
                                        current_buffs_p2['reflected'] = 0
                                        p1_remaininghp = p2_remaininghp
                                        p2 = p3
                                        p2_hp = p3_hp
                                        p2_name = p3_name
                                        p2_remaininghp = p3_remaininghp
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
                            p1, p2 = p2, p1
                            p1_hp, p2_hp = p2_hp, p1_hp
                            p1_remaininghp, p2_remaininghp = p2_remaininghp, p1_remaininghp
                            p1_name, p2_name = p2_name, p1_name
                            p1_color, p2_color = p2_color, p1_color

                            current_buffs_p2temp = {}
                            current_buffs_p2temp = deepcopy(current_buffs_p2)
                            current_buffs_p2.clear()
                            current_buffs_p2 = deepcopy(current_buffs_p1)
                            current_buffs_p1.clear()
                            current_buffs_p1 = deepcopy(current_buffs_p2temp)
                        embed.add_field(name=msg1.replace("{}",p2_name), value=msg2, inline=False)
                        await self.bot.say(embed=embed)
                        await asyncio.sleep(2)
                    else:
                        p1, p2 = p2, p1
                        p1_hp, p2_hp = p2_hp, p1_hp
                        p1_remaininghp, p2_remaininghp = p2_remaininghp, p1_remaininghp
                        p1_name, p2_name = p2_name, p1_name
                        p1_color, p2_color = p2_color, p1_color

                        current_buffs_p2temp = {}
                        current_buffs_p2temp = deepcopy(current_buffs_p2)
                        current_buffs_p2.clear()
                        current_buffs_p2 = deepcopy(current_buffs_p1)
                        current_buffs_p1.clear()
                        current_buffs_p1 = deepcopy(current_buffs_p2temp)

                except discord.errors.HTTPException:
                    embed4=discord.Embed(description="Discord is being a bitch again and is throwing HTTP400 errors. \nThis battle may be bugged for the rest of its duration.")
                    await self.bot.say(embed=embed4)
            prize = random.randint(50,200)
            if self.stats[p2]['buff']-self.stats[p1]['buff'] > 0:
                prize += int(1500*(self.stats[p2]['buff']-self.stats[p1]['buff']))
            embed = discord.Embed(color=p1_color,title=p1_name + " received " + str(prize) + " PMP for winning! Congratulations!")
            self.stats[p1]['money'] = self.stats[p1]['money'] + prize
            self.stats[p1]['win'] = self.stats[p1]['win'] + 1
            self.stats[p2]['lose'] = self.stats[p2]['lose'] + 1
            self.save_stats()
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
        elif self.moves[moveclass][moveid]['effect'] == "cause_status" and current_buffs_p2['statused'] == 0: #check if move causes status
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

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def getpmp(self, ctx):
        user = ctx.message.author
        randomp = random.randint(1,100)
        if randomp > 50:
            get = 100
        elif randomp > 25:
            get = 500
        elif randomp > 10:
            get = 1000
        elif random >1:
            get = 5000
        else:
            get = 10000
        self.stats[user.id]['money'] += get
        self.save_stats()
        await self.bot.say("You got " + str(get) + " PMP for free! Try again in 1 hour.")



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
        embed=discord.Embed(title=self.stats[user]['displayname'] + "\'s stats", color=self.stats[user]['color'])
        embed.set_thumbnail(url=self.stats[user]['pic'])
        #embed.set_image(url=self.stats[user]['pic'],height=300,width=300)
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
                        if self.moves[i][j]['image']:
                            embed.set_image(url=self.moves[i][j]['image'])
                        #embed.set_thumbnail(url=self.moves[i][j]['image']) #to be edited
                        embed.add_field(name="Class", value=str(i), inline=True)
                        embed.add_field(name="Category", value=self.moves[i][j]['category'], inline=True)
                        if self.moves[i][j]['random'] > 0:
                            rara = " ± " + str(self.moves[i][j]['random'])
                        else:
                            rara = ""
                        embed.add_field(name="Power", value=str(self.moves[i][j]['power']) + rara, inline=True)
                        embed.add_field(name="Accuracy", value=str(self.moves[i][j]['acc']), inline=True)
                        embed.add_field(name="Type", value=self.moves[i][j]['type'] + " " + self.types[self.moves[i][j]['type']]['icon'], inline=True)
                        embed.add_field(name="Origin", value=self.moves[i][j]['origin'], inline=True)
                        embed.add_field(name="Description", value=self.moves[i][j]['info'], inline=False)
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
            await self.bot.say('Cancelled due to timeout.')
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
