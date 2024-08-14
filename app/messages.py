class Message():
    def __init__(self, href, text, sender_name, time, bot):
        self.__href = href
        self.sender_name = sender_name
        self.text = text
        self.time = time
        self.__bot = bot

    def answer(self, text: str):
        self.__bot.send_message(self.__href, text)

    def __str__(self):
        return f'{self.sender_name}:{self.text[:50]}...'
    def data(self):
        return {
            'sender_name': self.sender_name,
            'text': self.text,
            'time': self.time,
        }
