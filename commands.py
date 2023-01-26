from collections import namedtuple
from email import message
from numpy import number
from imports import *
from regex import E
from config import token_ch

api = CoinGeckoAPI()



async def commands_handler(message: types.Message):

    await get_course()
    await get_x2donate()


    name = message.from_user.get_mention(as_html=True)

    i = f'''
👋 Привет <b>{name}</b>, я игровой бот <b>{config.full_bot_name}</b>
💸 Тебе как новому пользователю был выдан подарок в размере <code>{'{:,}'.format(config.start_money).replace(',', '.')}$</code>
❗️ Для ознакомление с моими командами, введи команду <code>Помощь</code> , или вибери кнопку <b>ниже</b>
➕ Так же ты можешь добавить бота в свой чат по кнопке <b>ниже</b>
    '''

    msg = message
    user_id = msg.from_user.id
    full_name = msg.from_user.full_name
    user_name = 'Игрок'
    user_status = "Player"
    status_block = 'off'
    stats_status = 'off'
    pref = 'Игрок'
    status_console = 'off'
    avatarka_start = 'none'
    klan_index = 0
    status_family = 0
    chat_id = message.chat.id
    result = time.localtime()


    if int(result.tm_mon) <= 9:
      p = "0"
    else:
      p = ''
    if int(result.tm_mday) <= 9:
      m = "0"
    else:
      m = ''
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
    times = f'{m}{result.tm_mday}.{p}{result.tm_mon}.{result.tm_year} | {h}{result.tm_hour}:{min}{result.tm_min}:{s}{result.tm_sec}'
    times2 = str(times)

    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None:
       photo_welcome = open('Photo/welcome.jpg', 'rb')
       cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, user_name, full_name, user_status, config.start_money, 0, 0, 0, status_block, times2, pref, 0, 0, 0, 0, stats_status))
       cursor.execute("INSERT INTO mine VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(user_id, full_name,status_block, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO farm VALUES(?, ?, ?, ?, ?);",(user_id, full_name,status_block, 0, 0))
       cursor.execute("INSERT INTO house VALUES(?, ?, ?, ?);",(user_id, user_name, 0, 0))
       cursor.execute("INSERT INTO cars VALUES(?, ?, ?, ?, ?);",(user_id, user_name, 0, 0, 0))
       cursor.execute("INSERT INTO user_case VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO bot_time VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, 0, 0, 0, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO time_bank VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO ob_time VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO console VALUES(?, ?);",(user_id, status_console))
       cursor.execute("INSERT INTO time_prefix VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO time_sms VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO channel_pov VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO avatarka VALUES(?, ?);",(user_id, avatarka_start))
       cursor.execute("INSERT INTO reput VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO h_module VALUES(?, ?);",(user_id, 0))
       connect.commit()
       print(f'Зарегестрировался в боте пользователь: {full_name}')

       await message.bot.send_photo(message.chat.id, photo_welcome, i, reply_markup=reg, parse_mode='html')
    else:
       pass
       
    
    check_update = cursor.execute(f'SELECT user_id from money_balance where user_id = "{user_id}"').fetchone()
    if check_update == None:
      await message.answer(f'🔁 Ваши данные были обновлены (следите за обновлениями на канале @{channel})')
      await register_money(user_id)
    else:
      pass


    
    
   
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       if chat_id == user_id:
          return await message.reply(f'❗️ Ваш аккаунт находиться в стадии <b>блокировки</b> ', parse_mode='html')
       return

    if message.forward_date != None:
       if chat_id == user_id:
          return await message.reply(f'❗️ Я не реагирую на <b>пер. сообщение</b>', parse_mode='html')
       return


    period = 1
    get = cursor.execute("SELECT stavka FROM ob_time WHERE user_id = ?",(message.from_user.id,)).fetchone()
    last_stavka = f"{int(get[0])}"
    stavkatime = time.time() - float(last_stavka)
    if stavkatime < period:
       chat_id = message.chat.id
       user_id = message.from_user.id

       if chat_id == user_id:
          return await message.reply(f'💬 <b>[ANTI-FLOOD]</b> - Не так быстро, в боте стоит ограничение между командами <b>{period} секунд(а)</b>', parse_mode='html')
       else:
          return
    else:
       user_id = message.from_user.id
       cursor.execute(f'UPDATE ob_time SET stavka = {time.time()} WHERE user_id = {user_id}')
       connect.commit()

    bot = Bot(token=token_ch)
    dp = Dispatcher(bot)
    
    if message.text.startswith('снять игроку') or message.text.startswith('Снять игроку'):
      if not message.reply_to_message:
               await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
               return

      if user_id != config.owner_id:
         return await message.reply(f'❗️Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')
      else:
         pass

      try:
         summ = int(message.text.split()[2])
      except:
         return await message.reply(f'<b>❗️ Неправильные аргументы</b> \n<b>❕ Пример:</b> <code>снять игроку 100</code>', parse_mode='html')
      
      reply_money = await user_money(message.reply_to_message.from_user.id)
      if reply_money < summ:
         return await message.reply(f'❗️ Вы не можете снять сумму больше, чем сам рублевый баланс игрока')
      else:
         pass
      
      new_user_money = reply_money - summ

      await update_money(message.reply_to_message.from_user.id, new_user_money)
      return await message.reply(f'❗️ Вы обновили рублевый баланс игрока <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> . Теперь его баланс: {new_user_money} руб.', parse_mode='html')


    if message.text.startswith('пополнить игроку') or message.text.startswith('Пополнить игроку'):
      if not message.reply_to_message:
               await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
               return

      if user_id != config.owner_id:
         return await message.reply(f'❗️Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')
      else:
         pass

      try:
         summ = int(message.text.split()[2])
      except:
         return await message.reply(f'<b>❗️ Неправильные аргументы</b> \n<b>❕ Пример:</b> <code>пополнить игроку 100</code>', parse_mode='html')
      
      reply_money = await user_money(message.reply_to_message.from_user.id)
      new_user_money = reply_money + summ

      await update_money(message.reply_to_message.from_user.id, new_user_money)
      return await message.reply(f'❗️ Вы обновили рублевый баланс игрока <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> . Теперь его баланс: {new_user_money} руб.', parse_mode='html')



    if message.text.startswith('пополнить') or message.text.startswith('Пополнить'):
        if message.chat.id != user_id:
            return await message.reply(f'<i><a href="t.me/{config.bot_name}">❗️ Авто оплата доступна только в личные сообщения с ботом</a></i>', parse_mode='html')
        try:
            donate = int(message.text.split()[1])
        except:
            await message.reply(f'❗️<b> Введены не правильно аргументы</b> !\n❕<b> Пример:</b> <code>пополнить 100</code>', parse_mode='html')
        
        if donate < 3:
            return await message.answer('💰 Минимальная сумма пополнение 3 рубля')
        else:
            pass

        comment = f'Online Donate | от {message.from_user.id} на {donate} руб.'

        bill = p2p.bill(amount=donate, lifetime=15, comment=comment)

        await add_check(message.from_user.id, donate, bill.bill_id)

        await message.reply(f'👍 Ваш чек на {donate} руб. готов \n✈️ Вы можете оплатить через <b><a href="{bill.pay_url}">ссылку</a></b> либо кнопку\n⌛️ Данная оплата будет действительна только 15 минут',reply_markup=pay(url=bill.pay_url, money=donate, bill=bill.bill_id),  parse_mode='html')



    if message.text.startswith('обменять') or message.text.startswith('Обменять'):
        users_money = await user_money(message.from_user.id)

        if users_money == 0:
            return await message.reply('❗️ У вас 0 рублей. Вы не можете обменять деньги на Donate-Coins')
        else:
            pass
        try:
            summ = message.text.split()[1]
        except:
            summ = int(users_money)

        try:
            summ = int(summ)
        except:
            return await message.reply('❗️<b> Введены не правильно аргументы .</b>\n❕<b> Пример:</b> <code>пополнить 100</code>', parse_mode='html')

        if summ <= 0:
            return await message.reply('❗️ Сумма обмена не может быть отрицательным числом')

        if summ > users_money:
            return await message.reply(f'❗️ Не хватает средств.\n💰 Баланс: {users_money} руб.')
        else:
            pass

        donate_coins = await user_donate(message.from_user.id)
        course_donate_coins = int(summ / 3)
        new_donate_coins = donate_coins + course_donate_coins
        await update_donate(message.from_user.id, new_donate_coins)
        await update_money(message.from_user.id, users_money - summ)
        await message.reply(f'🔁 Вы обменяли {summ} руб на {course_donate_coins} Donate-Coins.\n❕ Для просмотра своих Donate-Coins, напишите: <code>донат</code>', parse_mode='html')



    if message.text.lower() == 'курс':
        money1 = await course_money1()
        full_money1 = await utils.scor_summ(money1)
        cash_money1 = await course_cash_money1()

        money2 = await course_money2()
        full_money2 = await utils.scor_summ(money2)
        cash_money2 = await course_cash_money2()

        money3 = await course_money3()
        full_money3 = await utils.scor_summ(money3)
        cash_money3 = await course_cash_money3()

        course_pay = InlineKeyboardMarkup(row_width=2)
        course_pay.add(
        InlineKeyboardButton(text=f'💸 Купить {full_money1}', callback_data=f"pay_money1_{time.time()}"),
        InlineKeyboardButton(text=f'💸 Купить {full_money2}', callback_data=f"pay_money2_{time.time()}"),
        InlineKeyboardButton(text=f'💸 Купить {full_money3}', callback_data=f"pay_money3_{time.time()}")
        )

        course_pay.row(
        InlineKeyboardButton(text=f'💰 Пополнить', callback_data='info_donate')
        )
        
        await message.answer(f'''
👨‍💼 <b>{full_money1} - {cash_money1}RUB</b> 
🤵‍♂️ <b>{full_money2} - {cash_money2}RUB</b> 
🤴 <b>{full_money3} - {cash_money3}RUB</b>      
        ''', reply_markup=course_pay, parse_mode='html')


    if message.text.startswith('новый курс') or message.text.startswith('Новый курс'):
        if message.from_user.id != config.owner_id:
            return await message.answer('❗️ Сменить курс валют может только <b>владелец бота</b>', parse_mode='html')
        else:
            pass

        try:
            money1 = message.text.split()[2]
            money1 = await utils.sistem_number(money1)
            cash_money1 = int(message.text.split()[3])

            money2 = message.text.split()[4]
            money2 = await utils.sistem_number(money2)
            cash_money2 = int(message.text.split()[5])

            money3 = message.text.split()[6]
            money3 = await utils.sistem_number(money3)
            cash_money3 = int(message.text.split()[7])
        except ValueError:
            print(ValueError)
            #return await message.answer(f'Не правильно ввели оргументы (например: <code>новый курс 1e12 50 1e15 100 1e18 200</code> )', parse_mode='html')

        await add_cuorse(money1, cash_money1, money2, cash_money2, money3, cash_money3)
        await message.answer(f'<b>🔄 Был обновлен курс</b>\n<b>❕ Для просмотра нового курса, напишите:</b> <code>курс</code>', parse_mode='html')


    if message.text.startswith('x2donate статус') or message.text.startswith('X2donate статус'):
        if message.from_user.id != config.owner_id:
            return await message.answer('❗️ Х2 Донат может включать только <b>владелец бота</b>', parse_mode='html')
        else:
            pass

        status = message.text.split()[2]

        if status == 'on' or status == 'off':
            await update_status_x2donate(status)
            if status == 'on':
               status = 'включен'
               smile = '🚀'
            else:
               status = 'выключен'
               smile = '⛔️'
            await message.answer(f'{smile} X2 Донат был успешно {status}')
        else:
            return await message.answer(f'Ваш оргумент {status} не найден. Верные огрументы: on, off')
        

    if message.text.lower() in ['репорт', 'система репорта', 'репорты']:
       msg = message
       user_id = msg.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       await message.reply( f"""
⛔️Правила по использованию репортов
      ❗️ <b>Запрещено</b> материться, оскорблять кого-либо, проявлять неуважение к администрации и тому подобное.
      ❗️ <b>Запрещено</b> капсить, писать неразборчиво, использовать спам, писать один и тот-же текст несколько раз получивши на него ответ.
      ❗️ <b>Запрещено</b> всячески дразнить администрацию и отвлекать от работы.
      ❗️ <b>Запрещено</b> интересоваться/писать вещи которые ни коем образом ни относятся к игре
      ❗️ <b>Запрещена</b> реклама в любом её проявлении
      ❗️ <b>Запрещено</b> обращаться к своим друзьям администраторам по личным вопросам
      ❗️ <b>Запрещено</b> клеветать на игроков, обвинять их в нарушениях, которые они не совершали.
      ❗️ Репорт работает по принципу - <b>Вопрос/Просьба/Жалоба</b> (исключение - Приветствие) и не иначе. Иные формы обращения будут оставаться без ответа и будет выдано наказание.

⚠️Форма отправки репорта - <code>/report</code> <b>[сообщение]</b>

⛔️Прошу вас соблюдать правила отправки репорта
       """, parse_mode='html')
    if message.text.lower() in ["баланс", "Баланс", "Б", "б"]:
       msg = message
       user_id = msg.from_user.id
       
       chat_id = message.chat.id
       pref = cursor.execute("SELECT pref from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = str(pref[0])

       avatarka = cursor.execute("SELECT avatarka from avatarka where user_id = ?",(message.from_user.id,)).fetchone()
       avatarka = avatarka[0]

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = int(balance[0])
       balance2 = '{:,}'.format(balance).replace(',', '.')
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = int(bank[0])
       bank2 = '{:,}'.format(bank).replace(',', '.')
       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?",(message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])
       ethereum2 = '{:,}'.format(ethereum).replace(',', '.')

       c = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance).replace(',', '.')
       else:
        pass
       if bank >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          bank = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          bank2 = '{:,}'.format(bank).replace(',', '.')
       else:
        pass
       if ethereum >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          ethereum = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET ethereum = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          ethereum2 = '{:,}'.format(ethereum).replace(',', '.')
       else:
        pass

        obb_summ = balance + bank

        
        all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
        all_family2 = []
        proverka_family = 0
        for all_owner_id in all_family:
           all_family2.append(all_owner_id[0])

        user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()


        proverka_family = 0

        if user_id_family != None:
         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0] 

         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = f'{int(rank_family[0])} ранг'

        else:
         proverka_family += 1

        if user_id in all_family2:
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]   

         rank_family = 'Владелец семьи'
        else:
         proverka_family += 1
        
        if proverka_family == 2:
         family = ''
        else:
         family = f'\n<b>👨‍👩‍👧‍👦 Семья:</b> «<b>{name_family}</b>» <i>({rank_family})</i>'
       
       from utils import scor_summ

       obb_summ2 = await scor_summ(obb_summ)
       
       text_balance = f'''
<b>👤Ник:</b> <code><a href='tg://user?id={user_id}'>{user_name}</a></code>{family}
<b>💼Префикс:</b> <code>{pref} </code>
<b>💵Деньги:</b> <code>{balance2}$</code>
<b>🏛Банк:</b> <code>{bank2}$</code>
<b>🟪Эфириум:</b> <code>{ethereum2} шт</code>

<b>💰 Всего денег:</b> <code>{obb_summ2}$ </code>    
       '''

       if avatarka == 'apper':
          ava = open('Photo/apper.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava,text_balance, parse_mode='html')
          return
       
       if avatarka == 'admin':
          ava = open('Photo/админ.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava,text_balance, parse_mode='html')
          return
       
       if avatarka == 'girl':
          ava = open('Photo/girl.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, text_balance, parse_mode='html')
          return
       
       if avatarka == 'cheat':
          ava = open('Photo/cheat.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, text_balance, parse_mode='html')
          return
       
       if avatarka == 'dyp':
          ava = open('Photo/дюп.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, text_balance, parse_mode='html')
          return
       
       if avatarka == 'strach':
          ava = open('Photo/страж.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, f"👫 | Ник: <a href='tg://user?id={user_id}'>{user_name}</a> \n✏️ | Префикс: {pref} \n💰 | Деньги: {balance2}$ \n🏦 | Банк: {bank2}$\n🟣 | Эфириум: {ethereum2}🟪", parse_mode='html')
          return


       await bot.send_message(message.chat.id,text_balance, parse_mode='html')
    ################################################ПРОФИЛЬ#############################################################
    if message.text.lower() in ["профиль", "Профиль"]:
       msg = message
       chat_id = message.chat.id
       name = message.from_user.get_mention(as_html=True)

       time_register = cursor.execute("SELECT time_register FROM users WHERE user_id=?", (message.from_user.id,)).fetchall()
       time_register = time_register[0]

       user_id = msg.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reput = cursor.execute("SELECT reput from reput where user_id = ?",(message.from_user.id,)).fetchone()
       reput = int(reput[0])

       avatarka = cursor.execute("SELECT avatarka from avatarka where user_id = ?",(message.from_user.id,)).fetchone()
       avatarka = avatarka[0]

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?",(message.from_user.id,)).fetchone()
       rating = cursor.execute("SELECT rating from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = cursor.execute("SELECT pref from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = str(pref[0])
       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])
       donate_coins2 = '{:,}'.format(donate_coins).replace(',', '.')
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       game = cursor.execute("SELECT game from users where user_id = ?",(message.from_user.id,)).fetchone()
       game = int(game[0])
       game2 = '{:,}'.format(game).replace(',', '.')

       balance = int(balance[0])
       bank = int(bank[0])
       rating = int(rating[0])
       ethereum = int(ethereum[0])

       cars = cursor.execute("SELECT cars from cars where user_id = ?",(message.from_user.id,)).fetchone()
       cars = int(cars[0])

       house = cursor.execute("SELECT house from house where user_id = ?",(message.from_user.id,)).fetchone()
       house = int(house[0])
       
       all_org = 0
       all_proverka_family = 0

       all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
       all_family2 = []
      
       for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

       if user_id in all_family2:
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     

         family = f'\n    👨‍👩‍👧‍👦 <b>Семья:</b> <code>{name_family}</code>'

         all_org += 1
         all_proverka_family += 1
       else:
         pass

       user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

       if user_id_family != None:
         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     

         family = f'\n    👨‍👩‍👧‍👦 <b>Семья:</b> <code>{name_family}</code>'

         all_org += 1
         all_proverka_family += 1
       else:
         pass

       if all_org == 0:
         all_org2 = '\n      Вы не состоите в организациях 😿'
       else:
         all_org2 = '\n🏰 Организации:'
       
       if all_proverka_family == 0:
         family = ''
       else:
         pass


       d5 = 0

       if house == 1:
          house2 = '\n    <b>🏠Дом:</b> <code>Коробка</code>\n'
          d5 += 1
       if house == 2:
          house2 = '    <b>🏠Дом:</b> <code>Сарай</code>\n'
          d5 += 1
       if house == 3:
          house2 = '    <b>🏠Дом:</b> <code>Маленький домик</code>\n'
          d5 += 1
       if house == 4:
          house2 = '    <b>🏠Дом:</b> <code>Квартира</code>\n'
          d5 += 1
       if house == 5:
          house2 = '    <b>🏠Дом:</b> <code>Огромный дом</code>\n'
          d5 += 1
       if house == 6:
          house2 = '    <b>🏠Дом:</b> <code>Коттедж</code>\n'
          d5 += 1
       if house == 7:
          house2 = '    <b>🏠Дом:</b> <code>Вилла</code>\n'
          d5 += 1
       if house == 8:
          house2 = '    <b>🏠Дом:</b> <code>Загородный дом</code>\n'
          d5 += 1
       else:
          house2 = ''
          
       if cars == 1:
          cars2 = '    <b>🚘Машина:</b> <code>Самокат</code>\n'
          d5 += 1
       if cars == 2:
          cars2 = '    <b>🚘Машина:</b> <code>Велосипед</code>\n'
          d5 += 1
       if cars == 3:
          cars2 = '    <b>🚘Машина:</b> <code>Гироскутер</code>\n'
          d5 += 1
       if cars == 4:
          cars2 = '    <b>🚘Машина:</b> <code>Сегвей</code>\n'
          d5 += 1
       if cars == 5:
          cars2 = '    <b>🚘Машина:</b> <code>Мопед</code>\n'
          d5 += 1
       if cars == 6:
          cars2 = '    <b>🚘Машина:</b> <code>Мотоцикл</code>\n'
          d5 += 1
       if cars == 7:
          cars2 = '    <b>🚘Машина:</b> <code>ВАЗ 2109</code>\n'
          d5 += 1
       if cars == 8:
          cars2 = '    <b>🚘Машина:</b> <code>Квадроцикл</code>\n'
          d5 += 1
       if cars == 9:
          cars2 = '    <b>🚘Машина:</b> <code>Багги</code>\n'
          d5 += 1
       if cars == 10:
          cars2 = '    <b>🚘Машина:</b> <code>Вездеход</code>\n'
          d5 += 1
       if cars == 11:
          cars2 = '    <b>🚘Машина:</b> <code>Лада Xray</code>\n'
          d5 += 1
       if cars == 12:
          cars2 = '    <b>🚘Машина:</b> <code>Audi Q7</code>\n'
          d5 += 1
       if cars == 13:
          cars2 = '    <b>🚘Машина:</b> <code>BMW X6</code>\n'
          d5 += 1
       if cars == 14:
          cars2 = '    <b>🚘Машина:</b> <code>Toyota FT-HS</code>\n'
          d5 += 1
       if cars == 15:
          cars2 = '    <b>🚘Машина:</b> <code>BMW Z4 M</code>\n'
          d5 += 1
       if cars == 16:
          cars2 = '    <b>🚘Машина:</b> <code>Subaru WRX STI</code>\n'
          d5 += 1
       if cars == 17:
          cars2 = '    <b>🚘Машина:</b> <code>Lamborghini Veneno</code>\n'
          d5 += 1
       if cars == 18:
          cars2 = '    <b>🚘Машина:</b> <code>Tesla Roadster</code>\n'
          d5 += 1
       else:
          cars2 = ''

       if d5 == 0:
          d6 = '\n      У вас нету имущества 🙁'
       else:
          d6 = '🕋 | Имущество:\n'
       
       c = 999999999999999999999999
       if user_status == 'Player':
          priv = 'Пользователь'
       if user_status == 'Vip':
          priv = 'ВИП❤️'
       if user_status == 'Premium':
          priv = ' ПРЕМИУМ🧡'
       if user_status == 'Platina':
          priv = ' ПЛАТИНА💛'
       if user_status == 'Helper':
          priv = ' ХЕЛПЕР💚'
       if user_status == 'Sponsor':
          priv = ' СПОНСОР💙'
       if user_status == 'Osnovatel':
          priv = ' ОСНОВАТЕЛЬ💜'
       if user_status == 'Vladelec':
          priv = ' ВЛАДЕЛЕЦ🖤'
       if user_status == 'Bog':
          priv = ' БОГ🤍'
       if user_status == 'Vlaselin':
          priv = ' ВЛАСТЕЛИН🤎'
       if user_status == 'Owner':
          priv = 'OWNER ❗️'
       if user_status == 'Admin':
          priv = 'ADMIN ❗️'
       if user_status == 'Helper_Admin':
          priv = 'HELPER ADMIN ❗️'

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit() 
       else:
        pass
       from utils import scor_summ
       balance3 = await scor_summ(balance)
       
       if ethereum >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          ethereum = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET ethereum = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit() 
       else:
        pass
       
       ethereum3 = await scor_summ(ethereum)

       if bank >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          bank = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()   
       else:
        pass
       bank3 = await scor_summ(bank)

       if rating >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          rating = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET rating = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
       else:
        pass
       rating3 = await scor_summ(rating)


       text_profile= f'''
{name} , ваш профиль : 
👤 <b>Ник:</b> <code><a href='tg://user?id={user_id}'>{user_name}</a></code>
🔎 <b>ID:</b> <code>{user_id}</code>
💼 <b>Префикс:</b> <code>{pref} </code>
❗️ <b>Привилегия:</b> <code>{priv}</code>
💵 <b>Деньги:</b> <code>{balance3}</code>
🏛 <b>В банке:</b> <code>{bank3}</code>
🟪 <b>Эфириум:</b> <code>{ethereum3} шт</code>
💎 <b>Рейтинг:</b> <code>{rating3}</code>
📊 <b>Репутация:</b> <code>{reput}</code>
🪙 <b>Donate-coins:</b> <code>{donate_coins2}</code>
🎯 <b>Всего сыграно игр:</b> <code>{game2}</code>
<b>{d6}</b>{house2}{cars2}\n<b>{all_org2}</b>{family}

📆 <b>Дата регистрации:</b> <code>{time_register}</code>
       '''

       await bot.send_message(message.chat.id, text_profile,  parse_mode='html')

###########################################БАНК###########################################
    # bank
    if message.text.lower() in ["Банк", "банк"]:
       msg = message
       chat_id = message.chat.id
       
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank_hran = cursor.execute("SELECT bank2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = int(bank[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?",(message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       bank_hran = int(bank_hran[0])
       bank_hran2 = '{:,}'.format(bank_hran).replace(',', '.')
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = int(bank[0])
       depozit2 = '{:,}'.format(depozit).replace(',', '.')
       bank2 = '{:,}'.format(bank).replace(',', '.')
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2).replace(',', '.')

       c = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
       if bank >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          bank = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          bank2 = '{:,}'.format(bank).replace(',', '.')
       else:
          pass
       if bank_hran >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          bank_hran = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank2 = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          bank_hran2 = '{:,}'.format(bank_hran).replace(',', '.')
       else:
          pass
       if depozit >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          depozit = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET depozit = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          depozit2 = '{:,}'.format(depozit).replace(',', '.')

       

       await bot.send_message(message.chat.id,f"<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные о вашем банке 🏦\n\n👨‍💼 | Владелец: {user_name}\n🏛 | Основной счёт: {bank2}$\n💼 | Хранительный счёт: {bank_hran2}$\n🔐 | Деньги на депозите: {depozit2}$\n     💎 Статус депозита: {stats_depozit}\n     📈 Процент под депозит: {procent}\n      💵 Деньги на вывод: {money_vivod3}$", parse_mode='html')
    if message.text.startswith('процент') or message.text.startswith('Процент'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i2 = str(msg.text.split()[1])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2).replace(',', '.')
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i2 == 'снять':
          if summ <= money_vivod2 :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли проценты с депозита {summ2}$ 💵", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но снимать с процентов депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
   

   
    if message.text.startswith('депозит') or message.text.startswith('Депозит'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i = str(msg.text.split()[1])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i == 'положить':
          if summ <= balance :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили на депозит {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя ложить отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
       if i == 'снять':
          if summ <= depozit :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли с депозита {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
          
    if message.text.startswith("Банк положить") or message.text.startswith("банк положить"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       bank_p = int(su3)

       if bank_p >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя ложить в банк больше лимита")
          return

       print(f"{name} положил в банк: {bank_p}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_p).replace(',', '.')
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       period = 180
       get = cursor.execute(f"SELECT stavka FROM time_bank WHERE user_id = {user_id}").fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if bank_p > 0:
             if balance >= bank_p:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили в банк {bank2}$ {rwin}",
                                        parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bank = {bank + bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE time_bank SET stavka = {time.time()} WHERE user_id = {user_id}')
                connect.commit()

             elif int(balance) < int(bank_p):
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств! {rloser}", parse_mode='html')

          if bank_p <= 0:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя положить в банк отрицательное число! {rloser}",
                                     parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ложить в банк можно раз в 3 минуты", parse_mode='html')
    if message.text.startswith("Банк снять") or message.text.startswith("банк снять"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       bank_s = int(su3)
       print(f"{name} снял с банка: {bank_s}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_s).replace(',', '.')
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       if bank_s > 0:
          if bank >= bank_s:
             await bot.send_message(message.chat.id,
                                    f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли с банковского счёта {bank2}$ {rwin}",
                                    parse_mode='html')
             cursor.execute(f'UPDATE users SET bank = {bank - bank_s} WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance + bank_s} WHERE user_id = "{user_id}"')
             connect.commit()

          elif int(bank) < int(bank_s):
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств на банковском счету! {rloser}",
                                    parse_mode='html')


###########################################АДМИН КОМАНДЫ###########################################
    if message.text.startswith("Поделить") or message.text.startswith("поделить"):
       if not message.reply_to_message:
                await message.reply("❗️ <b>Эта команда должна быть ответом на сообщение</b>", parse_mode='html')
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       console = cursor.execute('SELECT user_id from users where user_status = "Owner"').fetchall()
       console2 = cursor.execute('SELECT user_id from users where user_status = "Helper_Admin"').fetchall()
       console3 = []

       for console_owner in console:
         console3.append(console_owner[0])
      
       for console_helper in console:
         console3.append(console_helper[0])
       
       if int(balance2 / perevod) <= 0:
          return await message.reply(f'❗️ <b>Запрещено</b> чтобы баланс игрока был равен отрицательному числу', parse_mode='html')
       else:
         pass
      
       text = f'''
⛔️ <b>Администратор:</b> <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ <b>Действие:</b> <code>Деление баланса</code>
💈 <b>Количество:</b> <code>{perevod2} раз</code>
👨 <b>Игроку:</b> <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       '''
       if user_status[0] == 'Owner':
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 / perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')

          await bot.send_message(config.owner_id,f'⚠️ <b>ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b> \n\n{text}', parse_mode='html')
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 / perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f"⚠️ <b>ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b> \n\n{text}", parse_mode='html')

          await bot.send_message(config.owner_id,f'⚠️ <b>ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b> \n\n{text}', parse_mode='html')
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 /  perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')



    
    if message.text.startswith('Выдать донат') or message.text.startswith('выдать донат'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)

       if user_status == 'Owner':
          text = f'''
⛔️ <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a><b>, вам было начислено <code>{'{:,}'.format(summ).replace(',','.')}</code> Donate Coins</b> 🪙
          '''
          await bot.send_message(message.chat.id,text, parse_mode='html')
          cursor.execute(f'UPDATE users SET donate_coins = {donate_coins + summ} WHERE user_id = {reply_user_id}')
          connect.commit()
       else:
          pass
    if message.text.lower() == 'забрать права':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          text = f'''
⛔️<b> Разработчик: <a href="tg://user?id={user_id}">{user_name}</a> забрал все права администрации у игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a></b>
          '''
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Player" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>OWNER</b>', parse_mode='html')

    if message.text.lower() == 'передать права':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          text = f'''
⛔️ <b>Разработчик: <a href='tg://user?id={user_id}'>{user_name}</a> передал все права игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a></b>
          '''
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Owner" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f"🆘 | Данная команда доступна только администрации с уровнем \"OWNER\"")
    if message.text.lower() == 'выдать админа':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          text = f'''
⛔️ Разработчик: <a href='tg://user?id={user_id}'>{user_name}</a> выдал права администратора уровня <b>ADMIN</b> игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
          '''
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Admin" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f"🆘 | Данная команда доступна только администрации с уровнем \"OWNER\"")
    if message.text.lower() == 'выдать хелпера':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          text = f'''
⛔️ |Разработчик: <a href='tg://user?id={user_id}'>{user_name}</a> выдал права администратора уровня <b>HELPER ADMIN</b> игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
          '''
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Helper_Admin" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>OWNER</b>', parse_mode='html')

    if message.text.lower() in ["админ", "Админ"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       admin_menu = InlineKeyboardMarkup(row_width=1)
       Admins_menu_up = InlineKeyboardButton(text='Войти ✅', callback_data='Admins_menu_up')
       admin_menu.add(Admins_menu_up)
       await bot.send_message(message.chat.id,f"<a href='tg://user?id={user_id}'>{user_name}</a>, войдите в админ меню 🆘", reply_markup=admin_menu, parse_mode='html')
    
    if message.text.startswith("Умножить") or message.text.startswith("умножить"):
       if not message.reply_to_message:
                await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
                return
                
       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 * perevod) >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  Достигнул лимит баланса! 999 фенд!", parse_mode='html')
          return
       
       text = f'''
⛔️ <b>Администратор:</b> <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ <b>Действие:</b> <code>Умножение баланса</code>
💈 <b>Количество:</b> <code>{perevod2} раз</code>
👨 <b>Игроку:</b> <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       '''
       if user_status[0] == 'Owner':

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await message.reply(text, parse_mode='html')

          await bot.send_message(config.owner_id, text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await message.reply(text, parse_mode='html')

          await bot.send_message(config.owner_id, text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')

    if message.text.startswith("выдать") or message.text.startswith("Выдать"):
       if not message.reply_to_message:
                await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 + perevod) >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  Достигнул лимит баланса! 999 фенд!", parse_mode='html')
          return
       text = f'''
⛔️ <b>Администратор:</b> <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ <b>Действие:</b> <code>Выдача денег</code>
💈 <b>Количество:</b> <code>{perevod2}$</code>
👨 <b>Игроку:</b> <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       '''
       if user_status[0] == 'Owner':
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id, text, parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id, text, parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return 
       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')


    if message.text.startswith("забрать") or message.text.startswith("Забрать"):
       if not message.reply_to_message:
                await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 - perevod) < 0:
         
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя заберать больше <b>баланса игрока</b>", parse_mode='html')
          return

       text = f''''
⛔️ <b>Администратор:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚙️ <b>Действие:</b> <code>Отбор денег</code>
💈 <b>Количество:</b> <code>{perevod2}$</code>
👨 <b>Игроку:</b> <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       '''

       if user_status[0] == 'Owner':
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id, text, parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id, text, parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')

    if message.text.lower() in ["обнулить", "Обнулить"]:
       if not message.reply_to_message:
                await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>")
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       reply_user_id = msg.reply_to_message.from_user.id
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()

       text = f'''
⛔️ <b>Администратор:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚙️ <b>Действие:</b> <code>Обнуление</code>
👨 <b>Игроку:</b> <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       '''

       if user_status[0] == 'Owner':
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET donate_coins = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET silver = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET gold = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'DELETE from user_family WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'DELETE from family WHERE owner_id = "{reply_user_id}"')
          

          connect.commit() 
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id,f'⚠️ <b>ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b> \n\n{text}', parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET silver = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET gold = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'DELETE from user_family WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'DELETE from family WHERE owner_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id,f'⚠️ <b>ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b> \n\n{text}', parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET silver = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET gold = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'DELETE from user_family WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'DELETE from family WHERE owner_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE user_case SET case_money = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE user_case SET case_donate = {0} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')
###########################################ПРАВИЛА###########################################
    if message.text.lower() in ["Правила", "правила"]:
       await bot.send_message(message.chat.id, f"""
🤬 | 1. Оскорбление [Мут - 15 минут ]
🤬 | 1.1 Оскорбление друзей личности [Мут - 10 минут]
🤬 | 1.2 Оскорбление родителем/родственников [Мут - 2 часа] + [ Варн ]
🤬 | 1.3 Оскорбление администрации [Мут - от 2 до 5 часов ] + [ Варн ]
🤬 | 1.4 Провокация на оскорбление [Мут - 5 минут]
🔞 | 2. Порнография в любом виде [Мут - 5 минут]
🔞 | 2.1 Спам контента порнографии [ Мут - 15 минут ]
🚷 | 3. Обман игроков [ Бан - 1 день ] + [ Варн ]
⛔️ | 4. Продажа игровой валюты [ Бан - 7 дней ] + [ Варн ] + [ Обнуление ]
⛔️ | 4.1 Продажа "Схем заработка" [Бан - 3 дня ] + [ Варн ]
⚠️ | 5. Капс (ПРИМЕР) [ Мут - 1 минута ]
⚠️ | 5.1 Флуд , спам [ Мут - 15 минут ]
⚠️ | 5.2 Не соглашёная реклама [ Мут - 1 час ] 
🆘 | 6. Любые действия связанные с вредом проекту [ Бан - 1 день ] + [ Варн ] [Если вред был нанесён тогда чс проекта ]
🆘 | 6.1 Читерство/Дюпинг в боте [ Обнуление ] + [ Варн ]      
       """, parse_mode='html')
###########################################ПОМОЩЬ###########################################
    if message.text.lower() in ["помощь", "Помощь"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])


       await bot.send_message(message.chat.id, f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, Вот информация о боте 🔎

📊 {config.channel} - <b>Игровой канал</b>
💬 {config.chat} - <b>Игровой чат</b>
💬 {config.chat2} - <b>Игровой чат</b>
🧑‍💻 {config.owner} - <b>Разработчик</b>

➖➖➖➖➖➖➖➖➖➖➖

📖 Доступные категории:

📝 <b>Основные</b>
🎮 <b>Игры </b>
🔨 <b>Работы</b>
🏘 <b>Имущество</b>
📖 <b>Привилегии</b>
⛔️ <b>Admins menu </b>
❕ <b>Остальные</b> 

➖➖➖➖➖➖➖➖➖➖➖
↘️Выберите одну из доступных <b>категорий </b>
    ''', reply_markup=help2, parse_mode='html')

###########################################СПИН#############################################
    if message.text.startswith("спин") or message.text.startswith("Спин"):
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])

        balance2 = '{:,}'.format(balance).replace(',', '.')
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        rx = random.randint(0, 1001)
        msg = message
        user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
        user_name = str(user_name[0])

        user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
        user_status = str(user_status[0])

        name = msg.from_user.full_name
        su = msg.text.split()[1]
        su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
        su3 = float(su2)
        summ = int(su3)

        summ2 = '{:,}'.format(summ).replace(',', '.')
        print(f"{name} поставил в спин: {summ} и выиграл/проиграл: {rx}")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))

        if user_status in ['Vlaselin', 'Bog']:
           period = 2
        elif user_status in ['Admin', 'Helper_Admin', 'Owner']:
           period = 1
        else:
           period = 5
         
        get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        loz = ['💩|👑|👑','💩|🖕|👑','💎|🖕|👑','💎|💣|🍌','👑|🍌|🖕','💎|🍓|💣']
        win = ['💎|🍓|🍌','👑|💎|🍓','🍓|👑|💎','💎|🍓|🍌','💎|🍓|🍓','🍌|🍌|💎']
        Twin = ['💎|💎|💎','🍓|🍓|🍓','👑|👑|👑','🍌|🍌|🍌']
        smtwin = ['🤯','🤩','😵','🙀']
        smwin = ['🙂', '😋', '😄', '🤑', '😃']
        loser = ['😔', '😕', '😣', '😞', '😢']
        rsmtwin = random.choice(smtwin)
        rsmtwin2 = random.choice(smtwin)
        rtwin = random.choice(Twin)
        rloser = random.choice(loser)
        rloser2 = random.choice(loser)
        rwin = random.choice(win)
        rloz = random.choice(loz)
        rsmwin = random.choice(smwin)
        rsmwin2 = random.choice(smwin)
        if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance).replace(',', '.')
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(0, 350):
                        c = Decimal(summ * 2)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2).replace(',', '.')

                        await bot.send_message(chat_id,
                                               f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 <b>Игра:</b> <code>Спин</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{rwin} - {c2}$</code>",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return

        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(351, 1000):
                        c = Decimal(summ * 0)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2).replace(',', '.')
                        await bot.send_message(chat_id,
                                               f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 <b>Игра:</b> <code>Спин</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Проигрыш:</b> <code>{rloz} - {c2}$</code>",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 0)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) == 1001:
                        c = Decimal(summ * 25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2).replace(',', '.')
                        await bot.send_message(chat_id,
                                               f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 <b>Игра:</b> <code>Спин</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{rwin} - {c2}$</code>",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 25)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return
                elif summ <= 1:
                    await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число! {rloser}",
                                           parse_mode='html')
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
        else:
            await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, извини. но играть можно только каждые {period} секунд. {rloser}",
                                       parse_mode='html')


################################################### GAME-VB ########################################


    if message.text.lower() in ['vb', "вб"]:
       msg = message
       user_id = msg.from_user.id
   
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот вся информация за игру "Game-VB" 🧊

📌 | Пример: /gamevb

⚠️ | ВАЖНО: Это игра, в которой нету ставки. В этой игре вы играете сразу на весь свой баланс

⚖️ | Шансы:
🟥 | 70% - LOSER - [0.1X]
🟩 | 30% - WIN - [1.5X]
       """, parse_mode='html')

#################################################### ФУТБОЛ ########################################

    if message.text.lower() in ['футбол', "фб"]:
       msg = message
       user_id = msg.from_user.id
   
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот вся информация за игру "Футбол" ⚽️

📌 | Пример: Футбол\Фб [ставка] | Футбол 1

⚖️ | Шансы:
🟥 | 29% - Промах - [0.2Х]
🟥 | 31% - Штанга - [0.4Х]
🟥 | 20% - Перекладина - [0.8X]
🟩 | 12% - Гол - [1.4X]
🟩 | 3% - Девятка - [2.3X]
🟩 | 1% - Крестовина - [4.3X]
""", parse_mode='html')





    if message.text.startswith('Фб') or message.text.startswith('фб'):
       msg = message
       user_id = msg.from_user.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance).replace(',', '.')

       rx = random.randint(0,9550)
       
       if user_status in ['Vlaselin', 'Bog']:
          period = 2
       elif user_status in ['Admin', 'Helper_Admin', 'Owner']:
          period = 1
       else:
          period = 5

       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0,2900):
                   i = summ - summ * 0.2
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Проигрыш:</b> <code>Промах! - {i3}$</code> <b>[0.2X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(2901,6000):
                   i = summ - summ * 0.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Проигрыш:</b> <code>Штанга! - {i3}$</code> <b>[0.4X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(6001,8000):
                   i = summ - summ * 0.8
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Проигрыш:</b> <code>Перекладина! - {i3}$</code> <b>[0.8X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(8001,9200):
                   i = summ * 1.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Гол! - {i3}$</code> <b>[1.4X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9201,9500):
                   i = summ * 2.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Девятка! - {i3}$</code> <b>[2.3X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9501,9550):
                   i = summ * 4.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Крестовина! - {i3}$</code> <b>[4.3X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в {period} секунд ", parse_mode='html')




    if message.text.startswith('Футбол') or message.text.startswith('футбол'):
       msg = message
       user_id = msg.from_user.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance).replace(',', '.')

       rx = random.randint(0,9550)
       
       if user_status in ['Vlaselin', 'Bog']:
          period = 2
       elif user_status in ['Admin', 'Helper_Admin', 'Owner']:
          period = 1
       else:
          period = 5
          
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0,2900):
                   i = summ - summ * 0.2
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Проигрыш:</b> <code>Промах! - {i3}$</code> <b>[0.2X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(2901,6000):
                   i = summ - summ * 0.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Проигрыш:</b> <code>Штанга! - {i3}$</code> <b>[0.4X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(6001,8000):
                   i = summ - summ * 0.8
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Проигрыш:</b> <code>Перекладина! - {i3}$</code> <b>[0.8X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(8001,9200):
                   i = summ * 1.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Гол! - {i3}$</code> <b>[1.4X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9201,9500):
                   i = summ * 2.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Девятка! - {i3}$</code> <b>[2.3X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9501,9550):
                   i = summ * 4.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Крестовина! - {i3}$</code> <b>[4.3X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в {period} секунд ", parse_mode='html')









##################################################КАЗИНО############################################
   
    if message.text.startswith('казино') or message.text.startswith('Казино'):
      try:
         msg = message
         user_id = msg.from_user.id

         games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         games = int(games[0])

         user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
         user_status = str(user_status[0])

         su = msg.text.split()[1]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         summ = int(su3)

         summ2 = '{:,}'.format(summ).replace(',', '.')
         
         comment = msg.text.split()[2:]
         comment2 = ' '.join(comment)

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = round(int(balance[0]))

         rx = random.randint(0, 960)

         if len(comment2) > 50:
            return await message.reply(f'❗️ <b>Ваш комментарий</b> не может быть больше чем 50 символов ', parse_mode='html')
         else:
            pass

         if comment2 == '':
            comment3 = ''
         else:
            comment3 = f'\n<b>💬 Комментарий:</b> <code>{comment2}</code>'
         if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance).replace(',', '.')

         if user_status in ['Vlaselin', 'Bog']:
            period = 2
         elif user_status in ['Admin', 'Helper_Admin', 'Owner']:
            period = 1
         else:
            period = 5

         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = f"{int(get[0])}"
         stavkatime = time.time() - float(last_stavka)

         if stavkatime < period:
            return await message.reply(f'❗️ Играть можно раз в <b>{period} секунд</b>', parse_mode='html')
         else:
            pass
         
         if balance < summ:
            return await message.reply(f'❗️ У вас <b>недостаточно средств</b>', parse_mode='html')
         else:
            pass
         
         if summ <= 0:
            return await message.reply('❗️ Ставка не может быть отрицательным числом <b>[0 и меньше]</b>', parse_mode='html')
         else:
            pass
         
         if int(rx) in range(0, 100):
            status_stavka = 'Проигрыш'
            stavka = summ
            stavka2 = summ2
            stavka_x = 'x0'
            stavka_smile = ['🙃', '😕', '😔', '😪']
            balance_new = balance - stavka
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
            connect.commit()

         if int(rx) in range(101, 350):
            status_stavka = 'Проигрыш'
            stavka = int(summ - summ * 0.3)
            stavka2 = '{:,}'.format(stavka).replace(',', '.')
            stavka_x = 'x0.3'
            stavka_smile = ['🙃', '😕', '😔', '😪']
            balance_new = balance - stavka
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.7} WHERE user_id = {user_id}')
            connect.commit()

         if int(rx) in range(351, 700):
            status_stavka = 'Проигрыш'
            stavka = int(summ - summ * 0.5)
            stavka2 = '{:,}'.format(stavka).replace(',', '.')
            stavka_x = 'x0.5'
            stavka_smile = ['🙃', '😕', '😔', '😪']
            balance_new = balance - stavka
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.5} WHERE user_id = {user_id}')
            connect.commit()

         if int(rx) in range(701, 850):
            status_stavka = 'Выигрыш'
            stavka = int(summ * 1.5)
            stavka2 = '{:,}'.format(stavka).replace(',', '.')
            stavka_x = 'x1.5'
            stavka_smile = ['🙃', '😕', '😔', '😪']
            balance_new = balance - stavka
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {(balance + summ * 1.5)} WHERE user_id = {user_id}')
            connect.commit()

         if int(rx) in range(851, 950):
            status_stavka = 'Выигрыш'
            stavka = int(summ * 2.8)
            stavka2 = '{:,}'.format(stavka).replace(',', '.')
            stavka_x = 'х2.8'
            stavka_smile = ['😌', '😇', '😲', '🤑']
            balance_new = balance 
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {(balance + summ * 2.8)} WHERE user_id = {user_id}')
            connect.commit()

         if int(rx) in range(951, 960):
            status_stavka = 'Выигрыш'
            stavka = int(summ * 5)
            stavka2 = '{:,}'.format(stavka).replace(',', '.')
            stavka_x = 'x5'
            stavka_smile = ['😌', '😇', '😲', '🤑']
            balance_new = (balance - summ) + stavka
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {(balance +summ * 5)} WHERE user_id = {user_id}')
            connect.commit()

         
         text = f'''
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
🤵‍♀️ <b>Игра:</b> <code>Казино</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>{status_stavka}:</b> <code>{stavka2}$</code>  <b>({stavka_x})</b>{comment3}
         '''
         await message.bot.send_message(message.chat.id, text, parse_mode='html')
         cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
         connect.commit()
      except IndexError:
         return await message.reply(f'❗️ <b>Вы не вели сумму ставки -</b> <code>казино 1</code> ', parse_mode='html')
      except ValueError:
         return await message.reply(f'❗️ <b>Вы не правильно ввели сумму - <code>казино 1</code> | <code>казино 1е1</code> | <code>казино 1к</code></b>', parse_mode='html')





###########################################PLINKO###########################################
    
    
    if message.text.startswith("плинко") or message.text.startswith("Плинко"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       win = ['🙂', '😋', '😄', '😃']
       loser = ['😔', '😕', '😣', '😞', '😢']
       rx = random.randint(0,937)
       rwin = random.choice(win)
       rloser = random.choice(loser)

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       name = msg.from_user.full_name 

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)

       summ2 = '{:,}'.format(summ).replace(',', '.')
       print(f"{name} поставил в казино: {summ} и выиграл/проиграл: {rx}")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance).replace(',', '.')

       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0,100):
                   c = Decimal(summ)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Проигрыш:</b> <code>0$</code> <b>[x0]</b>", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit()   
                   return                           
                if int(rx) in range(101,300):
                   c = Decimal(summ - summ * 0.25)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Проигрыш:</b> <code>{c2}$</code> <b>[x0.25]</b>", parse_mode='html')                   
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.75} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit()  
                   return   
                if int(rx) in range(301,600):
                   c = Decimal(summ * 0.5)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Проигрыш:</b> <code>{c2}$</code> <b>[x0.25]</b>", parse_mode='html')                   
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.75} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.5} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return  
                if int(rx) in range(601,850):
                   c = Decimal(summ - summ * 0.75)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x0.75]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.25} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return  
                if int(rx) in range(851,900):
                   c = Decimal(summ * 2)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x2]</b>", parse_mode='html')                   
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.75} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return 
                if int(rx) in range(901,930):
                   c = Decimal(summ * 3)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x3]</b>", parse_mode='html')                   
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 3)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return
                if int(rx) in range(931,932):
                    c = Decimal(summ * 29)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(config.owner_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x29]</b>", parse_mode='html')                   

                    await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x29]</b>", parse_mode='html')                   
                    cursor.execute(
                        f'UPDATE users SET balance = {(balance - summ) + (summ * 29)} WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                    connect.commit()
                if int(rx) in range(933,937):
                   c = Decimal(summ * 10)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x10]</b>", parse_mode='html')                   

                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x10]</b>", parse_mode='html')                   
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 10)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return 
             elif summ <= 1:
                  await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число! {rloser}", parse_mode='html')                                      
          elif int(balance) <= int(summ):
               await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
       else:
        await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, извини. но играть можно только каждые 5️⃣ секунд. {rloser}", parse_mode='html')
        return











###########################################РЕЙТИНГ###########################################
    if message.text.lower() == 'рейтинг':
       msg = message
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                    (message.from_user.id,)).fetchone()
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       bank = int(bank[0])
       rating = int(rating[0])
       rating2 = '{:,}'.format(rating).replace(',', '.')
       rey = ['👑','✨','✏️']
       ranrey = random.choice(rey)
       
      
       await bot.send_message(message.chat.id, f"💎 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш рейтинг - {rating2}", parse_mode='html')

    if message.text.startswith("рейтинг купить") or message.text.startswith("Рейтинг купить"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)

       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = int(rating[0])
       rating2 = '{:,}'.format(summ).replace(',', '.')
       c = summ * 150000000
       c2 = '{:,}'.format(c).replace(',', '.')

       if (summ + rating) >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя покупать рейтинг больше лимита")
          return

       if summ > 0:
          if int(balance) >= int(summ * 150000000):
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы повысили количество вашего рейтинга на {rating2}💎 за {c2}$! {rwin}", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance - c} WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET rating = {rating + summ} WHERE user_id = "{user_id}"')
             connect.commit()

 
       if int(balance) < int(summ * 150000000):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')

       if summ <= 0:
         await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя купить отрицательное число! {rloser}", parse_mode='html')
    
    if message.text.startswith("Рейтинг продать") or message.text.startswith("рейтинг продать"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = int(rating[0])
       c = summ * 100000000
       c2 = '{:,}'.format(c).replace(',', '.')
       rating2 = '{:,}'.format(summ).replace(',', '.')
       if summ > 0:
        if int(rating) >= int(summ):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы понизили количество вашего рейтинга на {rating2}💎 за {c2}$! {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + c} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE users SET rating = {rating - summ} WHERE user_id = "{user_id}"')
          connect.commit()

        if int(rating) < int(summ):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, у вас недостаточно рейтинга для его продажи! {rloser}", parse_mode='html')

       if summ <= 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя продать отрицательное число! {rloser}", parse_mode='html')


###########################################ПЕРЕВОДЫ###########################################
    if message.text.startswith("передать") or message.text.startswith("Передать"):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.full_name 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       id_perevod = int(msg.text.split()[2])
       
       name_id_perevod = cursor.execute(f'SELECT user_name from users where user_id ="{id_perevod}"')
       name_id_perevod = str(name_id_perevod[0])

       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       print(f"{name} перевел: {perevod} игроку на ID: {id_perevod}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       if perevod > 0:
          if balance >= perevod:  
             if user_status in ['Admin', 'Helper_Admin']:
               await bot.send_message(config.owner_id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег по ID\n💈 | Сумма: {perevod2}\n👨 | Игроку: {name_id_perevod}", parse_mode='html')

             await bot.send_message(id_perevod, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег по ID\n💈 | Сумма: {perevod2}\n👨 | Игроку: {name_id_perevod}", parse_mode='html')
             await message.reply_to_message.reply(f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег по ID\n💈 | Сумма: {perevod2}\n👨 | Игроку: {name_id_perevod}", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance - perevod} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{id_perevod}"')
             connect.commit()    
   
          elif int(balance) <= int(perevod):
             await message.reply( f'{user_name}, недостаточно средств! {rloser}', parse_mode='html')

       if perevod <= 0:
          await message.reply( f'{user_name}, нельзя перевести отрицательное число! {rloser}', parse_mode='html')  

    if message.text.startswith("Дать") or message.text.startswith("дать"):
       if not message.reply_to_message:
          await message.reply("Эта команда должна быть ответом на сообщение!")
          return
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.full_name 
       rname =  msg.reply_to_message.from_user.full_name 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       print(f"{name} перевел: {perevod} игроку {rname}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       
       
       if reply_user_id == user_id:
          await message.reply_to_message.reply(f'Вы не можете передать деньги сами себе! {rloser}', parse_mode='html')
          return

       if perevod > 0:
          if balance >= perevod:  
             await bot.send_message(config.owner_id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег\n💈 | Сумма: {perevod2}$\n👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

             await message.reply_to_message.reply(f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег\n💈 | Сумма: {perevod2}$\n👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance - perevod} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
             connect.commit()    
   
          elif int(balance) <= int(perevod):
             await message.reply( f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')

       if perevod <= 0:
          await message.reply( f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя перевести отрицательное число! {rloser}", parse_mode='html')  


###########################################ТОП###########################################
    if message.text.lower() in ["топ", "Топ"]:
       list = cursor.execute(f"SELECT * FROM users ORDER BY rating DESC").fetchmany(10)
       top_list = []
       user_id = message.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       num = 0

       

       for user in list:
           if user[7] >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
              c6 = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
           else:
              c6 = user[7]

           

           num += 1

           if num == 1:
              num2 = '1️⃣'
              num3 = ' <b>💎ТОП 1💎</b> |'
           if num == 2:
              num2 = '2️⃣'
              num3 = ''
           if num == 3:
              num2 = '3️⃣'
              num3 = ''
           if num == 4:
              num2 = '4️⃣'
              num3 = ''
           if num == 5:
              num2 = '5️⃣'
              num3 = ''
           if num == 6:
              num2 = '6️⃣'
              num3 = ''
           if num == 7:
              num2 = '7️⃣'
              num3 = ''
           if num == 8:
              num2 = '8️⃣'
              num3 = ''
           if num == 9:
              num2 = '9️⃣'
              num3 = ''
           if num == 10:
              num2 = '🔟'
              num3 = ''
           c = Decimal(c6)
           c2 = '{:,}'.format(c).replace(',', '.')

           if user[3] == 'Owner':
             stats = ' ✅<b>РАЗРАБОТЧИК</b>✅ |'
           if user[3] == 'Admin':
             stats = ' ⛔️<b>АДМИН</b>⛔️ |'
           if user[3] == 'Helper_Admin':
             stats = ' ⚠️<b>HELPER АДМИН</b>⚠️ |'
           if user[3] in ['Player', 'Vip', 'Premium', 'Platina', 'Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin']:
             stats = ''
           
           
           top_list.append(f"{num2} {user[1]} |{stats}{num3} 🔎 ID: <code>{user[0]}</code> | {c2}💎")

       top = "\n".join(top_list)
       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, топ 10 игроков бота:\n" + top, reply_markup=fulltop, parse_mode='html')
# Смена имени
    if message.text.startswith('Сменить ник') or message.text.startswith('cменить ник'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       chat_id = message.chat.id
       user_id = message.from_user.id
       su = " ".join(message.text.split()[2:])
       name = (su).replace('🇺🇦', '').replace('🇷🇺','').replace('🇷🇸','').replace('🇸🇰','').replace('🇸🇮','').replace('ᅠᅠᅠᅠᅠ','')

       if name in ['', ' ', '  ', '   ','    ', '     ', '      ', '       ','        ','         ','          ','           ','            ','              ','              ','               ','                ','            ']:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш ник не может быть пустым", parse_mode='html')
          return

       if len(name) <= 20:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно поменяли свое имя на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET user_name = \"{name}\" WHERE user_id = "{user_id}"')
          print(f"{user_name} сменил ник на {name}")

          all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
          all_family2 = []
          proverka_family = 0
          for all_owner_id in all_family:
            all_family2.append(all_owner_id[0])

          user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

          if user_id_family != None:
            cursor.execute(f'UPDATE user_family SET user_name = \"{name}\" WHERE user_id = "{user_id}"')
          else:
            pass

          if user_id in all_family2:
            cursor.execute(f'UPDATE family SET owner_name = \"{name}\" WHERE owner_id = "{user_id}"')
          else:
            pass

       else: 
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a> , ваш ник не может быть длинее 20 символов!", parse_mode='html')
    if message.text.lower() == 'Эфириум':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?", (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       await bot.send_message(message.chat.id,f"🟪 | <a href='tg://user?id={user_id}'>{user_name}</a>, количество эфириума: {ethereum}🟣")

    if message.text.lower() == 'эфириум курс':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       c = api.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']
       c2 = int(c)
       c3 = '{:,}'.format(c2).replace(',', '.')

       await bot.send_message(message.chat.id,f"🟪 | <a href='tg://user?id={user_id}'>{user_name}</a>, курс эфириума: {c3}🟣", parse_mode='html')
    if message.text.startswith('Эфириум') or message.text.startswith('эфириум'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       i = str(message.text.split()[1])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       d = int(su3)
       d2 = '{:,}'.format(d).replace(',', '.')
       c = api.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']
       c2 = int(c)
       c3 = '{:,}'.format(c2).replace(',', '.')

       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?", (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       summ = d * c2
       summ2 = '{:,}'.format(summ).replace(',', '.')

       if summ >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  достигнул лимит, 999 фенд")
          return

       if i == 'купить':
          if summ <= balance:
             if d > 0:
                await bot.send_message(message.chat.id, f" 💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {d2} эфириума 🟣 за {summ2}$", parse_mode='html')
                cursor.execute(f'UPDATE users SET ethereum = {ethereum + d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')
       if i == 'продать':
          if d <= ethereum:
             if d > 0:
                await bot.send_message(message.chat.id, f" 💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {d2} эфириума 🟣 за {summ2}$", parse_mode='html')
                cursor.execute(f'UPDATE users SET ethereum = {ethereum - d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')          
    
    
    if message.text.lower() == 'ограбить банк':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       x = random.randint(1,3)
       period = 86400 #86400 s 24h
       get = cursor.execute("SELECT stavka_bank FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       rx = random.randint(1000000,25000000)
       rx2 = '{:,}'.format(rx).replace(',', '.')
       if stavkatime > period:
          if int(x) in range(2,3):
             await bot.send_message(message.chat.id, f"🏦 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно ограбили банк на {rx2}$ ✅", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + rx} WHERE user_id ="{user_id}"')
             cursor.execute(f'UPDATE bot_time SET stavka_bank = {time.time()} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, вам не удалось ограбить банк", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ограбить банк можно раз в 24ч⏳", parse_mode='html')
# bonus 24h
    
    
    if message.text.lower() == 'ежедневный бонус':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       period = 86400 #86400 s = 24h
       get = cursor.execute("SELECT stavka_bonus FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       
       rx = random.randint(1000000,25000000)
       rx2 = '{:,}'.format(rx).replace(',', '.')

       if stavkatime > period:
          await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ежедневный бонус в сумме {rx2}$ 💵", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + rx}  WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bonus = {time.time()} WHERE user_id = "{user_id}"')
          connect.commit()
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, получать ежедневный бонус можно раз в 24ч⏳", parse_mode='html') 


#####################################КУБИК##############################################################
    if message.text.startswith('Кубик') or message.text.startswith('кубик'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])
         
         rx = random.randint(0,700)

         chil = int(message.text.split()[1])
         su = msg.text.split()[2]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         summ = int(su3)
         summ2 = '{:,}'.format(summ).replace(',', '.')
         
         
         
         summ_win = summ * 3
         summ_win2 = '{:,}'.format(summ_win).replace(',', '.')

         if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance).replace(',', '.')

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)
         if chil <= 6:
            if summ <= balance:
               if stavkatime > period:
                  if int(rx) in range(0,100):
                     if chil == 1:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲1 - {summ2}$\n🧾 | Выигрыш: 🎲1 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲1 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(101,200):
                     if chil == 2:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲2 - {summ2}$\n🧾 | Выигрыш: 🎲2 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲2 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(201,300):
                     if chil == 3:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲3 - {summ2}$\n🧾 | Выигрыш: 🎲3 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲3 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(401,500):
                     if chil == 4:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲4 - {summ2}$\n🧾 | Выигрыш: 🎲4 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲4 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(501,600):
                     if chil == 5:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲5 - {summ2}$\n🧾 | Выигрыш: 🎲5 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲5 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(601,700):
                     if chil == 6:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲6 - {summ2}$\n🧾 | Выигрыш: 🎲6 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲6 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
               else:
                  await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств!", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, данного числа нету в кубике!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример Кубик 6 1000", parse_mode='html')



#############################################################ЧЁТНОЕ \ НЕЧЁТНОЕ#########################################################



    if message.text.startswith('Нечётное') or message.text.startswith('нечётное'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])

         rx = random.randint(0,100)

         su = msg.text.split()[1]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         summ = int(su3)
         summ2 = '{:,}'.format(summ).replace(',', '.')

         if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance).replace(',', '.')

         summ_win = summ * 2
         summ_win2 = '{:,}'.format(summ_win).replace(',', '.')

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)

         if summ <= balance:
            if stavkatime > period:
               if int(rx) in range(0,65):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Нечётное - {summ2}$\n🧾 | Выигрыш: 🎲Чётное - 0$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
               if int(rx) in range(66,100):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Нечётное - {summ2}$\n🧾 | Выигрыш: 🎲Нечётное - {summ_win2}$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance + summ_win} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Чётное 1000", parse_mode='html')

    if message.text.startswith('Чётное') or message.text.startswith('чётное'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])

         rx = random.randint(0,100)

         su = msg.text.split()[1]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         summ = int(su3)
         summ2 = '{:,}'.format(summ).replace(',', '.')

         summ_win = summ * 2
         summ_win2 = '{:,}'.format(summ_win).replace(',', '.')

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)

         if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance).replace(',', '.')

         if summ <= balance:
            if stavkatime > period:
               if int(rx) in range(0,65):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Чётное - {summ2}$\n🧾 | Выигрыш: 🎲Нечётное - 0$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
               if int(rx) in range(66,100):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Чётное - {summ2}$\n🧾 | Выигрыш: 🎲Чётное - {summ_win2}$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance + summ_win} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Чётное 1000", parse_mode='html')




##################################################### WHEEL \ dice ##########################################################

    if message.text.startswith('dice') or message.text.startswith('Dice'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = user_status[0]

       game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       game = int(game[0])

       black_red = str(message.text.split()[1])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)


       summ2 = "{:,}".format(summ).replace(',', '.')

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance).replace(',', '.')

       if user_status in ['Bog','Vlaselin']:
          period = 2
       else:
          period = 5
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       if balance < summ:
          
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
          return
       if stavkatime > period:
          if black_red in ['ч',"черный","Ч", "Черный"]:
             rx = random.randint(0,1000)

             if rx in range(0,850):
                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: 0$ [🔴]   
               """, parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()
             if rx in range(851, 999):
                summ3 = summ * 2
                summ4 = '{:,}'.format(summ3).replace(',', '.')

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [⚫️]                       
               """, parse_mode='html')  
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.exencute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()   
             if rx == 1000:
                summ3 = summ * 8
                summ4 = '{:,}'.format(summ3).replace(',', '.')

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🟢]                        
               """, parse_mode='html')   
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit() 
          if black_red in ['к',"красный","К", "Красный"]:
             rx = random.randint(0,1000)

             if rx in range(0,850):
                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: 0$ [⚫️]   
               """, parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()
             if rx in range(851, 999):
                summ3 = summ * 2
                summ4 = '{:,}'.format(summ3).replace(',', '.')

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🔴]                       
               """, parse_mode='html')  
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.exencute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()   
             if rx == 1000:
                summ3 = summ * 8
                summ4 = '{:,}'.format(summ3).replace(',', '.')

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🟢]                        
               """, parse_mode='html')   
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()  

    if message.text.lower() in ['wheel','dice']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за игру Wheel 🎱

✒️ | Пример: dice [ч\к] [сумма]

⚙️ | ч - черный ⚫️
⚙️ | к - красный 🔴

⚖️ | Шансы: Черный ⚫️ - 50%, Красный 🔴 - 50%, Зерро 🟢 - 0.1%   
         """, parse_mode='html')

















############################################СИСТЕМА КРАФТА#############################
    if message.text.lower() == 'крафтить':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
   
       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       menu_craft = InlineKeyboardMarkup(row_width=2)
       resurs1 = InlineKeyboardButton(text='🟥 Кирка Zerro ⛏', callback_data='resurs1')
       resurs2 = InlineKeyboardButton(text='🟥 Грабли Zerro 🌾', callback_data='resurs2')
       resurs3 = InlineKeyboardButton(text='🟨 Кирка Cherick ⛏', callback_data='resurs3')
       resurs4 = InlineKeyboardButton(text='🟨 Грабли Cherick 🌾', callback_data='resurs4')
       menu_craft.add(resurs1, resurs2, resurs3, resurs4)

       if basement == 1:
          basement_name = 'Standard'
          basement_period = 30
       
       if basement == 2:
          basement_name = 'Plus++'
          basement_period = 15
      
       if basement == 3:
          basement_name = 'Euro Plus++'
          basement_period = 4
       

       if basement > 0:
          await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, добро пожаловать в подвал🕋

👤 | Владелец: {user_name}
🕋 | Подвал: {basement_name}
⏳ | Ограничение по времени: {basement_period} секунд

↘️Выберите предмет какой хотите скрафтить       
""",reply_markup=menu_craft, parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! У вас нету подвала", parse_mode='html')
    if message.text.lower() == 'система крафта':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные о системе крафта⚒

▶️ | ⬜️ - обычные
▶️ | 🟩 - редкие
▶️ | 🟦 - сверх-редкие
▶️ | 🟪 - эпические
▶️ | 🟥 - мифические
▶️ | 🟨 - легендарные


📦 | Предметы:
⛏ | [🟥] [1] Кирка Zerro 
🌾 | [🟥] [2] Грабли Zerro 
⛏ | [🟨] [3] Кирка Cherick 
🌾 | [🟨] [4] Грабли Cherick 

⚖️ | Шансы крафта предметов:
⛏ | [🟥] [1] Кирка Zerro - 35%
🌾 | [🟥] [2] Грабли Zerro - 35%
⛏ | [🟨] [3] Кирка Cherick - 10%
🌾 | [🟨] [4] Грабли Cherick - 10%

⚒ | Чтобы начать крафтить введите команду \"Крафтить\"
ℹ️ | Крафтить можно только при наличии подвала
ℹ️ | У каждого подвала есть свои ограничение по времени на крафт""", parse_mode='html')
########################################ДОМА########################################
    if message.text.lower() == 'продать подвал':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
    
       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       if basement == 1:
          summ = 5000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Standard'

       if basement == 2:
          summ = 10000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Plus++'

       if basement == 3:
          summ = 20000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Euro plus++'

       if basement > 0:
          await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🕋 |Действие: Продажа подвала\n🕋 | Подвал: {basement2}\n💈 |Продано за: {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас уже есть подвал", parse_mode='html')
          return


    if message.text.startswith('Купить подвал') or message.text.startswith('купить подвал') :
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
    
       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       member = int(message.text.split()[2])
       
       if member == 1:
          summ = 5000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Standard'

       if member == 2:
          summ = 10000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Plus++'

       if member == 3:
          summ = 20000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Euro plus++'

       if member > 0:
          if member < 4:
             if house > 0:
                if basement == 0:
                   if balance >= summ:
                      await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🕋 |Действие: Покупка подвала\n🕋 | Подвал: {basement2}\n💈 |Стоимость: {summ2}$", parse_mode='html')
                      cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                      cursor.execute(f'UPDATE house SET basement = {member} WHERE user_id = {user_id}')
                      connect.commit()
                   else:
                      await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средтсв!", parse_mode='html')
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас уже есть подвал", parse_mode='html')
             else:
                 await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету дома! Подвал можно покупать только имея дом", parse_mode='html')
          else:
              await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Нету такого номера подвала", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Нету такого номера подвала", parse_mode='html')



    if message.text.lower() in ['подвал', 'подвалы']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот список доступных подвалов 🕋

🕋 | [1] Standard - 5.000.000$
🕋 | [2] Plus++ - 10.000.000$
🕋 | [3] Euro Plus++ - 20.000.000$

🛒 Чтобы купить подвал себе в дом, введите команду \"Купить подвал [номер]\" """, parse_mode='html')
    
    
    
    
    if message.text.lower() == 'мой дом':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       if house == 1:
          house2 = 'Коробка'
       
       if house == 2:
          house2 = 'Сарай'

       if house == 3:
          house2 = 'Маленький домик'

       if house == 4:
          house2 = 'Квартира'

       if house == 5:
          house2 = 'Огромный дом'

       if house == 6:
          house2 = 'Коттедж'

       if house == 7:
          house2 = 'Вилла'

       if house == 8:
          house2 = 'Загородный дом'

       if basement == 1:
          basement2 = '\n🕋 | Подвал: Standard'


       if basement == 2:
          basement2 = '\n🕋 | Подвал: Plus++'
   

       if basement == 3:
          basement2 = '\n🕋 | Подвал: Euro Plus++'
      
       if basement == 0:
          basement2 = '\n🕋 | Подвал не имеиться'
         
       if house > 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш дом🏡\n\n👤 | Владелец: {user_name}\n🏠 | Дом: {house2}{basement2}\n\n🛒 Чтобы купить подвал , введите команду \"Подвалы\"\nℹ️ Чтобы продать подвал введите команду \"Продать подвал\"\nℹ️ Чтобы продать дом введите команду  \"Продать дом\"", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нету дома, что бы купить дом введите команду \"Дома\"", parse_mode='html')
    
    
    if message.text.lower() == 'продать дом':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       if basement == 1:
          basement2 = '\n🕋 | Подвал: Standard'
          summ_basement = 5000000

       if basement == 2:
          basement2 = '\n🕋 | Подвал: Plus++'
          summ_basement = 10000000

       if basement == 3:
          basement2 = '\n🕋 | Подвал: Euro Plus++'
          summ_basement = 20000000
       else:
          basement2 = ''
          summ_basement = 0

       if house == 1:
          house2 = 'Коробка'
          summ = 500000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 1


       if house == 2:
          house2 = 'Сарай'
          summ = 3000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 2
      
       if house == 3:
          house2 = 'Маленький домик'
          summ = 5000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 3
      
       if house == 4:
          house2 = 'Квартира'
          summ = 7000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 4
      
       if house == 5:
          house2 = 'Огромный дом'
          summ = 10000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 5

       if house == 6:
          house2 = 'Коттедж'
          summ = 50000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 6

       if house == 7:
          house2 = 'Вилла'
          summ = 100000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 7

       if house == 8:
          house2 = 'Загородный дом'
          summ = 5000000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 8

       if house > 0:
          await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏡 |Действие: Продажа дома\n🏠 | Дом: {house2}{basement2}\n💈 |Продано за: {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ + summ_basement} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас и так нету дома! Что бы купить дом введите команду \"Дома\"", parse_mode='html')
          return

    if message.text.startswith('купить дом') or message.text.startswith('Купить дом'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       member = int(message.text.split()[2])

       if member == 1:
          house2 = 'Коробка'
          summ = 500000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 1


       if member == 2:
          house2 = 'Сарай'
          summ = 3000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 2
      
       if member == 3:
          house2 = 'Маленький домик'
          summ = 5000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 3
      
       if member == 4:
          house2 = 'Квартира'
          summ = 7000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 4
      
       if member == 5:
          house2 = 'Огромный дом'
          summ = 10000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 5

       if member == 6:
          house2 = 'Коттедж'
          summ = 50000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 6

       if member == 7:
          house2 = 'Вилла'
          summ = 100000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 7

       if member == 8:
          house2 = 'Загородный дом'
          summ = 5000000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 8

       if house == 0:
          if member > 0:
             if member < 9:
                if summ <= balance:
                   await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏡 |Действие: Покупка дома\n🏠 | Дом: {house2}\n💈 |Стоимость: {summ2}$", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE house SET house = {member_house} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств!", parse_mode='html')               
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Нету такого номера дома!", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Нету такого номера дома!", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас уже есть дом, что бы продать дом введите команду \"Продать дом\"", parse_mode='html')







    if message.text.lower() == 'дома':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, доступные дома:
🏠 1. Коробка - 500.000$
🏠 2. Сарай - 3.000.000$
🏠 3. Маленький домик - 5.000.000$
🏠 4. Квартира - 7.000.000$
🏠 5. Огромный дом - 10.000.000$
🏠 6. Коттедж - 50.000.000$
🏠 7. Вилла - 100.000.000$
🏠 8. Загородный дом - 5.000.000.000$

🛒 Для покупки дома введите "Купить дом [номер]"
       
       """, parse_mode='html')  




#########################################МАШИНЫ#######################################################
    if message.text.lower() == 'моя машина':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       hp = cursor.execute("SELECT hp from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       benz = cursor.execute("SELECT benz from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])
       if benz < 0:
             benz2 = 0
       else:
          benz2 = benz
       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       
       if hp in range(76,100):
          hp2 = 'Хорошое 🟩'

       if hp in range(51,75):
          hp2 = 'Среднее 🟧 '
         
       if hp in range(26,50):
          hp2 = 'Плохое 🟥'

       if hp in range(2,25):
          hp2 = 'Ужасное 🛑'

       if hp < 2:
          hp2 = 'Требуется ремонт ⛔️'

       else:
          if hp == 100:
             hp2 = 'Хорошое 🟩'
          if hp == 76:
             hp2 = 'Хорошое 🟩'
          if hp == 75:
             hp2 = 'Среднее 🟧'
          if hp == 51:
             hp2 = 'Среднее 🟧'
          if hp == 50:
             hp2 = 'Плохое 🟥'
          if hp == 26:
             hp2 = 'Плохое 🟥'
          if hp == 25:
             hp2 = 'Ужасное 🛑'
          if hp == 2:
             hp2 = 'Ужасное 🛑'

       if cars > 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш автомобиль🚘\n\n👤 | Владелец: {user_name}\n🚗 | Автомобиль: {cars_name}\n🚨 | Состояние: {hp2}\n⛽️ | Бензин: {benz2}%\n💰 | Стоимость: {cars_summ2}$\n\nℹ️ Чтобы продать машину введите команду \"Машину продать\"", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! У вас и так нету машины", parse_mode='html')
     


    if message.text.lower() == 'машину продать':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')


       if cars > 0:
          await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Продажа машины\n🚘 | Машина: {cars_name}\n💈 |Проданно за: {cars_summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! У вас и так нету машины", parse_mode='html')
          return
      
    if message.text.startswith('Купить машину') or message.text.startswith('купить машину'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       member = int(message.text.split()[2])
       
       if member == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')


       if member > 0:
          if member < 19:
             if cars == 0:
                if balance >= cars_summ:
                   await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Покупка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: {cars_summ2}$", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - cars_summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET cars = {member} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! У вас уже есть машина", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')











    if message.text.lower() == 'машины':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, доступные машины:
🚗 1. Самокат - 10.000.000$
🚗 2. Велосипед - 15.000.000$
🚗 3. Гироскутер - 30.000.000$
🚗 4. Сегвей - 50.000.000$
🚗 5. Мопед - 90.000.000$
🚗 6. Мотоцикл - 100.000.000$
🚗 7. ВАЗ 2109 - 250.000.000$
🚗 8. Квадроцикл - 400.000.000$
🚗 9. Багги - 600.000.000$
🚗 10. Вездеход - 900.000.000$
🚗 11. Лада Xray - 1.400.000.000$
🚗 12. Audi Q7 - 2.500.000.000$
🚗 13. BMW X6 - 6.000.000.000$
🚗 14. Toyota FT-HS - 8.000.000.000$
🚗 15. BMW Z4 M - 10.000.000.000$
🚗 16. Subaru WRX STI - 40.000.000.000$
🚗 17. Lamborghini Veneno - 100.000.000.000$
🚗 18. Tesla Roadster - 300.000.000.000$

🛒 Для покупки машины введите "Купить машину [номер]"    
       
""", parse_mode='html')







############################################################ШАХТА############################################################
    if message.text.lower() == 'шахта':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id,f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за шахту ⛏

⛏ | Руды на шахте:
      🪨 | Камень -  40%
      ⛓ | Железо - 30%
      🪙 | Серебро - 15%
      🎇 | Бронза - 10%
      ⚜️ | Золото - 5%

ℹ️ | Чтобы продать какую руду , воспользуйтесь командой \"Продать [Руда] [Количество]\"
ℹ️ | Чтобы копать руду воспользуйтесь командой \"Копать руду\"       
       """, parse_mode='html')
    if message.text.startswith('продать') or message.text.startswith('Продать'):
      try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         # iron, silver, bronza, gold
         iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
         iron = int(iron[0])
         
         metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
         metall = int(metall[0])

         silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
         silver = int(silver[0])

         bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
         bronza = int(bronza[0])

         gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
         gold = int(gold[0])

         rud = str(message.text.split()[1])

         su = msg.text.split()[2]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         c = int(su3)

         summ = c * 25000
         summ2 = '{:,}'.format(summ).replace(',', '.')
         if rud == 'камень':
            if c <= iron:
               summ = c * 25000
               summ2 = '{:,}'.format(summ).replace(',', '.')
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} камень 🪨 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET iron = {iron - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
         if rud == 'железо':
            if c <= metall:
               summ = c * 45000
               summ2 = '{:,}'.format(summ).replace(',', '.')
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} железо ⛓ за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET metall = {metall - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')

         if rud == 'серебро':
            if c <= silver:
               summ = c * 125000
               summ2 = '{:,}'.format(summ).replace(',', '.')
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} серебро 🪙 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET silver = {silver - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
         if rud == 'бронзу':
            if c <= bronza:
               summ = c * 200000
               summ2 = '{:,}'.format(summ).replace(',', '.')
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} бронзы 🎇 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET bronza = {bronza - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')

         if rud == 'золото':
            if c <= gold:
               summ = c * 500000
               summ2 = '{:,}'.format(summ).replace(',', '.')
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} золото ⚜️ за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET bronza = {bronza - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
      except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Продать [камень, железо, серебро, бронзу, золото, лён, хлопок] 1", parse_mode='html')


    if message.text.lower() == 'копать руду':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       rx = random.randint(0,100)

      # iron, silver, bronza, gold
       iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
       iron = int(iron[0])
       
       metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
       metall = int(metall[0])

       silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
       silver = int(silver[0])

       bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])

       gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       
       rx_iron = random.randint(15,20)
       rx_metall = random.randint(10,15)
       rx_silver = random.randint(5,10)
       rx_bronza = random.randint(0,5)
       
       if pick == 'Cherick':
          period = 3
       else:
          period = 5
       get = cursor.execute("SELECT time_pick FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)

       if pick == 'Cherick':
          if stavkatime > period:
             if int(rx) in range(0,40):
                await bot.send_message(message.chat.id, f"🪨 | Вы успешно выкопали {rx_iron * 2} камня", parse_mode='html')
                cursor.execute(f'UPDATE mine SET iron = {iron + rx_iron * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(41,70):
                await bot.send_message(message.chat.id, f"⛓ | Вы успешно выкопали {rx_metall * 2} железа", parse_mode='html')
                cursor.execute(f'UPDATE mine SET metall = {metall + rx_metall * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(71,85):
                await bot.send_message(message.chat.id, f"🪙 | Вы успешно выкопали {rx_silver * 2} серебра", parse_mode='html')
                cursor.execute(f'UPDATE mine SET silver = {silver + rx_silver * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(86,95):
                await bot.send_message(message.chat.id, f"🎇 | Вы успешно выкопали {rx_bronza * 2} бронзы", parse_mode='html')
                cursor.execute(f'UPDATE mine SET bronza = {bronza + rx_bronza * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(96,100):
                await bot.send_message(message.chat.id, f"⚜️ | Вы успешно выкопали 2 золото", parse_mode='html')
                cursor.execute(f'UPDATE mine SET gold = {gold + 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать руду можно раз в {period} секунд!", parse_mode='html')
             return

       if pick == 'Zerro':
          if stavkatime > period:
             if int(rx) in range(0,40):
                await bot.send_message(message.chat.id, f"🪨 | Вы успешно выкопали {rx_iron * 2} камня", parse_mode='html')
                cursor.execute(f'UPDATE mine SET iron = {iron + rx_iron * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(41,70):
                await bot.send_message(message.chat.id, f"⛓ | Вы успешно выкопали {rx_metall * 2} железа", parse_mode='html')
                cursor.execute(f'UPDATE mine SET metall = {metall + rx_metall * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(71,85):
                await bot.send_message(message.chat.id, f"🪙 | Вы успешно выкопали {rx_silver * 2} серебра", parse_mode='html')
                cursor.execute(f'UPDATE mine SET silver = {silver + rx_silver * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(86,95):
                await bot.send_message(message.chat.id, f"🎇 | Вы успешно выкопали {rx_bronza * 2} бронзы", parse_mode='html')
                cursor.execute(f'UPDATE mine SET bronza = {bronza + rx_bronza * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(96,100):
                await bot.send_message(message.chat.id, f"⚜️ | Вы успешно выкопали 2 золото", parse_mode='html')
                cursor.execute(f'UPDATE mine SET gold = {gold + 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать руду можно раз в {period} секунд!", parse_mode='html')
             return

       if pick == 'on':
          if stavkatime > period:
             if int(rx) in range(0,40):
                await bot.send_message(message.chat.id, f"🪨 | Вы успешно выкопали {rx_iron} камня", parse_mode='html')
                cursor.execute(f'UPDATE mine SET iron = {iron + rx_iron} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(41,70):
                await bot.send_message(message.chat.id, f"⛓ | Вы успешно выкопали {rx_metall} железа", parse_mode='html')
                cursor.execute(f'UPDATE mine SET metall = {metall + rx_metall} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(71,85):
                await bot.send_message(message.chat.id, f"🪙 | Вы успешно выкопали {rx_silver} серебра", parse_mode='html')
                cursor.execute(f'UPDATE mine SET silver = {silver + rx_silver} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(86,95):
                await bot.send_message(message.chat.id, f"🎇 | Вы успешно выкопали {rx_bronza} бронзы", parse_mode='html')
                cursor.execute(f'UPDATE mine SET bronza = {bronza + rx_bronza} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(96,100):
                await bot.send_message(message.chat.id, f"⚜️ | Вы успешно выкопали 1 золото", parse_mode='html')
                cursor.execute(f'UPDATE mine SET gold = {gold + 1} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать руду можно раз в {period} секунд!", parse_mode='html')
             return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас нету кирки, что бы купить кирку введите команду \"Купить кирку\"", parse_mode='html')
          return
          




    if message.text.lower() == 'продать кирку':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]

       if pick == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! вы не можете продать кирку Cherick", parse_mode='html')

       if pick == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! вы не можете продать кирку Zerro", parse_mode='html')

       if pick == 'off':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас и так нету кирки, что бы купить кирку введите команду \"Купить кирку\"", parse_mode='html')

       if pick == 'on':
          await bot.send_message(message.chat.id, f"⛏ | Вы продали кирку за 5.000$ ", parse_mode='html')
          cursor.execute(f'UPDATE mine SET pick = "off" WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE users SET balance = {balance + 5000} WHERE user_id = "{user_id}"')
          connect.commit()
    if message.text.lower() == 'купить кирку':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]


       if pick == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть кирка Cherick", parse_mode='html')

       if pick == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть кирка Zerro", parse_mode='html')


       if pick == 'on':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть кирка, что бы продать кирку введите команду \"Продать кирку\"", parse_mode='html')

       if pick == 'off':
          if balance >= 5000:
             await bot.send_message(message.chat.id, f"⛏ | Вы купили кирку за 5.000$ ", parse_mode='html')
             cursor.execute(f'UPDATE mine SET pick = "on" WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance - 5000} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')



#################################################ФЕРМА#################################################
    if message.text.lower() in ['ферма', 'фермы']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за ферму 🌾

🌾 | Доступный урожай:
      🍃 | Лён =  5-10
      🌿 | Хлопок = 5-10

ℹ️ | Чтобы собрать какой то урожай, воспользуйтесь командой \"Собрать [лён\ хлопок]
ℹ️ | Чтобы продать какой-то урожай, воспользуйтесь командой \" Продать [лён\хлопок] [Количество]       
       """, parse_mode='html')
    if message.text.startswith('продать хлопок') or message.text.startswith('Продать хлопок'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       cotton = cursor.execute("SELECT cotton from farm where user_id = ?", (message.from_user.id,)).fetchone()
       cotton = int(cotton[0])
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       c = int(su3)
       c2 = '{:,}'.format(c).replace(',', '.')
       
       summ = c * 150000
       summ2 = '{:,}'.format(summ).replace(',', '.')

       if c <= cotton:
          await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c2} хлопка 🌿 за {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE farm SET cotton = {cotton - c} WHERE user_id = "{user_id}"')
          connect.commit()
       else:
          await bot.send_message(message.chat.id,f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько ресурсов!", parse_mode='html')



    if message.text.startswith('продать лён') or message.text.startswith('Продать лён'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       linen = cursor.execute("SELECT linen from farm where user_id = ?", (message.from_user.id,)).fetchone()
       linen = int(linen[0])
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       c = int(su3)
       c2 = '{:,}'.format(c).replace(',', '.')
       
       summ = c * 150000
       summ2 = '{:,}'.format(summ).replace(',', '.')

       if c <= linen:
          await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c2} лён 🍃 за {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE farm SET linen = {linen - c} WHERE user_id = "{user_id}"')
          connect.commit()
       else:
          await bot.send_message(message.chat.id,f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько ресурсов!", parse_mode='html')

    
    if message.text.startswith('cобрать') or message.text.startswith('Собрать'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         rake = cursor.execute("SELECT rake from farm where user_id = ?", (message.from_user.id,)).fetchone()
         rake = rake[0]

         linen = cursor.execute("SELECT linen from farm where user_id = ?", (message.from_user.id,)).fetchone()
         linen = int(linen[0])

         cotton = cursor.execute("SELECT cotton from farm where user_id = ?", (message.from_user.id,)).fetchone()
         cotton = int(cotton[0])

         rud = str(message.text.split()[1])

         rx_linen = random.randint(5,10)

      
         if rake == 'Cherick':
             period = 2
         else:
            period = 5
         get = cursor.execute("SELECT time_rake FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)
         
         if stavkatime > period:
            if rake == 'Cherick':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen * 2} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen * 2} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            if rake == 'Zerro':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen * 2} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen * 2} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            if rake == 'on':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас нету граблей, что бы купить грабли введите команду \"Купить грабли\"", parse_mode='html')
               return
         
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать урожай можно раз в {period} секунд!", parse_mode='html')     
            return      
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Собрать [лён, хлопок]", parse_mode='html')

          
    if message.text.lower() == 'продать грабли':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       rake = cursor.execute("SELECT rake from farm where user_id = ?", (message.from_user.id,)).fetchone()
       rake = rake[0]

       if rake == 'off':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас и так нету граблей, чтобы купить грабли введите команду \"Купить грабли\"", parse_mode='html')

       if rake == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Но вы не можете продать грабли Zerro", parse_mode='html')

       if rake == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Но вы не можете продать грабли Cherick", parse_mode='html')




       if rake == 'on':
         await bot.send_message(message.chat.id, f"⛏ | Вы продали грабли за 5.000$ ", parse_mode='html')
         cursor.execute(f'UPDATE farm SET rake = "off" WHERE user_id = "{user_id}"')
         cursor.execute(f'UPDATE users SET balance = {balance + 5000} WHERE user_id = "{user_id}"')
         connect.commit()

    if message.text.lower() == 'купить грабли':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       rake = cursor.execute("SELECT rake from farm where user_id = ?", (message.from_user.id,)).fetchone()
       rake = rake[0]

       if rake == 'on':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть грабли, что бы продать грабли введите команду \"Продать грабли\"", parse_mode='html')

       if rake == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть грабли", parse_mode='html')
 
       if rake == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть грабли", parse_mode='html')


       if rake == 'off':
          if balance >= 5000:
             await bot.send_message(message.chat.id, f"⛏ | Вы купили грабли за 5.000$ ", parse_mode='html')
             cursor.execute(f'UPDATE farm SET rake = "on" WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance - 5000} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')



###############################################ИНВЕНТАРЬ####################################################################

    if message.text.lower() == 'инвентарь':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       loser = ['😐', '😕','😟','😔','😓']
       rloser = random.choice(loser)

       farm = 0
       men = 0
       ob = 0

       linen = cursor.execute("SELECT linen from farm where user_id = ?", (message.from_user.id,)).fetchone()
       linen = int(linen[0])
       linen_f = '{:,}'.format(linen).replace(',', '.')

       cotton = cursor.execute("SELECT cotton from farm where user_id = ?", (message.from_user.id,)).fetchone()
       cotton = int(cotton[0])
       cotton_f = '{:,}'.format(cotton).replace(',', '.')

       iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
       iron = int(iron[0])
       iron_f = '{:,}'.format(iron).replace(',', '.')

       metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
       metall = int(metall[0])
       metall_f = '{:,}'.format(metall).replace(',', '.')

       silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
       silver = int(silver[0])
       silver_f = '{:,}'.format(silver).replace(',', '.')

       bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])
       bronza_f = '{:,}'.format(bronza).replace(',', '.')

       gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       gold_f = '{:,}'.format(gold).replace(',', '.')

       if iron > 0:
          iron2 = f'    🪨 | Камня: {iron_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          iron2 = ''

       if metall > 0:
          metall2 = f'    ⛓ | Железа: {metall_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          metall2 = ''
      
       if silver > 0:
          silver2 = f'    🪙 | Серебра: {silver_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          silver2 = ''

       if bronza > 0:
          bronza2 = f'    🎇 | Бронзы: {bronza_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          bronza2 = ''

       if gold > 0:
          gold2 = f'    ⚜️ | Золота: {gold_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          gold2 = ''

       if men > 0:
          men_2 = '\n⛏ | Шахта\n'
       else:
          men_2 = ''
       
       if linen > 0:
          linen2 = f'      🍃 | Лён: {linen_f} шт\n'
          farm = farm + 1
          ob = ob + 1
       else:
          linen2 = ''

       if cotton > 0:
          cotton2 = f'      🌿 | Хлопок: {cotton_f} шт\n'
          farm = farm + 1
          ob = ob + 1
       else:
          cotton2 = ''

       if farm > 0:
          farm2 = '🌾 | Ферма\n'
       else:
          farm2 = ''

       if ob == 0:
          ob2 = f'Вещи отсутствуют {rloser}'
       else:
          ob2 = ''
      
       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот ваш инвентарь:\n{ob2}{men_2}{iron2}{metall2}{silver2}{bronza2}{gold2}\n{farm2}{linen2}{cotton2}", parse_mode='html')

    if message.text.startswith('гонка') or message.text.startswith('Гонка'):

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       loser = ['😐', '😕','😟','😔','😓']
       rloser = random.choice(loser)

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_id = ?", (message.from_user.id,)).fetchone()
       cars = cars[0]

       hp = cursor.execute("SELECT hp from cars where user_id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       benz = cursor.execute("SELECT benz from cars where user_id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')


       rx = random.randint(0,1000)
       rx2 = random.randint(1,25)
       summ3 = summ * 2
       summ4 = '{:,}'.format(summ3).replace(',', '.')

       if summ < 1:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя играть на отрицательное число")
          return

       period = 5
       getе = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(getе[0])
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if summ <= balance:
             if cars > 0:
                if hp > 0:
                   if benz > 0:
                      if int(rx) in range(0,600):
                         await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏎 | Игра: Гонки\n🚘 | Машина: {cars_name}\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: 0$", parse_mode='html')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()
                      if int(rx) in range(601, 1000):
                         await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏎 | Игра: Гонки\n🚘 | Машина: {cars_name}\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {summ4}$", parse_mode='html')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance + summ * 2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()
                   else:
                      await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас закончился бензин в автомобиле", parse_mode='html')
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас поломался автомобиль , вы не можете участвовать в гонках", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Какие гонки без автомобиля? Купите автомобиль", parse_mode='html') 
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств", parse_mode='html') 
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! играй можно раз в {period} секунд", parse_mode='html') 




######################################################Привилегии \ Донат меню##############################################

    if message.text.lower() == 'донат':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?", (message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])
       donate_coins2 = '{:,}'.format(donate_coins).replace(',', '.')

       donate_menu = InlineKeyboardMarkup(row_width=2)
       donate_menu.row(
         InlineKeyboardButton(text=f'💰 Пополнить', callback_data='info_donate_online')
       )
       privilegii = InlineKeyboardButton(text='📝 Привилегии', callback_data='privilegii')
       case = InlineKeyboardButton(text='🎁 Кейсы', callback_data='case')
       adms = InlineKeyboardButton(text='⛔️ Права администратора', callback_data='adms')
       ysloviya_cash = InlineKeyboardButton(text='❗️ Условия покупок', callback_data='ysloviya_cash')
       prodazh_valyte = InlineKeyboardButton(text='💸 Продажа валюты', callback_data='prodazh_valyte')
       donate_menu.add(privilegii, adms, case, ysloviya_cash, prodazh_valyte)

       money = await user_money(message.from_user.id)
       
       x2donate_status = await status_x2donate()

       if x2donate_status == 'on':
         x2donate_status = 'Включен'
       else:
         x2donate_status = 'Выключен'

       await message.reply( f"""
❗️ Пояивились <b>проблемы с авто оплатой</b>, обращайтесь к {config.owner}
➖➖➖➖➖➖➖➖➖➖➖➖
👝 <b>Баланс:</b> <i>{'{:,}'.format(money).replace(',','.')} руб.</i>
🪙 <b>Donate-Coins:</b> <i>{donate_coins2} шт.</i>
🎗 <b>X2 Донат:</b> <i>{x2donate_status}</i>
➖➖➖➖➖➖➖➖➖➖➖➖
👾 <b>Команды:</b>
💰 <b>Пополнить баланс -</b> <code>пополнить 100</code>
📊 <b>Курс валют -</b> <code>курс</code>
🔁 <b>Обменять рубли в Donate-Coins -</b> <code>Обменять 100</code>
➖➖➖➖➖➖➖➖➖➖➖➖
🪙 <b>1 Donate-Coins =</b> <code>3Р</code> <b>/</b> <code>1грн</code> <b>/</b> <code>0.5 zl</code>
➖➖➖➖➖➖➖➖➖➖➖➖
🔎 <b>Категории:</b>
        <b>📝 Привилегии</b>
        <b>⛔️ Права администратора</b>
        <b>🎁 Кейсы</b>
        <b>❗️ Условия покупок</b>
➖➖➖➖➖➖➖➖➖➖➖➖
❗️ Прежде чем написать <b>владельцу бота</b> , посмотрите <b>условия покупок</b>
➖➖➖➖➖➖➖➖➖➖➖➖
⤵️ Выберите одну из <b>категорий</b>  
       """, reply_markup=donate_menu, parse_mode='html')
    if message.text.lower() == 'властелин':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ВЛАСТЕЛИН 🤎

🛒 | При покупке:
        1️⃣ | Бонус-кит ВЛАСТЕЛИН
        2️⃣ | Префикс ВЛАСТЕЛИН
        3️⃣ | 50.000.000$
        4️⃣ | 150 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс
        8️⃣ | Способность менять игрокам префикс
        9️⃣ | Ограничение на время в играх становиться 2 секунды

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ВЛАСТЕЛИН
        2️⃣ | Префикс ВЛАСТЕЛИН
        3⃣ | Способность менять себе префикс
        4⃣ | Способность менять игрокам префикс
        5⃣ | Ограничение на время в играх становиться 2 секунды

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'бог':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию БОГ 🤍

🛒 | При покупке:
        1️⃣ | Бонус-кит БОГ
        2️⃣ | Префикс БОГ
        3️⃣ | 25.000.000$
        4️⃣ | 100 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс
        8️⃣ | Способность менять игрокам префикс
        9️⃣ | Ограничение на время в играх становиться 2 секунды

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит БОГ
        2️⃣ | Префикс БОГ
        3⃣ | Способность менять себе префикс
        4⃣ | Способность менять игрокам префикс
        5⃣ | Ограничение на время в играх становиться 2 секунды

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'владелец':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ВЛАДЕЛЕЦ 🖤

🛒 | При покупке:
        1️⃣ | Бонус-кит ВЛАДЕЛЕЦ
        2️⃣ | Префикс ВЛАДЕЛЕЦ
        3️⃣ | 10.000.000$
        4️⃣ | 74 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс
        8️⃣ | Способность менять игрокам префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ВЛАДЕЛЕЦ
        2️⃣ | Префикс ВЛАДЕЛЕЦ
        3⃣ | Способность менять себе префикс
        4⃣ | Способность менять игрокам префикс

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'основатель':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ОСНОВАТЕЛЬ 💜

🛒 | При покупке:
        1️⃣ | Бонус-кит ОСНОВАТЕЛЬ
        2️⃣ | Префикс ОСНОВАТЕЛЬ
        3️⃣ | 4.000.000$
        4️⃣ | 54 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ОСНОВАТЕЛЬ
        2️⃣ | Префикс ОСНОВАТЕЛЬ
        3⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'спонсор':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию СПОНСОР 💙

🛒 | При покупке:
        1️⃣ | Бонус-кит СПОНСОР
        2️⃣ | Префикс СПОНСОР
        3️⃣ | 3.000.000$
        4️⃣ | 25 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Способность менять себе префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит СПОНСОР
        2️⃣ | Префикс СПОНСОР
        3⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"   
       """, parse_mode='html') 


    if message.text.lower() == 'хелпер':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ХЕЛПЕР 💚

🛒 | При покупке:
        1️⃣ | Бонус-кит ХЕЛПЕР
        2️⃣ | Префикс ХЕЛПЕР
        3️⃣ | 750.000$
        4️⃣ | 20 Рейтинга
        5️⃣ | Money-case 3 шт.
        6️⃣ | Способность менять себе префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ХЕЛПЕР
        2️⃣ | Префикс ХЕЛПЕР
        3⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"   
       """, parse_mode='html') 


    if message.text.lower() == 'платина':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ПЛАТИНА 💛

🛒 | При покупке:
        1️⃣ | Бонус-кит ПЛАТИНА
        2️⃣ | Префикс ПЛАТИНА
        3️⃣ | 550.000$
        4️⃣ | 10 Рейтинга
        5️⃣ | Money-case 1 шт.

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ПЛАТИНА
        2️⃣ | Префикс ПЛАТИНА

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"     
       """, parse_mode='html') 


    if message.text.lower() == 'премиум':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ПРЕМИУМ 🧡

🛒 | При покупке:
        1️⃣ | Бонус-кит ПРЕМИУМ
        2️⃣ | Префикс ПРЕМИУМ
        3️⃣ | 300.000$

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ПРЕМИУМ
        2️⃣ | Префикс ПРЕМИУМ

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"     
       """, parse_mode='html') 
    
    if message.text.lower() == 'вип':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ВИП ❤️

🛒 | При покупке:
        1️⃣ | Бонус-кит ВИП
        2️⃣ | Префикс ВИП
        3️⃣ | 250.000$

🎁 | При использовании Donate-Case:
       1️⃣ | Бонус-кит ВИП
       2️⃣ | Префикс ВИП

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"       
       """, parse_mode='html')  





###################################### КИТ-БОНУСЫ ##################################################
    if message.text.lower() == 'получить кит-бонус':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       user_status = cursor.execute('SELECT user_status from users where user_id = ?', (message.from_user.id,)).fetchone()
       user_status = user_status[0]

       balance = cursor.execute('SELECT balance from users where user_id = ?', (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       rating = cursor.execute('SELECT rating from users where user_id = ?', (message.from_user.id,)).fetchone()
       rating = int(rating[0])

       ethereum = cursor.execute('SELECT ethereum from users where user_id = ?', (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       metall = cursor.execute('SELECT metall from mine where user_id = ?', (message.from_user.id,)).fetchone()
       metall = int(metall[0])

       silver = cursor.execute('SELECT silver from mine where user_id = ?', (message.from_user.id,)).fetchone()
       silver = int(silver[0])

       bronza = cursor.execute('SELECT bronza from mine where user_id = ?', (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])

       gold = cursor.execute('SELECT gold from mine where user_id = ?', (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       period = 43200 #43200 s = 12h
       get = cursor.execute("SELECT time_kit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно получили свой кит-бонус", parse_mode='html')
          time.sleep(0.5)
          if user_status == 'Player':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⛓ 99 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 5 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 1000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 5} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET metall = {metall + 99} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vip':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 5,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 57 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 200🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 5000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 57} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 200} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Premium':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 101 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 25 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 250🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 25} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 101} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 250} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Platina':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 15,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 125 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 300🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 15000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 125} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 300} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Helper':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 25,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 100 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 500🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 25000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Sponsor':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 150,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 150000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Osnovatel':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 400,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 400000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vladelec':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 700,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 700000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Bog':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return

          if user_status == 'Vlaselin':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 100000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, администрация бота не может получать кит-бонус", parse_mode='html') 
             return   
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, получать кит-бонус можно раз в 12ч", parse_mode='html')

    if message.text.lower() == 'получить кит бонус':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       user_status = cursor.execute('SELECT user_status from users where user_id = ?', (message.from_user.id,)).fetchone()
       user_status = user_status[0]

       balance = cursor.execute('SELECT balance from users where user_id = ?', (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       rating = cursor.execute('SELECT rating from users where user_id = ?', (message.from_user.id,)).fetchone()
       rating = int(rating[0])

       ethereum = cursor.execute('SELECT ethereum from users where user_id = ?', (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       metall = cursor.execute('SELECT metall from mine where user_id = ?', (message.from_user.id,)).fetchone()
       metall = int(metall[0])

       silver = cursor.execute('SELECT silver from mine where user_id = ?', (message.from_user.id,)).fetchone()
       silver = int(silver[0])

       bronza = cursor.execute('SELECT bronza from mine where user_id = ?', (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])

       gold = cursor.execute('SELECT gold from mine where user_id = ?', (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       period = 43200 #43200 s = 12h
       get = cursor.execute("SELECT time_kit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно получили свой кит-бонус", parse_mode='html')
          time.sleep(0.5)
          if user_status == 'Player':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⛓ 99 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 5 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 1000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 5} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET metall = {metall + 99} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vip':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 5,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 57 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 200🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 5000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 57} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 200} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Premium':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 101 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 25 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 250🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 25} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 101} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 250} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Platina':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 15,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 125 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 300🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 15000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 125} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 300} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Helper':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 25,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 100 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 500🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 25000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Sponsor':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 150,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 150000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Osnovatel':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 400,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 400000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vladelec':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 700,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 700000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Bog':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return

          if user_status == 'Vlaselin':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 100000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, администрация бота не может получать кит-бонус", parse_mode='html') 
             return   
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, получать кит-бонус можно раз в 12ч", parse_mode='html')


    if message.text.lower() in ['кит-бонусы', 'кит бонусы', 'кит бонус', 'кит-бонус']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные о кит-бонусах 🎁

🎀 | Игрок:
      💰 | 1,000,000,000,000$
      ⛓ | 99 шт.
      💎 | 5 шт.
      🟣 | 100🟪

❤️ | Вип:
      💰 | 5,000,000,000,000$
      🪙 | 57 шт.
      💎 | 15 шт.
      🟣 | 200🟪

🧡 | Премиум:
      💰 | 10,000,000,000,000$
      🪙 | 101 шт.
      💎 |  25 шт.
      🟣 | 250🟪

💛 | Платина:
      💰 | 15,000,000,000,000$
      🪙 | 125 шт.
      💎 |  50 шт.
      🟣 | 300🟪

💚 | Хелпер:
      💰 | 25,000,000,000,000$
      🎇 | 50 шт.
      💎 |  100 шт.
      🟣 | 500🟪

💙 | Спонсор:
      💰 | 150,000,000,000,000$
      🎇 | 150 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

💜 | Основатель:
      💰 | 400,000,000,000,000$
      ⚜️ | 15 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

🖤 | ВЛАДЕЛЕЦ:
      💰 | 700,000,000,000,000$
      ⚜️ | 50 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

🤍 | БОГ:
      💰 | 10.000,000,000,000,000$
      ⚜️ | 150 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

🤎 | ВЛАСТЕЛИН:
      💰 | 100.000,000,000,000,000$
      ⚜️ | 500 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

ℹ️ Чтобы получить кит-бонус введите команду \"Получить кит-бонус\" 
ℹ️ Кит-бонус получить можно раз в 12ч      
       """, parse_mode='html')

####################################### ТОП Мажоров#######################################

    if message.text.lower() in ['топ багочей', 'топ мажоров', 'топ б']:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       from utils import scor_summ
       
       list = cursor.execute(f"SELECT * FROM users ORDER BY balance DESC").fetchmany(10)
       top_list = []

       num = 0

       for user in list:
          balance3 = await scor_summ(user[4])            
          num += 1

          if num == 1:
             num2 = '1️⃣'
             num3 = ' <b>💰ТОП 1💰</b> |'
          if num == 2:
             num2 = '2️⃣'
             num3 = ''
          if num == 3:
             num2 = '3️⃣'
             num3 = ''
          if num == 4:
             num2 = '4️⃣'
             num3 = ''
          if num == 5:
             num2 = '5️⃣'
             num3 = ''
          if num == 6:
             num2 = '6️⃣'
             num3 = ''
          if num == 7:
             num2 = '7️⃣'
             num3 = ''
          if num == 8:
             num2 = '8️⃣'
             num3 = ''
          if num == 9:
             num2 = '9️⃣'
             num3 = ''
          if num == 10:
             num2 = '🔟'
             num3 = ''
          
          if user[3] == 'Owner':
             stats = ' ✅<b>РАЗРАБОТЧИК</b>✅ |'
          if user[3] == 'Admin':
             stats = ' ⛔️<b>АДМИН</b>⛔️ |'
          if user[3] == 'Helper_Admin':
             stats = ' ⚠️<b>HELPER АДМИН</b>⚠️ |'
          if user[3] in ['Player', 'Vip', 'Premium', 'Platina', 'Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin']:
             stats = ''

          top_list.append(f"{num2} {user[1]} |{stats}{num3} 🔎 ID: <code>{user[0]}</code> | ${balance3} ")

       top = "\n".join(top_list)
       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 10 богачей в боте:\n" + top, reply_markup=fulltop, parse_mode='html')

############################## СИСТЕМА СООБЩЕНИЙ ####################################

    if message.text.lower() in ['система с', "система сообщений", "с сообщений", "с сообщение", "сс", "с с"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за систему сообщений 💬

ℹ️ | Пример команды: /m [ID] [сообщение]

⚠️ | Система сообщений была разработана для связи с игроками, у которых SMS SPAM BAN TELEGRAM        
       """, parse_mode='html')





##############################СИСТЕМА "e" ########################################

    if message.text.lower() in ['система е', 'е', 'e']:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за систему "e" ⚙️

🔩 | Информация:
<code>1e3</code> - 1.000$ - тыщ.
<code>1e6</code> - 1.000.000$ - млн.
<code>1e9</code> - 1.000.000.000$ - млрд.
<code>1e12</code> - 1.000.000.000.000$ - трлн.
<code>1e15</code> - 1.000.000.000.000.000$ - кврд.
<code>1e18</code> - 1.000.000.000.000.000.000$ - квнт.
<code>1e21</code> - 1.000.000.000.000.000.000.000$ - скст.
<code>1e24</code> - 1.000.000.000.000.000.000.000.000$ трикс.
<code>1e27</code> - 1.000.000.000.000.000.000.000.000.000$ твинкс.
<code>1e30</code> - 1.000.000.000.000.000.000.000.000.000.000$ септ.
<code>1e33</code> - 1.000.000.000.000.000.000.000.000.000.000.000$ октл.
<code>1e36</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000$ нонл.
<code>1e39</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000$ декал.
<code>1e42</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ эндк.
<code>1e45</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ доктл.
<code>1e48</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ гугл.
<code>1e51</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ кинд.
<code>1e54</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ трипт.
<code>1e57</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ срист.
<code>1e60</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ манит.
<code>1e63</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ гвинт.
<code>1е66</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ ланит.
<code>1е69</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ октит.
<code>1е72</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ новит.
<code>1е75</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ унд.
<code>1е78</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ конт.
<code>1е81</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ тент.
<code>1е84</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ фенд.

ℹ️ | <b>ПРИМЕР:</b> <i>казино 1е3</i>
    """, parse_mode='html')




##############################СИСТЕМА "К" ########################################

    if message.text.lower() in ['система к', 'к']:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за систему "К" ⚙️

🔩 | Информация:
<code>1к</code> - 1.000$ - тыщ.
<code>1кк</code> - 1.000.000$ - млн.
<code>1ккк</code> - 1.000.000.000$ - млрд.
<code>1кккк</code> - 1.000.000.000.000$ - трлн.
<code>1ккккк</code> - 1.000.000.000.000.000$ - кврд.
<code>1кккккк</code> - 1.000.000.000.000.000.000$ - квнт.
<code>1ккккккк</code> - 1.000.000.000.000.000.000.000$ - скст.
<code>1кккккккк</code> - 1.000.000.000.000.000.000.000.000$ трикс.
<code>1ккккккккк</code> - 1.000.000.000.000.000.000.000.000.000$ твинкс.
<code>1кккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000$ септ.
<code>1ккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000$ октл.
<code>1кккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000$ нонл.
<code>1ккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000$ декал.
<code>1кккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ эндк.
<code>1ккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ доктл.
<code>1кккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ гугл.
<code>1ккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ кинд.
<code>1кккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ трипт.
<code>1ккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ срист.
<code>1кккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ манит.
<code>1ккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ гвинт.
<code>1кккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ ланит.
<code>1ккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ октит.
<code>1кккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ новит.
<code>1ккккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ унд.
<code>1кккккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ конт.
<code>1ккккккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ тент.
<code>1кккккккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ фенд.

ℹ️ | <b>ПРИМЕР:</b> <i>казино 1к</i>
    """, parse_mode='html')




###################################### аватарки #######################################
    if message.text.lower() in ['убрать аву', "убрать аватарку", "удалить аву", "удалить аватарку"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0]) 

       await bot.send_message(message.chat.id, f"🪣 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно удалили свою аватарку", parse_mode='html')
       cursor.execute(f'UPDATE avatarka SET avatarka = "none" WHERE user_id = {user_id}')
       connect.commit()


    if message.text.lower() in ['ава', 'аватарки', "аватарка", "фото"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       strach_photo = open('Photo/страж.jpg', 'rb')

       cheat_photo = open('Photo/cheat.jpg', 'rb')

       apper_photo = open('Photo/apper.jpg', 'rb')

       dyp_photo = open('Photo/дюп.jpg', 'rb')

       girl_photo = open('Photo/girl.jpg', 'rb')

       admin_photo = open('Photo/админ.jpg', 'rb')

       ava_strach = InlineKeyboardMarkup(row_width=1)
       ava_strach2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_strach')
       ava_strach.add(ava_strach2)

       ava_cheat = InlineKeyboardMarkup(row_width=1)
       ava_cheat2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_cheat')
       ava_cheat.add(ava_cheat2)

       ava_apper = InlineKeyboardMarkup(row_width=1)
       ava_apper2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_apper')
       ava_apper.add(ava_apper2)

       ava_dyp = InlineKeyboardMarkup(row_width=1)
       ava_dyp2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_dyp')
       ava_dyp.add(ava_dyp2)

       ava_girl = InlineKeyboardMarkup(row_width=1)
       ava_girl2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_girl')
       ava_girl.add(ava_girl2)

       ava_admin = InlineKeyboardMarkup(row_width=1)
       ava_admin2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_admin')
       ava_admin.add(ava_admin2)

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, добро пожаловать в меню аватарок 🗾

ℹ️ | Всего аватарок: 4

ℹ️ | Доступные аватарки: ДЮППЕР, СТРАЖ, АППЕР, ЧИТЕР, ДЕВУШКА

⛔️ | Админ: АДМИН

ℹ️ | Аватарка ставиться на баланс

↘️ | Виберите одну аватарок ниже 
       """, parse_mode='html')
       await bot.send_photo(message.chat.id, strach_photo, '', reply_markup=ava_strach)
       await bot.send_photo(message.chat.id, cheat_photo, '', reply_markup=ava_cheat)
       await bot.send_photo(message.chat.id, apper_photo, '', reply_markup=ava_apper)
       await bot.send_photo(message.chat.id, dyp_photo, '', reply_markup=ava_dyp)
       await bot.send_photo(message.chat.id, girl_photo, '', reply_markup=ava_girl)
       await bot.send_photo(message.chat.id, admin_photo, '', reply_markup=ava_admin)




###################################### РЕПУТАЦИЯ + ###################################

    if message.text.lower() in ['+', '++', '+++', 'кросс', "молодец", "имба"]:
       user_id = message.from_user.id

       reply_user_id = message.reply_to_message.from_user.id
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = user_name[0]

       reput = cursor.execute("SELECT reput from reput where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reput = int(reput[0])

       if reply_user_id == user_id:
          await bot.send_message(message.chat.id, f"📝 Жулик, не голосуй", parse_mode='html')
          return

       await bot.send_message(message.chat.id, f"📊 | Вы успешно повысили репутацию  <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> . Теперь его репутация: {reput + 1}", parse_mode='html')
       cursor.execute(f'UPDATE reput SET reput = {reput + 1} WHERE user_id = {reply_user_id}')
       connect.commit()


###################################### РП КОМАНДЫ ####################################

    if message.text.lower() in ["рп-команды", "РП-команды"]:
       user_name = message.from_user.get_mention(as_html=True)
       await bot.send_message(message.chat.id, f"{user_name}, список РП-команд:\n🤗 | Обнять\n👏 | Похлопать\n👨‍💻 | Заскамить\n☕️ | Пригласить на чай\n👉👌 | Изнасиловать\n🤝 | Взять за руку\n📱 | Подарить айфон\n✋ | Дать пять\n😬 | Укусить\n🤛 | Ударить\n🤲 | Прижать\n💋 | Чмок\n💋 | Поцеловать\n😼 | Кусь\n🤲 | Прижать\n🔪 | Убить\n🤜 | Уебать\n💰 | Украсть\n🔞 | Выебать\n👅 | Отсосать\n👅 | Отлизать\n🔞 | Трахнуть\n🔥 | Сжечь", parse_mode='html')

    if message.text.lower() in ["чмок", "Чмок"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"💋 | {user_name} чмокнул(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["кусь", "Кусь"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"😼 | {user_name} кусьнул(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["обнять", "Обнять"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤗 | {user_name} обнял(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["поцеловать", "Поцеловать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"💋 | {user_name} поцеловал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["дать пять", "Дать пять"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"✋ | {user_name} дал(-а) пять {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["подарить айфон", "Подарить айфон"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"📱 | {user_name} подарил(-а) айфон {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["ударить", "Ударить"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤛 | {user_name} ударил(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["заскамить", "Заскамить"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👨‍💻 | {user_name} заскамил(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["прижать", "Прижать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤲 | {user_name} прижал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["укусить", "Укусить"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"😬 | {user_name} укусил(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["взять за руку", "Взять за руку"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤝 | {user_name} взял(-а) за руку {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["прижать", "Прижать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤲 | {user_name} прижал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["похлопать", "Похлопать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👏 | {user_name} похлопал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["изнасиловать", "Изнасиловать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👉👌 | {user_name} изнасиловал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["пригласить на чай", "Пригласить на чай"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"☕️ | {user_name} пригласил(-а) на чай {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["убить", "Убить"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔪 | {user_name} убил(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["уебать", "Уебать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤜 | {user_name} уебал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["украсть", "Украсть"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"💰 | {user_name} украл(-а) {reply_user_name}", parse_mode='html')

    if message.text.lower() in ["отсосать", "Отсосать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👅 | {user_name} отсосал(-а) {reply_user_name}", parse_mode='html')

    if message.text.lower() in ["отлизать", "Отлизать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👅 | {user_name} отлизал(-а) {reply_user_name}", parse_mode='html')

    if message.text.lower() in ["выебать", "Выебать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔞 | {user_name} выебал(-а) {reply_user_name}", parse_mode='html')

    if message.text.lower() in ["сжечь", "Сжечь"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔥 | {user_name} сжёг {reply_user_name}", parse_mode='html')

    if message.text.lower() in ["трахнуть", "Трахнуть"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔞 | {user_name} трахнул(-а) {reply_user_name}", parse_mode='html')
########################################PROMO#########################################
    if message.text.lower() in ['очистить промокоды', 'reset promo']:
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_status = str(user_status[0])

         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()

         if user_status == 'Owner':
            cursor.execute(f'DELETE from promo')
            cursor.execute(f'DELETE from promo_active')
            connect.commit()
            all_dell_promo = 0

            for delete_promo in all_promo:
               all_dell_promo += 1
               await message.answer(f'➖ промокод <code>{delete_promo[0]}</code> был <b>удалён</b>', parse_mode='html')

            await message.reply(f"✅ Всё промокоды были удалены\n🔢 Количество удаленных промокодов: {'{:,}'.format(all_dell_promo).replace(',','.')}")

            
         else:
            return await message.reply(f'❗️ Данная команда доступна от прав администратора <b>OWNER<b>', parse_mode='html')





    if message.text.startswith('промо') or message.text.startswith('Промо') or message.text.startswith('Промокод') or message.text.startswith('промокод'):
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         balance = cursor.execute(f'SELECT balance from users where user_id = {user_id}').fetchone()
         balance = int(balance[0])

         donate_coins = cursor.execute(f'SELECT donate_coins from users where user_id = {user_id}').fetchone()
         donate_coins = int(donate_coins[0])

         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()
         all_promo2 = []

         for item in all_promo:
            all_promo2.append(item[0])



         promo = str(message.text.split()[1])

         if str(promo) in str(all_promo2):
            
            proverka = cursor.execute(f'SELECT active from promo_active where user_id = {user_id} and promo = "{promo}"').fetchone()

            if proverka != None:
               return await message.reply(f'❗️ <b>Вы использовали промокод</b> <code>{promo}</code>', parse_mode='html')
            else:
               pass

            name_promo = cursor.execute(f'SELECT promo from promo where promo = "{promo}"').fetchone()
            name_promo = name_promo[0]

            status_promo = cursor.execute(f'SELECT status from promo where promo = "{promo}"').fetchone()
            status_promo = status_promo[0]

            owner_promo = cursor.execute(f'SELECT owner from promo where promo = "{promo}"').fetchone()
            owner_promo = owner_promo[0]

            priz_promo = cursor.execute(f'SELECT priz from promo where promo = "{promo}"').fetchone()
            priz_promo = int(priz_promo[0])
   
            active_promo = cursor.execute(f'SELECT active from promo where promo = "{promo}"').fetchone()
            active_promo = int(active_promo[0])

            ob_active_promo = cursor.execute(f'SELECT ob_active from promo where promo = "{promo}"').fetchone()
            ob_active_promo = int(ob_active_promo[0])

            if ob_active_promo == active_promo:
               return await message.reply(f'❗️ Промокод больше <b>не действительный</b>', parse_mode='html')
            else:
               pass
            

            if status_promo == 'money':
               priz2 = '{:,}'.format(priz_promo).replace(',', '.')
               priz = f'{priz2}$'
               new_balance = balance + priz_promo
               new_balance2 = '{:,}'.format(int(new_balance)).replace(',','.')
               update_profile = f'💸 <b>Теперь ваш текущий баланс:</b>  <code>{new_balance2}$</code>'
               cursor.execute(f'UPDATE promo SET ob_active = {ob_active_promo + 1} WHERE promo = "{promo}"')
               cursor.execute(f'UPDATE users SET balance = {int(new_balance)} where user_id = {user_id}')
               cursor.execute("INSERT INTO promo_active VALUES(?, ?, ?);",(user_id, promo,1))
            elif status_promo == 'donate_coins':
               priz2 = '{:,}'.format(priz_promo).replace(',', '.')
               priz = f'{priz2} Donate-Coins'
               update_profile = ''
               cursor.execute(f'UPDATE promo SET ob_active = {ob_active_promo + 1} WHERE promo = "{promo}"')
               cursor.execute(f'UPDATE users SET donate_coins = {donate_coins + priz_promo} where user_id = {user_id}')
               cursor.execute("INSERT INTO promo_active VALUES(?, ?, ?);",(user_id, promo,1))
            else:
               return await message.reply(f'<b>Error: No status promo in [Money, Donate-Coins, Donate-Case, Money-Case]</b>', parse_mode='html')
            
            
            text = f'''
✅ <b>Вы успешно использовали промокод <code>{promo}</code> и получили  <code>{priz}</code></b>
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💼 <b>Создатель промокода:</b>  <code>{owner_promo}</code>
{update_profile}
            '''

            await message.reply(text, parse_mode='html')
         else:
            return await message.reply(f'❗️ Нету такого промокода')


    if message.text.startswith('+админ промо'):
      try:
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_status = str(user_status[0])

         if user_status != 'Owner':
            return await message.reply(f'❗️ Данная команда доступна от прав администратора <b>OWNER</b>', parse_mode='html')
         else:
            pass

         new_promo = message.text.split()[2]

         status_promo = int(message.text.split()[3])

         summ_promo = int(message.text.split()[4])

         active_promo = int(message.text.split()[5])

         opis = message.text.split()[6:]

         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()
         all_promo2 = []

         for all_promo3 in all_promo:
            all_promo2.append(all_promo3[0])

         if new_promo in all_promo2:
            return await message.reply(f'❗️ <b>Данный промокод <code>{new_promo}</code> уже существует</b>', parse_mode='html')
         else:
            pass


         if status_promo == 1:
            status = 'donate_coins'
            cursor.execute("INSERT INTO promo VALUES(?, ?, ?, ?, ?, ?);",(new_promo, status, user_name, summ_promo, active_promo, 0))
            text = f'''
🖊 <b>Промокод:</b> <code>{new_promo}</code>
🪙 <b>Содержит: Donate-Coins</b>
💼 <b>Создатель:</b> <code>{user_name}</code>

👥 <b>Количество использований:</b> <code>{active_promo} раз(а)</code>
👤<b> На одного человека:</b> <code>{summ_promo} Donate-Coins 🪙</code>
            '''

         else:
            text = f'''
❗️ Неправильно ведены аргументы | пример: <code>+админ промо</code> <i>[название промокода] [номер статуса] [сумма на 1 человека]</i>  [количество активаций] 

❕ Номера статусов:
      1 - Donate-Coins
      2 - Donate-Case
      3 - Money-Case
         '''
            return await message.reply(text, parse_mode='html')
      
         await message.reply(text, parse_mode='html')

      except IndexError:
         text = f'''
❗️ Неправильно ведены аргументы | пример: <code>+админ промо</code> <i>[название промокода] [номер статуса] [сумма на 1 человека]</i>  [количество активаций] 

❕ Номера статусов:
      1 - Donate-Coins
      2 - Donate-Case
      3 - Money-Case
         '''
         await message.reply(text, parse_mode='html')


      except ValueError:
         text = f'''
❗️ Неправильно ведены аргументы | пример: <code>+админ промо</code> <i>[название промокода] [номер статуса] [сумма на 1 человека] [количество активаций] </i>

❕ Номера статусов:
      1 - Donate-Coins
      2 - Donate-Case
      3 - Money-Case
         '''
         await message.reply(text, parse_mode='html')




    if message.text.startswith('+промо') or message.text.startswith('+Промо') or message.text.startswith('+Промокод') or message.text.startswith('+промокод'):
      try:
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         balance = cursor.execute(f'SELECT balance from users where user_id = {user_id}').fetchone()
         balance = int(balance[0])
      
         user_status = cursor.execute(f'SELECT user_status from users where user_id = {user_id}').fetchone()
         user_status = user_status[0]

         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()
         all_promo2 = []

         for all_promo3 in all_promo:
            all_promo2.append(all_promo3[0])
         new_promo = str(message.text.split()[1])

         su1 = message.text.split()[2]
         su2 = (su1).replace('.', '').replace(',', '').replace('е',' e').replace("к", 'k').replace('k', '000').replace('все', 'всё')
         su3 = float(su2)
         summ = int(su3)

         su1_2 = message.text.split()[3]
         su2_2 = (su1_2).replace('.', '').replace(',', '').replace('е',' e').replace("к", 'k').replace('k', '000')
         su3_2 = float(su2_2)
         active_users = int(su3_2)

         opis = message.text.split()[4:]

         all_users = cursor.execute(f'SELECT * from users').fetchall()
         all_users = len(all_users)

         if summ < 100:
            return await message.reply(f'❗️ Cумма должна быть не меньше <code>100$</code>', parse_mode='html')
         else:
            pass

         if active_users > all_users:
            return await message.reply(f'❗️ Вы не можете создать промокод больше чем на <b>{all_users} использований</b>', parse_mode='html')
         else:
            pass
         
         if len(new_promo) < 3:
            return await message.reply(f'❗️ Промокод должен быть <b>больше 3 символов</b>', parse_mode='html')
         else:
            pass

         if new_promo in all_promo2:
            return await message.reply(f'❗️ <b>Данный промокод <code>{new_promo}</code> уже существует</b>', parse_mode='html')
         else:
            pass
         
         if summ > balance:
            return await message.reply(f'❗️ У вас <b>недостаточно средств</b>', parse_mode='html')
         else:
            pass

         if summ <= 0:
            return await message.reply(f'❗️ Сумма не должна быть отрицательным числом <b>[0 и меньше]</b>', parse_mode='html')
         else:
            pass
         
         user_summ = summ / active_users
         user_summ2 = int(user_summ)

         text_opis = ' '.join(opis)

         if text_opis == '':
            opis2 = ''
         else:
            text_opis = ' '.join(opis)
            opis2 = f'\n<b>💭 Описание:</b> <code>{text_opis}</code>'

         text = f'''
<b>🖊 Промокод:</b> <code>{new_promo}</code>
<b>🏛 Содержит:</b> <code>{'{:,}'.format(summ).replace(',', '.')}$</code>
<b>💼 Создатель:</b> <code>{user_name}</code>{opis2}

<b>👥 Количество использований:</b> <code>{active_users} раз(a)</code>
<b>👤 На одного человека:</b> <code>{'{:,}'.format(user_summ2).replace(',', '.')}$</code>
         '''

         if user_status in ['Admin', 'Helper_Admin']:
            await message.reply('❗️ Администрации запрещено создавать промокоды')

            await message.bot.send_message(config.admin_chat_id, f'⛔️ Администратор <b>{user_name}</b> (<code>{user_id}</code>) только что попытался создать промокод.', parse_mode='html')
            return await message.bot.send_message(config.admin_chat_id, text, parse_mode='html')
         else:
            pass

            
         status = 'money'
         try:
            cursor.execute("INSERT INTO promo VALUES(?, ?, ?, ?, ?, ?);",(new_promo, status, user_name, user_summ2, active_users, 0))
            cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
            connect.commit()
            await message.reply(text, parse_mode='html')
         except OverflowError:
            cursor.execute("INSERT INTO promo VALUES(?, ?, ?, ?, ?, ?);",(new_promo, status, user_name, 0, active_users, 0))
            cursor.execute(f'UPDATE promo SET priz = {user_summ2} WHERE promo = "{new_promo}"')
            cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
            connect.commit()
            await message.reply(text, parse_mode='html')
      except IndexError:
         text = f'''
❗️ Неправильно введены <b>аргументы!</b>
❕ <code>+промо </code> <b>[название] [сумма] [количество использований]</b>
         '''
         await message.reply(text, parse_mode='html')

      except ValueError:
         text = f'''
❗️ Неправильно введены <b>аргументы!</b>
❕ <code>+промо </code> <b>[название] [сумма] [количество использований]</b>
         '''
         await message.reply(text, parse_mode='html')
















########################################        Смена префикса          ######################################
    if message.text.startswith('Поменять префикс') or message.text.startswith('поменять префикс') or message.text.startswith('Сменить префикс') or message.text.startswith('сменить префикс'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       prefix = ' '.join(message.text.split()[2:])
       if len(prefix) <= 20:
          if user_status in ['Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin', 'Admin', 'Helper_Admin', 'Owner']:
             await bot.send_message(message.chat.id, f"🔒 | Вы успешно сменили свой префикс на {prefix}")
             cursor.execute(f'UPDATE users SET pref = "{prefix}" WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять префикс можно только от привилегии \"ХЕЛПЕР\"", parse_mode='html')
             return
       else:
          await bot.send_message(message.chat.id, f"🆘 | Игрок, менять префикс не может быть более 20 символов!", parse_mode='html')
          return


    if message.text.startswith('+игроку префикс') or message.text.startswith('+игроку префикс'):
       user_id = message.from_user.id


       reply_user_id = message.reply_to_message.from_user.id
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)


       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       prefix = ' '.join(message.text.split()[2:])
       if len(prefix) <= 20:
          period = 900
          get = cursor.execute("SELECT stavka FROM time_prefix WHERE user_id = ?", (message.from_user.id,)).fetchone()
          last_stavka = f"{int(get[0])}"
          stavkatime = time.time() - float(last_stavka)
          if user_status == 'Owner':
             period = 0
          if stavkatime > period:
             if user_status in ['Vladelec', 'Bog', 'Vlaselin', 'Admin', 'Helper_Admin', 'Owner']:
                await bot.send_message(message.chat.id, f"🔒 | Вы сменили игроку {reply_user_name} префикс на {prefix}", parse_mode='html')
                cursor.execute(f'UPDATE users SET pref = "{prefix}" WHERE user_id = {reply_user_id}')
                cursor.execute(f'UPDATE time_prefix SET stavka = "{time.time()}" WHERE user_id = {reply_user_id}')
                connect.commit()
                return
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять префикс можно только от привилегии \"ВЛАДЕЛЕЦ\"", parse_mode='html')
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять игроку ник можно раз в 15 минут", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | Игрок, менять префикс не может быть более 20 символов!", parse_mode='html')
          return
    
    








#####################################################      КЕЙСЫ             ####################################################
    if message.text.lower() in ["открыть кейсы", "открыть кейс"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
       money_case = int(money_case[0])

       donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
       donate_case = int(donate_case[0])

       ob_member = 0

       if money_case > 0:
          ob_member += 1
       else:
          pass

       if donate_case > 0:
          ob_member += 1
       else:
          pass

       if ob_member < 1:
          await bot.send_message(message.chat.id, f"""
🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету не каких кейсов 
          """,parse_mode='html')
          return
       
       case_shop1 = InlineKeyboardMarkup(row_width=2)
       money_case1 = InlineKeyboardButton(text='Открыть Money-Case 💸', callback_data='up_money_case')
       donate_case2 = InlineKeyboardButton(text='Открыть Donate-Case 🧧', callback_data='up_donate_case')
       case_shop1.add(money_case1, donate_case2)

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот ваши кейсы 🎁

💸 | Money-Case - {money_case} шт.
🧧 | Donate-Case - {donate_case} шт.

↘️ Виберите один из кейсов, который хотите открыть 
       """,reply_markup=case_shop1, parse_mode='html')

    if message.text.lower() == 'кейсы':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
       money_case = int(money_case[0])

       donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
       donate_case = int(donate_case[0])
      
       ob_members = 0

       if donate_case > 0:
          ob_members += 1
          donate_case2 = f'      🧧 | Donate-Case - {donate_case} шт.\n'
       else:
          donate_case2 = ''

       if money_case > 0:
          ob_members += 1
          money_case2 = f'      💸 | Money-Case - {money_case} шт.\n'
       else:
          money_case2 = ''

       if ob_members > 0:
          casee = '🎁 | Ваши кейсы:\n'
       else:
          casee = '😟 | У вас нету кейсов...'

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за кейсы 🎁

💸 | Money-Case - 50 Donate-Coins 🪙
🧧 | Donate-Case - 100 Donate-Coins 🪙

{casee}{donate_case2}{money_case2}

🖲 | Чтобы открыть один из кейсов, напишите команду \"Открыть кейсы\"
       """, parse_mode='html')





#################################################### !канал ################################
    if message.text.lower() in ['канал', "!канал", "channel"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       channel_pov = cursor.execute("SELECT members from channel_pov where user_id = ?", (message.from_user.id,)).fetchone()
       channel_pov = int(channel_pov[0])

       if channel_pov > 0:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы уже получили деньги за подписку",parse_mode='html')
          return
       
       sub_pov = InlineKeyboardMarkup(row_width=1)
       channel_push = InlineKeyboardButton(text='КАНАЛ 🔈', url='https://t.me/qwechannel')
       channel_poverk = InlineKeyboardButton(text='ПРОВЕРИТЬ ✅', callback_data='channel_poverk')
       sub_pov.add(channel_push, channel_poverk)

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот условия задание 💠

🔈 | Подписаться на канал

💰 | Приз: 500.000.000.000.000.000$

↘️ Виберите одну кнопку ниже...       
       """, reply_markup=sub_pov, parse_mode='html')
       user_channel_status = await bot.get_chat_member(chat_id="@qwechannel", user_id=message.from_user.id)
       if user_channel_status['status'] != 'left':
          print('GOOD')
       else:
          print('Luser')

    



############################### ВДЗУ - ВЫДАЧА ДЕНЕГ ЗА УЧАСТНИКОВ ################################################
    if message.text.startswith('вдзу статус') or message.text.startswith('Вдзу статус'):

         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         status = str(message.text.split()[2])

         if user_id == config.owner_id:
            if status == 'off':
               cursor.execute(f'UPDATE wdzy SET status = "off"')
               connect.commit()
               text = f'❌  Вы <b>выключили</b> раздачу в чате {config.chat2}'
            elif status == 'on':
               cursor.execute(f'UPDATE wdzy SET status = "on"')
               connect.commit()
               text = f'✅ Вы <b>включили</b> выдачу в чате {config.chat2}'
            else:
               text = f'❗️ Не распознано «<b>{status}</b>» | Пример: <code>вдзу статус</code> <i>[off/on]</i>'

            await message.reply(text, parse_mode='html')
         else:
            return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')

    if message.text.startswith('вдзу сумма') or message.text.startswith('Вдзу сумма'):

         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         su = message.text.split()[2]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         summ = int(su3)

         if user_id == config.owner_id:
            cursor.execute(f'UPDATE wdzy SET summ = {summ}')
            connect.commit()

            text = f'''
♻️ <b>Обновлена</b> сумма за 1 участника - <code>{'{:,}'.format(summ).replace(',','.')}$</code>
            '''
            await message.reply(text, parse_mode='html')
         else:
            return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')






    if message.text.lower() == 'вдзу':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       if user_id == config.owner_id:
         summ = cursor.execute(f'SELECT summ from wdzy').fetchone()
         summ = int(summ[0])

         status = cursor.execute(f'SELECT status from wdzy').fetchone()
         status = status[0]

         if status == 'off':
            status2 = 'Выдача отключена ❌'
         else:
            status2 = 'Выдача включена ✅'

         text = f'''
👤 ВДЗУ [ WDZY ] - ВЫДАЧА ДЕНЕГ ЗА УЧАСТНИКОВ 

💭 Чат - {config.chat2}
💸 Сумма за 1 участника - {'{:,}'.format(summ).replace(',','.')}$
👉 Статус выдачи - {status2}

❗️ <code>вдзу сумма</code> <i>[сумма]</i> <b>- Устоновка суммы за 1 участника в чате</b>
❗️ <code>вдзу статус</code> <i>[off\on]</i><b> - Устоновка статуса выдачи </b>
         '''
         await message.reply(text, parse_mode='html')
       else:
         return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')








########################################### СЕМЬЯ СЕМЬИ ####################################
    

    if message.text.lower() == 'пригласить в семью':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if reply_user_id == user_id:
         return await message.reply(f'❗️ Вы не можете пригласить <b>самого себя</b> в семью.', parse_mode='html')
      else:
         pass
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass
      
      if rank_family < 2:
         return await message.reply(f'❗️ Приглашать игроков в семью можно от <b>2 ранга</b>', parse_Mode='html')
      else:
         pass

      user1 = message.reply_to_message.from_user.id
      user2 = reply_user_name
      keyboard = types.InlineKeyboardMarkup()
      keyboard.add(types.InlineKeyboardButton(text="✅ Принять приглашение", callback_data=f"accept_{user1}:{user2}:{name_family}"))

      text = f'''
👶 <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, вас приглашают в семью «<b>{name_family}</b>»
      '''

      await message.answer(text, reply_markup=keyboard, parse_mode='html')

    if message.text.startswith('cоздать семью') or message.text.startswith('Создать семью'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
       all_family2 = []
       
       for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])
      
       if user_id in all_family2:
         return await message.reply(f'❗️У вас есть <b>своя семья.</b> Зачем вам ещё одна? | <code>Распустить семью</code> - удаление семьи ', parse_mode='html')
       else:
         pass

       user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

       if user_id_family != None:
         return await message.reply('❗️ Вы уже <b>состоите в семье</b> | напишите «<code>выйти с семьи</code>» - для выхода с вашей семьи',parse_mode='html')
       else:
         pass

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])

       if donate_coins < config.cash_family:
         return await message.reply(f'❗️ <b>Недостаточно Donate-Coins</b> | Стоимость: <b>{config.cash_family} Donate-Coins</b> 🪙')
       else:
         pass
       
       name_family = message.text.split()[2:]
       name_family2 = ' '.join(name_family)
       full_name_family = (name_family2).replace(' ','').replace('🇷🇺', '').replace('Россия', 'россия').replace('россия', '')

       if len(full_name_family) < 4:
         return await message.reply('❗️ Название семьи должна быть больше <b>4 символов</b>', parse_Mode='html')
       elif len(full_name_family) > 35:
         return await message.reply(f'❗️ Название семьи должна быть меньше <b>35 символов</b>', parse_mode='html')
       else:
         pass

       all_family_name = cursor.execute('SELECT name from family').fetchall()
       all_family_name2 = []

       for all_family_name3 in all_family_name:
         all_family_name2.append(all_family_name3[0])
      
       if full_name_family in all_family_name2:
         return await message.reply(f'❗️ Семья с названием «<b>{full_name_family}</b>» уже существует', parse_mode='html')
       else:
         pass
       
       family_id = cursor.execute('SELECT id from family_id').fetchone()
       family_id = int(family_id[0])
       new_family_id = family_id + 1

       text = f'''
✅ Вы успешно создали семью «<b>{full_name_family}</b>»
       '''

       text2 = f'''
❕ Для просмотра своей семьи напишите <code>моя семья</code>
       '''
       time_family = time.time()
       opis = ''
       cursor.execute(f'UPDATE family_id SET id = {new_family_id}')
       cursor.execute("INSERT INTO family VALUES(?, ?, ?, ?, ?, ?, ?);",(full_name_family, user_id, user_name, new_family_id, 0, opis, time_family))
       connect.commit()
       await message.answer(text, parse_mode='html')
       await message.answer(text2, parse_mode='html')





    if message.text.lower() in ['моя семья', "семья"]:
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0
      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      owner_name = cursor.execute(f'SELECT owner_name from family where name = "{name_family}"').fetchone()
      owner_name = owner_name[0]

      rank3 = cursor.execute(f'SELECT user_name from user_family where rank = {3} and family = "{name_family}"').fetchall()
      all_rank3 = []

      for user_rank3 in rank3:
         all_rank3.append(user_rank3[0])

      full_all_rank3 = ' '.join(all_rank3)

      if full_all_rank3 == '':
         full_all_rank3 = 'Отсутствуют 😕'
      else:
         pass

      rank2 = cursor.execute(f'SELECT user_name from user_family where rank = {2} and family = "{name_family}"').fetchall()
      all_rank2 = []

      for user_rank2 in rank2:
         all_rank2.append(user_rank2[0])

      full_all_rank2 = ' '.join(all_rank2)

      if full_all_rank2 == '':
         full_all_rank2 = 'Отсутствуют 😕'
      else:
         pass
      
      id_family = cursor.execute(f'SELECT id from family where name = "{name_family}"').fetchone()
      id_family = int(id_family[0])

      sqlite_select_query2 = f"""SELECT * from user_family where family = \"{name_family}\""""
      cursor.execute(sqlite_select_query2)
      all_user_family = cursor.fetchall()

      balance_family = cursor.execute(f'SELECT balance from family where name = "{name_family}"').fetchone()
      balance_family = int(balance_family[0])

      opis_family = cursor.execute(f'SELECT opis from family where name = "{name_family}"').fetchone()
      opis_family = opis_family[0]
      
      if opis_family == '':
         opis_family = 'Пустое'
      else:
         pass

      text = f'''
Информация за семью «<b>{name_family}</b>» 👨‍👩‍👧‍👦
➖➖➖➖➖➖➖➖
🤵‍♂️ Основатель семьи: {owner_name}
👨‍💻 Заместитель (3 ранг): {full_all_rank3} 
🧑‍💼 Помощники (2 ранг): {full_all_rank2} 
➖➖➖➖➖➖➖➖
🔎 ID: <code>{id_family}</code>
👥 Игроков в семье: <b>{len(all_user_family)}</b>
💰 Мешок семьи: <code>{balance_family} с. монет</code>
💭 Описания семьи: <i>{opis_family}</i>
      '''
      await message.reply(text, parse_mode='html')






    if message.text.lower() == 'выйти с семьи':
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      
      if status_owner_family == 'on':
         return await message.reply(f'❗️ Вы <b>владелец семьи</b>, вы не можете покинуть свою семью | Пропишите <code>Распустить семью</code> для её удаление', parse_mode='html')
      else:
         pass

      cursor.execute(f'DELETE from user_family where family = "{name_family}"')

      text = f'''
😧 Вы покинули семью «<b>{name_family}</b>» 
      '''

      await message.reply(text, parse_mode='html')

    if message.text.lower() == 'распустить семью':
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if status_owner_family == 'off':
         return await message.reply(f'❗️ Распустить семью может только <b>её владелец</b>', parse_mode='html')
      else:
         pass

      cursor.execute(f'DELETE from family where name = "{name_family}"')
      cursor.execute(f'DELETE from user_family where family = "{name_family}"')

      text = f'''
🥲 Вы успешно распустили семью «<b>{name_family}</b>»
      '''

      await message.reply(text, parse_mode='html')
    if message.text.startswith('+описание семьи'):
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family5 = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family5 = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Менять описание семьи можно только с <b>3 ранга</b>', parse_mode='html')
      else:
         pass

      new_opis = message.text[16:]
      
      if len(new_opis) > 150:
         return await message.reply('❗️ Описание должно быть не больше <b>150 символов</b>', parse_mode='html')
      else:
         pass
      
      cursor.execute(f'UPDATE family SET opis = "{new_opis}" where name = "{name_family5}"')

      text = f'''
✅ Вы <b>успешно</b> поменяли описание семьи
      '''

      await message.reply(text, parse_mode='html')





    if message.text.lower() == 'выгнать из семьи':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if user_id == reply_user_id:
         return await message.reply('❗️ Вы не можете выгнать сами себя | Воспользуйтесь командой <code>Выйти с семьи</code>', parse_mode='html')
      else:
         pass

      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'

         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Выганять участников можно от <b>3 ранга</b>', parse_mode='html')
      else:
         pass
      
      reply_proverka_family = 0

      reply_user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {reply_user_id}').fetchone()

      if reply_user_id_family != None:
         reply_rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {reply_user_id}').fetchone()
         reply_rank_family = int(reply_rank_family[0])  

         reply_name_family = cursor.execute(f'SELECT family from user_family where user_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_user_id in all_family2:
         reply_rank_family = 3
         
         reply_name_family = cursor.execute(f'SELECT name from family where owner_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_proverka_family == 2:
         return await message.reply(f'❗️ Этот игрок не состоит в клане')
      else:
         pass
      
      if reply_name_family != name_family:
         return await message.reply(f'❗️ Этот игрок состоит не в вашем клане')
      else:
         pass


      if reply_rank_family == 3:
         if status_owner_family == 'on':
            pass
         else:
            return await message.reply(f'❗️ Вы не можете выгнать человека с <b>3 рангом</b> | <i>Под силу только владельцу семьи</i>', parse_mode='html')
      else:
         pass

      cursor.execute(f'DELETE from user_family where user_id = {reply_user_id}')
      connect.commit()

      text = f'''
👀 Вы выгнали <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> с семьи «<b>{name_family}</b>»
      '''

      await message.reply(text, parse_mode='html')


    if message.text.lower() == '+ранг семьи':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if user_id == reply_user_id:
         return await message.reply('❗️ Вы не можете повысить сам себе ранг')
      else:
         pass

      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'

         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Повышать ранг в семье можно от <b>3 ранга</b>', parse_mode='html')
      else:
         pass
      
      reply_proverka_family = 0

      reply_user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {reply_user_id}').fetchone()

      if reply_user_id_family != None:
         reply_rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {reply_user_id}').fetchone()
         reply_rank_family = int(reply_rank_family[0])  

         reply_name_family = cursor.execute(f'SELECT family from user_family where user_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_user_id in all_family2:
         reply_rank_family = 3
         
         reply_name_family = cursor.execute(f'SELECT name from family where owner_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_proverka_family == 2:
         return await message.reply(f'❗️ Этот игрок не состоит в клане')
      else:
         pass
      
      if reply_name_family != name_family:
         return await message.reply(f'❗️ Этот игрок состоит не в вашем клане')
      else:
         pass

      if reply_rank_family == 3:
         return await message.reply(f'❗️ У данного игрока максимальный ранг', parse_mode='html')
      else:
         pass
      

      cursor.execute(f'UPDATE user_family SET rank = {reply_rank_family + 1} WHERE user_id = {reply_user_id}')
      connect.commit()

      text = f'''
🔼 Вы повысили на 1 ранг игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
      '''
      await message.reply(text, parse_mode='html')







    if message.text.lower() == '-ранг семьи':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if user_id == reply_user_id:
         return await message.reply('❗️ Вы не можете понизить сам себе ранг')
      else:
         pass

      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'

         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Понижать ранг в семье можно от <b>3 ранга</b>', parse_mode='html')
      else:
         pass
      
      reply_proverka_family = 0

      reply_user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {reply_user_id}').fetchone()

      if reply_user_id_family != None:
         reply_rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {reply_user_id}').fetchone()
         reply_rank_family = int(reply_rank_family[0])  

         reply_name_family = cursor.execute(f'SELECT family from user_family where user_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_user_id in all_family2:
         reply_rank_family = 3
         
         reply_name_family = cursor.execute(f'SELECT name from family where owner_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_proverka_family == 2:
         return await message.reply(f'❗️ Этот игрок не состоит в клане')
      else:
         pass
      
      if reply_name_family != name_family:
         return await message.reply(f'❗️ Этот игрок состоит не в вашем клане')
      else:
         pass

      if reply_rank_family == 3:
         if status_owner_family == 'on':
            pass
         else:
            return await message.reply(f'❗️ Вы не можете понизить человека с <b>3 рангом</b> | <i>Под силу только владельцу семьи</i>', parse_mode='html')
      else:
         pass
      
      if reply_rank_family == 1:
         return await message.reply(f'❗️ У данного игрока и так минимальный ранг.')
      else:
         pass

      cursor.execute(f'UPDATE user_family SET rank = {reply_rank_family - 1} WHERE user_id = {reply_user_id}')
      connect.commit()

      text = f'''
🔽 Вы понизили на 1 ранг игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
      '''
      await message.reply(text, parse_mode='html')








    if message.text.startswith('Купить монеты') or message.text.startswith('купить монеты'):
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      reput = cursor.execute("SELECT reput from reput where user_id = ?",(message.from_user.id,)).fetchone()
      reput = int(reput[0])

      su = msg.text.split()[2]
      su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
      su3 = float(su2)
      summ = int(su3)

      summ2 = '{:,}'.format(summ).replace(',', '.')
      
      if summ < 10:
         return await message.reply(f'❗️ Можно покупать только от <code>10</code> <b>семейных монет</b>', parse_mode='html')
      else:
         pass

      if summ > reput:
         return await message.reply(f'❗️ У вас недостаточно <b>репутации</b> | <i>1 с. монета = 1 репутация</i>', parse_mode='html')
      else:
         pass

      if summ <= 0:
         return await message.reply(f'❗️ Сумма не должна быть отрицательным число <b>[0 и меньше]</b>', parse_mode='html')
      else:
         pass
      
      balance_family = cursor.execute(f'SELECT balance from family where name = "{name_family}"').fetchone()
      balance_family = balance_family[0]

      cursor.execute(f'UPDATE family SET balance = {balance_family + summ} WHERE name = "{name_family}"')
      cursor.execute(f'UPDATE reput SET reput = {reput - summ} WHERE user_id = "{user_id}"')
      connect.commit()

      text = f'''
💰 Вы положили в семейный мешок <code>{summ2}</code> семейный монет
      '''

      await message.reply(text, parse_mode='html')









    if message.text.startswith('+название семьи'):
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family5 = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family5 = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Менять название семьи можно только с <b>3 ранга</b>', parse_mode='html')
      else:
         pass

      user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_status = user_status[0]

      if user_status in ['Helper_Admin', 'Owner']:
         period = 1
      else:
         period = 604800 #7d

      get = cursor.execute(f'SELECT time_name FROM family WHERE name = "{name_family5}"').fetchone()
      last_stavka = f"{int(get[0])}"
      stavkatime = time.time() - float(last_stavka)

      if stavkatime < period:
         times2 = time.localtime(float(get[0]))
         print(times2)

         if times2.tm_mday <= 9:
            tm_mday2 = 0
         else:
            tm_mday2 = ''
         
         if times2.tm_mon <= 9:
            tm_mon2 = 0
         else:
            tm_mon2 = ''

         if times2.tm_hour <= 9:
            tm_hour2 = 0
         else:
            tm_hour2 = ''

         if times2.tm_min <= 9:
            tm_min2 = 0
         else:
            tm_min2 = ''

         full_times2 = f'{tm_mday2}{times2.tm_mday}.{tm_mon2}{times2.tm_mon}.{times2.tm_year} в {tm_hour2}{times2.tm_hour}:{tm_min2}{times2.tm_min}'

         return await message.reply(f'❗️ Менять название семьи, можно раз в <b>7 дней</b> | Последнее изменение название было <code>{full_times2}</code>', parse_mode='html')
      else:
         pass

      name_family = message.text.split()[2:]
      name_family2 = ' '.join(name_family)
      full_name_family = (name_family2).replace(' ','').replace('🇷🇺', '').replace('Россия', 'россия').replace('россия', '')

      if len(full_name_family) < 4:
         return await message.reply('❗️ Название семьи должна быть больше <b>4 символов</b>', parse_Mode='html')
      elif len(full_name_family) > 35:
         return await message.reply(f'❗️ Название семьи должна быть меньше <b>35 символов</b>', parse_mode='html')
      else:
         pass

      all_family_name = cursor.execute('SELECT name from family').fetchall()
      all_family_name2 = []

      for all_family_name3 in all_family_name:
         all_family_name2.append(all_family_name3[0])
   
      if full_name_family in all_family_name2:
         return await message.reply(f'❗️ Семья с названием «<b>{full_name_family}</b>» уже существует', parse_mode='html')
      else:
         pass

      cursor.execute(f'UPDATE family SET name = "{full_name_family}" where name = "{name_family5}"')

      sqlite_select_query27 = f"""SELECT * from user_family where family = \"{name_family5}\""""
      cursor.execute(sqlite_select_query27)
      full_user_id_family_update = cursor.fetchall()

      for update_name_family_user_id in full_user_id_family_update:
         print(update_name_family_user_id[1])
         cursor.execute(f'UPDATE user_family SET family = "{full_name_family}" where user_id = "{update_name_family_user_id[1]}"')
      connect.commit()

      text = f'''
✅ Вы успешно изменили название семьи с <b>{name_family5}</b> на <b>{full_name_family}</b>
      '''

      await message.reply(text, parse_mode='html')




    if message.text.lower() == 'информация о семьях':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       text = f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за «<b>СЕМЬИ</b>» 👨‍👩‍👧‍👦

✏️ <b><code>Создать семью</code> <i>[название]</i> - команда для создание свой семьи <i>(Стоимость: {config.cash_family} Donate-Coins 🪙)</i></b>
👨‍👩‍👧‍👦 <b><code>Моя семья</code> | <code>семья</code> - вывод информации за семью в которой вы состоите </b>
⚙️ <b><code>+название семьи</code> <i>[название]</i> - Меняет название семьи <i>( можно раз в 7d) (от 3 ранга)</i></b>
💎 <b><code>Купить монеты</code> <i>[количество]</i> - Покупка семейный монет в мешок семьи</b>
➖ <b><code>-ранг семьи</code> - Понизить игрока в семье на 1 ранг ниже <i>(от 3 ранга)</i></b>
➕ <b><code>+ранг семьи</code> - Повысить игрока в семье на 1 ранг выше <i>(от 3 ранга)</i></b>
👶 <b><code>Пригласить в семью</code> - Приглашение в вашу семью <i>(от 2 ранга)</i></b>
❌ <b><code>Выгнать из семьи</code> - Исключение игрока из вашей семьи <i>(от 3 ранга)</i></b>
💭 <b><code>+описание семьи</code> <i>[описание]</i> - Устоновка описание в вашей семье <i>(от 3 ранга)</i></b>
😔 <b><code>Распустить семью</code> - Удаление семьи <i>(от 3 ранга)</i></b>
🔙 <b><code>Выйти с семьи</code> - Выход с семьи </b>

❗️ Будьте окуратней при <b>выдаче ранга игроку</b>
       '''
       
       await message.reply(text, parse_mode='html')

















##########################################################################
    if message.text.lower() == 'реклама':
      user_id = message.from_user.id

      if user_id != config.owner_id:
         return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')
      else:
         pass

      await utils.advertising_utils(1, message)
   
    if message.text.lower() == 'post реклама':
      user_id = message.from_user.id

      if user_id != config.owner_id:
         return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')
      else:
         pass
      
      await utils.advertising_utils(2, message)

async def chats_handler(message):
   status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
   status_block = str(status_block[0])

   if status_block == 'on':
      return


   user_id = message.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
   user_status = str(user_status[0])

   if user_status in ['Owner', 'Helper_Admin', 'Admin']:
      chats = cursor.execute(f'SELECT * from chats')
      list_chat = []
      num = 0

      for chat in chats:
         
         num += 1

         list_chat.append(f'📎 <b>NAME: {chat[1]} | 🔎 ID:</b> <code>{chat[0]}</code> <b>| 📅 DATA:</b> <code>{chat[2]}</code>')
      
      list = '\n'.join(list_chat)

      await message.reply(list, parse_mode='html')
   else:
      return await message.reply('❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')




async def register_chat_handler(message):
   status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
   status_block = str(status_block[0])

   if status_block == 'on':
      return

   user_id = message.from_user.id
   user_name = message.from_user.get_mention(as_html=True)

   chat_id = message.chat.id
   group_name = message.chat.full_name
   cursor.execute(f"SELECT chat_id FROM chats WHERE chat_id = '{chat_id}'")

   if user_id == chat_id:
      return await message.reply('❗️ Нельзя регистрировать ЛС бота, в <b>качестве чата</b>', parse_mode='html')

   if cursor.fetchone() is None:
      text_register_chat = f'''
💭 <code>{user_name}</code> , вы <b>успешно зарегистрировали</b> чат <code>{group_name}</code> 
      '''
      time_register = f'{datetime.now()}'
      photo_new_chat = open('Photo/newchat.jpg', 'rb')
      cursor.execute("INSERT INTO chats VALUES(?, ?, ?);", (chat_id, group_name, time_register[:19]))
      connect.commit()

      await bot.send_photo(message.chat.id, photo_new_chat, text_register_chat, parse_mode='html')
   else:
      return await message.reply(f'❗️ <code>{group_name}</code> <b>уже зарегистрирован</b>', parse_mode='html')

async def cl_handler(message):
   try:
      status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
      status_block = str(status_block[0])

      if status_block == 'on':
         return


      
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      su1 = str(message.text.split()[1])
      win = numexpr.evaluate(f'{su1}')
      win2 = '{:,}'.format(win).replace(',', '.')

      text_cl = f'''
➗ <b>{su1}</b> = <code>{win2}</code>
      '''
      await message.reply(text_cl, parse_mode='html')
   except OverflowError :
      text = f'''
❗️ <b>Ошибка</b> , слишком большое число 
      '''
      await message.reply(f'{text}', parse_mode='html')
   except SyntaxError:
      text = f'''
❗️ <b>Ошибка</b>, в примере есть STRING [буквы, символы]
      '''
      await message.reply(f'{text}', parse_mode='html')

   except TypeError:
      text = f'''
❗️ <b>Ошибка</b>, число должно быть полным
      '''
      await message.reply(f'{text}', parse_mode='html')

async def reset_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return

    msg = message
    user_id = msg.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    reply_user_id = int(message.text.split()[1])

    text = ' '.join(message.text.split()[2:])


    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"""
⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ |Действие: Обнуление по ID
💈 |Причина: {text} 
👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       """, parse_mode='html')

       await message.bot.send_message(message.chat.id, f"""
⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ |Действие: Обнуление по ID
💈 |Причина: {text} 
👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'DELETE from user_family WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'DELETE from family WHERE owner_id = "{reply_user_id}"')

       connect.commit()
       await message.bot.send_message(reply_user_id, f"""
<b>🆘 | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, ВЫ БЫЛИ ОБНУЛЕНЫ | 🆘</b>
💭 | Причина: <i>{text}</i>
⛔️ | Администратором: <a href='tg://user?id={user_id}'>{user_name}</a> 
       """, parse_mode='html')
       return

    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"""
⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ |Действие: Обнуление по ID
💈 |Причина: {text} 
👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'DELETE from user_family WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'DELETE from family WHERE owner_id = "{reply_user_id}"')
       connect.commit()
       await message.bot.send_message(reply_user_id, f"""
<b>🆘 | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, ВЫ БЫЛИ ОБНУЛЕНЫ | 🆘</b>
💭 | Причина: <i>{text}</i>
⛔️ | Администратором: <a href='tg://user?id={user_id}'>{user_name}</a> 
       """, parse_mode='html')
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна от прав админитсратора \"ХЕЛПЕР АДМИН\"", parse_mode='html')




async def ban_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    if not message.reply_to_message:
       await message.reply("Эта команда должна быть ответом на сообщение!")
       return


    msg = message
    user_id = msg.from_user.id
    reply_user_id = msg.reply_to_message.from_user.id
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    reply_user_name = str(reply_user_name[0])

    


    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'{full_name} выдал бан игроку: {reply_full_name}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':

       if reply_user_id == config.owner_id:
         return await message.reply(f'❗️ Вы не можете дать бан <b>владельцу бота</b>', parse_mode='html')
       else:
         pass

       await message.bot.send_message(config.owner_id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'{full_name} выдал бан игроку: {reply_full_name}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')



async def ban_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    msg = message
    user_id = msg.from_user.id
    reply_user_id = int(message.text.split()[1])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    


    if user_status == 'Owner':
       await message.bot.send_message(reply_user_id, f"📛 | <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был заблокирован по ID", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       
       print(f'{full_name} выдал бан игроку: {reply_user_name}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       if reply_user_id == config.owner_id:
         return await message.reply(f'❗️ Вы не можете дать бан <b>владельцу бота</b>', parse_mode='html')
       else:
         pass


       await message.bot.send_message(reply_user_id, f"📛 | <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был заблокирован по ID", parse_mode='html')
       await message.bot.send_message(config.owner_id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       
       print(f'{full_name} выдал бан игроку: {reply_user_name}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')






async def unban_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    if not message.reply_to_message:
       await message.reply("Эта команда должна быть ответом на сообщение!")
       return

    msg = message
    user_id = msg.from_user.id
    reply_user_id = msg.reply_to_message.from_user.id
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    reply_user_name = str(reply_user_name[0])

    

    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'{full_name} выдал разбан игроку: {reply_full_name}')
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')




async def unban_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return

    
    msg = message
    user_id = msg.from_user.id
    reply_user_id = int(message.text.split()[1])

    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    

    if user_status == 'Owner':
       await message.bot.send_message(reply_user_id, f"✅ | <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был разблокирован по ID", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта по ID\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(reply_user_id, f"✅ | <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был разблокирован по ID", parse_mode='html')
       await message.bot.send_message(config.owner_id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта по ID\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта по ID\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'{full_name} выдал разбан игроку: {reply_full_name}')
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')



async def reset_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    msg = message
    user_id = msg.from_user.id
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    

    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Масовое обнуление\n💈 | Время: навсегда\n👨 |Игроку: Всем игрокам", parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {config.start_money}')
       cursor.execute(f'UPDATE users SET bank = {0}')
       cursor.execute(f'UPDATE users SET depozit = {0}')
       cursor.execute(f'UPDATE users SET rating = {0}')
       cursor.execute(f'UPDATE users SET ethereum = {100}')
       cursor.execute(f'UPDATE mine SET iron = {0}')
       cursor.execute(f'UPDATE mine SET metall = {0}')
       cursor.execute(f'UPDATE mine SET silver = {0}')
       cursor.execute(f'UPDATE mine SET bronza = {0}')
       cursor.execute(f'UPDATE mine SET gold = {0}')
       cursor.execute(f'UPDATE farm SET linen = {0}')
       cursor.execute(f'UPDATE farm SET cotton = {0}')
       cursor.execute(f'UPDATE house SET house = {0}')
       cursor.execute(f'UPDATE house SET basement = {0}')
       cursor.execute(f'UPDATE cars SET cars = {0}')
       cursor.execute(f'UPDATE cars SET hp = {0}')
       cursor.execute(f'UPDATE cars SET benz = {0}')
       cursor.execute(f'UPDATE bot_time SET stavka_games = {0} ')
       cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} ')
       cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} ')
       cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_pick = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_rake = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_craft = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_kit = {0} ')
       cursor.execute(f'UPDATE family SET balance = {0} ')
       connect.commit()
       full_name = msg.from_user.full_name
       print(f'{full_name} сделал масовое обнуление')
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"OWNER\"", parse_mode='html')


async def help_admins_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_id = message.from_user.id

    await message.bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация для администрации чата ⛔️

1️⃣ /channel_mute [количество] [м\д\ч] [причина] - Выдача затычки игроку 
2️⃣ /channel_ban [количество] [м\д\ч] [причина] - Выдача бана игроку
3️⃣ /channel_unmute - снятие затычки игроку 
4️⃣ /channel_unban - снятие бана игроку 

ℹ️Команды работают ответом на сообщение нарушителя     
    """, parse_mode='html')



async def warn_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    reply_user_id = message.reply_to_message.from_user.id

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute("SELECT warn from warn where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    warn = int(warn[0])

    warn2 = warn + 1
   
    if user_status == 'Owner':
       if warn2 > 5:
          await message.bot.send_message(message.chat.id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Helper_Admin':

       if reply_user_id == config.owner_id:
         return await message.reply(f'❗️ Вы не можете дать варн <b>владельцу бота</b>', parse_mode='html')
       else:
         pass

       if warn2 > 5:
          await message.bot.send_message(message.chat.id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')

       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')
    
    


async def warn_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    reply_user_id = int(message.text.split()[1])

    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute(f"SELECT warn from warn where user_id = {reply_user_id}").fetchone()
    warn = int(warn[0])

    warn2 = warn + 1
   
    if user_status == 'Owner':
       if warn2 > 5:
          await message.bot.send_message(reply_user_id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован из-за 6\6 варнов", parse_mode='html')

          await message.bot.send_message(message.chat.id, f"⚠️ | Аккаунт: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Helper_Admin':

       if reply_user_id == config.owner_id:
         return await message.reply(f'❗️ Вы не можете дать варн <b>владельцу бота</b>', parse_mode='html')
       else:
         pass


       if warn2 > 5:
          await message.bot.send_message(reply_user_id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован из-за 6\6 варнов", parse_mode='html')

          await message.bot.send_message(config.owner_id, f"⚠️ | Аккаунт: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> был заблокирован ", parse_mode='html')

          await message.bot.send_message(message.chat.id, f"⚠️ | Аккаунт: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')

       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')



async def unwarn_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    reply_user_id = int(message.text.split()[1])

    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute(f"SELECT warn from warn where user_id = {reply_user_id}").fetchone()
    warn = int(warn[0])

    warn2 = warn - 1
   
    if user_status == 'Owner':
       if warn2 < 0:
          await message.bot.send_message(message.chat.id, f"🆘 | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Helper_Admin':
       if warn2 < 0:
          await message.message.bot.send_message(message.chat.id, f"🆘 | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Owner':
       await message.message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')



async def unwarn_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    if not message.reply_to_message:
       await message.reply("🆘 | Эта команда должна быть ответом на сообщение!")
       return   
    reply_user_id = message.reply_to_message.from_user.id

    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute(f"SELECT warn from warn where user_id = {reply_user_id}").fetchone()
    warn = int(warn[0])

    warn2 = warn - 1
   
    if user_status == 'Owner':
       if warn2 < 0:
          await message.bot.send_message(message.chat.id, f"🆘 | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Helper_Admin':
       if warn2 < 0:
          await message.bot.send_message(message.chat.id, f"🆘 | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')



async def report_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_id = message.from_user.id

    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    text = message.text[7:]
    
    if text == '':
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, репорт не может быть пустым", parse_mode='html')
       return
    rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
    for row in rows:
       await message.bot.send_message(row[0], f"<b>🆘ВАМ ПРИШЁЛ РЕПОРТ🆘</b>\n👨 | Отправитель: <a href='tg://user?id={user_id}'>{user_name}</a>\n💬 |Сообщение: <i>{text}</i>", parse_mode='html')

    await message.bot.send_message(config.owner_id,f"""
<b>🆘ВАМ ПРИШЁЛ РЕПОРТ🆘</b>
👨 | Отправитель: <a href='tg://user?id={user_id}'>{user_name}</a>  
💬 |Сообщение: <i>{text}</i>
    """, parse_mode='html')  
    await message.bot.send_message(message.chat.id, f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш репорт был успешно отправлен администрации", parse_mode='html')



async def channelunban_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return

    await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
    await message.reply(f'👤 | Администратор: {name1}\n📲 | Разбанил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>',  parse_mode='html')

async def channelban_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return
    comment = " ".join(message.text.split()[1:])
    await message.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False))
    await message.reply(f'👤 | Администратор: {name1}\n🛑 | Забанил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: навсегда\n📃 | Причина: {comment}',  parse_mode='html')


async def channelunmute_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return
    await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
    await message.reply(f'👤 | Администратор: {name1}\n🔊 | Размутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>',  parse_mode='html')


async def channelmute_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return
    try:
       muteint = int(message.text.split()[1])
       mutetype = message.text.split()[2]
       comment = " ".join(message.text.split()[3:])
    except IndexError:
       await message.reply('ℹ | Не хватает аргументов!\nПример:\n<code>/мут 1 ч причина</code>')
       return
    if mutetype == "ч" or mutetype == "часов" or mutetype == "час":
       dt = datetime.now() + timedelta(hours=muteint)
       timestamp = dt.timestamp()
       await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
       await message.reply(f'👤 | Администратор: {name1}\n🛑 | Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: {muteint} {mutetype}\n📃 | Причина: {comment}',  parse_mode='html')
    if mutetype == "м" or mutetype == "минут" or mutetype == "минуты":
       dt = datetime.now() + timedelta(minutes=muteint)
       timestamp = dt.timestamp()
       await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
       await message.reply(f'👤 | Администратор: {name1}\n🛑 | Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: {muteint} {mutetype}\n📃 | Причина: {comment}',  parse_mode='html')
    if mutetype == "д" or mutetype == "дней" or mutetype == "день":
       dt = datetime.now() + timedelta(days=muteint)
       timestamp = dt.timestamp()
       await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
       await message.reply(f'👤 | Администратор: {name1}\n | 🛑Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: {muteint} {mutetype}\n📃 | Причина: {comment}',  parse_mode='html')



async def disconect_database_handler(message):
    if not message.reply_to_message:
       await message.bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, эта команда должна быть ответом на сообщение", parse_mode='html')
       return
       

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return

    user_id = message.from_user.id
    reply_user_id = message.reply_to_message.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    i = f'''
🗄 Вы удалили <b>{user_name}</b> с базы данных 
   '''

    i2 = f'''
❗️ Данная команда доступна от прав администратора <b>OWNER</b>
❕Для приобретение данных прав, напишите команду <code>Донат</code>
   '''

    text = [i, i2]
    if user_status == 'Owner':
        await message.reply(text[0], parse_mode='html')
        cursor.execute(f'DELETE from users where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from mine where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from user_case where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from farm where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from house where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from cars where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from bot_time where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from time_bank where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from ob_time where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from time_prefix where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from time_sms where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from warn where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from console where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from channel_pov where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from avatarka where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from reput where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from h_module where user_id = {reply_user_id}')
        connect.commit()
    else:  
        await message.reply(text[1], parse_mode='html')

async def gamevb_handler(message):
   status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
   status_block = str(status_block[0])

   if status_block == 'on':
       return
   msg = message
   user_id = msg.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   period = 5

   balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
   balance = int(balance[0])



   get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
   last_stavka = f"{int(get[0])}"
   stavkatime = time.time() - float(last_stavka)
   if stavkatime > period:
      if balance > 0:
         await message.bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вы уверены что хотите сыграть в GAME-VB ? 🧊

ℹ️ | В этой игре вы играете сразу на весь <b>баланс</b>

↘️ Выберите одну кнопку ниже         
""",reply_markup=gamevbmenu,  parse_mode='html')
      else:
         await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас недостаточно средств! ", parse_mode='html')
   else:
      await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд", parse_mode='html')         

      
async def info_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    msg = message
    user_id = msg.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    

    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    reply_user_id = int(message.text.split()[1])

    balance = cursor.execute(f"SELECT balance from users where user_id = {reply_user_id}").fetchone()
    balance = int(balance[0])
    balance2 = '{:,}'.format(balance).replace(',', '.')

    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    bank = cursor.execute(f"SELECT bank from users where user_id = {reply_user_id}").fetchone()
    bank = int(bank[0])
    bank3 = '{:,}'.format(bank).replace(',', '.')

    user_tg_name = 'Аккаунт'

    reply_user_status = cursor.execute(f"SELECT user_status from users where user_id = {reply_user_id}").fetchone()
    reply_user_status = str(reply_user_status[0])

    ethereum = cursor.execute(f"SELECT ethereum from users where user_id = {reply_user_id}").fetchone()
    ethereum = int(ethereum[0])
    ethereum2 = '{:,}'.format(ethereum).replace(',', '.')

    rating = cursor.execute(f"SELECT rating from users where user_id = {reply_user_id}").fetchone()
    rating = int(rating[0])
    rating2 = '{:,}'.format(rating).replace(',', '.')

    status_block = cursor.execute(f"SELECT status_block from users where user_id = {reply_user_id}").fetchone()
    status_block = str(status_block[0])

    time_register = cursor.execute(f"SELECT time_register from users where user_id = {reply_user_id}").fetchone()
    time_register = time_register[0]

    pref = cursor.execute(f"SELECT pref from users where user_id = {reply_user_id}").fetchone()
    pref = str(pref[0])

    donate_coins = cursor.execute(f"SELECT donate_coins from users where user_id = {reply_user_id}").fetchone()
    donate_coins = int(donate_coins[0])
    donate_coins2 = '{:,}'.format(donate_coins).replace(',', '.')

    bank2 = cursor.execute(f"SELECT bank2 from users where user_id = {reply_user_id}").fetchone()
    bank2 = int(bank2[0])
    bank22 = '{:,}'.format(bank2).replace(',', '.')

    depozit = cursor.execute(f"SELECT depozit from users where user_id = {reply_user_id}").fetchone()
    depozit = int(depozit[0])
    depozit2 = '{:,}'.format(depozit).replace(',', '.')

    if user_status != ['Owner', 'Helper_Admin', 'Admin']:
       user_status2 = 'Пользователь'
    if user_status in ['Owner', 'Helper_Admin', 'Admin']:
       await message.bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные о <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> :

💬 | Телеграм: <a href='tg://user?id={reply_user_id}'>{user_tg_name}</a>
🟢 | Статус: {reply_user_status}
🟩 | Статус блокировки: {status_block}

👤 | Ник: {reply_user_name}
💰 | Баланс: {balance2}$
🏪 | Банковский счёт: {bank3}$
🏪 | Хранительный счёт: {bank22}$
🏛 | Депозит: {depozit2}$
🟪 | Эфириум: {ethereum2} 🟣
💎 | Рейтинг: {rating2} 💎
🪙 | Donate-Coins: {donate_coins2} 🪙

📆 | Дата регистрации: {time_register}     
       """, parse_mode='html')



async def info_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    msg = message
    user_id = msg.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    if not message.reply_to_message:
       await message.bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, эта команда должна быть ответом на сообщение", parse_mode='html')
       return
       
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    reply_user_id = message.reply_to_message.from_user.id

    balance = cursor.execute(f"SELECT balance from users where user_id = {reply_user_id}").fetchone()
    balance = int(balance[0])
    balance2 = '{:,}'.format(balance).replace(',', '.')

    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    bank = cursor.execute(f"SELECT bank from users where user_id = {reply_user_id}").fetchone()
    bank = int(bank[0])
    bank3 = '{:,}'.format(bank).replace(',', '.')

    user_tg_name = message.reply_to_message.from_user.get_mention(as_html=True)

    reply_user_status = cursor.execute(f"SELECT user_status from users where user_id = {reply_user_id}").fetchone()
    reply_user_status = str(reply_user_status[0])

    ethereum = cursor.execute(f"SELECT ethereum from users where user_id = {reply_user_id}").fetchone()
    ethereum = int(ethereum[0])
    ethereum2 = '{:,}'.format(ethereum).replace(',', '.')

    rating = cursor.execute(f"SELECT rating from users where user_id = {reply_user_id}").fetchone()
    rating = int(rating[0])
    rating2 = '{:,}'.format(rating).replace(',', '.')

    status_block = cursor.execute(f"SELECT status_block from users where user_id = {reply_user_id}").fetchone()
    status_block = str(status_block[0])

    time_register = cursor.execute(f"SELECT time_register from users where user_id = {reply_user_id}").fetchone()
    time_register = time_register[0]

    pref = cursor.execute(f"SELECT pref from users where user_id = {reply_user_id}").fetchone()
    pref = str(pref[0])

    donate_coins = cursor.execute(f"SELECT donate_coins from users where user_id = {reply_user_id}").fetchone()
    donate_coins = int(donate_coins[0])
    donate_coins2 = '{:,}'.format(donate_coins).replace(',', '.')

    bank2 = cursor.execute(f"SELECT bank2 from users where user_id = {reply_user_id}").fetchone()
    bank2 = int(bank2[0])
    bank22 = '{:,}'.format(bank2).replace(',', '.')

    depozit = cursor.execute(f"SELECT depozit from users where user_id = {reply_user_id}").fetchone()
    depozit = int(depozit[0])
    depozit2 = '{:,}'.format(depozit).replace(',', '.')

    if user_status in ['Owner', 'Helper_Admin', 'Admin']:
       await message.bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные о <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> :

💬 | Телеграм: {user_tg_name}
🟢 | Статус: {reply_user_status}
🟩 | Статус блокировки: {status_block}

👤 | Ник: {reply_user_name}
💰 | Баланс: {balance2}$
🏪 | Банковский счёт: {bank3}$
🏪 | Хранительный счёт: {bank22}$
🏛 | Депозит: {depozit2}$
🟪 | Эфириум: {ethereum2} 🟣
💎 | Рейтинг: {rating2} 💎
🪙 | Donate-Coins: {donate_coins2} 🪙

📆 | Дата регистрации: {time_register}     
       """, parse_mode='html')

async def start_handler(message):



    name = message.from_user.get_mention(as_html=True)
    i = f'''
👋 Привет <b>{name}</b>, я игровой бот <b>{config.full_bot_name}</b>
💸 Тебе как новому пользователю был выдан подарок в размере <code>{'{:,}'.format(config.start_money).replace(',', '.')}$</code>
❗️ Для ознакомление с моими командами, введи команду <code>Помощь</code> , или вибери кнопку <b>ниже</b>
➕ Так же ты можешь добавить бота в свой чат по кнопке <b>ниже</b>
    '''
    i2 = f'''
❗️ <b>{name}</b>, вы уже зарегистрированы в боте
❕ Если у вас возникла какая то проблема с какой то командой, обратитесь к {config.owner} для повторной регистрации <b>[Если у вас SPAM BAN, то вы можете обратиться к нему через данного бота с помощью команд /m [ID] [message] или через команду /report ]</b>
    '''

    text_register = [i, i2]
    photo_welcome = open('Photo/welcome.jpg', 'rb')
    msg = message
    user_id = msg.from_user.id
    full_name = msg.from_user.full_name
    user_name = 'Игрок'
    user_status = "Player"
    status_block = 'off'
    stats_status = 'off'
    pref = 'Игрок'
    status_console = 'off'
    avatarka_start = 'none'
    klan_index = 0
    status_family = 0
    chat_id = message.chat.id
    result = time.localtime()

    if int(result.tm_mon) <= 9:
      p = "0"
    else:
      p = ''
    times = f'{result.tm_mday}.{p}{result.tm_mon}.{result.tm_year} | {result.tm_hour}:{result.tm_min}:{result.tm_sec}'
    times2 = str(times)

    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None:
       cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, user_name, full_name, user_status, config.start_money, 0, 0, 0, status_block, times2, pref, 0, 0, 0, 0, stats_status))
       cursor.execute("INSERT INTO mine VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(user_id, full_name,status_block, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO farm VALUES(?, ?, ?, ?, ?);",(user_id, full_name,status_block, 0, 0))
       cursor.execute("INSERT INTO house VALUES(?, ?, ?, ?);",(user_id, user_name, 0, 0))
       cursor.execute("INSERT INTO cars VALUES(?, ?, ?, ?, ?);",(user_id, user_name, 0, 0, 0))
       cursor.execute("INSERT INTO user_case VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO bot_time VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, 0, 0, 0, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO promo1 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO time_bank VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO ob_time VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO console VALUES(?, ?);",(user_id, status_console))
       cursor.execute("INSERT INTO time_prefix VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO time_sms VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO promo1 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO channel_pov VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO avatarka VALUES(?, ?);",(user_id, avatarka_start))
       cursor.execute("INSERT INTO reput VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO h_module VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO promo2 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo3 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo4 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo5 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo6 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo7 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo8 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo9 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo10 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo11 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo12 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo13 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo14 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo15 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo16 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo17 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo18 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo19 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo20 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo21 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo22 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo23 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo24 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo25 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo26 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo27 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo28 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo29 VALUES(?, ?, ?);",(user_id, 0, 0))

       connect.commit()
       print(f'Зарегестрировался в боте пользователь: {full_name}')
       await bot.send_photo(message.chat.id, photo_welcome, text_register[0], reply_markup=reg, parse_mode='html')

    else:
       await bot.send_photo(message.chat.id, photo_welcome, text_register[1], reply_markup=reg, parse_mode='html')


async def sistem_message_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
        return
    try:
        text = ' '.join(message.text.split()[2:])

        msg = message
        user_id = msg.from_user.id
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
        user_name = str(user_name[0])

        reply_user_id = int(message.text.split()[1])
        reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
        reply_user_name = str(reply_user_name[0])

        period = 5
        get = cursor.execute("SELECT stavka FROM time_sms WHERE user_id = ?", (message.from_user.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)

        if len(text) > 35:
            await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, сообщение не может быть более чем 35 символов ", parse_mode='html')
            return
        if stavkatime > period:
            await message.bot.send_message(user_id, f"💬 | [Я ➡️ <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>] {text}", parse_mode='html')
            await message.bot.send_message(reply_user_id, f"💬 | [<a href='tg://user?id={user_id}'>{user_name}</a> ➡️ Я] {text}", parse_mode='html')
            cursor.execute(f'UPDATE time_sms SET stavka = {time.time()} WHERE user_id = {user_id}')
            connect.commit()
            return
        else:
            await message.bot.send_message(user_id, f"🆘 | Игрок, сообщение писать можно раз в 5 секунд", parse_mode='html')
            return
    except:
        await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Либо вы не правильно ID, или данный игрок не играет в бота", parse_mode='html')
        return



async def info_donate_callback(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f'Чтобы пополнить счёт, введите команду: <code>пополнить</code> <i>(сумма)</i>', parse_mode='html')


async def check_pays_callback(callback: types.CallbackQuery):
    bill_id = str(callback.data[10:])
    info = await get_check(bill_id)

    if info == False:
        return callback.answer(f'Счёт не найден')
    else:
        pass

    if str(p2p.check(bill_id=bill_id).status) == 'PAID':
        users_money = await user_money(callback.from_user.id)
        donate = int(info[1])

        x2donate_status = await status_x2donate()

        if x2donate_status == 'on':
            await update_money(callback.from_user.id, users_money + donate * 2)
            await delete_check(bill_id)
            await callback.message.answer(f'✅ <b>{callback.from_user.full_name}, вы успешно оплатили свой счёт и получили {donate * 2} руб.</b> <i>🎗X2 Донат</i>', parse_mode='html')
            return
        else:
            pass
        await update_money(callback.from_user.id, users_money + donate)
        await delete_check(bill_id)
        await callback.message.answer(f'✅ <b>{callback.from_user.full_name}, вы успешно оплатили свой счёт и получили {donate} руб.</b>', parse_mode='html')
    else:
        await callback.message.answer('Вы не оплатили счёт', reply_markup=pay(False, bill=bill_id))


async def pay_money3_callback(callback: types.CallbackQuery):
    times = float(callback.data[11:])

    last_time = f"{int(times)}"
    sec_time = time.time() - float(last_time)

    period = 60
    if sec_time >= period:
        await callback.message.delete()
        return await callback.message.answer(f'⏰ {callback.from_user.full_name} Срок действия этой кнопки истёк. Кнопка была удалена')
    else:
        pass

    money_pay = await course_money3()
    cash_money_pay = await course_cash_money3()

    users_money = await user_money(callback.from_user.id)

    if users_money < cash_money_pay:
        return await callback.answer('❗️ У вас не хватает средств')
    else:
        pass
    
    users_balance = await user_balance(callback.from_user.id)

    await update_money(callback.from_user.id, users_money - cash_money_pay)
    await update_balance(callback.from_user.id, users_balance + money_pay)
    full_summ = await utils.scor_summ(money_pay)
    await callback.message.answer(f'🎉 Вы успешно купили <b>{full_summ}</b>', parse_mode='html')





async def pay_money1_callback(callback: types.CallbackQuery):
    times = float(callback.data[11:])

    last_time = f"{int(times)}"
    sec_time = time.time() - float(last_time)

    period = 60
    if sec_time >= period:
        await callback.message.delete()
        return await callback.message.answer(f'⏰ {callback.from_user.full_name} Срок действия этой кнопки истёк. Кнопка была удалена')
    else:
        pass

    money_pay = await course_money1()
    cash_money_pay = await course_cash_money1()

    users_money = await user_money(callback.from_user.id)

    if users_money < cash_money_pay:
        return await callback.answer('❗️ У вас не хватает средств')
    else:
        pass
    
    users_balance = await user_balance(callback.from_user.id)

    await update_money(callback.from_user.id, users_money - cash_money_pay)
    await update_balance(callback.from_user.id, users_balance + money_pay)
    full_summ = await utils.scor_summ(money_pay)
    await callback.message.answer(f'🎉 Вы успешно купили <b>{full_summ}</b>', parse_mode='html')




async def pay_money2_callback(callback: types.CallbackQuery):
    times = float(callback.data[11:])

    last_time = f"{int(times)}"
    sec_time = time.time() - float(last_time)

    period = 60
    if sec_time >= period:
        await callback.message.delete()
        return await callback.message.answer(f'⏰ {callback.from_user.full_name} Срок действия этой кнопки истёк. Кнопка была удалена')
    else:
        pass

    money_pay = await course_money2()
    cash_money_pay = await course_cash_money2()

    users_money = await user_money(callback.from_user.id)

    if users_money < cash_money_pay:
        return await callback.answer('❗️ У вас не хватает средств')
    else:
        pass
    
    users_balance = await user_balance(callback.from_user.id)

    await update_money(callback.from_user.id, users_money - cash_money_pay)
    await update_balance(callback.from_user.id, users_balance + money_pay)
    full_summ = await utils.scor_summ(money_pay)
    await callback.message.answer(f'🎉 Вы успешно купили <b>{full_summ}</b>', parse_mode='html')




async def priglashenie_callback(call: types.CallbackQuery):

   user1, user2, name_family = call.data.replace('accept_', '', 1).split(':')
   print(call.from_user.id, user1)
   
   if int(call.from_user.id) == int(user1):
      pass
   else:
      return await call.answer('Приглашение не для тебя ❗️')

   user_id = call.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(call.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
   all_family2 = []
   
   for all_owner_id in all_family:
      all_family2.append(all_owner_id[0])

   if user_id in all_family2:
      return await call.message.answer(f'❗️У вас есть <b>своя семья.</b> Зачем вам ещё одна? | <code>Распустить семью</code> - удаление семьи ', parse_mode='html')
   else:
      pass

   user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

   if user_id_family != None:
      return await call.message.answer('❗️ Вы уже <b>состоите в семье</b> | напишите «<code>выйти с семьи</code>» - для выхода с вашей семьи',parse_mode='html')
   else:
      pass

   text = f'''
✅ <a href='tg://user?id={user1}'>{user2}</a>, вы приняли приглашение в семью «<b>{name_family}</b>». Вы теперь состоите в семье
   '''

   text2 = f'''
❗️ В вашу семью «<b>{name_family}</b>» вступил <a href='tg://user?id={user1}'>{user2}</a>
   '''
   owner_id_family = cursor.execute(f"SELECT owner_id from family where name = \"{name_family}\"").fetchone()
   owner_id_family = owner_id_family[0]

   cursor.execute("INSERT INTO user_family VALUES(?, ?, ?, ?);",(user2, user1, name_family, 1))
   await call.message.bot.send_message(owner_id_family, text2, parse_mode='html')
   await call.message.answer(text, parse_mode='html')


async def organiz_callback(callback: types.CallbackQuery):
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       text = f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за все организации 🏰

👨‍👩‍👧‍👦 <code>Информация о семьях</code> <b>- Выводит список команд семьей</b>
       '''
       
       await callback.message.edit_text(text,reply_markup=help_back, parse_mode='html')









async def top_f_callback(callback: types.CallbackQuery):
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       list = cursor.execute(f"SELECT * FROM family ORDER BY balance DESC").fetchmany(10)
       top_list = []

       num = 0

       for user in list:

          num += 1

          if num == 1:
             num2 = '1️⃣'
             num3 = ' <b>🎯ТОП 1🎯</b> |'
          if num == 2:
             num2 = '2️⃣'
             num3 = ''
          if num == 3:
             num2 = '3️⃣'
             num3 = ''
          if num == 4:
             num2 = '4️⃣'
             num3 = ''
          if num == 5:
             num2 = '5️⃣'
             num3 = ''
          if num == 6:
             num2 = '6️⃣'
             num3 = ''
          if num == 7:
             num2 = '7️⃣'
             num3 = ''
          if num == 8:
             num2 = '8️⃣'
             num3 = ''
          if num == 9:
             num2 = '9️⃣'
             num3 = ''
          if num == 10:
             num2 = '🔟'
             num3 = ''
          
          balance = '{:,}'.format(user[4]).replace(',','.')
          
          if user[1] == config.owner_id:
            pass
          else:
            text = f'{num2} {user[0]} |{num3} 🔎 ID: <code>{user[3]}</code> | {balance} с. монет'

          top_list.append(text)  


       if top_list == ['']:
         top_f = '\n    ❗️ <b>На данный момент нету ни одной семьи</b>'
       else:
         top_f = '\n'.join(top_list)

       await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 10 семьей в «<b>{config.full_bot_name}</b>»:\n" + top_f, parse_mode='html')


async def top_а_callback(callback: types.CallbackQuery):
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       list = cursor.execute(f"SELECT * FROM users ORDER BY game DESC").fetchmany(10)
       top_list = []

       num = 0

       for user in list:

          num += 1

          if num == 1:
             num2 = '1️⃣'
             num3 = ' <b>🎯ТОП 1🎯</b> |'
          if num == 2:
             num2 = '2️⃣'
             num3 = ''
          if num == 3:
             num2 = '3️⃣'
             num3 = ''
          if num == 4:
             num2 = '4️⃣'
             num3 = ''
          if num == 5:
             num2 = '5️⃣'
             num3 = ''
          if num == 6:
             num2 = '6️⃣'
             num3 = ''
          if num == 7:
             num2 = '7️⃣'
             num3 = ''
          if num == 8:
             num2 = '8️⃣'
             num3 = ''
          if num == 9:
             num2 = '9️⃣'
             num3 = ''
          if num == 10:
             num2 = '🔟'
             num3 = ''

          top_list.append(f'{num2} {user[1]} |{num3} 🔎 ID: <code>{user[0]}</code> | {user[12]} всего игр')  

       top_a = '\n'.join(top_list)

       await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 10 азартных игроков в боте:\n" + top_a, parse_mode='html')

async def top_y_callback(callback: types.CallbackQuery):
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       list = cursor.execute(f"SELECT * FROM reput ORDER BY reput DESC").fetchmany(10)
       top_list = []

       num = 0

       for user in list:
          user_top = cursor.execute(f'SELECT user_name from users where user_id = {user[0]}').fetchone()
          user_top = user_top[0]

          num += 1

          summ = '{:,}'.format(user[1]).replace(',','.')

          if num == 1:
             num2 = '1️⃣'
             num3 = ' <b>📈ТОП 1📈</b> |'
          if num == 2:
             num2 = '2️⃣'
             num3 = ''
          if num == 3:
             num2 = '3️⃣'
             num3 = ''
          if num == 4:
             num2 = '4️⃣'
             num3 = ''
          if num == 5:
             num2 = '5️⃣'
             num3 = ''
          if num == 6:
             num2 = '6️⃣'
             num3 = ''
          if num == 7:
             num2 = '7️⃣'
             num3 = ''
          if num == 8:
             num2 = '8️⃣'
             num3 = ''
          if num == 9:
             num2 = '9️⃣'
             num3 = ''
          if num == 10:
             num2 = '🔟'
             num3 = ''
          

          top_list.append(f'{num2} {user_top} |{num3} 🔎 ID: <code>{user[0]}</code> | 📊 {summ} репутации')  
       top_y = '\n'.join(top_list)

       await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 10 успешных игроков в боте:\n" + top_y, parse_mode='html')




async def top_b_callback(callback: types.CallbackQuery):
       import utils
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       list = cursor.execute(f"SELECT * FROM users ORDER BY balance DESC").fetchmany(10)
       top_list = []

       num = 0

       for user in list:
          balance3 = await utils.scor_summ(user[4])
            
          num += 1

          if num == 1:
             num2 = '1️⃣'
             num3 = ' <b>💰ТОП 1💰</b> |'
          if num == 2:
             num2 = '2️⃣'
             num3 = ''
          if num == 3:
             num2 = '3️⃣'
             num3 = ''
          if num == 4:
             num2 = '4️⃣'
             num3 = ''
          if num == 5:
             num2 = '5️⃣'
             num3 = ''
          if num == 6:
             num2 = '6️⃣'
             num3 = ''
          if num == 7:
             num2 = '7️⃣'
             num3 = ''
          if num == 8:
             num2 = '8️⃣'
             num3 = ''
          if num == 9:
             num2 = '9️⃣'
             num3 = ''
          if num == 10:
             num2 = '🔟'
             num3 = ''
          
          if user[3] == 'Owner':
             stats = ' ✅<b>РАЗРАБОТЧИК</b>✅ |'
          if user[3] == 'Admin':
             stats = ' ⛔️<b>АДМИН</b>⛔️ |'
          if user[3] == 'Helper_Admin':
             stats = ' ⚠️<b>HELPER АДМИН</b>⚠️ |'
          if user[3] in ['Player', 'Vip', 'Premium', 'Platina', 'Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin']:
             stats = ''

          
          top_list.append(f"{num2} {user[1]} |{stats}{num3} 🔎 ID: <code>{user[0]}</code> | ${balance3} ")

       top = "\n".join(top_list)
       await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 10 богачей в боте:\n" + top, parse_mode='html')

async def top_callback(callback: types.CallbackQuery):
       list = cursor.execute(f"SELECT * FROM users ORDER BY rating DESC").fetchmany(10)
       top_list = []
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (callback.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       num = 0

       

       for user in list:
           if user[7] >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
              c6 = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
           else:
              c6 = user[7]

           

           num += 1

           if num == 1:
              num2 = '1️⃣'
              num3 = ' <b>💎ТОП 1💎</b> |'
           if num == 2:
              num2 = '2️⃣'
              num3 = ''
           if num == 3:
              num2 = '3️⃣'
              num3 = ''
           if num == 4:
              num2 = '4️⃣'
              num3 = ''
           if num == 5:
              num2 = '5️⃣'
              num3 = ''
           if num == 6:
              num2 = '6️⃣'
              num3 = ''
           if num == 7:
              num2 = '7️⃣'
              num3 = ''
           if num == 8:
              num2 = '8️⃣'
              num3 = ''
           if num == 9:
              num2 = '9️⃣'
              num3 = ''
           if num == 10:
              num2 = '🔟'
              num3 = ''
           c = Decimal(c6)
           c2 = '{:,}'.format(c).replace(',', '.')

           if user[3] == 'Owner':
             stats = ' ✅<b>РАЗРАБОТЧИК</b>✅ |'
           if user[3] == 'Admin':
             stats = ' ⛔️<b>АДМИН</b>⛔️ |'
           if user[3] == 'Helper_Admin':
             stats = ' ⚠️<b>HELPER АДМИН</b>⚠️ |'
           if user[3] in ['Player', 'Vip', 'Premium', 'Platina', 'Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin']:
             stats = ''

           top_list.append(f"{num2}. {user[1]} |{stats}{num3} ID: <code>{user[0]}</code> |  — {c2}💎 ")

       top = "\n".join(top_list)
       await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, топ 10 игроков бота:\n" + top, parse_mode='html')



async def prodazh_valyte_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    text = f'''
📊<b> Для просмотра курса валют, пропишите:</b> <code>курс</code>
    '''
    await callback.message.edit_text(text, parse_mode='html')
async def ysloviya_cash_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    text = f'''
🌐  <b>УСЛОВИЯ ПОКУПОК В ИГРОВОМ БОТЕ {config.full_bot_name}</b>

<b>❗️ ОПЛАТА С ЮМАНИ И ДРУГИХ БАНКОВ</b>
<i>- Если вы не имеете QIWI, и так же банковскую карточку, тогда по поводу покупки обращайтесь к {config.owner}</i>

❗️<b> ОПЛАТА С УКРАИНЫ 🇺🇦</b>
<i>- Для жителей Украины, которые хотят пополнить свой счёт, прошу обратиться к {config.owner} </i>

<b>❗️ ДРУГИЕ ВАЛЮТЫ</b>
<i>- Если у вас не рубли, а доллары , эвро, грн , злотые, тогда прошу обратиться к {config.owner}</i>
'''

    await callback.message.answer(text, parse_mode='html')


async def oston_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>,  вот список остальных команд ❕

🧮 <code>.cl 2+2</code> - <b>данная команда позволяет считать любые математические примеры</b>
🖼  <code>Ава</code> | <code>Удалить аву</code> - <b>с помощью этой команды можно поставить аватарку на баланс, и так же её удалить </b>
💰 <code>Ограбить банк</code> - <b>команда с помощью какой можно ограбить банк</b>
🎁 <code>Кит-бонусы</code> - <b>выводит информацию за кит бонусы</b>
💭 <code>Рп-команды</code> - <b>команда выводит список доступных рп-команд</b>
🎁 <code>Ежедневный бонус</code> - <b>Позволяет получить ежедневный бонус</b>
💼 <code>промо</code> | <code>+промо</code> - <b>Активация промокодов, создания своего промокода</b>

ℹ️ Что бы использовать команду , напишите команду <b>сообщением </b>
    ''', reply_markup=help_back , parse_mode='html')
async def register_help_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])



    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, Вот информация о боте 🔎

📊 {config.channel} - <b>Игровой канал</b>
💬 {config.chat} - <b>Игровой чат</b>
💬 {config.chat2} - <b>Игровой чат</b>
🧑‍💻 {config.owner} - <b>Разработчик</b>

➖➖➖➖➖➖➖➖➖➖➖

📖 Доступные категории:

📝 <b>Основные</b>
🎮 <b>Игры </b>
🔨 <b>Работы</b>
🏘 <b>Имущество</b>
📖 <b>Привилегии</b>
⛔️ <b>Admins menu </b>
❕ <b>Остальные</b> 
🏰 <b>Организации</b>

➖➖➖➖➖➖➖➖➖➖➖
↘️Выберите одну из доступных <b>категорий </b>
    ''', reply_markup=help2, parse_mode='html')



async def osn2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот список основных команд📝

🕴 <code>Профиль</code> - <b>выводит ваш игровой профиль</b>
🔎 <code>Ник</code>  <b>|</b> <code>Сменить ник</code>  - <b>Выводит ваш ник, и так же его меняет </b>
⚙️ <code>Сменить префикс</code>  <b>|</b> <code>+игроку префикс</code>  - <b>меняет префикс себе, меняет префикс игроку.</b>
👝 <code>Б</code>  <b>|</b> <code>Баланс</code>  - <b>выводит ваш игровой баланс</b>
🏦 <code>Банк</code>  <b>|</b> <code>Банк положить 1</code>  <b>|</b> <code>Банк снять 1</code>  - <b>выводит ваш игровой банк с депозитом , позволяет положить в банк сумму, позволяет снять с банка сумму</b>
🏛 <code>Депозит положить 1</code>  <b>|</b> <code>Депозит снять 1</code>  <b>|</b> <code>Процент снять 1</code>  - <b>Позволяет положить на депозит , позволяет снять с депозита , позволяет снять накапанный процент с депозита </b>
🟣 <code>Эфириум курс</code>  <b>|</b> <code>Эфириум купить 1</code>  <b>|</b> <code>Эфириум продать  1</code>  - <b>Выводит курс эфириума, позволяет купить эфириум, позволяет продать эфириум</b>
💎  <code>Рейтинг</code> <b>|</b> <code>Рейтинг купить 1</code> <b>|</b> <code>Рейтинг продать 1</code> - <b>Выводит ваш игровой рейтинг, позволяет купить рейтинг, позволяет продать рейтинг</b>
🤝 <code>Дать 1</code>  <b>|</b> <code>Передать 1</code>  [ID] - <b>Позволяет передать деньги игроку, позволяет передать деньги игроку по ID</b>
👑 <code>Топ</code>  <b>|</b> <code>Топ б</code>  - <b>Выводит топ по рейтингу игроков, выводит топ по игровому балансу игроков</b>
👮‍♂️ <code>Репорт</code>  - <b>Выводит информацию за систему репортов</b>

ℹ️ Что бы использовать команду , <b>напишите команду сообщением</b>
    ''', reply_markup=help_back , parse_mode='html')



async def admins_menu_up_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    admins_menu = InlineKeyboardMarkup(row_width=2)
    statistic = InlineKeyboardButton(text='Статистика 👥', callback_data='statistic')
    admins_comands = InlineKeyboardButton(text='Админ команды 📝', callback_data='admins_comands')
    admins_menu.add(statistic, admins_comands)
    
    su4 = user_status

    text = f'''
✅ <b>УСПЕШНЫЙ ВХОД В АДМИН МЕНЮ</b>

❗️ Права администратора: <b>{su4}</b>

➖➖➖➖➖➖➖➖➖➖➖➖➖➖
🔐 Категории

<b>👥 Статистика бота</b>
<b>📝 Админ команды</b>

➖➖➖➖➖➖➖➖➖➖➖➖➖➖
↘️ Выбери одну из <b>категорий</b>
    '''
    if user_status == 'Owner':
       await callback.message.edit_text(text, reply_markup=admins_menu , parse_mode='html')
       return

    if user_status == 'Helper_Admin':
       await callback.message.edit_text(text, reply_markup=admins_menu , parse_mode='html')
       return
    if user_status == 'Admin':
       await callback.message.edit_text(text, reply_markup=admins_menu , parse_mode='html')
       return
    else:
       await callback.message.edit_text(f"<a href='tg://user?id={user_id}'>{user_name}</a>,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику <a href='t.me/haeshka_qwe_per/'>Хаешка</a>  ⚠️ ", parse_mode='html')


async def statiskik_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    
    sqlite_select_query = """SELECT * from users"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Admin\""""
    cursor.execute(sqlite_select_query2)
    records2 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Helper_Admin\""""
    cursor.execute(sqlite_select_query2)
    records3 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Owner\""""
    cursor.execute(sqlite_select_query2)
    records4 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from chats"""
    cursor.execute(sqlite_select_query2)
    chats = cursor.fetchall()

    stats222 = InlineKeyboardMarkup(row_width=1)
    ob_statistik2 = InlineKeyboardButton(text='Общая статистика 🔎', callback_data='stats222')
    
    stats222.add(ob_statistik2)

    text = f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот статистика бота  📊

🤵 <b>Игроков:</b> <code>{'{:,}'.format(len(records)).replace(',', '.')}</code>
💬 <b>Чатов: </b><code>{'{:,}'.format(len(chats)).replace(',', '.')}</code>

👨‍⚖️ <b>OWNER:</b> <code>{len(records4)}</code>
👮‍♀️ <b>HELPER-ADMINS:</b> <code>{len(records3)}</code>
🤠 <b>ADMIN:</b> <code>{len(records2)}</code>
    '''
    if user_status == "Admin":
       await callback.message.answer(text,reply_markup=stats222, parse_mode='html')
       return
    if user_status == "Helper_Admin":
       await callback.message.answer(text,reply_markup=stats222, parse_mode='html')
       return

    if user_status == "Owner":
       await callback.message.answer(text,reply_markup=stats222, parse_mode='html')
       return
    else:
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику <a href='t.me/haeshka_qwe_per/'>Хаешка</a>  ⚠️ ", parse_mode='html')


async def ob_Statisyik_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = user_status[0]

    sqlite_select_query21 = """SELECT * from users where user_status = \"Vip\""""
    cursor.execute(sqlite_select_query21)
    vip = cursor.fetchall()

    sqlite_select_query22 = """SELECT * from users where user_status = \"Premium\""""
    cursor.execute(sqlite_select_query22)
    premium = cursor.fetchall()

    sqlite_select_query23 = """SELECT * from users where user_status = \"Platina\""""
    cursor.execute(sqlite_select_query23)
    platina = cursor.fetchall()

    sqlite_select_query24 = """SELECT * from users where user_status = \"Helper\""""
    cursor.execute(sqlite_select_query24)
    helper = cursor.fetchall()

    sqlite_select_query25 = """SELECT * from users where user_status = \"Sponsor\""""
    cursor.execute(sqlite_select_query25)
    sponsor = cursor.fetchall()

    sqlite_select_query26 = """SELECT * from users where user_status = \"Osnovatel\""""
    cursor.execute(sqlite_select_query26)
    osnovatel = cursor.fetchall()

    sqlite_select_query27 = """SELECT * from users where user_status = \"Vladelec\""""
    cursor.execute(sqlite_select_query27)
    vladelec = cursor.fetchall()

    sqlite_select_query28 = """SELECT * from users where user_status = \"Bog\""""
    cursor.execute(sqlite_select_query28)
    bog = cursor.fetchall()

    sqlite_select_query29 = """SELECT * from users where user_status = \"Vlaselin\""""
    cursor.execute(sqlite_select_query29)
    vlaselin = cursor.fetchall()

    sqlite_select_query = """SELECT * from users"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Admin\""""
    cursor.execute(sqlite_select_query2)
    records2 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Helper_Admin\""""
    cursor.execute(sqlite_select_query2)
    records3 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Owner\""""
    cursor.execute(sqlite_select_query2)
    records4 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from family"""
    cursor.execute(sqlite_select_query2)
    all_family = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from user_family"""
    cursor.execute(sqlite_select_query2)
    all_family_users = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from chats"""
    cursor.execute(sqlite_select_query2)
    all_chats = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users WHERE status_block = 'on'"""
    cursor.execute(sqlite_select_query2)
    block_users = cursor.fetchall()

    if user_status in ['Owner', 'Helper_Admin']:
       await callback.message.answer(f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот общая статистика бота 🔎

🔓 <b>Основная</b>
         👤 <b>Игроков:</b> <code>{'{:,}'.format(len(records)).replace(',', '.')}</code>
         🌐 <b>Чатов с ботом:</b> <code>{'{:,}'.format(len(all_chats)).replace(',','.')}</code>

🔰 <b>Привилегии</b>
         ❤️ <b>ВИП:</b> <code>{len(vip)}</code>
         🧡 <b>ПРЕМИУМ:</b> <code>{len(premium)}</code>
         💛 <b>ПЛАТИНА:</b> <code>{len(platina)}</code>
         💚 <b>ХЕЛПЕР:</b> <code>{len(helper)}</code>
         💙 <b>СПОНСОР:</b> <code>{len(sponsor)}</code>
         💜 <b>ОСНОВАТЕЛЬ:</b> <code>{len(osnovatel)}</code>
         🖤 <b>ВЛАДЕЛЕЦ:</b> <code>{len(vladelec)}</code>
         🤍 <b>БОГ:</b> <code>{len(bog)}</code>
         🤎 <b>ВЛАСТЕЛИН:</b> <code>{len(vlaselin)}</code>

🏰 <b>Организации:</b>
        👨‍👩‍👧‍👦 <b>Семьей:</b> <code>{len(all_family)}</code>
        👶 <b>Состоят в семье:</b> <code>{len(all_family_users)}</code>

🛑 <b>Администрация</b>
         💂‍♂️ <b>Заблокированных игроков:</b> <code>{len(block_users)}</code>
         ⛔️ <b>ADMIN:</b> <code>{len(records2)}</code>
         ⚠️ <b>HELPER-ADMIN:</b> <code>{len(records3)}</code>
         ✅ <b>OWNER</b>: <code>{len(records4)}    </code>    
       """, parse_mode='html')
    else:
       await callback.message.answer(f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, статистика бота доступна только от прав администратора \"HELPER-ADMINS\" ", parse_mode='html')



async def admin_commands_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0]) 
    if user_status == 'Owner':
       commands = '''
1️⃣ | Выдать [сумма]
2️⃣ | Забрать [сумма]
3️⃣ | Умножить [количество]
4️⃣ | Обнулить
5️⃣ | /ban
6️⃣ | /unban
7️⃣ |Выдать админа
8️⃣ | Выдать хелпера
9️⃣ | Передать права
🔟 | Забрать права
1️⃣1️⃣ | /reset
1️⃣2️⃣ | /warn
1️⃣3️⃣ | reset_id [ID]
1️⃣4️⃣ | /info
1️⃣5️⃣ | /info_id [ID]
1️⃣6️⃣ | Поделить [количество]
1️⃣7️⃣ | /ban_id [ID]
1️⃣8️⃣ | /unban_id [ID]
1️⃣9️⃣ | /warn_id [ID]
2️⃣0️⃣ | /unwarn_id [ID]
2️⃣1️⃣ | /disconect_database
2️⃣2️⃣ | /chats 
2️⃣3️⃣ | reset promo | очистить промо - очистка всех промокодов
2️⃣4️⃣ | новый курс 1е15 10 10е18 100 100е21 1000
2️⃣5️⃣ | пополнить игроку 100
2️⃣6️⃣ | снять игроку 100
2️⃣7️⃣ | x2donate статус off/on
       '''

    if user_status == 'Helper_Admin':
       commands = '''
1️⃣ | Выдать [сумма]
2️⃣ | Забрать [сумма]
3️⃣ | Умножить [количество]
4️⃣ | Обнулить
5️⃣ | /ban
6️⃣ | /unban
7️⃣ | /warn
8️⃣ | reset_id [ID]
9️⃣ | /info
🔟 | /info_id [ID]
1️⃣1️⃣ | Поделить [количество]
1️⃣2️⃣ | /ban_id [ID]
1️⃣3️⃣ | /unban_id [ID]
1️⃣4️⃣ | /warn_id [ID]
1️⃣5️⃣ | /unwarn_id [ID]
1️⃣6️⃣ | /chats
       '''
    if user_status == 'Admin':
       commands = '''
1️⃣ | Выдать [сумма]
2️⃣ | Забрать [сумма]
3️⃣ | Умножить [количество]
4️⃣ | Обнулить
5️⃣ | /info
6️⃣ | Поделить [количество]
7️⃣ | /chats
       '''
    if user_status == 'Admin':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот список администраторских команд 📝\n{commands}", parse_mode='html')
       return
    if user_status == 'Helper_Admin':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот список администраторских команд 📝\n{commands}", parse_mode='html')
       return
    if user_status == 'Owner':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот список администраторских команд 📝\n{commands}", parse_mode='html')
       return
    else:
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику <a href='t.me/haeshka_qwe_per/'>Хаешка</a>  ⚠️", parse_mode='html')


async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот список игровых команд 📝

🧊 <code>/gamevb</code> | <code>вб</code> - <b>игра на весь баланс, выводит информацию за игру</b>
⚽️ <code>Футбол  1</code> | <code>Фб 1</code> - <b>Азартная игра футбол</b>
🎱 <code>Dice ч 1</code> | <code>Dice к 1</code> | <code>Wheel</code> - <b>Азартная игра , со ставкой на чёрный цвет, ставка на красный цвет, выводит информацию за игру</b>
🤵‍♀️ <code>Казино 1</code> - <b>Азартная игра казино</b>
◾️ <code>Плинко 1</code> -  <b>Азартная игра Плинко</b>
🎰 | <code>Спин 1</code> - <b>Азартная игра Спин</b>
🎲 <code>Кубик 1</code> <b>[до 7]</b> <code>1</code> - <b>Азартная игра Кубик</b>
🎲 <code>Чётное 1</code> | <code>нечётное 1</code> - <b>Азартная игра Чётное нечётное со ставкой на чётное , со ставкой на нечётное</b>
🏎 <code>Гонка 1</code> - <b>Гонки со ставками </b>

ℹ️ Что бы использовать команду , напишите команду <b>сообщением</b>
    ''', reply_markup=help_back , parse_mode='html')


async def rabot2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот список работних команд📝

⛏ <code>Шахта</code> | <code>Купить кирку</code> | <code>Копать руду</code> | <code>Продать</code> <b>[название руды] [количество] - Выводит информацию за шахту, покупка кирки для добычи руды, добыча руды, продажа руды</b>

🌾  <code>Ферма</code> | <code>Купить грабли</code> | <code>Собрать</code> <b>[название урожая]</b> | <code>Продать</code> <b>[название урожая] [количество] - Выводит информацию за ферму, покупка граблей для сбора урожая , сбор урожая , продажа урожая </b>

ℹ️ Что бы использовать команду , напишите команду <b>сообщением</b>
    ''', reply_markup=help_back , parse_mode='html')


async def im2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот все команды на имущество📝

🏠  <code>Дома</code> | <code>Мой дом</code> - <b>Выводит список доступных домов для покупки и так же информацию для покупки, выводит информацию за ваш дом</b>

🕋 <code>Подвалы</code> | <code>Продать подвал</code> - <b>Выводит список доступных подвалов и так информацию за покупки их , позволяет продать подвал</b>

🛠 <code>Крафтить</code> | <code>Система крафта</code> - <b>позволяет крафтить предметы и так далее , выводит информацию за крафт предметов</b>

🚘 <code>Машины</code> | <code>Моя машина</code> - <b>Выводит доступные машины , и так же информацию за покупку их , выводит информацию за вашу машину</b>

🚗 <code>Заправить</code> | <code>Починить</code> - <b>Позволяет вам заправить ваш автомобиль , позволяет его починить [На тех. работах]</b>

ℹ️ Что бы использовать команду , напишите команду <b>сообщением</b>
    ''', reply_markup=help_back , parse_mode='html')


async def priv2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a> , вот все доступные привилегии📝

❤️ <code>ВИП</code> - <b>Выводит список возможностей привилегии ВИП</b>
🧡 <code>ПРЕМИУМ</code> - <b>Выводит список возможностей привилегии ПРЕМИУМ</b>
💛 <code>ПЛАТИНА</code> - <b>Выводит список возможностей привилегии ПЛАТИНА</b>
💚 <code>ХЕЛПЕР</code> - <b>Выводит список возможностей привилегии ХЕЛПЕР</b>
💙 <code>СПОНСОР</code> - <b>Выводит список возможностей привилегии СПОНСОР</b>
💜 <code>ОСНОВАТЕЛЬ</code> - <b>Выводит список возможностей привилегии ОСНОВАТЕЛЬ</b>
🖤 <code>ВЛАДЕЛЕЦ</code> - <b>Выводит список возможностей привилегии ВЛАДЕЛЕЦ</b>
🤍 <code>БОГ</code> - <b>Выводит список возможностей привилегии БОГ</b>
🤎 <code>ВЛАСТЕЛИН</code> - <b>Выводит список возможностей привилегии ВЛАСТЕЛИН</b>

ℹ️ Что бы использовать команду , напишите команду <b>сообщением</b>
    ''', reply_markup=help_back , parse_mode='html')



async def craft_resurs1(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,750):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Zerro ⛏\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(751,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Zerro ⛏\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Кирка Zerro⛏\n🔱 | Уникальность: Х2 Добыча ресурсов", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET pick = "Zerro" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)



async def craft_resurs2(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,750):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Zerro 🌾\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(751,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Zerro 🌾\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Грабли Zerro 🌾\n🔱 | Уникальность: Х2 Добыча ресурсов", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE farm SET rake = "Zerro" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)




async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,900):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Cherick ⛏\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(901,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Cherick ⛏\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Кирка Cherick ⛏\n🔱 | Уникальность: Х2 Добыча ресурсов, Ограничение на время снимаеться на 50%", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET pick = "Cherick" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)


async def resurs4_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,900):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Cherick 🌾\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(901,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Cherick 🌾\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Грабли Cherick 🌾\n🔱 | Уникальность: Х2 Добыча ресурсов, Ограничение на время снимаеться на 50%", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE farm SET rake = "Cherick" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)




async def case_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    case_shop = InlineKeyboardMarkup(row_width=2)
    money_case1 = InlineKeyboardButton(text='💸 Money-Case', callback_data='money_case')
    donate_case2 = InlineKeyboardButton(text='🧧 Donate-Case', callback_data='donate_case')
    case_shop.add(money_case1, donate_case2)

    money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
    money_case = int(money_case[0])

    donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
    donate_case = int(donate_case[0])
    
    ob_members = 0

    if donate_case > 0:
       ob_members += 1
       donate_case2 = f'      🧧 | Donate-Case - {donate_case} шт.\n'
    else:
       donate_case2 = ''

    if money_case > 0:
       ob_members += 1
       money_case2 = f'      💸 | Money-Case - {money_case} шт.\n'
    else:
       money_case2 = ''
   
    if ob_members > 0:
       casee = '🎁 | Ваши кейсы:\n'
    else:
       casee = '😟 | У вас нету кейсов...'

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за кейсы 🎁

💸 | Money-Case - 50 Donate-Coins 🪙
🧧 | Donate-Case - 100 Donate-Coins 🪙

{casee}{money_case2}{donate_case2}

🛒 Чтобы купить\посмотреть информацию, виберите кнопку ниже ⬇️  
    """, reply_markup=case_shop,  parse_mode='html')
 


async def donate_case_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    donate_case_cash = InlineKeyboardMarkup(row_width=2)
    donate_case_cash1 = InlineKeyboardButton(text='🛒 Купить кейс', callback_data='donate_case_cash1')
    donate_case_cash.add(donate_case_cash1)

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за Donate-Case 🧧

ℹ️ | В 1 Donate-Case падает рандомно случайная привилегия!

🛒 Чтобы купить нажмите кнопку ниже 🔽
    """, reply_markup=donate_case_cash,  parse_mode='html')


async def donate_case_cash1_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
    donate_case = int(donate_case[0])

    if donate_coins >= 100:
       await callback.message.answer(f"🧧 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купил 1 Donate-Case", parse_mode='html')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 100} WHERE user_id = {user_id}')
       connect.commit()
       return
    else:
       await callback.message.answer(f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не достаточно Donate-Coins 🪙", parse_mode='html')



async def up_donate_case_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
    donate_case = int(donate_case[0])

    if donate_case < 1:
       await callback.message.answer( f"🆘 | Игрок, у вас нету Донат кейсов", parse_mode='html')
       return
   
    rx = random.randint(0, 935)

    if int(rx) in range(0,500):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>💚 ХЕЛПЕР</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Helper" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ХЕЛПЕР 💚" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(501,750):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>💙 СПОНСОР</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Sponsor" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "СПОНСОР 💙" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(751,850):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>💜 ОСНОВАТЕЛЬ</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Osnovatel" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ОСНОВАТЕЛЬ 💜" WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(851,900):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>🖤 ВЛАДЕЛЕЦ</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Vladelec" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВЛАДЕЛЕЦ 🖤" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(901,925):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>🤍 БОГ</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Bog" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "БОГ 🤍" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(925,935):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>🤎 ВЛАСТЕЛИН</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Vlaselin" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВЛАСТЕЛИН 🤎" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()


async def up_money_case_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
    money_case = int(money_case[0])

    balance = cursor.execute(f'SELECT balance from users where user_id = {user_id}').fetchone()
    balance = int(balance[0])

    if money_case < 1:
       await callback.message.answer( f"🆘 | Игрок, у вас нету Money кейсов", parse_mode='html')
       return
       
    rx = random.randint(0, 100000000000000000000000000000)
    rx2 = '{:,}'.format(rx).replace(',', '.')

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вы открыли Money-Case 💸

🔎 | Результат: {rx2}$    
    """, parse_mode='html')
    cursor.execute(f'UPDATE users SET balance = {balance + rx} WHERE user_id = {user_id}')
    cursor.execute(f'UPDATE user_case SET case_money = {money_case - 1} WHERE user_id = {user_id}')
    connect.commit()


async def money_case_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    money_case_cash = InlineKeyboardMarkup(row_width=2)
    money_case_cash1 = InlineKeyboardButton(text='🛒 Купить кейс', callback_data='money_case_cash1')
    money_case_cash.add(money_case_cash1)

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за Money-Case 💸

ℹ️ | В 1 Money-Case выпадает от 0$ и до 999гугл.

🛒 Чтобы купить нажмите кнопку ниже 🔽
    """, reply_markup=money_case_cash,  parse_mode='html')



async def money_case_cash1_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
    money_case = int(money_case[0])

    if donate_coins >= 50:
       await callback.message.answer(f"💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купил 1 Money-Case", parse_mode='html')
       cursor.execute(f'UPDATE user_case SET case_money = {money_case + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 50} WHERE user_id = {user_id}')
       connect.commit()
       return
    else:
       await callback.message.answer(f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не достаточно Donate-Coins 🪙", parse_mode='html')


async def privilegii_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    privilegii_inline = InlineKeyboardMarkup(row_width=3)
    vip = InlineKeyboardButton(text='❤️ ВИП ', callback_data='vip')
    premium = InlineKeyboardButton(text='🧡 ПРЕМИУМ', callback_data='premium')
    platina = InlineKeyboardButton(text='💛 ПЛАТИНА', callback_data='platina')
    helper = InlineKeyboardButton(text='💚 ХЕЛПЕР', callback_data='helper')
    sponsor = InlineKeyboardButton(text='💙 СПОНСОР', callback_data='sponsor')
    osnovatel = InlineKeyboardButton(text='💜 ОСНОВАТЕЛЬ', callback_data='osnovatel')
    vladelec = InlineKeyboardButton(text='🖤 ВЛАДЕЛЕЦ', callback_data='vladelec')
    bog = InlineKeyboardButton(text='🤍 БОГ', callback_data='bog')
    vlastelin = InlineKeyboardButton(text='🤎 ВЛАСТЕЛИН', callback_data='vlastelin')
    privilegii_inline.add(vip, premium, platina, helper, sponsor, osnovatel, vladelec, bog, vlastelin)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот все доступные привилегии📝

❤️ | ВИП - 10 Donate-coins 🪙
🧡 | ПРЕМИУМ - 30 Donate-coins 🪙
💛 | ПЛАТИНА - 50 Donate-coins 🪙
💚 | ХЕЛПЕР - 100 Donate-coins 🪙
💙 | СПОНСОР - 155 Donate-coins 🪙
💜 | ОСНОВАТЕЛЬ - 170 Donate-coins 🪙
🖤 | ВЛАДЕЛЕЦ - 250  Donate-coins 🪙
🤍 | БОГ - 300 Donate-coins 🪙
🤎 | ВЛАСТЕЛИН - 350 Donate-coins 🪙

🛒 Чтобы купить привилегию , виберите её ниже
ℹ️ Чтобы посмотреть возможности привилегий , виберите привилегию ниже   
    """, reply_markup=privilegii_inline,  parse_mode='html')


async def vip_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    vip_menu = InlineKeyboardMarkup(row_width=1)
    cash_vip = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_vip')
    
    vip_menu.add(cash_vip)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ВИП ❤️

🛒 | При покупке:
        1️⃣ | Бонус-кит ВИП
        2️⃣ | Префикс ВИП
        3️⃣ | 250.000$

🎁 | При использовании Donate-Case:
       1️⃣ | Бонус-кит ВИП
       2️⃣ | Префикс ВИП

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=vip_menu,  parse_mode='html')



