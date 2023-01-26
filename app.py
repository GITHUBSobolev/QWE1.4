from imports import *

print(Fore.BLACK + Back.WHITE + """

█▀▀ █▀█ █▀█ █▀▄   █▀ █▀▀ █▀█ █ █▀█ ▀█▀
█▄█ █▄█ █▄█ █▄▀   ▄█ █▄▄ █▀▄ █ █▀▀ ░█░

▀█▀ ░ █▀▄▀█ █▀▀ ░░▄▀ █▀▀ █▀█ █▀█ █▀▄ █▀ █▀▀ █▀█ █ █▀█ ▀█▀ █▀
░█░ ▄ █░▀░█ ██▄ ▄▀░░ █▄█ █▄█ █▄█ █▄▀ ▄█ █▄▄ █▀▄ █ █▀▀ ░█░ ▄█


""")

init(autoreset=True)

# subprocess.check_call([sys.executable, "-m", "pip", "install", '-U', "-r", "requirements.txt"])


logging.basicConfig(level=logging.INFO)

#CoinGecko
api = CoinGeckoAPI()


# bot init
bot = Bot(token=config.token, disable_web_page_preview=True)
dp = Dispatcher(bot)

async def on_shutdown(dp: Dispatcher):
    print(f"{Fore.RED + Style.BRIGHT} Бот остоновлен {Fore.WHITE}Developer: RUsobolev")

async def on_startup(dp: Dispatcher):

    result = time.localtime()

    if int(result.tm_hour) <= 9:
      h = "0"
    else:
      h = ''
    if int(result.tm_min) <= 9:
      min = "0"
    else:
      min = ''
    if int(result.tm_sec) <= 9:
      s = "0"
    else:
       s = ''

    print(f"{Style.BRIGHT + Fore.GREEN}Бот запущен {Fore.WHITE}")
    await register_handlers(dp)
    await bot.send_message(config.owner_id, f'''
🟩<b> БОТ БЫЛ ЗАПУЩЕН -</b> <code>{h}{result.tm_hour}:{min}{result.tm_min}:{s}{result.tm_sec}</code>

⚙️ <b>НАСТРОЙКА ВЫДАЧИ ДЕНЕГ ЗА УЧАСТИКОВ -</b> <code>вдзу</code>
спасибо что используешь код от @GOODSCRIPTS
    ''', parse_mode='html')
    await bot.send_message(config.owner_id, f'''
📊 <b>КАНАЛ -</b> <code>@{config.channel_name}</code>
📎 <b>ССЫЛКА НА ВЛАДЕЛЬЦА - {config.owner}</b>
📎 <b>ССЫЛКА НА КАНАЛ - {config.channel}</b>
📎 <b>ССЫЛКА НА ЧАТ - {config.chat}</b>
📎 <b>ССЫЛКА НА ВТОРОЙ ЧАТ - {config.chat2}</b>
    ''', parse_mode='html')


