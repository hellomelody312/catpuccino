import os
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

    @commands.command(pass_context=True, no_pm=True, name='summon')
    async def summon(self, context, *, acchon:str = None):
        """Summon ai đó để làm điều bạn muốn."""
        author = context.message.author
        summoner = str(author.nick)
        if summoner == "None":
            summoner = str(author.name)
        if acchon != None:
            char = str(random.choice(self.charas))
            message = acchon
            await self.bot.say(summoner + ' triệu hồi ' + char + ' để ' + message + '.')
        else:
            char = str(random.choice(self.charas))
            message = str(random.choice(self.actions)).format(victim=summoner)
            rand = randint(0,100)
            if rand > 50:
                if any (c in char for c in ("Hermione Granger","Giáo sư McGonnagal","Ron Weasley","Harry Potter")):
                    message = "xài phép " + str(random.choice(self.spells)).format(victim=summoner) + " đánh "+ summoner +" sml"
                elif char == "Sakura Kinomoto":
                    message = "xài thẻ bài " + str(random.choice(self.cards)).format(victim=summoner)
                elif char == "Bích Nụ":
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