async def cash_vip_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 10:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ВИП", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Vip" where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 100} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 10000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВИП ❤️" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 10} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def premium_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    premium_menu = InlineKeyboardMarkup(row_width=1)
    cash_premium = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_premium')
    
    premium_menu.add(cash_premium)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ПРЕМИУМ 🧡

🛒 | При покупке:
        1️⃣ | Бонус-кит ПРЕМИУМ
        2️⃣ | Префикс ПРЕМИУМ
        3️⃣ | 300.000$

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ПРЕМИУМ
        2️⃣ | Префикс ПРЕМИУМ

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=premium_menu,  parse_mode='html')



async def cash_premium_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 30:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ПРЕМИУМ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Premium" where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 300} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 100000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ПРЕМИУМ 🧡" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 30} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def platina_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    platina_menu = InlineKeyboardMarkup(row_width=1)
    cash_platina = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_platina')
    
    platina_menu.add(cash_platina)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ПЛАТИНА 💛

🛒 | При покупке:
        1️⃣ | Бонус-кит ПЛАТИНА
        2️⃣ | Префикс ПЛАТИНА
        3️⃣ | 550.000$
        4️⃣ | 10 Рейтинга
        5️⃣ | Money-case 1 шт.

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ПЛАТИНА
        2️⃣ | Префикс ПЛАТИНА

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=platina_menu,  parse_mode='html')




