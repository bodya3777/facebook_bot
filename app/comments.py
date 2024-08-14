class Comment():
    def __init__(self, href: str, name: str, text: str, bot):
        self.__href = href
        self.name = name
        self.text = text
        self.__bot = bot

    def __str__(self):
        return  self.name + self.text[:50]

    def data(self):
        return {
            'name': self.name,
            'text': self.text
        }
    def answer(self, text: str):
        self.__bot.send_coment(self.__href, text)
