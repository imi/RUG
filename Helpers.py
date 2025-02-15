from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

fileName = f"usernames.txt"

def write_file(text):
  with open(fileName, "w") as f:
    f.write(text)
  return fileName

def return_main_markup():
  buttons = InlineKeyboardMarkup()
  buttons.add(InlineKeyboardButton("Triple Usernames", callback_data="triple"), InlineKeyboardButton("Multi letters Usernames", callback_data="multi"))
  buttons.add(InlineKeyboardButton("Special Usernames", callback_data="special"))
  buttons.add(InlineKeyboardButton("Author", callback_data="author"))
  return buttons

def edit_message(bot, cid: int, mid: int, text: str, buttons = None):
  btns = InlineKeyboardMarkup()
  if isinstance(buttons, list):
    for btn in range(len(buttons)):
      if btn == len(buttons) - 1: 
        t = buttons[btn][0]
        c = buttons[btn][1]
        btns.add(InlineKeyboardButton(t, callback_data=c))
        break
      else: 
        t1, t2 = buttons[btn][0], buttons[btn + 1][0]
        c1, c2 = buttons[btn][1], buttons[btn + 1][1]
        btns.add(InlineKeyboardButton(t1, callback_data=c1), InlineKeyboardButton(t2, callback_data=c2))
  else: btns = buttons
  bot.edit_message_text(chat_id=cid, message_id=mid, text=text, reply_markup=btns)