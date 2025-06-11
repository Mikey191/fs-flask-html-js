# backend.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = 'products.db'

# 1. Функция для создания таблицы

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 2. Функция для добавления продукта

def add_product(title):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()

# 4. Функция для получения всех продуктов

def get_all_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

# 3. Эндпоинт для добавления продукта

@app.route('/add-product', methods=['POST'])
def add_product_endpoint():
    data = request.get_json()
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    add_product(title)
    return jsonify({'message': 'Product added successfully'})

# 4. Эндпоинт для получения всех продуктов

@app.route('/products', methods=['GET'])
def get_products_endpoint():
    products = get_all_products()
    return jsonify([{'id': p[0], 'title': p[1]} for p in products])

if __name__ == '__main__':
    create_table()
    app.run(debug=True, port=8000)
