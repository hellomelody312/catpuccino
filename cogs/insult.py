import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from random import choice as randchoice
from random import choice
import os


class Insult:

    """Airenkun's Insult Cog"""
    def __init__(self, bot):
        self.bot = bot
        self.insults = fileIO("data/insult/insults.json","load")
        self.khens = fileIO("data/insult/insults2.json","load")

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def insult(self, ctx, user : discord.Member=None, times : int=1):
        """Insults the user (max 10)"""
        msg = ' '
        if times > 10 and ctx.message.author.id != "293041932542672896":
            await self.bot.say(randchoice("Gì chửi nhiều vậy má??  <:ree:397654450518360074> Tém tém bớt coi!!","Hãy văn minh, đừng chửi nhiều quá. <:dep:379728193558413312>", "Muốn bot sập luôn à mà chửi nhiều thế? <:duh:386506307722805248>"))
        else:
            if user != None:
                nem = str(user.nick)
                if nem == "None":
                    nem = str(user.name)
                if user.id == self.bot.user.id:
                    if ctx.message.author.id == "293041932542672896":
                        await self.bot.say("Sao anh nỡ chửi em anh mil huhu...")
                    else:
                        msg = randchoice([", mày đần tới mức nghĩ chụy ngu mà tự chửi mình hả? Xem lại mình đi cái thứ não bò!",
                                          " Đù ghê luôn. Thấy tao ngầu quá tính chửi tao hả mày? <:ro:437654455505125406>",
                                          " giờ vẫn có đứa tính kêu tao chửi tao. Tao khô lời <:ro:437654455505125406>"])
                        nem = ctx.message.author.mention
                        await self.bot.say(nem + msg)
                elif user.id == "293041932542672896":
                    msg = randchoice(["Kìa anh Mil, có đứa kêu em chửi anh kìa.",
                                      "Sir Meocu già ai cũng biết rồi, lười chửi lém.",
                                      "Tao biết Mil nó mê trai nè. Nó mê Thỏ.",
                                      "Ngủ điều độ vào cho khỏe mil à :heart:"])
                    await self.bot.say(msg)
                else:
                    for xz in range (0,times):
                        if user.id == "378900391879901185":
                            nem = randchoice(["Rô biến thái","Rô vô dụng","rô"])
                        if user.id == "324968191967232000":
                            nem = randchoice(["gal hay NTR Pokemon kia","gal chảnh","Gal kia"])
                        if user.id == "123385776628039680":
                            nem = randchoice(["Admin vô dụng","DT mê trai","DT biến thái","DT"])
                        if user.id == "226366391509450752":
                            nem = randchoice(["Hal vd","Hal bánh bèo"])
                        if user.id == "303854270057545729":
                            nem = randchoice(["lãnh đạo phát xít","mèo","mèo kia","mèo mê trai","mèo bánh bèo"])
                        if user.id == "391758777025560588":
                            nem = randchoice(["gién","Jen vd","gién tởm lợm","eww con gién"])
                        if user.id == "378857713838456833":
                            nem = randchoice(["Yin vd","Yin bánh bèo","yin bắt pkm toàn fail","Buljangnan"])
                        insulth = randchoice(self.insults).format(randchoice(["tên ","con "])+ nem)
                        insultf = insulth[:1].upper() + insulth[1:]
                        await self.bot.say(insultf)
            else:
                chuinguoc = randchoice(self.insults).format(randchoice(["tên ","con ","thứ "]) + str(ctx.message.author.mention))
                chuinguoc2 = chuinguoc[:1].upper() + chuinguoc[1:]
                await self.bot.say(chuinguoc2)

    @commands.command(pass_context=True, no_pm=True)
    async def khen(self, ctx, user : discord.Member=None):
        """Khen ai đó"""

        msg = ' '
        if user != None:
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = "Khổ ghê, tui biết tui đẹp mà."
                await self.bot.say(msg)
            elif user.id == "293041932542672896":
                 msg = "Mil tuyệt vời nhứt quả đất luôn."
                 await self.bot.say(msg)
            else:
                nem = str(user.nick)
                if nem == "None":
                   nem = str(user.name)
                await self.bot.say(nem + "," + msg + randchoice(self.khens))
        else:
            await self.bot.say(ctx.message.author.mention + msg + randchoice(self.khens))

def check_folders():
    folders = ("data", "data/insult/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    """Moves the file from cogs to the data directory. Important -> Also changes the name to insults.json"""
    insults = {"You ugly as hell damn. Probably why most of your friends are online right?"}

    if not os.path.isfile("data/insult/insults.json"):
        if os.path.isfile("cogs/put_in_cogs_folder.json"):
            print("moving default insults.json...")
            os.rename("cogs/put_in_cogs_folder.json", "data/insult/insults.json")
        else:
            print("creating default insults.json...")
            fileIO("data/insult/insults.json", "save", insults)


def setup(bot):
    check_folders()
    check_files()
    n = Insult(bot)
    bot.add_cog(n)
