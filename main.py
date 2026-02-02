import telebot
from telebot import types
import requests
import json
import html

TOKEN = "8570307264:AAFCCteqteDyGMRYzGKiup9pmEMA5bqo7WU"
CHANNEL_ID = -1003563079845
CHANNEL_LINK = "https://t.me/+F_eqZewu2FcyYWY0"
API_TOKEN = "0jv8SQHONMpyRmyRKImo8jT1d4AYqsNu"
API_URL = "https://api.depsearch.sbs/"

bot = telebot.TeleBot(TOKEN)

user_states = {}
user_data = {}
user_messages = {}

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
            
            btn1 = types.InlineKeyboardButton(text="Phone", callback_data="phone")
            btn2 = types.InlineKeyboardButton(text="Email", callback_data="email")
            btn3 = types.InlineKeyboardButton(text="SNILS", callback_data="snils")
            markup.row(btn1, btn2, btn3)
            
            btn4 = types.InlineKeyboardButton(text="INN", callback_data="inn")
            btn5 = types.InlineKeyboardButton(text="Car num", callback_data="car_num")
            btn6 = types.InlineKeyboardButton(text="VK", callback_data="vk")
            markup.row(btn4, btn5, btn6)
            
            btn7 = types.InlineKeyboardButton(text="Facebook", callback_data="facebook")
            btn8 = types.InlineKeyboardButton(text="Telegram", callback_data="telegram")
            btn9 = types.InlineKeyboardButton(text="OK", callback_data="ok")
            markup.row(btn7, btn8, btn9)
            
            msg = bot.send_video(chat_id=chat_id, video=video, caption="<b>Выберите функцию поиска!</b>", parse_mode='HTML', reply_markup=markup)
            user_messages[chat_id] = msg.message_id
    except FileNotFoundError:
        markup = types.InlineKeyboardMarkup()
        
        btn1 = types.InlineKeyboardButton(text="Phone", callback_data="phone")
        btn2 = types.InlineKeyboardButton(text="Email", callback_data="email")
        btn3 = types.InlineKeyboardButton(text="SNILS", callback_data="snils")
        markup.row(btn1, btn2, btn3)
        
        btn4 = types.InlineKeyboardButton(text="INN", callback_data="inn")
        btn5 = types.InlineKeyboardButton(text="Car num", callback_data="car_num")
        btn6 = types.InlineKeyboardButton(text="VK", callback_data="vk")
        markup.row(btn4, btn5, btn6)
        
        btn7 = types.InlineKeyboardButton(text="Facebook", callback_data="facebook")
        btn8 = types.InlineKeyboardButton(text="Telegram", callback_data="telegram")
        btn9 = types.InlineKeyboardButton(text="OK", callback_data="ok")
        markup.row(btn7, btn8, btn9)
        
        msg = bot.send_message(chat_id=chat_id, text="<b>Выберите функцию поиска!</b>", parse_mode='HTML', reply_markup=markup)
        user_messages[chat_id] = msg.message_id

def edit_to_input(chat_id, search_type, text):
    markup = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton(text="Back", callback_data="back_to_menu")
    markup.add(back_btn)
    
    try:
        if chat_id in user_messages:
            try:
                bot.edit_message_caption(chat_id=chat_id, message_id=user_messages[chat_id], caption=text, reply_markup=markup, parse_mode='HTML')
            except:
                bot.edit_message_text(chat_id=chat_id, message_id=user_messages[chat_id], text=text, reply_markup=markup, parse_mode='HTML')
    except Exception as e:
        print(f"Ошибка редактирования: {e}")
    
    user_states[chat_id] = search_type

