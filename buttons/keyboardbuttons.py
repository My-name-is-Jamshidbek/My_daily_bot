import datetime

from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

#kontaktni olish uchun butoon
keyboard_kontakt = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_kontakt.add(KeyboardButton(text="kontaktni ulashish", request_contact=True))

'''
quyidagilar admin  uchun
'''
keyboard_admin_menu_1 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_admin_menu_1.add(
    KeyboardButton(text='Foydalanuvchilar'),
    KeyboardButton(text='Reklama'),
)

keyboard_admin_rozibolish = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_admin_rozibolish.add(
    KeyboardButton(text='Tasdiqlash'),
    KeyboardButton(text='Bekor qilish'),
)

keyboard_user_menu_1 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_user_menu_1.add(
    KeyboardButton(text='👨‍💻Dasturchi malumoti👨‍💻'),
    KeyboardButton(text='Reja qo\'shish'),
    KeyboardButton(text='Rejalar'),
)

def get_week_menu():
    days_of_week = ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', "Juma", "Shanba", "Yakshanba"]
    current_week = []
    for i in range(7):
        current_date = datetime.date.today() + datetime.timedelta(days=i)
        current_week.append(days_of_week[current_date.weekday()] + f" {current_date.day}/{current_date.month}")
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for day in current_week:
        menu.add(day)
    menu.add("Chiqish")
    return menu

import datetime
import aiogram.types as types

def get_btn(btns):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for btn in btns:
        menu.add(btn)
    return menu
