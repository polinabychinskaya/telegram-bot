import sqlite3 as sq

db = sq.connect('tg.db')
cur = db.cursor()

async def db_start():
    cur.execute('CREATE TABLE IF NOT EXISTS items('
                'i_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'name TEXT,'
                'phone TEXT,'
                'items TEXT,'
                'time TEXT,'
                'delivery TEXT,'
                'pay TEXT,'
                'wrap TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS goods('
                'i_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'good_name TEXT,'
                'good_desc TEXT,'
                'good_price TEXT,'
                'good_photo TEXT,'
                'good_category TEXT)')
    db.commit()

async def add_order(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO items (name, phone, items, time, delivery, pay, wrap) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (data['name'], data['phone'], data['items'], data['time'], data['delivery'], data['pay'], data['wrap']))
        db.commit()

async def add_good(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO goods (good_name, good_desc, good_price, good_photo, good_category) VALUES (?, ?, ?, ?, ?)',
                    (data['good_name'], data['good_desc'], data['good_price'], data['good_photo'], data['good_type']))
        db.commit()



