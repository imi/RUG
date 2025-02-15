from itertools import product
from telebot import TeleBot, logger
from telebot.types import Message, CallbackQuery
from string import digits, ascii_lowercase
from SpecialUS import specialUS
from Helpers import *
import logging

token = input("BOT TOKEN: ")
bot = TeleBot(token=token)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s", datefmt="%H:%M:%S")
logger  = logging.getLogger("telebot")
logger.setLevel = logging.ERROR
pattern = {}

def generate_triples(chars: str):
  usernames = []
  for mix in product(chars, repeat=3):
    usernames.append("_".join(mix))
  return write_file("\n".join(usernames))

def generate_pens(chars: str, lens):
  usernames: list[str] = []
  for char in chars:
    for dif_char in chars:
      for at in range(lens):
        username: list = []
        for i in range(lens):
          if i == at: username.append(char)
          else: username.append(dif_char)
        usernames.append("".join(username))
        if dif_char == char:
          break
  return write_file("\n".join(usernames))

def gen(m: Message):
  generate_pens(ascii_lowercase, int(m.text))
  with open(fileName, "rb") as fn:
    bot.send_document(chat_id=m.chat.id, document=fn)

def genn2(m: Message):
  chars = ascii_lowercase + digits if m.text.lower() == "no" else m.text
  text = "\n".join(specialUS(chars, pattern["pattern"]).new())
  write_file(text)
  with open(fileName, "rb") as f:
    bot.send_document(m.chat.id, document=f)

def genn(m: Message):
  mm = bot.send_message(m.chat.id, text="Do you wanna use your own letters, numbers, or semples?\nif yes, send your chars.\nif no, send no.")
  pattern["pattern"] = m.text
  bot.register_next_step_handler(mm, genn2)

def startBot():
  @bot.message_handler(commands=['start'])
  def reply(m: Message):
    bot.reply_to(m, text="Random usernames/text generator\n", reply_markup=return_main_markup())

  @bot.callback_query_handler(func=lambda c: True)
  def button(btn: CallbackQuery):
    cid, mid = btn.from_user.id, btn.message.id
    if btn.data == "author":
     edit_message(bot, cid, mid, "Fully Developed by @Pwwwww", [["Back ", "back"]])
    if btn.data == "back":
      edit_message(bot, cid, mid, "Random usernames/text generator\n-\nFully developed by @Pwwwww", return_main_markup())
    if btn.data == "triple":
      fn = generate_triples(ascii_lowercase)
      with open(fn, "rb") as fn:
        bot.send_document(chat_id=cid, document=fn)
    if btn.data == "multi":
      m = bot.send_message(btn.from_user.id, "Length of usernames?")
      bot.register_next_step_handler(m, gen)
    if btn.data == "special":
      mark = InlineKeyboardMarkup()
      mark.add(InlineKeyboardButton("Return Back", callback_data="back"))
      mes = bot.send_message(cid, """
      Send the pattern of usernames similiraly to this form: a&L&N--&Rxx
      &L -> a random letter
      &N -> a random number
      &R -> random number/letter/char
                             
      Any other letter/char/number will remain UNCHANGED and in its POSITION
""", reply_markup=mark)
      bot.register_next_step_handler(mes, genn)
  logger.info("bot started seccessfully")
  bot.polling(True, none_stop=True)

startBot()