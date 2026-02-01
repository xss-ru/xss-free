import telebot
from telebot import types

TOKEN = "8570307264:AAFCCteqteDyGMRYzGKiup9pmEMA5bqo7WU"
CHANNEL_ID = -1003563079845
CHANNEL_LINK = "https://t.me/+F_eqZewu2FcyYWY0"

bot = telebot.TeleBot(TOKEN)

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        send_main_menu(message.chat.id)
    else:
        send_subscription_request(message.chat.id)

def send_subscription_request(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    subscribe_btn = types.InlineKeyboardButton(text="Подписаться", url=CHANNEL_LINK)
    check_btn = types.InlineKeyboardButton(text="Проверить", callback_data="check_subscription")
    markup.add(subscribe_btn, check_btn)
    bot.send_message(chat_id=chat_id, text="Для того что бы бесплатно пользоваться ботом, подпишитесь на канал.", reply_markup=markup)

def send_main_menu(chat_id):
    try:
        with open('onion.mp4', 'rb') as video:
            markup = types.InlineKeyboardMarkup()
            
            row1 = []
            row1.append(types.InlineKeyboardButton(text="Phone", callback_data="phone"))
            row1.append(types.InlineKeyboardButton(text="Email", callback_data="email"))
            row1.append(types.InlineKeyboardButton(text="SNILS", callback_data="snils"))
            markup.row(*row1)
            
            row2 = []
            row2.append(types.InlineKeyboardButton(text="INN", callback_data="inn"))
            row2.append(types.InlineKeyboardButton(text="Car num", callback_data="car_num"))
            row2.append(types.InlineKeyboardButton(text="VK", callback_data="vk"))
            markup.row(*row2)
            
            row3 = []
            row3.append(types.InlineKeyboardButton(text="Facebook", callback_data="facebook"))
            row3.append(types.InlineKeyboardButton(text="Telegram", callback_data="telegram"))
            row3.append(types.InlineKeyboardButton(text="OK", callback_data="ok"))
            markup.row(*row3)
            
            bot.send_video(chat_id=chat_id, video=video, caption="<b>Выберите функцию поиска!</b>", parse_mode='HTML', reply_markup=markup)
    except FileNotFoundError:
        markup = types.InlineKeyboardMarkup()
        
        row1 = []
        row1.append(types.InlineKeyboardButton(text="Phone", callback_data="phone"))
        row1.append(types.InlineKeyboardButton(text="Email", callback_data="email"))
        row1.append(types.InlineKeyboardButton(text="SNILS", callback_data="snils"))
        markup.row(*row1)
        
        row2 = []
        row2.append(types.InlineKeyboardButton(text="INN", callback_data="inn"))
        row2.append(types.InlineKeyboardButton(text="Car num", callback_data="car_num"))
        row2.append(types.InlineKeyboardButton(text="VK", callback_data="vk"))
        markup.row(*row2)
        
        row3 = []
        row3.append(types.InlineKeyboardButton(text="Facebook", callback_data="facebook"))
        row3.append(types.InlineKeyboardButton(text="Telegram", callback_data="telegram"))
        row3.append(types.InlineKeyboardButton(text="OK", callback_data="ok"))
        markup.row(*row3)
        
        bot.send_message(chat_id=chat_id, text="<b>Выберите функцию поиска!</b>", parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "check_subscription":
        user_id = call.from_user.id
        if check_subscription(user_id):
            send_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "Вы ещё не подписались на канал!")
            send_subscription_request(call.message.chat.id)
    elif call.data in ["phone", "email", "snils", "inn", "car_num", "vk", "facebook", "telegram", "ok"]:
        bot.answer_callback_query(call.id, f"Вы выбрали: {call.data}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
