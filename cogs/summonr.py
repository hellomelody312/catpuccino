import os
import re
import random
from random import randint
import discord
from .utils import checks
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils.dataIO import fileIO


class Summonr:
    def __init__(self, bot):
        self.bot = bot
        self.filename = 'data/summonr/summonr.json'
        self.summons = dataIO.load_json(self.filename)
        self.charas = self.summons["charas"]
        self.actions = self.summons["actions"]
        self.actions.append('táng chết {victim}')
        self.spells = self.summons["spells"]
        self.cards = self.summons["cards"]
        self.songs = self.summons["songs"]

    @commands.command(pass_context=True, no_pm=True, name='summon')
    async def summon(self, context, *, acchon:str = None):
        """Summon ai đó để làm điều bạn muốn."""
        author = context.message.author
        summoner = str(author.nick)
        char = str(random.choice(self.charas))
        if summoner == "None":
            summoner = str(author.name)
        if acchon != None:
            censor = ["chịch","rape","r@pe","rếp","gangbang","hiếp","hấp diêm","thông"]
            censored = False
            for censor_search in censor:
                if re.search(censor_search, acchon):
                    censored = True
                    await self.bot.say(char + ' hiện lên tát 6900 cái vào mặt ' + summoner + ' vì tội biến thái rồi biến mất.')
            if not censored:
                message = acchon
                await self.bot.say(summoner + ' triệu hồi ' + char + ' để ' + message + '.')
        else:
            #char = str(random.choice(self.charas))
            message = str(random.choice(self.actions)).format(victim=summoner)
            if message == "hát":
                message = message + ' ' + str(random.choice(self.songs))
            rand = randint(0,100)
            if rand > 50:
                if any (c in char for c in ("Hermione Granger, phù thủy xuất sắc nhứt lứa tuổi của mình,",
                                            "Giáo sư Minerva McGonnagal",
                                            "Ron Weasley, vị Vua của chúng ta,",
                                            "Harry Potter, Cậu bé Đã Sống Sót và Suýt Chết Mấy Lần Nữa Nhưng Vẫn Không Chết,")):
                    message = "xài phép " + str(random.choice(self.spells)).format(victim=summoner) + " đánh "+ summoner +" sml"
                elif char == "Sakura Kinomoto, con ông cháu cha bánh bèo chủ nhân của những thẻ bài chỉ vì được chống lưng,":
                    message = "xài thẻ bài " + str(random.choice(self.cards)).format(victim=summoner)
                elif char == "Bích Nụ, người bán bánh tráng trộn chạy hàng đầu thế giới,":
                    message = "thồn bánh tráng trộn đầy họng " + summoner
            await self.bot.say(char + ' hiện lên ' + message + '.')




def check_folder():
    if not os.path.exists('data/summonr'):
        print('Creating data/summonr folder...')
        os.makedirs('data/summonr')


def check_file():
    data = {}
    f = 'data/summonr/summonr.json'
    if not dataIO.is_valid_json(f):
        print('Creating default summonr.json...')
        dataIO.save_json(f, data)


def setup(bot):
    check_folder()
    check_file()
    n = Summonr(bot)
    bot.add_cog(n)
