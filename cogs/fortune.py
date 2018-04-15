# Developed by Redjumpman for Redbot
from discord.ext import commands
from random import choice as randchoice
from random import randint
from random import shuffle


class Fortune():
    """Fortune Cookie Commands."""
    colors = ["xanh dương","đỏ","hường","tím mộng mơ","trắng","đen tuyền","xanh chuối","hồng neon","vàng neon","cầu vồng","trong suốt","xám","đỏ chấm bi","hồng chấm bi","xanh dương kẻ sọc",
                  "cam","lục","chàm","càng diêm dúa càng tốt","sịp hôm qua vừa mặc","đen trắng sọc tù nhân","da người"]
    charas = ["Hatsune Miku","Guzma","Milotic","DT","Hello Kitty","Gyarados","Chikapu","Mimikkyu","Madoka","Giovanni","Maxie `:heart:` Archie","Kukui","Lillie","Gladion","Hau","giáo sư Oak","Cynthia","Wallace",
                  "Jynx","Ditto","Pyukumuku","Togedemaru","Doraemon","Eevee","Vaporeon","Touya Kinomoto","Yue","Cerberus","Clow Reed","Li Syaoran","Daidouji Tomoyo","Ryan Raynolds","Togepi","Alolan Raichu","Dialga",
                  "Giratina","Arceus","Mewtwo","Shaymin","Sakura Kinomoto","Entei","Raikou","Suicune","Primal Groudon", "Kyogre","Victini","Zygarde","Solgaleo","Lunala","Bibi","Thần Mèo","Doge","Lucario",
                  "Taylor Swift","Katy Perry","Iron Man", "Bích Nụ","Mai Ngô","Panda","Donald Trump","Putin","Harry Potter","Lady Gaga","Chị Dậu","Captain America","Người Dơi","Người Nhện","Hulk",
                  "Nicki Minaj","Hermione Granger","Giáo sư McGonnagal","Ron Weasley","RO","Một người nào đó trong chatbox này","Batman","Superman","Loki","Thor", "mẹ bạn","bố bạn"]
    constellations = ["Bạch Dương","Kim Ngưu","Song Tử","Cự Giải","Sư Tử","Xử Nữ","Thiên Bình","Thiên Yết","Nhân Mã","Ma Kết","Bảo Bình","Song Ngư"]


    def __init__(self, bot):
        self.bot = bot

    def fortuneshuffle():
        def hr():
            h = randint(0,23)
            return(h)
        def mn():
            m = randint(0,59)
            return(m)
        fortune = randchoice(["Ngày mai đừng nhòm lên trời vào lúc " + str(randint(0,23)) + "h" + str(randint(0,23)) + " phút. Phân chim rơi đó.",
                              "Tình hình tài chính của bạn đang gặp một xíu trục trặc nhỏ. Gặp người cung " + randchoice(Fortune.constellations) + " để tăng vận.",
                              "Điện thoại thông minh, máy tính dù rất hữu ích nhưng đừng bám dính lấy nó hoài. Hãy ra khỏi thế giới ảo và hòa mình vào cuộc sống thực tế đầy màu sắc ngoài kia đi nào!",
                              "Nếu đi ngủ mà ngứa đít thì đừng trách sáng ngủ dậy tay bốc mùi.",
                              "Sắp có người cung " + randchoice(Fortune.constellations) + " đến mang cho bạn một bất ngờ. Xấu tốt chưa biết.",
                              "Tè trong gió đừng trách gió thổi ngược nước tè.",
                              "Hôm nay, bạn nên mở rộng thế giới quan của mình bằng cách thưởng thức văn hoá nghệ thuật nhiều hơn. Thử vẽ 1 bức tranh " + randchoice(Fortune.charas) + " xem nào.",
                              "Hợp nhất với cung " + randchoice(Fortune.constellations) + ", tránh gặp cung " + randchoice(Fortune.constellations),
                              "Đừng nghe mấy cái bói trước.",
                              "Nên ăn " + str(randint(0,53)) + " que kem để gặp may mắn hôm nay!",
                              "Có thể bị insult " + str(randint(0,50)) + " lần trong ngày hôm nay.",
                              "Mai bạn sẽ đi qua " + randchoice(["1 triệu","100 nghìn","1 nghìn","20000", "500000"]) + " đồng rớt ngoài đường nhưng không thấy nên không lụm.",
                              "Đi đường coi chừng giẫm phải " + randchoice(["cứt", "lá cây", "kẹo chewing gum", "xà bông", "dầu bôi trơn"]) + ".",
                              "Dường như “người ấy” đang cảm thấy có chút gì đó không thoải mái hoặc ấm ức với bạn. Phải chăng vì những ngày này bạn quá chú tâm vào công việc nên không có thời gian quan tâm, chăm sóc người ấy?",
                              "Mặc đồ màu " + randchoice(Fortune.colors) + " ra đường để gặp vận may.",
                              "Ngày mai tránh mặc đồ màu " + randchoice(Fortune.colors) + " ra đường kẻo xui.",
                              "Nên đổi màn hình máy tính thành màu " + randchoice(Fortune.colors) + " để gặp vận may.",
                              "Nên đổi màn hình máy tính thành hình " + randchoice(Fortune.charas) + " để gặp vận may.",
                              "Đổi avatar thành hình " + randchoice(Fortune.charas) + " để gặp vận may.",
                              "Nếu không muốn " + randchoice(Fortune.charas) + " xử đẹp thì mua sịp màu " + randchoice(Fortune.colors) + " về mặc ngay.",
                              "Đôi khi mệt vcl cóc muốn bói nữa.",
                              "Mua sịp màu " + randchoice(Fortune.colors) + " về mặc để lấy hên.",
                              "Vào lúc " + str(randint(0,23)) + "h" + str(randint(0,23)) + " phút sẽ có UFO bay qua đầu nhưng bạn không hề hay biết.",
                              "Đêm ngủ coi chừng tè dầm.",
                              "Nếu bạn nghĩ một con bot discord có thể bói đúng thì bạn tin người vcl.",
                              "Đêm nay có thể mơ thấy " + randchoice(Fortune.charas) + ".",
                              randchoice(Fortune.charas) + " gửi lời 'tắt máy đi ngủ đi'.",
                              randchoice(Fortune.charas) + " và " + randchoice(Fortune.charas) + " vừa nhắc tới bạn và họ quyết định ghé thăm bạn trong tương lai gần.",
                              "Chúc mừng! Bạn vẫn biết đọc!",
                              "Nếu được tôi muốn đổi màu tên thành màu " + randchoice(Fortune.colors) + " ghê. Bạn cũng nên đổi đi.",
                              "Bạn có quen ai cung " + randchoice(Fortune.constellations) + " không? Mai tặng nó cái sịp màu " + randchoice(Fortune.colors) + " thử đi.",
                              "Mua vé số thử đi biết đâu trúng" + randchoice([str(randint(1,999)) + " cây vàng", str(randint(1,999)) + " triệu", str(randint(1,999)) + " tỷ","1 nghìn đồng"]) + "."])
        return(fortune)

    @commands.command(name="fortune")
    async def _cookie(self):
            """Ask for your fortune

            And look deeply into my scales
            """
            return await self.bot.say(Fortune.fortuneshuffle())


def setup(bot):
    bot.add_cog(Fortune(bot))
