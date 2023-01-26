from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
import utils

info_donate_online = InlineKeyboardMarkup(row_width=1)
info_donate_online.add(
    InlineKeyboardButton(text=f'💰 Пополнить', callback_data='info_donate')
)

def course_pay(money1, money2, money3):
    course_pay = InlineKeyboardMarkup(row_width=1)
    full_money1 = utils.scor_summ(money1)
    full_money2 = utils.scor_summ(money2)
    full_money3 = utils.scor_summ(money3)
    course_pay.add(
    InlineKeyboardButton(text=f'💸 Купить {full_money1}', callback_data=f'pay_money1_{money1}'),
    InlineKeyboardButton(text=f'💸 Купить {full_money2}', callback_data=f'pay_money1_{money2}'),
    InlineKeyboardButton(text=f'💸 Купить {full_money3}', callback_data=f'pay_money1_{money3}')
    )

    return course_pay
def pay(Isurl=True, url='', bill='', money=''):
    pay = InlineKeyboardMarkup(row_width=1)

    if Isurl == True:
        pay.add(
        InlineKeyboardButton(text=f'🧾 Счёт на {money} руб.', url=url)
        )

    pay.add(
    InlineKeyboardButton(text=f'Проверить оплату', callback_data=f'check_pay_{bill}')
    )

    return pay

reg = InlineKeyboardMarkup(row_width=1)
register_help = InlineKeyboardButton(text='❗️ Помощь', callback_data='register_help')
add_bot = InlineKeyboardButton(text='➕ Добавить бота в чат', url=f't.me/{config.bot_name}?startgroup=1')
reg.add(register_help, add_bot)

gamevbmenu = InlineKeyboardMarkup(row_width=1)
gamevb = InlineKeyboardButton(text='ИГРАТЬ 🎮', callback_data='gamevb')
gamevbmenu.add(gamevb)

help2 = InlineKeyboardMarkup(row_width=2)
Osn2 = InlineKeyboardButton(text='Основные 📝', callback_data='Osn2')
game2 = InlineKeyboardButton(text='Игры 🎮', callback_data='game2')
rabot2 = InlineKeyboardButton(text='Работы 🔨', callback_data='rabot2')
Im2 = InlineKeyboardButton(text='Имущество 🏘 ', callback_data='Im2')
Priv2 = InlineKeyboardButton(text='Привилегии 📖', callback_data='Priv2')
Adm2 = InlineKeyboardButton(text='Admins menu ⛔️', callback_data='Admins_menu_up')
oston = InlineKeyboardButton(text='Остальные ❕', callback_data='oston')
organiz = InlineKeyboardButton(text='Организации 🏰', callback_data='organiz')
help2.add(Osn2, game2, rabot2, Im2, Priv2, Adm2, oston, organiz)

help_back = InlineKeyboardMarkup(row_width=1)
help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='register_help')
help_back.add(help_back2)

fulltop = InlineKeyboardMarkup(row_width=1)
top = InlineKeyboardButton(text='💎 Топ игроков', callback_data='top')
top_b = InlineKeyboardButton(text='💰 Топ богачей', callback_data='top_b')
top_y = InlineKeyboardButton(text='📊 Топ успешных', callback_data='top_y')
top_а = InlineKeyboardButton(text='🎯 Топ азартных', callback_data='top_а')
top_f = InlineKeyboardButton(text='👨‍👩‍👧‍👦 Топ семьей', callback_data='top_f')
fulltop.add(top, top_b, top_y, top_а, top_f)

advertising = InlineKeyboardMarkup(row_width=1)
advertising.add(
    InlineKeyboardButton(text='👮‍♂️ ПРОБИТЬ ДРУГА', url='t.me/check_user_ip_robot'),
    InlineKeyboardButton(text='💰 КУПИТЬ СКРИПТ', url='t.me/tb_haeshka')
    )