async def register_handlers(dp: Dispatcher):

   cursor.execute("INSERT INTO wdzy VALUES(?, ?);",(0, 'off'))
   cursor.execute("INSERT INTO family_id VALUES(?);",(str(0)))

   dp.register_message_handler(
      new_chat_content_types, content_types=['new_chat_members']
   )

   dp.register_message_handler(
      chats_handler, commands=['chats'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      register_chat_handler, commands=['register_chat'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      cl_handler, commands=['cl'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      reset_id_handler, commands=['reset_id'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      ban_handler, commands=['ban'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      ban_id_handler, commands=['ban_id'], commands_prefix='!?./'
   )


   dp.register_message_handler(
      unban_handler, commands=['unban'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      unban_id_handler, commands=['unban_id'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      reset_handler, commands=['reset'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      help_admins_handler, commands=['help_admins'], commands_prefix='!?./'
   )


   dp.register_message_handler(
      unwarn_id_handler, commands=['unwarn_id'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      warn_id_handler, commands=['warn_id'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      warn_handler, commands=['warn'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      unwarn_handler, commands=['unwarn'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      report_handler, commands=['report'], commands_prefix='!?./'
   )


   dp.register_message_handler(
      channelunban_handler, commands=['channel_unban'], commands_prefix='!?./', is_chat_admin=True
   )

   dp.register_message_handler(
      channelban_handler, commands=['channel_ban'], commands_prefix='!?./', is_chat_admin=True
   )

   dp.register_message_handler(
      channelunmute_handler, commands=['channel_unmute'], commands_prefix='!?./', is_chat_admin=True
   )


   dp.register_message_handler(
      channelmute_handler, commands=['channel_mute'], commands_prefix='!?./', is_chat_admin=True
   )

   dp.register_message_handler(
      info_id_handler, commands=['info_id'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      info_handler, commands=['info'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      sistem_message_handler, commands=['m'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      gamevb_handler, commands=['gamevb'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      disconect_database_handler, commands=['disconect_database'], commands_prefix='!?./'
   )

   dp.register_message_handler(
      start_handler, commands=['start'], commands_prefix='!?./'
   )


   dp.register_message_handler(
      commands_handler
   )

   dp.register_callback_query_handler(
      gamevb_callback, text="gamevb"
   )

   dp.register_callback_query_handler(
      ava_admin_callback, text="ava_admin"
   )

   dp.register_callback_query_handler(
      ava_girl_callback, text="ava_girl"
   )

   dp.register_callback_query_handler(
      ava_dyp_callback, text="ava_dyp"
   )

   dp.register_callback_query_handler(
      ava_apper_callback, text="ava_apper"
   )

   dp.register_callback_query_handler(
      ava_cheat_callback, text="ava_cheat"
   )


   dp.register_callback_query_handler(
      ava_strach_callback, text="ava_strach"
   )

   dp.register_callback_query_handler(
      channel_proverk_callback, text="channel_poverk"
   )

   dp.register_callback_query_handler(
      owner_cash_callback, text="owner_cash"
   )

   dp.register_callback_query_handler(
      helper_admins_cash_callback, text="helper_admins_cash"
   )

   dp.register_callback_query_handler(
      admins_cash_callback, text="admins_cash"
   )

   dp.register_callback_query_handler(
      adms_callback, text="adms"
   )

   dp.register_callback_query_handler(
      cash_vlastelin_callback, text="cash_vlaselin"
   )

   dp.register_callback_query_handler(
      vlastelin_callback, text="vlastelin"
   )

   dp.register_callback_query_handler(
      cash_bog_callback, text="cash_bog"
   )

   dp.register_callback_query_handler(
      bog_callback, text="bog"
   )

   dp.register_callback_query_handler(
      cash_vladelec_callback, text="cash_vladelec"
   )

   dp.register_callback_query_handler(
      vladelec_callback, text="vladelec"
   )

   dp.register_callback_query_handler(
      cash_osnovatel_callback, text="cash_osnovatel"
   )

   dp.register_callback_query_handler(
      osnovatel_callback, text="osnovatel"
   )

   dp.register_callback_query_handler(
      cash_sponsor_callback, text="cash_sponsor"
   )

   dp.register_callback_query_handler(
      sponsor_callback, text="sponsor"
   )

   dp.register_callback_query_handler(
      cash_helper_callback, text="cash_helper"
   )

   dp.register_callback_query_handler(
      helper_callback, text="helper"
   )

   dp.register_callback_query_handler(
      cash_platina_callback, text="cash_platina"
   )

   dp.register_callback_query_handler(
      platina_callback, text="platina"
   )

   dp.register_callback_query_handler(
      cash_premium_callback, text="cash_premium"
   )

   dp.register_callback_query_handler(
      premium_callback, text="premium"
   )

   dp.register_callback_query_handler(
      cash_vip_callback, text="cash_vip"
   )

   dp.register_callback_query_handler(
      vip_callback, text="vip"
   )

   dp.register_callback_query_handler(
      privilegii_callback, text="privilegii"
   )

   dp.register_callback_query_handler(
      money_case_cash1_callback, text="money_case_cash1"
   )

   dp.register_callback_query_handler(
      money_case_callback, text="money_case"
   )

   dp.register_callback_query_handler(
      up_money_case_callback, text="up_money_case"
   )

   dp.register_callback_query_handler(
      up_donate_case_callback, text="up_donate_case"
   )

   dp.register_callback_query_handler(
      donate_case_cash1_callback, text="donate_case_cash1"
   )

   dp.register_callback_query_handler(
      donate_case_callback, text="donate_case"
   )

   dp.register_callback_query_handler(
      case_callback, text="case"
   )

   dp.register_callback_query_handler(
      resurs4_callback, text="resurs4"
   )

   dp.register_callback_query_handler(
      craft_resurs3, text="resurs3"
   )

   dp.register_callback_query_handler(
      craft_resurs2, text="resurs2"
   )

   dp.register_callback_query_handler(
      craft_resurs1, text="resurs1"
   )

   dp.register_callback_query_handler(
      priv2_callback, text="Priv2"
   )

   dp.register_callback_query_handler(
      im2_callback, text="Im2"
   )

   dp.register_callback_query_handler(
      rabot2_callback, text="rabot2"
   )

   dp.register_callback_query_handler(
      game2_callback, text="game2"
   )

   dp.register_callback_query_handler(
      admin_commands_callback, text="admins_comands"
   )

   dp.register_callback_query_handler(
      ob_Statisyik_callback, text="stats222"
   )

   dp.register_callback_query_handler(
      statiskik_callback, text="statistic"
   )

   dp.register_callback_query_handler(
      admins_menu_up_callback, text="Admins_menu_up"
   )

   dp.register_callback_query_handler(
      osn2_callback, text="Osn2"
   )

   dp.register_callback_query_handler(
      register_help_callback, text="register_help"
   )

   dp.register_callback_query_handler(
      oston_callback, text="oston"
   )

   dp.register_callback_query_handler(
      ysloviya_cash_callback, text="ysloviya_cash"
   )

   dp.register_callback_query_handler(
      prodazh_valyte_callback, text="prodazh_valyte"
   )

   dp.register_callback_query_handler(
      top_callback, text="top"
   )

   dp.register_callback_query_handler(
      top_b_callback, text="top_b"
   )

   dp.register_callback_query_handler(
      top_y_callback, text="top_y"
   )

   dp.register_callback_query_handler(
      top_а_callback, text="top_а"
   )

   dp.register_callback_query_handler(
      organiz_callback, text="organiz"
   )

   dp.register_callback_query_handler(
      top_f_callback, text="top_f"
   )

   dp.register_callback_query_handler(
      info_donate_callback, text="info_donate_online"
   )

   dp.register_callback_query_handler(
      check_pays_callback, text_contains="check_pay_"
   )

   dp.register_callback_query_handler(
      pay_money3_callback, text_contains="pay_money3_"
   )

   dp.register_callback_query_handler(
      pay_money1_callback, text_contains="pay_money1_"
   )

   dp.register_callback_query_handler(
      pay_money2_callback, text_contains="pay_money2_"
   )

   dp.register_callback_query_handler(
      priglashenie_callback, lambda call: call.data.startswith('accept_')
   )


