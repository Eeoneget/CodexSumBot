import sqlite3

conn = sqlite3.connect('Datatelegram.db')
cursor = conn.cursor()

def table_exist(table_name):
    cursor.execute(f'''SELECT count (name) FROM sqlite_master WHERE TYPE = 'table' AND name='{table_name}' ''')


cursor.execute('''CREATE TABLE telegram(
    id INTEGER,
    user_id INTEGER,
    user_name INTEGER)
    ''')
