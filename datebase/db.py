import sqlite3

connect = sqlite3.connect("datebase/users.db")
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS bill_chek(
user_id INT,
money INT,
bill_id TEXT
)
""")


cursor.execute("""CREATE TABLE IF NOT EXISTS money_balance(
money INT,
user_id INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS x2donate(
status TEXT
)
""")


cursor.execute("""CREATE TABLE IF NOT EXISTS course(
money1 INT,
cash_money1 INT,
money2 INT,
cash_money2 INT,
money3 INT,
cash_money3 INT
)
""")


cursor.execute("""CREATE TABLE IF NOT EXISTS user_family(
user_name STRING,
user_id INT,
family STRING,
rank INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS family_id(
id INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS family(
name STRING,
owner_id INT,
owner_name STRING,
id INT,
balance INT,
opis STRING,
time_name INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS users( 
user_id BIGINT,
user_name STRING,
user_tg_name STRING,
user_status STRING,
balance INT,
bank BIGINT,
ethereum INT,
 rating INT,
status_block STRING,
time_register INT,
pref STRING,
donate_coins INT,
game INT,
bank2 INT,
depozit INT,
stats_status STRING
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS wdzy(
summ INT,
status STRING
)
""")


cursor.execute("""CREATE TABLE IF NOT EXISTS cash_money(
number1 STRING,
summ1 INT,
number2 STRING,
summ2 INT,
number3 STRING,
summ3 INT
)
""")


cursor.execute("""CREATE TABLE IF NOT EXISTS promo(
    promo STRING,
    status STRING,
    owner STRING,
    priz BIGINT,
    active INT,
    ob_active INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS promo_active(
    user_id INT,
    promo STRING,
    active INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS chats(
    chat_id INT,
    chat_name STRING,
    time_register STRING
)
""")


cursor.execute("""CREATE TABLE IF NOT EXISTS mine(
    user_id INT,
    user_name STRING,
    pick STRING,
    iron INT,
    metall INT,
    silver INT,
    bronza INT,
    gold INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS user_case(
    user_id INT,
    case_money INT,
    case_donate INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS farm(
    user_id INT,
    user_name STRING,
    rake STRING,
    linen INT,
    cotton INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS house(
    user_id INT,
    user_name STRING,
    house INT,
    basement INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS cars(
    user_id INT,
    user_name STRING,
    cars INT,
    hp INT,
    benz INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS bot_time(
    user_id INT,
    stavka_games INT,
    stavka_bank INT,
    stavka_bonus INT,
    stavka_depozit INT,
    time_pick INT,
    time_rake INT,
    time_craft INT,
    time_kit INT
)
""")


cursor.execute("""CREATE TABLE IF NOT EXISTS time_bank(
    user_id INT,
    stavka INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS ob_time(
    user_id INT,
    stavka INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS time_prefix(
    user_id INT,
    stavka INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS time_sms(
    user_id INT,
    stavka INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS warn(
    user_id INT,
    warn INT 
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS console(
    user_id INT,
    status STRING 
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS channel_pov(
    user_id INT,
    members INT   
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS avatarka(
    user_id INT,
    avatarka STRING   
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS reput(
    user_id INT,
    reput INT   
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS h_module(
    user_id INT,
    h_status INT   
)
""")

async def add_cuorse(money1, cash_money1, money2, cash_money2, money3, cash_money3):
    cursor.execute(f'UPDATE course SET money1 = "{money1}"')
    cursor.execute(f'UPDATE course SET money2 = "{money2}"')
    cursor.execute(f'UPDATE course SET money3 = "{money3}"')

    cursor.execute(f'UPDATE course SET cash_money1 = "{cash_money1}"')
    cursor.execute(f'UPDATE course SET cash_money2 = "{cash_money2}"')
    cursor.execute(f'UPDATE course SET cash_money3 = "{cash_money3}"')

    connect.commit()

async def get_check(bill_id):
    cursor.execute(f'SELECT * from bill_chek where bill_id = "{bill_id}"')
    result = cursor.fetchone()
    connect.commit()

    if result is None:
        return False
    else:
        return result

async def update_status_x2donate(status):
    cursor.execute(f'UPDATE x2donate SET status = "{status}"')
    connect.commit()

async def status_x2donate():
    cursor.execute(f'SELECT status from x2donate')
    text = cursor.fetchone()
    connect.commit()

    return str(text[0])

async def get_x2donate():
    cursor.execute('SELECT status from x2donate')
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO x2donate VALUES(?);", ('off',))
        connect.commit()
    else:
        pass

async def get_course():
    cursor.execute('SELECT money1 from course')
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO course VALUES(?, ?, ?, ?, ?, ?);", (1000000000000, 50, 1000000000000000, 100, 1000000000000000000, 200))
        connect.commit()
    else:
        pass

async def delete_check(bill_id):
    cursor.execute(f'DELETE FROM bill_chek WHERE bill_id = "{bill_id}"')
    connect.commit()

async def register_money(user_id):
    cursor.execute("INSERT INTO money_balance VALUES(?, ?);", (0, user_id))
    connect.commit()

async def add_check(user_id, money, bill_id):
    cursor.execute("INSERT INTO bill_chek VALUES(?, ?, ?);", (user_id, money, bill_id))
    connect.commit()

async def course_cash_money3():
    cursor.execute(f'SELECT cash_money3 from course')
    number = cursor.fetchone()
    connect.commit()

    return int(number[0])

async def course_cash_money2():
    cursor.execute(f'SELECT cash_money2 from course')
    number = cursor.fetchone()
    connect.commit()

    return int(number[0])

async def course_cash_money1():
    cursor.execute(f'SELECT cash_money1 from course')
    number = cursor.fetchone()
    connect.commit()

    return int(number[0])

async def course_money3():
    cursor.execute(f'SELECT money3 from course')
    number = cursor.fetchone()
    connect.commit()

    return int(number[0])

async def course_money2():
    cursor.execute(f'SELECT money2 from course')
    number = cursor.fetchone()
    connect.commit()

    return int(number[0])

async def course_money1():
    cursor.execute(f'SELECT money1 from course')
    number = cursor.fetchone()
    connect.commit()

    return int(number[0])

async def user_donate(user_id):
    cursor.execute(f'SELECT donate_coins from users where user_id = {user_id}')
    balance = cursor.fetchone()
    connect.commit()

    return int(balance[0])

async def user_balance(user_id):
    cursor.execute(f'SELECT balance from users where user_id = {user_id}')
    balance = cursor.fetchone()
    connect.commit()

    return int(balance[0])

async def user_money(user_id):
    cursor.execute(f'SELECT money from money_balance where user_id = {user_id}')
    money = cursor.fetchone()
    connect.commit()

    return int(money[0])

async def update_balance(user_id, number):
    cursor.execute(f'UPDATE users SET balance = "{number}" WHERE user_id = {user_id}')
    connect.commit()

async def update_donate(user_id, number):
    cursor.execute(f'UPDATE users SET donate_coins = "{number}" WHERE user_id = {user_id}')
    connect.commit()

async def update_money(user_id, money):
    cursor.execute(f'UPDATE money_balance SET money = "{money}" WHERE user_id = {user_id}')
    connect.commit()