async def cash_platina_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 50:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ПЛАТИНА", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Platina" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 800} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 400000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ПЛАТИНА 💛" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 50} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def helper_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    helper_menu = InlineKeyboardMarkup(row_width=1)
    cash_helper = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_helper')
    
    helper_menu.add(cash_helper)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ХЕЛПЕР 💚

🛒 | При покупке:
        1️⃣ | Бонус-кит ХЕЛПЕР
        2️⃣ | Префикс ХЕЛПЕР
        3️⃣ | 750.000$
        4️⃣ | 20 Рейтинга
        5️⃣ | Money-case 3 шт.
        6️⃣ | Способность менять себе префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ХЕЛПЕР
        2️⃣ | Префикс ХЕЛПЕР
        3⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=helper_menu,  parse_mode='html')



async def cash_helper_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 100:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ХЕЛПЕР", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Helper" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 3} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 1300} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 700000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ХЕЛПЕР 💚" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 100} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def sponsor_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    sponsor_menu = InlineKeyboardMarkup(row_width=1)
    cash_sponsor = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_sponsor')
    
    sponsor_menu.add(cash_sponsor)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию СПОНСОР 💙

🛒 | При покупке:
        1️⃣ | Бонус-кит СПОНСОР
        2️⃣ | Префикс СПОНСОР
        3️⃣ | 3.000.000$
        4️⃣ | 25 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Способность менять себе префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит СПОНСОР
        2️⃣ | Префикс СПОНСОР
        3⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=sponsor_menu,  parse_mode='html')




