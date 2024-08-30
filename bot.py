from telebot import TeleBot
from telebot.types import LabeledPrice
from keyboard_bot import *
from localization.bot_lang import cataloge, products_len_count
from localization.keyboard_lang import menu
from repository.laptop_db import PostgreSql_laptop
from repository.monitor_db import PostgreSql_monitor
from repository.pc_db import PostgreSql_computer
from configs.config import Config

cfg_token = Config().token
clt_token = Config().click_token
bot = TeleBot(cfg_token)

user_langs = {}

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    bot.send_message(chat_id, f"Assalomu Aleykum {first_name}!\n\nOnline Magazinga xush kelibsiz!")
    localization(message)


def localization(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Ozizga mos bolgan Tilni tanlang!\n\nSelect a language!\n\nВыберите язык!", reply_markup=generate_localization())
    bot.register_next_step_handler(message, main_menu)

def main_menu(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id)
    if message.text == '🇺🇿UZ':
        lang = "uz"

    if message.text == '🇷🇺RU':
        lang = "ru"

    if message.text == '🇬🇧EN':
        lang = "en"

    bot.send_message(chat_id, cataloge[lang], reply_markup=generate_catalog(lang))

    if message.text == '/start':
        return start(message)

    user_langs[chat_id] = lang
    bot.register_next_step_handler(message, main_catalogs)


def main_catalogs(message, product_id=0, products=None):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id)
    if message.text == menu[lang]:
        return start(message)

    if message.text == laptops[lang]:
        products = PostgreSql_laptop().select_data()

    if message.text == computers[lang]:
        products = PostgreSql_computer().select_data()

    if message.text == monitors[lang]:
        products = PostgreSql_monitor().select_data()

    if message.text == straight[lang] and product_id < len(products):
        product_id += 1

    if message.text == to_back[lang] and product_id > 0:
        product_id -= 1
#------------------------------------------------------------------------------------------------------------------------
    product = products[product_id]

    product_title = product[0]
    product_url = product[1]
    image = product[2]
    product_price = product[3]
    product_description = product[4]
    bot.send_photo(chat_id, image, caption=f'{"Brand_name"}: {product_title}\n\n'
                                           f'{"Description"}: {product_description}'
                                           f'\n\n{"Price"}: {product_price}',
                   reply_markup=generate_inline_url(product_url, lang))

    user_message = bot.send_message(chat_id, f"{products_len_count[lang]} : {len(products) - (product_id + 1)}",
                                    reply_markup=generate_pagination(lang))

    if message.text == "Oldinga" and len(products) - (product_id + 1) == 0:
        bot.delete_message(chat_id, message.id + 2)
        bot.send_message(chat_id, "No products!", reply_markup=generate_pagination(lang))
        product_id = product_id - len(products)  # -1
    bot.register_next_step_handler(user_message, main_catalogs, product_id, products)


@bot.callback_query_handler(func=lambda call: True)
def get_callback_data(call):
    chat_id = call.message.chat.id
    if call.data == "buy":
        product_info = call.message.caption.split(": ")
        product_price = ""
        price = product_info[-1].replace('UZS', "")
        for x in price:
            if x.isdigit():
                product_price += x

        INVOICE = {
            "title": product_info[1],
            "description": product_info[3],
            "invoice_payload": "bot-defined invoice payload",
            "provider_token": clt_token,
            "start_parameter": "pay",
            "currency": "UZS",
            "prices": [LabeledPrice(label=product_info[1], amount=int(product_price + "00"))],
        }

        bot.send_invoice(chat_id, **INVOICE)


@bot.pre_checkout_query_handler(func=lambda query: True)
def invoice_checkout(query):
    """Проверка чека"""

    # Проверим условие, если заказ не проходит проверку
    if query.invoice_payload != "expected_payload":  # Например, проверка на payload
        bot.answer_pre_checkout_query(query.id, ok=False, error_message="Ошибка оплаты!")
    else:
        bot.answer_pre_checkout_query(query.id, ok=True)


bot.polling()
