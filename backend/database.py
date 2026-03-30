import sqlite3

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # customers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT UNIQUE
        )
    ''')

    # orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            items TEXT,
            total REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            items TEXT,
            total REAL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            stock INTEGER
        )
    ''')

    cursor.execute("""
        INSERT OR IGNORE INTO products (id, name, price, stock)
            VALUES 
            (1, 'Espresso', 120, 50),
            (2, 'Latte', 150, 50),
            (3, 'Cappuccino', 140, 50)
    """)

    conn.commit()
    conn.close()

def insert_customer(name, contact):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO customers (name, contact) VALUES (?, ?)",
        (name, contact)
    )

    conn.commit()
    conn.close()

def get_customer(contact):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers WHERE contact=?", (contact,))
    user = cursor.fetchone()

    conn.close()
    return user

def insert_order(customer_id, items, total):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO orders (customer_id, items, total) VALUES (?, ?, ?)",
        (customer_id, items, total)
    )

    conn.commit()
    conn.close()

def get_orders():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()
    return data

def complete_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE orders SET status='Completed' WHERE id=?",
        (order_id,)
    )

    conn.commit()
    conn.close()