async def cash_sponsor_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 155:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию СПОНСОР", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Sponsor" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 10000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 5000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "СПОНСОР 💙" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 155} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def osnovatel_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    osnovatel_menu = InlineKeyboardMarkup(row_width=1)
    cash_osnovatel = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_osnovatel')
    
    osnovatel_menu.add(cash_osnovatel)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ОСНОВАТЕЛЬ 💜

🛒 | При покупке:
        1️⃣ | Бонус-кит ОСНОВАТЕЛЬ
        2️⃣ | Префикс ОСНОВАТЕЛЬ
        3️⃣ | 4.000.000$
        4️⃣ | 54 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ОСНОВАТЕЛЬ
        2️⃣ | Префикс ОСНОВАТЕЛЬ
        3⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=osnovatel_menu,  parse_mode='html')



async def cash_osnovatel_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 170:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ОСНОВАТЕЛЬ ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Osnovatel" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 100000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 20000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ОСНОВАТЕЛЬ 💜" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 170} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def vladelec_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    vladelec_menu = InlineKeyboardMarkup(row_width=1)
    cash_vladelec = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_vladelec')
    
    vladelec_menu.add(cash_vladelec)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> ,  вот данные за привилегию ВЛАДЕЛЕЦ 🖤

🛒 | При покупке:
        1️⃣ | Бонус-кит ВЛАДЕЛЕЦ
        2️⃣ | Префикс ВЛАДЕЛЕЦ
        3️⃣ | 10.000.000$
        4️⃣ | 74 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс
        8️⃣ | Способность менять игрокам префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ВЛАДЕЛЕЦ
        2️⃣ | Префикс ВЛАДЕЛЕЦ
        3⃣ | Способность менять себе префикс
        4⃣ | Способность менять игрокам префикс

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=vladelec_menu,  parse_mode='html')




