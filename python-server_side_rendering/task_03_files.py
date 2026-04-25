#!/usr/bin/python3
from flask import Flask, render_template, request
import csv
import json
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent


def load_json_products():
    path = BASE_DIR / "products.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv_products():
    path = BASE_DIR / "products.csv"
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


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
        products_list = load_json_products()
    elif source == "csv":
        products_list = load_csv_products()
    else:
        return render_template(
            "product_display.html",
            products=[],
            error="Wrong source"
        )

    if product_id:
        product = find_product(products_list, product_id)
        if not product:
            return render_template(
                "product_display.html",
                products=[],
                error="Product not found"
            )
        products_list = [product]

    return render_template(
        "product_display.html",
        products=products_list,
        error=None
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
