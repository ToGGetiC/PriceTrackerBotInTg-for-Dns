import sqlite3

def init_db():
    conn = sqlite3.connect('prices.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            last_price INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

def update_price(url, new_price):
    conn = sqlite3.connect('prices.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO products (url, last_price) 
        VALUES (?, ?)
        ON CONFLICT(url) DO UPDATE SET last_price = excluded.last_price
    ''', (url, new_price))
    
    conn.commit()
    conn.close()
    print(f"База данных обновлена: {url} -> {new_price}")

if __name__ == "__main__":
    init_db()
    print("База данных готова!")