async def cash_vladelec_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])

    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 250:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ВЛАДЕЛЕЦ  ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Vladelec" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 1000000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 100000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВЛАДЕЛЕЦ 🖤" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 250} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def bog_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    bog_menu = InlineKeyboardMarkup(row_width=1)
    cash_bog = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_bog')
    
    bog_menu.add(cash_bog)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию БОГ 🤍

🛒 | При покупке:
        1️⃣ | Бонус-кит БОГ
        2️⃣ | Префикс БОГ
        3️⃣ | 25.000.000$
        4️⃣ | 100 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс
        8️⃣ | Способность менять игрокам префикс
        9️⃣ | Ограничение на время в играх становиться 2 секунды

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит БОГ
        2️⃣ | Префикс БОГ
        3⃣ | Способность менять себе префикс
        4⃣ | Способность менять игрокам префикс
        5⃣ | Ограничение на время в играх становиться 2 секунды

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=bog_menu,  parse_mode='html')



async def cash_bog_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])

    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 300:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию БОГ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Bog" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 10000000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 500000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "БОГ 🤍" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 300} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def vlastelin_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    vlaselin_menu = InlineKeyboardMarkup(row_width=1)
    cash_vlaselin = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_vlaselin')
    
    vlaselin_menu.add(cash_vlaselin)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ВЛАСТЕЛИН 🤎

