from discord.ext import commands
import random
import discord
from random import randint
from random import choice as randchoice
import re
import requests
from cogs.utils.dataIO import dataIO
from .utils.dataIO import fileIO

class Engine:
    """leavin you in the dust!"""

    def __init__(self, bot):
        self.bot = bot
        self.people = dataIO.load_json("data/engine/people.json")
        self.charas = self.people["charas"]
        self.actions = self.people["actions"]
        self.songs = self.people["songs"]

    @commands.command(pass_context=True)
    async def deletjson(self, ctx):
        requests.delete('https://api.jsonbin.io/b/5b080e2fc2e3344ccd96c120',headers={'secret-key':'$2a$10$IXFUMwjYBlG.b3YdVhXrXO7CBuvGiW18GE9aqg8PoCFEBeQKMTRvy'})
        await self.bot.say("ok.")

    @commands.command(pass_context=True)
    async def vroom(self, ctx):
        """You don't need no instruction manual to be free!!"""
        embed=discord.Embed(color=0xe90169) #start battle
        embed.add_field(name="jhasdjads", value="jasndj", inline=False)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def soulmate(self, ctx, gender :str =None,*,victim:str=None):
        """;soulmate [male/female] [victim's name]"""
        ge =" "
        msg=""
        choice = str(randchoice(self.charas[0]+self.charas[1]))
        if victim!=None:
            nem = victim
        elif ctx.message.author.nick:
            nem = ctx.message.author.nick
        else:
            nem = ctx.message.author.name
        if gender!=None:
            troll = randint(1,100)
            if gender.lower() == "m" or gender.lower() == "male":
                if troll > 7:
                    choice = str(randchoice(self.charas[0]))
                    ge = ge + "nam"
                else:
                    choice = str(randchoice(self.charas[1]))
                    ge = ge + "nữ"
                    msg= msg + "Kiếm nam hoài không chán ư, sao không thử đổi vị 1 chút? "
            elif gender.lower() == "f" or gender.lower() == "female":
                if troll > 7:
                    choice = str(randchoice(self.charas[1]))
                    ge = ge + "nữ"
                else:
                    choice = str(randchoice(self.charas[0]))
                    ge = ge + "nam"
                    msg= msg + "Kiếm nữ hoài không chán ư, sao không thử đổi vị 1 chút? "
            else:
                if victim!=None:
                    nem = gender + " " + nem
                else:
                    nem = gender
                ge = ""
        else:
            ge = ""
        if ctx.message.author.id == "343674681829621761":
            if randint(1,10) > 7:
                choice = "Bram Greenfeld"
        if randint(2,100) < 9:
            choice = "không ai cả"
        msg = msg + "Người" + ge +" hợp với " + nem + " là " + choice
        if choice == "không ai cả":
            if ge!="":
                if ge == " nam":
                    msg = msg + " Nhưng nếu là nữ thì có " + str(randchoice(self.charas[1])) + " hợp đó."
                elif ge == " nữ":
                    msg = msg + " Nhưng nếu là nam thì có " + str(randchoice(self.charas[0])) + " hợp đó."
            else:
                msg = msg + ". Thôi FA suốt đời đi là vừa."
        else:
            action = str(randchoice(self.actions))
            if action == "hát":
                song = str(randchoice(self.songs))
                action = action + " " + song
            msg = msg + ". Các bạn nên " + action + " đi."
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True, name='rate')
    async def rate(self, ctx, *, rate:str = None):
        """Đánh giá thứ gì đó theo thang điểm 100."""
        if rate != None:
            score = randint(-1,101)
            special = randint(1,100)
            if score/100 < 0:
                cmt = randchoice(["Thảm hại chưa cưng","thôi đi nhảy cầu đi","tởm","ewwwwwww","<:ro:437654455505125406>"])
            elif score == 0:
                cmt = randchoice(["muhaahAhAhaHHahha",":smile:","Nice","<:ro:437654455505125406>"])
            elif 0 < score/100 < 0.18:
                cmt = randchoice(["tệ vl","Thôi bỏ đi cưng","rác rưởi","thứ rẻ rách","eww","đứa nào tính slash ship hả?","<:ro:437654455505125406>"])
            elif score/100 < 0.35:
                cmt = randchoice(["could be better","muốn thử lại hông?","rác vl","vd","<:kuk:438360479275155456>"])
            elif score/100 < 0.5:
                cmt = randchoice(["meh","tàm tạm","ít ra gần trung bình rồi","chấp nhận được","duh","<:doge:379114406099025920>"])
            elif score/100 < 0.75:
                cmt = randchoice(["cũng ok","có triển vọng","ít ra trên trung bình rồi","có tiềm năng","mm hmm","<:thatbooty:378887011744088064>"])
            elif score/100 < 0.9:
                cmt = randchoice(["Có vẻ tốt","khá đấy","Nai xừ <:dep:379728193558413312>","khá ổn","ghê chưa"])
            elif score/100 < 1:
                cmt = randchoice(["Ghê lun","Hay","Hài lòng chưa?","đứa nào nói rig ta chửi","mood tốt nên cho tốt đó","đù <:dep:379728193558413312>","vl cao"])
            else:
                cmt = randchoice(["Purrfecttttt","VÃI LỜ","Ghê ghê ghê","Đù <:dep:379728193558413312>","Ahahahahahhha","sắp có người ghen tị <:yin:442214143483838464>","kiểu gì cũng có đứa kêu rigged"])
            if special < 3:
                score = 1000
                cmt = randchoice(["SAIKOU DESU WA","A ĐÙ LIT VCL","Gk3^^^^^^^","UNSTOPPABLE"])
            elif special == 100 or re.search('mil',rate):
                score = 9001
                cmt = "IT'S OVER 9000!!!!"
            await self.bot.say(rate + ": " + str(score) + "/100. " + cmt)
        else:
            if ctx.message.author.nick:
                nem = ctx.message.author.nick
            else:
                nem = ctx.message.author.name
            await self.bot.say(nem + ": " + str(randint(0,101)) + "/100.")

    @commands.command(pass_context=True, no_pm=True, name='rank')
    async def rank(self, ctx, *, text:str=None):
        """Đánh giá nhiều thứ gì đó ;rank 1;2;3;4;5"""
        if not re.search(';',str(text)):
            await self.bot.say("input something more, dumbass")
        else:
            rank = text.split(";")
            random.shuffle(rank)
            msg = " > ".join(str(x) for x in rank)
            await self.bot.say(msg)



def setup(bot):
    bot.add_cog(Engine(bot))
