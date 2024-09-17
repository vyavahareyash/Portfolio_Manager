import sqlite3

DATABASE = 'portfolio.db'
TABLE ='Transactions'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create the Transactions table if it doesn't exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            order_type TEXT NOT NULL,
            stock_symbol TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    
    print("DB initialized")

def add_transaction(transaction_date_str, order_type, stock_symbol, quantity):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(f"""INSERT INTO {TABLE} (date, order_type, stock_symbol, quantity) VALUES (?, ?, ?, ?)""", 
                   (transaction_date_str, order_type, stock_symbol, quantity))
    
    conn.commit()
    conn.close()
    
    
    