🛒 | При покупке:
        1️⃣ | Бонус-кит ВЛАСТЕЛИН
        2️⃣ | Префикс ВЛАСТЕЛИН
        3️⃣ | 50.000.000$
        4️⃣ | 150 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс
        8️⃣ | Способность менять игрокам префикс
        9️⃣ | Ограничение на время в играх становиться 2 секунды

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ВЛАСТЕЛИН
        2️⃣ | Префикс ВЛАСТЕЛИН
        3⃣ | Способность менять себе префикс
        4⃣ | Способность менять игрокам префикс
        5⃣ | Ограничение на время в играх становиться 2 секунды

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=vlaselin_menu,  parse_mode='html')



async def cash_vlastelin_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])

    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 300:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ВЛАСТЕЛИН ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Vlaselin" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 10000000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 500000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВЛАСТЕЛИН 🤎" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 300} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def adms_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    admins_menu_cash = InlineKeyboardMarkup(row_width=2)
    admins_cash = InlineKeyboardButton(text='⛔️ ADMIN', callback_data='admins_cash')
    helper_admins_cash = InlineKeyboardButton(text='⛔️ HELPER-ADMIN', callback_data='helper_admins_cash')
    owner_cash = InlineKeyboardButton(text='⛔️ OWNER', callback_data='owner_cash')
    admins_menu_cash.add(admins_cash, helper_admins_cash, owner_cash)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за статусы администраторов⛔️

