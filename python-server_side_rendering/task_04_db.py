#!/usr/bin/python3
from flask import Flask, render_template, request
import json
import csv
import sqlite3
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent


def load_json():
    with open(BASE_DIR / "products.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv():
    with open(BASE_DIR / "products.csv", "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_sql():
    conn = sqlite3.connect(BASE_DIR / "products.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price FROM Products")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": r[0], "name": r[1], "category": r[2], "price": r[3]}
        for r in rows
    ]


def init_db():
    conn = sqlite3.connect(BASE_DIR / "products.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    cursor.execute("DELETE FROM Products")

    cursor.execute("""
        INSERT INTO Products (id, name, category, price)
        VALUES
        (1, 'Laptop', 'Electronics', 799.99),
        (2, 'Coffee Mug', 'Home Goods', 15.99)
    """)

    conn.commit()
    conn.close()


def find_product(products, pid):
    for p in products:
        if str(p.get("id")) == str(pid):
            return p
    return None


@app.route("/products")
def products():
    source = request.args.get("source")
    pid = request.args.get("id")

    if source == "json":
        data = load_json()
    elif source == "csv":
        data = load_csv()
    elif source == "sql":
        data = load_sql()
    else:
        return render_template("product_display.html",
                               products=[],
                               error="Wrong source")

    if pid:
        product = find_product(data, pid)
        if not product:
            return render_template("product_display.html",
                                   products=[],
                                   error="Product not found")
        data = [product]

    return render_template("product_display.html",
                           products=data,
                           error=None)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
