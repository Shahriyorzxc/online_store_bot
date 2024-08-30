from telebot import types

from localization.keyboard_lang import *



def generate_localization():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_uz = types.KeyboardButton(text="🇺🇿UZ")
    btn_ru = types.KeyboardButton(text="🇷🇺RU")
    btn_en = types.KeyboardButton(text="🇬🇧EN")
    keyboard.row(btn_uz, btn_ru, btn_en)
    return keyboard


def generate_catalog(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_laptop = types.KeyboardButton(text=laptops[lang])
    btn_monitor = types.KeyboardButton(text=monitors[lang])
    btn_pc = types.KeyboardButton(text=computers[lang])
    keyboard.row(btn_laptop, btn_monitor, btn_pc)
    return keyboard


def generate_inline_url(url, lang):
    keyboard = types.InlineKeyboardMarkup()
    btn_more_bay = types.InlineKeyboardButton(text=buy_product[lang], callback_data="buy")
    btn_url = types.InlineKeyboardButton(text=information[lang], url=url)
    keyboard.row(btn_more_bay, btn_url)
    return keyboard


def generate_pagination(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_next = types.KeyboardButton(text=straight[lang])
    btn_prev = types.KeyboardButton(text=to_back[lang])
    btn_menu = types.KeyboardButton(text=menu[lang])
    keyboard.row(btn_prev, btn_next)
    keyboard.row(btn_menu)
    return keyboard