1️⃣ | ADMIN - 400Р
4️⃣ | HELPER-ADMIN - 1.500Р
5️⃣ | OWNER - 5.000Р

↘️ Чтобы посмотреть возможности , виберите статус ниже   
    """,reply_markup=admins_menu_cash,  parse_mode='html' )
  


async def admins_cash_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ADMIN ⛔️

1️⃣ | Выдача валюты
2️⃣ | Отбор валюты
3️⃣ | Умножение валюты
4️⃣ | Обнуление
5️⃣ | Просмотр профиля игрока
6️⃣ | Поделить баланс
7️⃣ | Просмотр список зарегистрированный чатов 

🛒 Для покупки администраторских прав , обратитесь к Владельцу бота - <a href='t.me/haeshka_qwe_per/'>Хаешка</a> 
    """,  parse_mode='html' )


async def helper_admins_cash_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за HELPER-ADMIN ⛔️

1️⃣ | Выдача валюты
2️⃣ | Отбор валюты
3️⃣ | Умножение валюты
4️⃣ | Обнуление
5️⃣ | Выдача бана
6️⃣ | Выдача разбана
7️⃣ | Поделить баланс
8️⃣ | Просмотр профила 
9️⃣ | Просмотр профиля по ID 
🔟 | Выдача варна 
1️⃣1️⃣ | Отбор варна
1️⃣2️⃣ | Выдача бана по ID
1️⃣3️⃣ | Выдача разбана по ID
1️⃣4️⃣ | Выдача варна по ID
1️⃣5️⃣ | Отбор варна по ID
1️⃣6️⃣ | Обнуление по ID
1️⃣7️⃣ | ДОСТУП К КОНСОЛИ БОТА
1️⃣8️⃣ | ДОСТУП К РЕПОРТАМ
1️⃣9️⃣ | Просмотр список зарегистрированный чатов 

