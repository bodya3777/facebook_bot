# Facebook Bot

This project is a bot designed to automate interactions with the mobile version of Facebook. The bot allows you to log in, retrieve messages, send replies, and interact with forms.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/bodya3777/facebook_bot.git
    cd facebook_bot
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Bot Initialization

To start using the bot, create an instance of the `Bot` class:

```python
from bot import Bot

bot = Bot(login='your_email', password='your_password')
```
### Read and answer messages

```python
from app.bot import Bot

bot = Bot(login='your_email', password='your_password')
messages = bot.check_messages()
for message in messages:
   print(message.data())
    if condition:
        #to reply to a message
       message.answer('your text here')
```


### Read and answer comments

```python
from app.bot import Bot

bot = Bot(login='your_email', password='your_password')
comments = bot.get_comments()
for comment in comments:
   print(comment.data())
    if condition:
        #to reply to a comment
       comment.answer('your text here')
```