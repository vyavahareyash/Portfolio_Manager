import sqlite3

DATABASE = 'portfolio.db'
TABLE ='Transactions'

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