🛒 Для покупки администраторских прав , обратитесь к Владельцу бота - <a href='t.me/haeshka_qwe_per/'>Хаешка</a> 
    """,  parse_mode='html' )



async def owner_cash_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за OWNER ⛔️

1️⃣ | Выдача валюты
2️⃣ | Отбор валюты
3️⃣ | Умножение валюты
4️⃣ | Обнуление
5️⃣ | Выдача бана
6️⃣ | Выдача разбана
7️⃣ |Поделить баланс
8️⃣ | Выдача прав администратора "ADMIN"
9️⃣ | Выдача прав администратора "HELPER-ADMIN"
🔟 | Выдача Donate-Coins
1️⃣1️⃣ | МАССОВОЕ ОБНУЛЕНИЕ
1️⃣2️⃣ | Выдача бана по ID
1️⃣3️⃣ | Выдача разбана по ID
1️⃣4️⃣ | Выдача варна
1️⃣5️⃣ | Отбор варна 
1️⃣6️⃣ | Выдача варна по ID
1️⃣7️⃣ | Отбор варна по ID
1️⃣8️⃣ | Возможность посмотреть профиль игрока
1️⃣9️⃣ | Возможность посмотреть профиль игрока по ID
2️⃣0️⃣ | Возможность выдать права администратора "OWNER"
2️⃣1️⃣ | ДОСТУП К КОНСОЛИ БОТА
2️⃣2️⃣ | ДОСТУП К РЕПОРТАМ
2️⃣3️⃣ | ВОЗМОЖНОСТЬ УДАЛЯТЬ ИГРОКОВ С БАЗЫ ДАННЫХ
2️⃣4️⃣ | Просмотр список зарегистрированный чатов

🛒 Для покупки администраторских прав , обратитесь к Владельцу бота - <a href="t.me/haeshka_qwe_per/">Хаешка</a>
    """,  parse_mode='html' )



async def channel_proverk_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
   balance = int(balance[0])
   user_channel_status = await bot.get_chat_member(chat_id="@qwechannel", user_id=callback.from_user.id)

   channel_pov = cursor.execute("SELECT members from channel_pov where user_id = ?", (callback.from_user.id,)).fetchone()
   channel_pov = int(channel_pov[0])

   if channel_pov > 0:
      await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы уже получили деньги за подписку", parse_mode='html')
      return

   if user_channel_status['status'] != 'left':
      await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно подписались на канал ✅", parse_mode='html')
      await callback.message.answer( f"💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили приз в размере  500.000.000.000.000.000$", parse_mode='html')
      cursor.execute(f'UPDATE channel_pov SET members = {1} WHERE user_id = {user_id}')
      cursor.execute(f'UPDATE users SET balance = {balance + 500000000000000000} WHERE user_id = {user_id}')
      connect.commit()
   else:
      await callback.message.answer( f"❌ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не подписались на канал, попробуйте снова", parse_mode='html')



async def ava_strach_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"СТРАЖ\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "strach" WHERE user_id = {user_id}')
   connect.commit()


async def ava_cheat_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"ЧИТЕР\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "cheat" WHERE user_id = {user_id}')
   connect.commit()



async def ava_apper_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"АППЕР\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "apper" WHERE user_id = {user_id}')
   connect.commit()



async def ava_dyp_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"ДЮППЕР\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "dyp" WHERE user_id = {user_id}')
   connect.commit()



async def ava_girl_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"ДЕВУШКА\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "girl" WHERE user_id = {user_id}')
   connect.commit()


async def ava_admin_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_status = str(user_status[0])

   if user_status in ['Admin', 'Helper_Admin', 'Owner']:
      await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"АДМИН\"", parse_mode='html')
      cursor.execute(f'UPDATE avatarka SET avatarka = "admin" WHERE user_id = {user_id}')
      connect.commit()
      return
   else:
      await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику <a href='t.me/haeshka_qwe_per/'>Хаешка</a>  ⚠️", parse_mode='html')



async def gamevb_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
   balance = int(balance[0])

   game = cursor.execute("SELECT game from users where user_id = ?",(callback.from_user.id,)).fetchone()
   game = int(game[0])

   balance2 = '{:,}'.format(balance).replace(',', '.')


   rx = random.randint(0, 10000)

   period = 5
   get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
   last_stavka = f"{int(get[0])}"
   stavkatime = time.time() - float(last_stavka)
   if stavkatime > period:
      if balance > 0:
         if int(rx) in range(0, 7000):
            i = balance - balance * 0.1
            i2 = int(i)
            i3 = '{:,}'.format(i2).replace(',', '.')
            await callback.message.answer(  f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🧊 | Игра: GAME-VB
🎟 | Ставка: {balance2}$
🧾 | Проигрыш: {i3}$ [0.1X]            
""", parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
            connect.commit()
            return
         if int(rx) in range(7001, 10000):
            i = balance * 1.5
            i2 = int(i)
            i3 = '{:,}'.format(i2).replace(',', '.')
            await callback.message.answer( f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🧊 | Игра: GAME-VB
🎟 | Ставка: {balance2}$
🧾 | Выигрыш: {i3}$ [1.5X]            
""", parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
            connect.commit()
            return
      else:
         await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас недостаточно средств! ", parse_mode='html')
   else:
      await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд", parse_mode='html')         




async def new_chat_content_types(message):
    user = message.new_chat_members[0].username
    user_id = message.new_chat_members[0].id
    user_name = message.new_chat_members[0].first_name
    group_name = message.chat.full_name
    status_bot = message.new_chat_members[0].is_bot

    welcome_photo = open('Photo/welcome.jpg', 'rb')

    if user == config.bot_name:

        chat_id = message.chat.id
        cursor.execute(f"SELECT chat_id FROM chats WHERE chat_id = '{chat_id}'")

        if cursor.fetchone() is None:
            text = f'''
        💭 <code>{user_name}</code> , вы <b>успешно зарегистрировали</b> чат <code>{group_name}</code> 
            '''
            time_register = f'{datetime.now()}'
            photo_new_chat = open('Photo/newchat.jpg', 'rb')
            cursor.execute("INSERT INTO chats VALUES(?, ?, ?);", (chat_id, group_name, time_register[:19]))
            connect.commit()

            await message.answer(text, parse_mode='html')
        else:
            pass

        text = f'''
🎯Я игровой бот <b>{config.full_bot_name}</b> 
🙏 Спасибо что <b>добавили меня</b> в чат <code>{group_name}</code> | Вы можете его <b>зарегистрировать чат в боте</b> командой <code>/register_chat</code>
❗️ Для того чтобы я работал в вашем чате, мне нужны <b>права администратора</b>
        '''
    elif status_bot == True:
        text = f'''
❗️ В чат <b>добавили бота</b> <code><a href='tg://user?id={user_id}'>{user_name}</a></code>
➖➖➖➖➖➖➖➖➖➖➖➖
🔎 <b>АЙДИ :</b> <code>{user_id}</code>
🧷 <b>ЮЗЕР :</b> <b>@{user}</b>
👤 <b>ИМЯ :</b> <code>{user_name}</code>
        '''
    else:       

        msg = message
        user_name1 = 'Игрок'
        user_status = "Player"
        status_block = 'off'
        stats_status = 'off'
        pref = 'Игрок'
        status_console = 'off'
        avatarka_start = 'none'
        klan_index = 0
        status_family = 0
        result = time.localtime()

        if int(result.tm_mon) <= 9:
            p = "0"
        else:
            p = ''
        if int(result.tm_mday) <= 9:
            m = "0"
        else:
            m = ''
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
        times = f'{m}{result.tm_mday}.{p}{result.tm_mon}.{result.tm_year} | {h}{result.tm_hour}:{min}{result.tm_min}:{s}{result.tm_sec}'
        times2 = str(times)

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
        if cursor.fetchone() is None:
            photo_welcome = open('Photo/welcome.jpg', 'rb')
            cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, user_name1, user_name, user_status, config.start_money, 0, 0, 0, status_block, times2, pref, 0, 0, 0, 0, stats_status))
            cursor.execute("INSERT INTO mine VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(user_id, user_name,status_block, 0, 0, 0, 0, 0))
            cursor.execute("INSERT INTO farm VALUES(?, ?, ?, ?, ?);",(user_id, user_name,status_block, 0, 0))
            cursor.execute("INSERT INTO house VALUES(?, ?, ?, ?);",(user_id, user_name, 0, 0))
            cursor.execute("INSERT INTO cars VALUES(?, ?, ?, ?, ?);",(user_id, user_name, 0, 0, 0))
            cursor.execute("INSERT INTO user_case VALUES(?, ?, ?);",(user_id, 0, 0))
            cursor.execute("INSERT INTO bot_time VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, 0, 0, 0, 0, 0, 0, 0, 0))
            cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
            cursor.execute("INSERT INTO time_bank VALUES(?, ?);",(user_id, 0))
            cursor.execute("INSERT INTO ob_time VALUES(?, ?);",(user_id, 0))
            cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
            cursor.execute("INSERT INTO console VALUES(?, ?);",(user_id, status_console))
            cursor.execute("INSERT INTO time_prefix VALUES(?, ?);",(user_id, 0))
            cursor.execute("INSERT INTO time_sms VALUES(?, ?);",(user_id, 0))
            cursor.execute("INSERT INTO channel_pov VALUES(?, ?);",(user_id, 0))
            cursor.execute("INSERT INTO avatarka VALUES(?, ?);",(user_id, avatarka_start))
            cursor.execute("INSERT INTO reput VALUES(?, ?);",(user_id, 0))
            cursor.execute("INSERT INTO h_module VALUES(?, ?);",(user_id, 0))
            connect.commit()

            print(f'Зарегестрировался в боте пользователь: {user_name}')
        else:
            pass
            
        chat_id = message.chat.id
        print(chat_id)
        if chat_id == config.chat_id:

            status_wdzy = cursor.execute(f'SELECT status from wdzy').fetchone()
            status_wdzy = status_wdzy[0]

            if status_wdzy == 'on':
                summ_wdzy = cursor.execute(f'SELECT summ from wdzy').fetchone()
                summ_wdzy = int(summ_wdzy[0])

                left_user_id = message.from_user.id
                
                if left_user_id == user_id:
                    return

                left_balance = cursor.execute(f'SELECT balance from users where user_id = {left_user_id}').fetchone()
                left_balance = int(left_balance[0])

                left_user_name = cursor.execute(f'SELECT user_name from users where user_id = {left_user_id}').fetchone()
                left_user_name = str(left_user_name[0])

                cursor.execute(f'UPDATE users SET balance = {left_balance + summ_wdzy} where user_id = {left_user_id}')
                connect.commit()
                
                text = f'''
🎁 {left_user_name} вы получили <code>{'{:,}'.format(summ_wdzy).replace(',','.')}$</code> за <b>добавление участника </b>
                '''
                
                try:
                    await message.bot.send_message(left_user_id, text, parse_mode='html')
                except:
                    pass

            else:
                pass
        else:
            pass

        text = f'''
👋 <b>Добро пожаловать <a href='tg://user?id={user_id}'>{user_name}</a> в чат</b> <code>{group_name}</code>
    '''

    await message.answer(text, parse_mode='html')


