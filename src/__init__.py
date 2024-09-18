import sqlite3

DATABASE = 'portfolio.db'
TABLE_TRANSACTION ='Transactions'
TABLE_POSITION = 'Positions'


conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Create the Transactions table if it doesn't exist
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {TABLE_TRANSACTION} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        order_type TEXT NOT NULL,
        stock_symbol TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL
    )
''')

conn.commit()
conn.close()