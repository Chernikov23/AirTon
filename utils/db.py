import sqlite3

# Имя файла базы данных
db_name = 'user_data.db'

def init_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        tgid INTEGER NOT NULL UNIQUE,
        referral_link TEXT NOT NULL,
        invited_users_count INTEGER DEFAULT 0
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS balance (
        id INTEGER PRIMARY KEY,
        amount INTEGER NOT NULL
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS referrals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referrer_id INTEGER NOT NULL,
        referred_id INTEGER NOT NULL,
        UNIQUE(referrer_id, referred_id)
    );
    ''')
    # Инициализируем баланс, если он еще не был установлен
    cursor.execute('SELECT * FROM balance WHERE id = 1')
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO balance (id, amount) VALUES (1, 100000)')
    conn.commit()
    conn.close()

def add_user(username, tgid, referral_link):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (username, tgid, referral_link, invited_users_count)
    VALUES (?, ?, ?, ?)
    ''', (username, tgid, referral_link, 0))
    conn.commit()
    conn.close()

def user_exists(tgid):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE tgid = ?', (tgid,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def get_user_by_tgid(tgid):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE tgid = ?', (tgid,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_balance():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT amount FROM balance WHERE id = 1')
    balance = cursor.fetchone()[0]
    conn.close()
    return balance

def decrease_balance(amount=1):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('UPDATE balance SET amount = amount - ? WHERE id = 1', (amount,))
    conn.commit()
    conn.close()

def increase_user_invites(tgid, amount=1):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET invited_users_count = invited_users_count + ? WHERE tgid = ?', (amount, tgid))
    conn.commit()
    conn.close()

def add_referral(referrer_id, referred_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO referrals (referrer_id, referred_id) VALUES (?, ?)', (referrer_id, referred_id))
    conn.commit()
    conn.close()

def referral_exists(referrer_id, referred_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM referrals WHERE referrer_id = ? AND referred_id = ?', (referrer_id, referred_id))
    referral = cursor.fetchone()
    conn.close()
    return referral is not None

def get_top_referrers(limit=10):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT username, invited_users_count
    FROM users
    ORDER BY invited_users_count DESC
    LIMIT ?
    ''', (limit,))
    top_referrers = cursor.fetchall()
    conn.close()
    return top_referrers

def get_total_users():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    conn.close()
    return total_users