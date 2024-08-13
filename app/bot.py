from typing import List

import requests, pickle, time, random
from bs4 import BeautifulSoup

class Message():
    def __init__(self, href, text, sender_name, time, bot):
        self.__href = href
        self.sender_name = sender_name
        self.text = text
        self.time = time
        self.__bot = bot

    def answer(self, text):
        self.__bot.send_message(self.__href, text)

    def __str__(self):
        return f'{self.sender_name}:{self.text[:50]}...'
    def data(self):
        return {
            'sender_name': self.sender_name,
            'text': self.text,
            'time': self.time,
        }
class Bot:
    """Use this class for administration account"""
    __PAUSE_MIN = 3
    __PAUSE_MAX = 60
    MAIN_URL = 'https://m.facebook.com/'
    # changing this may cause errors
    USER_AGENT = 'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.36 (KHTML, like Gecko) Version/10.3.2.2836 Mobile Safari/537.36'

    def __init__(self, login: str, password: str, use_pause:bool=True):
        """Set account login, password and use_pause for pause before requests"""
        self.__use_pause = use_pause
        self.__session = requests.Session()
        self.__session.headers.update({
            'User-Agent': Bot.USER_AGENT
        })
        self.__login = login
        self.__password = password
        if not self.__load_session():
            self._login()

    def _get_full_href(self, href: str):
        return href if Bot.MAIN_URL in href else Bot.MAIN_URL + href

    def get_page(self, href: str):
        href = self._get_full_href(href)
        if self.__use_pause:
            time.sleep(random.randint(Bot.__PAUSE_MIN, Bot.__PAUSE_MAX))
        r = self.__session.get(href)
        return r

    def send_form(self, href: str, data: dict):
        href = self._get_full_href(href)
        if self.__use_pause:
            time.sleep(random.randint(Bot.__PAUSE_MIN, Bot.__PAUSE_MAX))
        r  = self.__session.post(href, data)
        return  r

    def __get_data_from_form(self, form: BeautifulSoup):
        inputs = form.find_all('input')
        post_data = {}
        for input_elem in inputs:
            if input_elem.get('type') == 'hidden':
                name = input_elem.get('name')
                value = input_elem.get('value', '')
                if name:
                    post_data[name] = value
        return post_data


    def _login(self):
        print('login')
        r = self.__session.get(self.MAIN_URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        login_form = soup.form
        post_data = self.__get_data_from_form((login_form))
        post_data['email'] = self.__login
        post_data['pass'] = self.__password
        self.send_form(login_form['action'], post_data)
        self.__save_session()
    def __save_session(self):
        with open(f'cookies/{self.__login}.pkl', 'wb') as f:
            pickle.dump(self.__session.cookies, f)

    def __load_session(self):
        try:
            with open(f'cookies/{self.__login}.pkl', 'rb') as f:
                self.__session.cookies.update(pickle.load(f))
            return True
        except FileNotFoundError:
            return False

    def check_messages(self) -> List:
        """This function return dict with only new, unread messages"""
        page = self.get_page('messages/')
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find(id ='root').find('div').find_all('div')[1]
        html_messages = table.find_all('td')
        messages = []
        for message in html_messages:
            message_classes = message.get('class')
            if 'bw' in message_classes:
                message_datas = message.find_all('h3')
                messages.append(Message(
                        href=message_datas[0].find('a')['href'],
                        text=message_datas[1].text,
                        time=message_datas[2].text,
                        sender_name=message_datas[0].text,
                        bot=self
                    )
                )
        return messages

    def send_message(self, href: str, text: str):
        """Use this to send a message, the href parameter to link to the chat"""
        message_page = self.get_page(href)
        soup = BeautifulSoup(message_page.text, 'html.parser')
        form = soup.find_all('form')[1]
        data = self.__get_data_from_form(form)
        data['body'] = text
        self.send_form(form['action'], data)