def api_request(query, search_type):
    try:
        url = f"{API_URL}quest={query}?token={API_TOKEN}&lang=ru"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "results" in data and data["results"]:
                return {"success": True, "data": data["results"]}
            else:
                return {"success": False, "error": "Данные не найдены"}
        elif response.status_code == 403:
            return {"success": False, "error": "Ошибка доступа"}
        elif response.status_code == 404:
            return {"success": False, "error": "Данные не найдены"}
        else:
            return {"success": False, "error": f"Ошибка сервера: {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"Ошибка соединения: {str(e)}"}

def escape_html_special(text):
    if text is None:
        return "Не указано"
    
    if not isinstance(text, str):
        text = str(text)
    
    text = html.escape(text)
    
    replacements = {
        '&lt;': '<',  
        '&gt;': '>',  
        '&quot;': '"',
        '&#x27;': "'",
        '&#x2F;': '/',
        '&amp;': '&',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '/': '&#x2F;',
        '&': '&amp;',
        '\u003c': '&lt;',
        '\u003e': '&gt;',
        '\u0026': '&amp;',
        '\u0027': '&#x27;',
        '\u0022': '&quot;',
        '\u005c': '\\',
        '\u0000': '',
        '\u0001': '',
        '\u0002': '',
        '\u0003': '',
        '\u0004': '',
        '\u0005': '',
        '\u0006': '',
        '\u0007': '',
        '\u0008': '',
        '\u000b': '',
        '\u000c': '',
        '\u000e': '',
        '\u000f': '',
        '\u0010': '',
        '\u0011': '',
        '\u0012': '',
        '\u0013': '',
        '\u0014': '',
        '\u0015': '',
        '\u0016': '',
        '\u0017': '',
        '\u0018': '',
        '\u0019': '',
        '\u001a': '',
        '\u001b': '',
        '\u001c': '',
        '\u001d': '',
        '\u001e': '',
        '\u001f': '',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    text = text.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
    
    return text

def format_results(results, current_index, query, search_type):
    if not results or current_index >= len(results):
        return "Данные не найдены"
    
    result = results[current_index]
    
    if search_type == "phone":
        title = f"Information by number: {escape_html_special(query)}"
    elif search_type == "email":
        title = f"Information by email: {escape_html_special(query)}"
    elif search_type == "snils":
        title = f"Information by SNILS: {escape_html_special(query)}"
    elif search_type == "inn":
        title = f"Information by INN: {escape_html_special(query)}"
    elif search_type == "car_num":
        title = f"Information by car: {escape_html_special(query)}"
    elif search_type == "vk":
        title = f"Information by VK: {escape_html_special(query)}"
    elif search_type == "facebook":
        title = f"Information by Facebook: {escape_html_special(query)}"
    elif search_type == "telegram":
        title = f"Information by Telegram: {escape_html_special(query)}"
    elif search_type == "ok":
        title = f"Information by OK: {escape_html_special(query)}"
    else:
        title = f"Information: {escape_html_special(query)}"
    
    lines = []
    items = list(result.items())
    
    for i, (key, value) in enumerate(items):
        safe_key = escape_html_special(key)
        safe_value = escape_html_special(value)
        
        if i == len(items) - 1:
            lines.append(f"└─<b>{safe_key}</b>: <code>{safe_value}</code>.")
        else:
            lines.append(f"├─<b>{safe_key}</b>: <code>{safe_value}</code>.")
    
    formatted_text = title + "\n" + "\n".join(lines)
    return formatted_text

def show_results(chat_id, query, search_type, results, current_index=0):
    formatted_text = format_results(results, current_index, query, search_type)
    
    markup = types.InlineKeyboardMarkup()
    
    if len(results) > 1:
        prev_index = (current_index - 1) % len(results)
        next_index = (current_index + 1) % len(results)
        
        prev_btn = types.InlineKeyboardButton(text="◀️ Back", callback_data=f"page_{prev_index}_{search_type}_{query}")
        page_btn = types.InlineKeyboardButton(text=f"{current_index + 1}/{len(results)}", callback_data="current_page")
        next_btn = types.InlineKeyboardButton(text="Next ▶️", callback_data=f"page_{next_index}_{search_type}_{query}")
        markup.row(prev_btn, page_btn, next_btn)
    
    back_btn = types.InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")
    markup.add(back_btn)
    
    try:
        if chat_id in user_messages:
            try:
                bot.edit_message_caption(chat_id=chat_id, message_id=user_messages[chat_id], caption=formatted_text, parse_mode='HTML', reply_markup=markup)
            except:
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=user_messages[chat_id], text=formatted_text, parse_mode='HTML', reply_markup=markup)
                except:
                    bot.delete_message(chat_id=chat_id, message_id=user_messages[chat_id])
                    msg = bot.send_message(chat_id=chat_id, text=formatted_text, parse_mode='HTML', reply_markup=markup)
                    user_messages[chat_id] = msg.message_id
    except Exception as e:
        print(f"Ошибка редактирования результатов: {e}")
        try:
            bot.delete_message(chat_id=chat_id, message_id=user_messages[chat_id])
            msg = bot.send_message(chat_id=chat_id, text=formatted_text, parse_mode='HTML', reply_markup=markup)
            user_messages[chat_id] = msg.message_id
        except:
            msg = bot.send_message(chat_id=chat_id, text=formatted_text, parse_mode='HTML', reply_markup=markup)
            user_messages[chat_id] = msg.message_id
    
    user_data[chat_id] = {
        "search_type": search_type,
        "query": query,
        "results": results,
        "current_index": current_index
    }

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    
    if call.data == "check_subscription":
        if check_subscription(user_id):
            send_main_menu(chat_id)
        else:
            bot.answer_callback_query(call.id, "Вы ещё не подписались на канал!")
            send_subscription_request(chat_id)
    
    elif call.data == "back_to_menu":
        send_main_menu(chat_id)
        if chat_id in user_states:
            del user_states[chat_id]
    
    elif call.data.startswith("page_"):
        parts = call.data.split("_")
        if len(parts) >= 4:
            index = int(parts[1])
            search_type = parts[2]
            query = "_".join(parts[3:])
            
            if chat_id in user_data:
                user_data[chat_id]["current_index"] = index
                show_results(chat_id, query, search_type, user_data[chat_id]["results"], index)
            else:
                bot.answer_callback_query(call.id, "Сессия устарела")
    
    elif call.data == "phone":
        edit_to_input(chat_id, "phone", "Отправьте номер телефона")
        bot.answer_callback_query(call.id)
    
    elif call.data == "email":
        edit_to_input(chat_id, "email", "Отправьте email")
        bot.answer_callback_query(call.id)
    
    elif call.data == "snils":
        edit_to_input(chat_id, "snils", "Отправьте СНИЛС")
        bot.answer_callback_query(call.id)
    
    elif call.data == "inn":
        edit_to_input(chat_id, "inn", "Отправьте ИНН")
        bot.answer_callback_query(call.id)
    
    elif call.data == "car_num":
        edit_to_input(chat_id, "car_num", "Отправьте номер машины/VIN/ГРЗ")
        bot.answer_callback_query(call.id)
    
    elif call.data == "vk":
        edit_to_input(chat_id, "vk", "Отправьте ID Вконтакте")
        bot.answer_callback_query(call.id)
    
    elif call.data == "facebook":
        edit_to_input(chat_id, "facebook", "Отправьте ID Facebook")
        bot.answer_callback_query(call.id)
    
    elif call.data == "telegram":
        edit_to_input(chat_id, "telegram", "Отправьте ID Telegram")
        bot.answer_callback_query(call.id)
    
    elif call.data == "ok":
        edit_to_input(chat_id, "ok", "Отправьте ID Одноклассники")
        bot.answer_callback_query(call.id)
    
    else:
        bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    
    if chat_id not in user_states:
        return
    
    search_type = user_states[chat_id]
    query = message.text.strip()
    
    if not query:
        edit_to_input(chat_id, search_type, "Пожалуйста, введите данные для поиска")
        return
    
    try:
        if chat_id in user_messages:
            try:
                bot.edit_message_caption(chat_id=chat_id, message_id=user_messages[chat_id], caption="⌛ Идет поиск...", parse_mode='HTML')
            except:
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=user_messages[chat_id], text="⌛ Идет поиск...", parse_mode='HTML')
                except:
                    bot.delete_message(chat_id=chat_id, message_id=user_messages[chat_id])
                    msg = bot.send_message(chat_id=chat_id, text="⌛ Идет поиск...", parse_mode='HTML')
                    user_messages[chat_id] = msg.message_id
    except:
        pass
    
    if search_type == "phone":
        if not query.startswith("+"):
            query = "+" + query.lstrip("+")
    
    result = api_request(query, search_type)
    
    if result["success"]:
        show_results(chat_id, query, search_type, result["data"])
    else:
        markup = types.InlineKeyboardMarkup()
        back_btn = types.InlineKeyboardButton(text="Back to menu", callback_data="back_to_menu")
        markup.add(back_btn)
        
        try:
            if chat_id in user_messages:
                try:
                    bot.edit_message_caption(chat_id=chat_id, message_id=user_messages[chat_id], caption=f"❌ Ошибка: {result['error']}", parse_mode='HTML', reply_markup=markup)
                except:
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=user_messages[chat_id], text=f"❌ Ошибка: {result['error']}", parse_mode='HTML', reply_markup=markup)
                    except:
                        bot.delete_message(chat_id=chat_id, message_id=user_messages[chat_id])
                        msg = bot.send_message(chat_id=chat_id, text=f"❌ Ошибка: {result['error']}", parse_mode='HTML', reply_markup=markup)
                        user_messages[chat_id] = msg.message_id
        except Exception as e:
            print(f"Ошибка редактирования ошибки: {e}")
    
    if chat_id in user_states:
        del user_states[chat_id]

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
