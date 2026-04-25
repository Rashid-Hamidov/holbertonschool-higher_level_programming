#!/usr/bin/python3
from flask import Flask, render_template, request
import csv
import json
import sqlite3
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent


def load_json_products():
    with open(BASE_DIR / "products.json", "r", encoding="utf-8") as file:
        return json.load(file)


def load_csv_products():
    with open(BASE_DIR / "products.csv", "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_sql_products():
    conn = sqlite3.connect(BASE_DIR / "products.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price FROM Products")
    rows = cursor.fetchall()
    conn.close()

    products = []
    for row in rows:
        products.append({
            "id": str(row[0]),
            "name": row[1],
            "category": row[2],
            "price": str(row[3]),
        })
    return products


def find_product(products, product_id):
    for product in products:
        if str(product.get("id")) == str(product_id):
            return product
    return None


@app.route("/products")
def products():
    source = request.args.get("source")
    product_id = request.args.get("id")

    if source == "json":
        data = load_json_products()
    elif source == "csv":
        data = load_csv_products()
    elif source == "sql":
        data = load_sql_products()
    else:
        return render_template(
            "product_display.html",
            products=[],
            error="Wrong source"
        )

    if product_id:
        product = find_product(data, product_id)
        if not product:
            if source == "sql":
                return render_template(
                    "product_display.html",
                    products=[],
                    error="Product not found in SQL source"
                )
            return render_template(
                "product_display.html",
                products=[],
                error="Product not found"
            )
        data = [product]

    return render_template(
        "product_display.html",
        products=data,
        error=None
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
