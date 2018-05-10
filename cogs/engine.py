from discord.ext import commands
import random
from random import randint
from random import choice as randchoice
import re
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
    async def vroom(self, ctx):
        """You don't need no instruction manual to be free!!"""
        await self.bot.say("VROOM VROOM!")

    @commands.command(pass_context=True)
    async def soulmate(self, ctx, gender :str =None,*,victim:str=None):
        """You don't need no instruction manual to be free!!"""
        if victim!=None:
            nem = victim
        elif ctx.message.author.nick:
            nem = ctx.message.author.nick
        else:
            nem = ctx.message.author.name
        if gender!=None:
            ge = " "
            if gender.lower() == "m" or gender.lower() == "male":
                choice = str(randchoice(self.charas[0]))
                ge = ge + "nam"
            elif gender.lower() == "f" or gender.lower() == "female":
                choice = str(randchoice(self.charas[1]))
                ge = ge + "nữ"
            else:
                choice = str(randchoice(self.charas[0]+self.charas[1]))
                nem = gender + nem
        if ctx.message.author.id == "343674681829621761":
            if randint(1,10) > 5:
                choice = "Bram Grenfeld"
        action = str(randchoice(self.actions))
        if action == "hát":
            song = str(randchoice(self.songs))
            action = action + " " + song
        await self.bot.say("Người" + ge +" hợp với " + nem + " là " + choice + ". Các bạn nên " + action + " đi.")

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
