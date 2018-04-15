# https://pastebin.com/5fuMCbU4
import sqlite3
connection = sqlite3.connect("store.db")
connection.execute("DROP TABLE IF EXISTS products;")
connection.execute("""
CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name text,
  category VARCHAR(20), 
  price DECIMAL(5, 2), 
  quantity INTEGER, 
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""")

connection.close()
