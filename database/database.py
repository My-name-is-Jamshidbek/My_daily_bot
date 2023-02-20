import sqlite3
from datetime import datetime
from config import DATABASE_NAME
import datetime as dt

# Foydalanuvchilar jadvalini yaratish uchun funksiya
def create_users_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE users
                 (phone_number INTEGER, telegram_id INTEGER, join_time TEXT)''')
    conn.commit()
    conn.close()

# Yangi foydalanuvchini jadvalga qo'shish uchun funksiya
def add_user(phone_number, telegram_id):
    join_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (phone_number, telegram_id, join_time))
    conn.commit()
    conn.close()

# Foydalanuvchilar sonini qaytarish uchun funksiya
def count_users():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count

# Foydalanuvchilar telegram IDlarini list shaklida qaytarish uchun funksiya
def get_all_telegram_ids():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT telegram_id FROM users")
    telegram_ids = [row[0] for row in c.fetchall()]
    conn.close()
    return telegram_ids


def create_rejalar_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rejalar
                (telegram_id INTEGER, reja_nomi TEXT, reja_tavsifi TEXT,
                 reja_mojallangan_vaqt TEXT, ajratilgan_vaqt INTEGER,
                 yil INTEGER, oy INTEGER, kun INTEGER, soat INTEGER, daqiqa INTEGER)''')
    conn.commit()
    conn.close()

def add_reja(telegram_id, reja_nomi, reja_tavsifi, reja_mojallangan_vaqt, ajratilgan_vaqt, yil, oy, kun, soat, daqiqa):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO rejalar VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (telegram_id, reja_nomi, reja_tavsifi, reja_mojallangan_vaqt, ajratilgan_vaqt, yil, oy, kun, soat, daqiqa))
    conn.commit()
    conn.close()

def get_rejalarni_korish(telegram_id, yil, oy, kun):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT reja_nomi FROM rejalar WHERE telegram_id=? AND yil=? AND oy=? AND kun=?",
              (telegram_id, yil, oy, kun))
    rejalarni_korish = c.fetchall()
    conn.close()
    rr = []
    for i in rejalarni_korish:rr.append(i[0])
    return rr

def get_reja_malumotlari(telegram_id, yil, oy, kun, reja_nomi):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT reja_nomi, reja_tavsifi, reja_mojallangan_vaqt, ajratilgan_vaqt, yil, oy, kun, soat, daqiqa FROM rejalar WHERE telegram_id=? AND yil=? AND oy=? AND kun=? AND reja_nomi=?",
              (telegram_id, yil, oy, kun, reja_nomi))
    reja_malumotlari = c.fetchone()
    conn.close()
    return reja_malumotlari

def delete_reja(telegram_id, yil, oy, kun, reja_nomi):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM rejalar WHERE telegram_id=? AND yil=? AND oy=? AND kun=? AND reja_nomi=?",
              (telegram_id, yil, oy, kun, reja_nomi))
    conn.commit()
    conn.close()


def get_date_by_day_of_week(day_of_week):
    days_of_week = ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba']
    today = dt.datetime.today()
    try:
        day_of_week_index = days_of_week.index(day_of_week)
        t = True
    except:
        return False, 0, 0, 0
    days_until_day_of_week = (day_of_week_index - today.weekday()) % 7
    target_date = today + dt.timedelta(days=days_until_day_of_week)
    return t, target_date.year, target_date.month, target_date.day


