from discord.ext import commands
import random
from random import randint
from random import choice as randchoice
import re

class Engine:
    """leavin you in the dust!"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def vroom(self, ctx):
        """You don't need no instruction manual to be free!!"""
        await self.bot.say("VROOM VROOM!")

    @commands.command(pass_context=True, no_pm=True, name='rate')
    async def rate(self, ctx, *, rate:str = None):
        """Đánh giá thứ gì đó theo thang điểm 100."""
        if rate != None:
            score = randint(-1,101)
            special = randint(1,100)
            if score/100 < 0:
                cmt = randchoice(["Thảm hại chưa cưng","thôi đi nhảy cầu đi","tởm"])
            elif score == 0:
                cmt = randchoice(["muhaahAhAhaHHahha",":smile:","Nice"])
            elif 0 < score/100 < 0.15:
                cmt = randchoice(["tệ vl","Thôi bỏ đi cưng","đứa nào tính slash ship hả?"])
            elif score/100 < 0.35:
                cmt = randchoice(["could be better","muốn thử lại hông?","rr","vd"])
            elif score/100 < 0.65:
                cmt = randchoice(["meh","tàm tạm","ít ra gần trung bình rồi","chấp nhận được"])
            elif score/100 < 0.9:
                cmt = randchoice(["Có vẻ tốt","khá đấy","Nai xừ","khá ổn","cũng ok"])
            elif score/100 < 1:
                cmt = randchoice(["Ghê lun","Hay","Hài lòng chưa?","đứa nào nói rig ta chửi","mood tốt nên cho tốt đó","đù","vl cao"])
            else:
                cmt = randchoice(["Purrfecttttt","VÃI LỜ","Ghê ghê ghê","Kinh","Ahahahahahhha","sắp có người ghen tị","kiểu gì cũng có đứa kêu rigged"])
            if special < 3:
                score = 1000
                cmt = randchoice(["SAIKOU DESU WA","A ĐÙ LIT VCL","Gk3^^^^^^^","UNSTOPPABLE"])
            elif special == 100:
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
