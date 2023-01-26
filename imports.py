from aifc import Error
import logging
import subprocess
import sys
from ntpath import join
from colorama import Fore, Back, Style, init
from os import times
import os
import sqlite3
import random
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import quote_html
from datetime import datetime, timedelta
from decimal import Decimal
from time import gmtime
from time import strptime
import asyncio
from bs4 import BeautifulSoup
import requests
from pycoingecko import CoinGeckoAPI
import numexpr
from threading import Thread
from config import token_ch
from background import keep_alive
#from pyqiwip2p import QiwiP2P

from inline import (
    pay,
    help2, 
    gamevbmenu, 
    reg, 
    help_back, 
    fulltop,
    advertising,
    course_pay,
    info_donate_online
)
import config

#p2p = QiwiP2P(auth_key=config.QiwiP2P_token)

from datebase.db import (
    register_money,
    cursor,
    connect,
    update_money,
    update_donate,
    update_balance,
    user_money,
    user_balance,
    user_donate,
    course_money1,
    course_money2,
    course_money3,
    course_cash_money1,
    course_cash_money2,
    course_cash_money3,
    add_check,
    delete_check,
    get_course,
    get_x2donate,
    status_x2donate,
    update_status_x2donate,
    get_check,
    add_cuorse
    )
import utils
from commands import (
    start_handler,
    channelmute_handler,
    disconect_database_handler, 
    gamevb_handler, 
    sistem_message_handler, 
    info_handler, 
    info_id_handler, 
    channelmute_handler, 
    channelunmute_handler, 
    channelban_handler,
    channelunban_handler, 
    report_handler, 
    unwarn_id_handler, 
    unwarn_handler, 
    warn_handler, 
    warn_id_handler, 
    help_admins_handler, 
    reset_handler, 
    unban_id_handler, 
    unban_handler, 
    ban_id_handler, 
    ban_handler, 
    reset_id_handler, 
    cl_handler, 
    register_chat_handler, 
    chats_handler
)

from commands import commands_handler

from commands import (
    info_donate_callback,
    check_pays_callback,
    pay_money1_callback,
    pay_money2_callback,
    pay_money3_callback,
    top_f_callback,
    priglashenie_callback,
    organiz_callback,
    top_а_callback,
    top_y_callback,
    top_b_callback,
    top_callback,
    gamevb_callback, 
    ava_admin_callback, 
    ava_girl_callback, 
    ava_dyp_callback, 
    ava_apper_callback, 
    ava_cheat_callback , 
    ava_strach_callback, 
    owner_cash_callback, 
    channel_proverk_callback, 
    helper_admins_cash_callback, 
    admins_cash_callback, 
    adms_callback, 
    cash_vlastelin_callback, 
    vlastelin_callback, 
    cash_bog_callback, 
    bog_callback, 
    cash_vladelec_callback, 
    vladelec_callback, 
    cash_osnovatel_callback, 
    osnovatel_callback, 
    cash_sponsor_callback, 
    sponsor_callback, 
    cash_helper_callback, 
    helper_callback, 
    cash_platina_callback, 
    platina_callback, 
    cash_premium_callback, 
    premium_callback, 
    cash_vip_callback, 
    vip_callback, 
    privilegii_callback, 
    money_case_cash1_callback, 
    money_case_callback, 
    up_money_case_callback, 
    up_donate_case_callback, 
    donate_case_cash1_callback, 
    donate_case_callback, 
    case_callback, 
    resurs4_callback, 
    craft_resurs3, 
    craft_resurs2, 
    craft_resurs1, 
    priv2_callback, 
    im2_callback, 
    rabot2_callback, 
    game2_callback, 
    admin_commands_callback, 
    ob_Statisyik_callback, 
    statiskik_callback, 
    admins_menu_up_callback, 
    osn2_callback, 
    register_help_callback, 
    oston_callback, 
    ysloviya_cash_callback, 
    prodazh_valyte_callback
)

from commands import (
    new_chat_content_types
)

from app import on_shutdown, on_startup




