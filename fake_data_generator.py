import random
import shutil
from datetime import date, datetime, timedelta
from pathlib import Path
from collections import defaultdict

import pandas as pd
from faker import Faker


SEED = 42
TODAY = date(2025, 12, 31)
OUTPUT_DIR = Path.home() / "Desktop" / "abc_foodmart_fake_data"

fake = Faker("en_US")
random.seed(SEED)
Faker.seed(SEED)

ROW_COUNTS = {
    "store": 5,
    "department": 7,
    "product_category": 12,
    "product": 150,
    "vendor": 20,
    "vendor_product": 250,
    "customer": 200,
    "customer_loyalty_account": 160,
    "employee": 75,
    "store_department": 35,
    "inventory": 750,
    "purchase_order": 100,
    "purchase_order_line": 300,
    "delivery": 90,
    "sales_transaction": 1000,
    "sales_transaction_line": 3000,
    "payment": 1000,
    "shift_schedule": 450,
    "payroll_record": 150,
    "accounting_record": 1100,
}

ALLOWED_STATUS = {
    "store": {"open"},
    "vendor": {"active"},
    "product": {"active", "seasonal"},
    "employment": {"active", "inactive", "leave"},
    "shift": {"completed", "missed"},
    "purchase_order": {"created", "shipped", "received", "cancelled"},
    "delivery": {"ontime", "delayed", "partial", "cancelled"},
    "account": {"active", "inactive"},
}

BOROUGH_ADDRESSES = {
    "Queens": [
        "12-01 Astoria Blvd, Astoria, Queens, NY",
        "44-15 Queens Blvd, Sunnyside, Queens, NY",
        "88-21 Roosevelt Ave, Jackson Heights, Queens, NY",
        "99-05 Northern Blvd, Corona, Queens, NY",
        "73-11 Main St, Flushing, Queens, NY",
    ],
    "Brooklyn": [
        "145 Flatbush Ave, Brooklyn, NY",
        "820 Fulton St, Brooklyn, NY",
        "212 Bedford Ave, Brooklyn, NY",
        "305 Court St, Brooklyn, NY",
        "7813 5th Ave, Brooklyn, NY",
    ],
}

DEPARTMENTS = [
    ("Produce", "Fresh fruits and vegetables"),
    ("Dairy", "Milk, yogurt, eggs, and cheese"),
    ("Meat", "Fresh and packaged meat"),
    ("Bakery", "Bread, cakes, and pastries"),
    ("Frozen", "Frozen meals and desserts"),
    ("Beverages", "Drinks and refreshments"),
    ("Personal Care", "Health and household personal care"),
]

PRODUCT_CATEGORIES = [
    "Produce", "Dairy", "Meat", "Bakery", "Frozen", "Beverages",
    "Personal Care", "Pantry", "Snacks", "Seafood", "Household", "Deli",
]


PRODUCT_TEMPLATES = {
    "Produce": [
        {"name": "Bananas", "options": [("each", "each", (0.29, 0.79)), ("1 lb", "lb", (0.69, 1.49)), ("2 lb", "lb", (1.29, 2.49))], "perishable": True},
        {"name": "Apples", "options": [("each", "each", (0.79, 1.49)), ("2 lb", "bag", (2.49, 4.99)), ("3 lb", "bag", (3.49, 5.99))], "perishable": True},
        {"name": "Spinach", "options": [("5 oz", "pack", (1.99, 3.49)), ("10 oz", "pack", (3.49, 5.49))], "perishable": True},
        {"name": "Tomatoes", "options": [("1 lb", "lb", (1.49, 3.49)), ("each", "each", (0.79, 1.49))], "perishable": True},
        {"name": "Potatoes", "options": [("3 lb", "bag", (2.99, 4.99)), ("5 lb", "bag", (4.99, 7.99))], "perishable": True},
        {"name": "Lettuce", "options": [("each", "each", (1.49, 2.99))], "perishable": True},
        {"name": "Avocados", "options": [("each", "each", (0.99, 2.49)), ("4 count", "bag", (3.99, 6.99))], "perishable": True},
        {"name": "Onions", "options": [("2 lb", "bag", (1.99, 3.99)), ("3 lb", "bag", (2.99, 4.99)), ("each", "each", (0.69, 1.29))], "perishable": True},
        {"name": "Carrots", "options": [("1 lb", "bag", (1.29, 2.49)), ("2 lb", "bag", (2.49, 3.99))], "perishable": True},
        {"name": "Blueberries", "options": [("6 oz", "pack", (2.99, 4.99)), ("12 oz", "pack", (4.99, 6.99))], "perishable": True},
    ],
    "Dairy": [
        {"name": "Whole Milk", "options": [("0.5 gallon", "gallon", (2.49, 3.99)), ("1 gallon", "gallon", (3.99, 5.99))], "perishable": True},
        {"name": "Greek Yogurt", "options": [("5.3 oz", "cup", (1.29, 2.49)), ("16 oz", "tub", (3.99, 6.49)), ("4 pack", "pack", (4.99, 7.99))], "perishable": True},
        {"name": "Butter", "options": [("8 oz", "pack", (2.99, 4.99)), ("16 oz", "pack", (4.99, 7.99))], "perishable": True},
        {"name": "Cheddar Cheese", "options": [("8 oz", "pack", (2.99, 5.49)), ("16 oz", "pack", (5.49, 8.99))], "perishable": True},
        {"name": "Eggs", "options": [("6 count", "pack", (2.49, 4.49)), ("12 count", "pack", (3.49, 6.49)), ("18 count", "pack", (5.49, 8.99))], "perishable": True},
        {"name": "Cream Cheese", "options": [("8 oz", "pack", (2.49, 4.49))], "perishable": True},
        {"name": "Half and Half", "options": [("16 oz", "oz", (2.49, 3.99)), ("32 oz", "oz", (3.99, 5.49))], "perishable": True},
        {"name": "Sour Cream", "options": [("8 oz", "tub", (1.99, 3.49)), ("16 oz", "tub", (3.49, 5.49))], "perishable": True},
        {"name": "Mozzarella", "options": [("8 oz", "pack", (2.99, 4.99)), ("16 oz", "pack", (4.99, 7.49))], "perishable": True},
        {"name": "Skim Milk", "options": [("0.5 gallon", "gallon", (2.49, 3.99)), ("1 gallon", "gallon", (3.99, 5.99))], "perishable": True},
    ],
    "Meat": [
        {"name": "Chicken Breast", "options": [("1 lb", "lb", (5.99, 8.99)), ("2 lb", "lb", (10.99, 15.99)), ("family pack", "pack", (12.99, 18.99))], "perishable": True},
        {"name": "Ground Beef", "options": [("1 lb", "lb", (5.99, 8.99)), ("2 lb", "lb", (11.99, 16.99))], "perishable": True},
        {"name": "Pork Chops", "options": [("1 lb", "lb", (6.99, 10.99)), ("2 lb", "lb", (12.99, 17.99))], "perishable": True},
        {"name": "Turkey Slices", "options": [("8 oz", "pack", (3.99, 6.99)), ("16 oz", "pack", (6.99, 10.99))], "perishable": True},
        {"name": "Bacon", "options": [("12 oz", "pack", (4.99, 7.99)), ("16 oz", "pack", (6.99, 9.99))], "perishable": True},
        {"name": "Sausage", "options": [("12 oz", "pack", (4.99, 7.99)), ("16 oz", "pack", (6.49, 9.49))], "perishable": True},
        {"name": "Ribeye Steak", "options": [("1 lb", "lb", (12.99, 19.99)), ("2 lb", "lb", (24.99, 34.99))], "perishable": True},
        {"name": "Chicken Wings", "options": [("1 lb", "lb", (4.99, 7.99)), ("2 lb", "lb", (8.99, 13.99))], "perishable": True},
        {"name": "Ham", "options": [("8 oz", "pack", (3.99, 6.99)), ("16 oz", "pack", (6.99, 10.99))], "perishable": True},
        {"name": "Beef Roast", "options": [("1 lb", "lb", (8.99, 13.99)), ("2 lb", "lb", (16.99, 25.99)), ("3 lb", "lb", (24.99, 34.99))], "perishable": True},
    ],
    "Bakery": [
        {"name": "White Bread", "options": [("20 oz", "loaf", (2.49, 4.49))], "perishable": True},
        {"name": "Bagels", "options": [("4 count", "pack", (2.99, 4.49)), ("6 count", "pack", (3.99, 5.49))], "perishable": True},
        {"name": "Croissants", "options": [("4 count", "pack", (3.99, 5.99)), ("6 count", "pack", (4.99, 6.99))], "perishable": True},
        {"name": "Muffins", "options": [("4 count", "pack", (3.99, 5.99)), ("6 count", "pack", (4.99, 7.49))], "perishable": True},
        {"name": "Chocolate Cake", "options": [("single", "each", (7.99, 14.99))], "perishable": True},
        {"name": "Dinner Rolls", "options": [("12 count", "pack", (2.99, 4.99))], "perishable": True},
        {"name": "Baguette", "options": [("single", "each", (2.49, 4.49))], "perishable": True},
        {"name": "Donuts", "options": [("6 count", "box", (4.99, 7.99)), ("12 count", "box", (8.99, 12.99))], "perishable": True},
        {"name": "Cookies", "options": [("8 oz", "box", (2.99, 5.49)), ("12 oz", "box", (4.49, 6.99))], "perishable": True},
        {"name": "Cupcakes", "options": [("4 count", "box", (4.99, 7.99)), ("6 count", "box", (6.99, 9.99))], "perishable": True},
    ],
    "Frozen": [
        {"name": "Frozen Pizza", "options": [("12 inch", "box", (4.99, 8.99)), ("16 inch", "box", (7.99, 11.99))], "perishable": True},
        {"name": "Ice Cream", "options": [("16 oz", "tub", (3.99, 6.49)), ("48 oz", "tub", (5.99, 9.49))], "perishable": True},
        {"name": "Frozen Vegetables", "options": [("12 oz", "bag", (1.99, 3.49)), ("16 oz", "bag", (2.99, 4.49))], "perishable": True},
        {"name": "Chicken Nuggets", "options": [("16 oz", "bag", (4.99, 7.99)), ("32 oz", "bag", (7.99, 11.99))], "perishable": True},
        {"name": "Frozen Waffles", "options": [("10 count", "box", (2.99, 4.99))], "perishable": True},
        {"name": "French Fries", "options": [("16 oz", "bag", (2.99, 4.99)), ("32 oz", "bag", (4.99, 6.99))], "perishable": True},
        {"name": "Frozen Berries", "options": [("12 oz", "pack", (3.99, 6.49)), ("24 oz", "pack", (6.49, 9.99))], "perishable": True},
        {"name": "Fish Sticks", "options": [("16 oz", "box", (4.99, 7.99))], "perishable": True},
        {"name": "Frozen Dumplings", "options": [("12 oz", "bag", (4.99, 7.99)), ("24 oz", "bag", (7.99, 10.99))], "perishable": True},
        {"name": "Frozen Meals", "options": [("10 oz", "box", (3.49, 5.99)), ("16 oz", "box", (4.99, 7.49))], "perishable": True},
    ],
    "Beverages": [
        {"name": "Orange Juice", "options": [("32 oz", "bottle", (2.99, 4.99)), ("59 oz", "bottle", (4.49, 6.99))], "perishable": False},
        {"name": "Cola", "options": [("12 oz", "bottle", (1.49, 2.49)), ("20 oz", "bottle", (2.29, 3.49)), ("12 pack", "case", (6.99, 9.99))], "perishable": False},
        {"name": "Sparkling Water", "options": [("12 oz", "can", (1.29, 2.29)), ("8 pack", "case", (4.99, 7.99))], "perishable": False},
        {"name": "Bottled Water", "options": [("16.9 oz", "bottle", (0.99, 1.99)), ("24 pack", "case", (4.99, 8.99))], "perishable": False},
        {"name": "Coffee", "options": [("12 oz", "bag", (5.99, 9.99)), ("32 oz", "bottle", (2.49, 4.49))], "perishable": False},
        {"name": "Tea", "options": [("20 count", "box", (2.99, 5.49)), ("64 oz", "bottle", (2.49, 4.49))], "perishable": False},
        {"name": "Energy Drink", "options": [("12 oz", "can", (2.49, 3.99)), ("4 pack", "case", (7.99, 11.99))], "perishable": False},
        {"name": "Sports Drink", "options": [("20 oz", "bottle", (1.79, 2.99)), ("8 pack", "case", (8.99, 13.99))], "perishable": False},
        {"name": "Apple Juice", "options": [("32 oz", "bottle", (2.49, 4.49)), ("64 oz", "bottle", (4.49, 6.99))], "perishable": False},
        {"name": "Lemonade", "options": [("32 oz", "bottle", (2.49, 4.49)), ("59 oz", "bottle", (3.99, 5.99))], "perishable": False},
    ],
    "Personal Care": [
        {"name": "Shampoo", "options": [("12 oz", "bottle", (3.99, 8.99)), ("20 oz", "bottle", (6.99, 12.99))], "perishable": False},
        {"name": "Toothpaste", "options": [("4 oz", "tube", (2.49, 4.99)), ("6 oz", "tube", (3.99, 6.99))], "perishable": False},
        {"name": "Body Wash", "options": [("12 oz", "bottle", (3.99, 7.99)), ("18 oz", "bottle", (5.99, 9.99))], "perishable": False},
        {"name": "Soap", "options": [("3 count", "pack", (2.99, 5.49)), ("6 count", "pack", (4.99, 7.99))], "perishable": False},
        {"name": "Deodorant", "options": [("2.6 oz", "stick", (3.99, 6.99))], "perishable": False},
        {"name": "Lotion", "options": [("12 oz", "bottle", (4.99, 8.99)), ("20 oz", "bottle", (6.99, 11.99))], "perishable": False},
        {"name": "Facial Tissue", "options": [("1 box", "box", (1.99, 3.49)), ("4 pack", "pack", (6.49, 9.99))], "perishable": False},
        {"name": "Toothbrush", "options": [("single", "pack", (1.99, 3.99)), ("2 pack", "pack", (3.49, 5.49))], "perishable": False},
        {"name": "Hand Sanitizer", "options": [("8 oz", "bottle", (2.49, 4.99)), ("16 oz", "bottle", (4.49, 6.99))], "perishable": False},
        {"name": "Mouthwash", "options": [("16 oz", "bottle", (3.99, 6.99)), ("32 oz", "bottle", (5.99, 8.99))], "perishable": False},
    ],
    "Pantry": [
        {"name": "Rice", "options": [("1 lb", "bag", (1.49, 2.99)), ("2 lb", "bag", (2.99, 4.99)), ("5 lb", "bag", (5.99, 9.99))], "perishable": False},
        {"name": "Pasta", "options": [("16 oz", "box", (1.49, 3.49))], "perishable": False},
        {"name": "Olive Oil", "options": [("16 oz", "bottle", (5.99, 9.99)), ("32 oz", "bottle", (9.99, 14.99))], "perishable": False},
        {"name": "Peanut Butter", "options": [("16 oz", "jar", (2.99, 4.99)), ("28 oz", "jar", (4.99, 7.99))], "perishable": False},
        {"name": "Cereal", "options": [("12 oz", "box", (3.49, 5.99)), ("18 oz", "box", (4.99, 7.99))], "perishable": False},
        {"name": "Flour", "options": [("2 lb", "bag", (1.99, 3.99)), ("5 lb", "bag", (3.99, 6.99))], "perishable": False},
        {"name": "Sugar", "options": [("2 lb", "bag", (1.99, 3.99)), ("4 lb", "bag", (3.49, 5.99))], "perishable": False},
        {"name": "Tomato Sauce", "options": [("15 oz", "can", (1.29, 2.49)), ("24 oz", "jar", (2.49, 4.49))], "perishable": False},
        {"name": "Black Beans", "options": [("15 oz", "can", (1.29, 2.49))], "perishable": False},
        {"name": "Oats", "options": [("18 oz", "canister", (2.99, 4.99)), ("42 oz", "canister", (4.99, 7.99))], "perishable": False},
    ],
    "Snacks": [
        {"name": "Potato Chips", "options": [("8 oz", "bag", (2.99, 4.99)), ("12 oz", "bag", (4.49, 6.49))], "perishable": False},
        {"name": "Pretzels", "options": [("10 oz", "bag", (2.49, 4.49)), ("16 oz", "bag", (3.99, 5.99))], "perishable": False},
        {"name": "Granola Bars", "options": [("6 count", "box", (2.99, 4.99)), ("12 count", "box", (4.99, 7.49))], "perishable": False},
        {"name": "Cookies", "options": [("8 oz", "pack", (2.49, 4.49)), ("12 oz", "pack", (3.99, 5.99))], "perishable": False},
        {"name": "Crackers", "options": [("8 oz", "box", (2.49, 4.49)), ("16 oz", "box", (3.99, 5.99))], "perishable": False},
        {"name": "Popcorn", "options": [("3 count", "box", (2.99, 4.99)), ("6 count", "box", (4.99, 6.99))], "perishable": False},
        {"name": "Trail Mix", "options": [("8 oz", "bag", (3.99, 6.99)), ("16 oz", "bag", (6.99, 9.99))], "perishable": False},
        {"name": "Chocolate Bar", "options": [("single", "bar", (1.29, 2.49)), ("6 pack", "pack", (5.49, 8.49))], "perishable": False},
        {"name": "Gummy Candy", "options": [("5 oz", "bag", (1.99, 3.49)), ("10 oz", "bag", (3.49, 5.49))], "perishable": False},
        {"name": "Tortilla Chips", "options": [("10 oz", "bag", (2.99, 4.99)), ("16 oz", "bag", (4.49, 6.49))], "perishable": False},
    ],
    "Seafood": [
        {"name": "Salmon Fillet", "options": [("1 lb", "lb", (9.99, 16.99)), ("2 lb", "lb", (18.99, 28.99))], "perishable": True},
        {"name": "Shrimp", "options": [("12 oz", "pack", (7.99, 12.99)), ("2 lb", "bag", (14.99, 21.99))], "perishable": True},
        {"name": "Tuna Steak", "options": [("1 lb", "lb", (10.99, 18.99))], "perishable": True},
        {"name": "Cod Fillet", "options": [("1 lb", "lb", (8.99, 14.99))], "perishable": True},
        {"name": "Crab Cakes", "options": [("2 count", "pack", (6.99, 10.99)), ("4 count", "pack", (10.99, 15.99))], "perishable": True},
        {"name": "Tilapia", "options": [("1 lb", "lb", (6.99, 11.99))], "perishable": True},
        {"name": "Scallops", "options": [("12 oz", "pack", (9.99, 15.99))], "perishable": True},
        {"name": "Mussels", "options": [("1 lb", "lb", (5.99, 9.99)), ("2 lb", "lb", (10.99, 15.99))], "perishable": True},
        {"name": "Fish Fillet", "options": [("1 lb", "lb", (7.99, 12.99))], "perishable": True},
        {"name": "Lobster Tail", "options": [("2 count", "pack", (14.99, 24.99))], "perishable": True},
    ],
    "Household": [
        {"name": "Paper Towels", "options": [("2 pack", "pack", (4.99, 7.99)), ("6 pack", "pack", (11.99, 16.99))], "perishable": False},
        {"name": "Dish Soap", "options": [("16 oz", "bottle", (2.99, 4.99)), ("32 oz", "bottle", (4.99, 7.99))], "perishable": False},
        {"name": "Laundry Detergent", "options": [("50 oz", "bottle", (7.99, 12.99)), ("100 oz", "bottle", (12.99, 18.99))], "perishable": False},
        {"name": "Trash Bags", "options": [("20 count", "box", (5.99, 9.99)), ("40 count", "box", (9.99, 14.99))], "perishable": False},
        {"name": "Aluminum Foil", "options": [("25 sq ft", "box", (2.99, 4.99)), ("75 sq ft", "box", (4.99, 7.99))], "perishable": False},
        {"name": "Sponges", "options": [("3 count", "pack", (2.49, 4.49)), ("6 count", "pack", (4.49, 6.49))], "perishable": False},
        {"name": "Cleaning Spray", "options": [("24 oz", "bottle", (3.49, 5.99))], "perishable": False},
        {"name": "Plastic Wrap", "options": [("100 sq ft", "box", (2.99, 4.99)), ("200 sq ft", "box", (4.99, 6.99))], "perishable": False},
        {"name": "Napkins", "options": [("100 count", "pack", (2.49, 4.49)), ("250 count", "pack", (4.49, 6.49))], "perishable": False},
        {"name": "Bleach", "options": [("32 oz", "bottle", (2.99, 4.99)), ("64 oz", "bottle", (4.49, 6.49))], "perishable": False},
    ],
    "Deli": [
        {"name": "Turkey Sandwich", "options": [("single", "each", (5.99, 8.99))], "perishable": True},
        {"name": "Potato Salad", "options": [("12 oz", "container", (3.99, 5.99)), ("24 oz", "container", (6.49, 8.99))], "perishable": True},
        {"name": "Coleslaw", "options": [("12 oz", "container", (3.49, 5.49)), ("24 oz", "container", (5.99, 8.49))], "perishable": True},
        {"name": "Chicken Salad", "options": [("12 oz", "container", (4.99, 6.99)), ("24 oz", "container", (7.99, 10.99))], "perishable": True},
        {"name": "Mac and Cheese", "options": [("12 oz", "container", (4.49, 6.49)), ("24 oz", "container", (7.49, 9.99))], "perishable": True},
        {"name": "Ham Slices", "options": [("8 oz", "pack", (3.99, 5.99)), ("16 oz", "pack", (6.99, 9.99))], "perishable": True},
        {"name": "Roast Beef Slices", "options": [("8 oz", "pack", (4.99, 6.99)), ("16 oz", "pack", (7.99, 10.99))], "perishable": True},
        {"name": "Fresh Pasta Salad", "options": [("12 oz", "container", (4.49, 6.49)), ("24 oz", "container", (7.49, 9.99))], "perishable": True},
        {"name": "Prepared Soup", "options": [("16 oz", "container", (4.49, 6.99)), ("32 oz", "container", (7.99, 10.99))], "perishable": True},
        {"name": "Wrap", "options": [("single", "each", (5.99, 8.99))], "perishable": True},
    ],
}

CATEGORY_RULES = {
    "Produce": {
        "names": ["Bananas", "Apples", "Spinach", "Tomatoes", "Potatoes", "Lettuce", "Avocados", "Onions", "Carrots", "Blueberries"],
        "units": ["lb", "each", "bag"],
        "perishable": True,
        "price_range": (0.79, 6.99),
        "statuses": ["active", "active", "active", "seasonal"],
    },
    "Dairy": {
        "names": ["Whole Milk", "Greek Yogurt", "Butter", "Cheddar Cheese", "Eggs", "Cream Cheese", "Half and Half", "Sour Cream", "Mozzarella", "Skim Milk"],
        "units": ["gallon", "pack", "oz", "tub"],
        "perishable": True,
        "price_range": (2.49, 9.99),
        "statuses": ["active", "active", "active", "seasonal"],
    },
    "Meat": {
        "names": ["Chicken Breast", "Ground Beef", "Pork Chops", "Turkey Slices", "Bacon", "Sausage", "Ribeye Steak", "Chicken Wings", "Ham", "Beef Roast"],
        "units": ["lb", "pack"],
        "perishable": True,
        "price_range": (4.99, 22.99),
        "statuses": ["active", "active", "active", "seasonal"],
    },
    "Bakery": {
        "names": ["White Bread", "Bagels", "Croissants", "Muffins", "Chocolate Cake", "Dinner Rolls", "Baguette", "Donuts", "Cookies", "Cupcakes"],
        "units": ["loaf", "pack", "each", "box"],
        "perishable": True,
        "price_range": (1.99, 14.99),
        "statuses": ["active", "active", "seasonal"],
    },
    "Frozen": {
        "names": ["Frozen Pizza", "Ice Cream", "Frozen Vegetables", "Chicken Nuggets", "Frozen Waffles", "French Fries", "Frozen Berries", "Fish Sticks", "Frozen Dumplings", "Frozen Meals"],
        "units": ["box", "bag", "oz", "pack"],
        "perishable": True,
        "price_range": (2.99, 12.99),
        "statuses": ["active", "active", "seasonal"],
    },
    "Beverages": {
        "names": ["Orange Juice", "Cola", "Sparkling Water", "Bottled Water", "Coffee", "Tea", "Energy Drink", "Sports Drink", "Apple Juice", "Lemonade"],
        "units": ["bottle", "pack", "case", "oz"],
        "perishable": False,
        "price_range": (1.29, 15.99),
        "statuses": ["active", "active", "seasonal"],
    },
    "Personal Care": {
        "names": ["Shampoo", "Toothpaste", "Body Wash", "Soap", "Deodorant", "Lotion", "Facial Tissue", "Toothbrush", "Hand Sanitizer", "Mouthwash"],
        "units": ["bottle", "pack", "tube", "bar"],
        "perishable": False,
        "price_range": (1.99, 13.99),
        "statuses": ["active", "active", "seasonal"],
    },
    "Pantry": {
        "names": ["Rice", "Pasta", "Olive Oil", "Peanut Butter", "Cereal", "Flour", "Sugar", "Tomato Sauce", "Black Beans", "Oats"],
        "units": ["lb", "bag", "box", "jar", "bottle", "can"],
        "perishable": False,
        "price_range": (1.49, 11.99),
        "statuses": ["active", "active", "seasonal"],
    },
    "Snacks": {
        "names": ["Potato Chips", "Pretzels", "Granola Bars", "Cookies", "Crackers", "Popcorn", "Trail Mix", "Chocolate Bar", "Gummy Candy", "Tortilla Chips"],
        "units": ["bag", "box", "pack", "bar"],
        "perishable": False,
        "price_range": (1.19, 8.99),
        "statuses": ["active", "active", "seasonal"],
    },
    "Seafood": {
        "names": ["Salmon Fillet", "Shrimp", "Tuna Steak", "Cod Fillet", "Crab Cakes", "Tilapia", "Scallops", "Mussels", "Fish Fillet", "Lobster Tail"],
        "units": ["lb", "pack"],
        "perishable": True,
        "price_range": (6.99, 24.99),
        "statuses": ["active", "active", "seasonal"],
    },
    "Household": {
        "names": ["Paper Towels", "Dish Soap", "Laundry Detergent", "Trash Bags", "Aluminum Foil", "Sponges", "Cleaning Spray", "Plastic Wrap", "Napkins", "Bleach"],
        "units": ["pack", "bottle", "box"],
        "perishable": False,
        "price_range": (2.49, 18.99),
        "statuses": ["active", "active", "seasonal"],
    },
    "Deli": {
        "names": ["Turkey Sandwich", "Potato Salad", "Coleslaw", "Chicken Salad", "Mac and Cheese", "Ham Slices", "Roast Beef Slices", "Fresh Pasta Salad", "Prepared Soup", "Wrap"],
        "units": ["lb", "pack", "container", "each"],
        "perishable": True,
        "price_range": (3.99, 14.99),
        "statuses": ["active", "active", "seasonal"],
    },
}

BRANDS = [
    "Fresh Choice", "Golden Farm", "Metro Select", "Daily Harvest", "Urban Pantry",
    "Nature Basket", "Prime Goods", "Brooklyn Best", "Queens Choice", "Value Fresh",
    "Homestyle", "Market Plus", "Sunrise", "Pure Living", "Classic Kitchen"
]

VENDOR_NAMES_LOCAL = [
    "Brooklyn Fresh Supply", "Queens Produce Hub", "Metro Dairy Partners",
    "Atlantic Meat Co", "East River Bakery Supply", "Harbor Frozen Foods",
    "City Beverage Source", "Local Pantry Wholesale", "Urban Seafood LLC", "Tri-State Deli Goods"
]

VENDOR_NAMES_NATIONAL = [
    "National Food Distributors", "American Grocery Supply", "Prime Retail Wholesale",
    "United Beverage Group", "FreshLine National", "Standard Household Supply",
    "PureCare Distribution", "North Coast Foods", "BluePeak Wholesale", "Continental Goods"
]

JOB_RULES = {
    "Cashier": {"pay_type": "hourly", "hourly_min": 16.00, "hourly_max": 20.00, "departments": ["Beverages", "Bakery", "Produce", "Dairy", "Frozen", "Personal Care", "Meat"]},
    "Stock Associate": {"pay_type": "hourly", "hourly_min": 17.00, "hourly_max": 22.00, "departments": ["Produce", "Dairy", "Meat", "Bakery", "Frozen", "Beverages", "Personal Care"]},
    "Department Manager": {"pay_type": "salary", "salary_min": 52000.00, "salary_max": 72000.00, "departments": ["Produce", "Dairy", "Meat", "Bakery", "Frozen", "Beverages", "Personal Care"]},
    "Assistant Manager": {"pay_type": "salary", "salary_min": 65000.00, "salary_max": 85000.00, "departments": ["Produce", "Dairy", "Meat", "Bakery", "Frozen", "Beverages", "Personal Care"]},
    "Store Manager": {"pay_type": "salary", "salary_min": 85000.00, "salary_max": 115000.00, "departments": ["Produce", "Dairy", "Meat", "Bakery", "Frozen", "Beverages", "Personal Care"]},
}

AISLE_MAP = {
    "Produce": ("A01", "Produce aisle"),
    "Dairy": ("A02", "Dairy aisle"),
    "Meat": ("A03", "Meat aisle"),
    "Bakery": ("A04", "Bakery aisle"),
    "Frozen": ("A05", "Frozen aisle"),
    "Beverages": ("A06", "Beverages aisle"),
    "Personal Care": ("A07", "Personal care aisle"),
    "Pantry": ("A08", "Pantry aisle"),
    "Snacks": ("A09", "Snacks aisle"),
    "Seafood": ("A10", "Seafood aisle"),
    "Household": ("A11", "Household aisle"),
    "Deli": ("A12", "Deli aisle"),
}

CATEGORY_DEMAND_WEIGHT = {
    "Produce": 20, "Snacks": 18, "Beverages": 18, "Dairy": 15, "Bakery": 12,
    "Pantry": 12, "Frozen": 10, "Meat": 8, "Deli": 7, "Household": 5,
    "Personal Care": 4, "Seafood": 3,
}

HOUR_WEIGHTS = {
    8: 2, 9: 3, 10: 4, 11: 5, 12: 6, 13: 6, 14: 5,
    15: 6, 16: 7, 17: 9, 18: 10, 19: 9, 20: 6
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def money(value: float) -> float:
    return round(float(value), 2)


def us_phone() -> str:
    return f"718-555-{random.randint(1000, 9999)}"


def random_date(start: date, end: date) -> date:
    if start > end:
        start, end = end, start
    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def weighted_choice(options):
    values = [item[0] for item in options]
    weights = [item[1] for item in options]
    return random.choices(values, weights=weights, k=1)[0]


def weekend_weighted_sale_date(start_date: date, end_date: date) -> date:
    dates = []
    weights = []
    current = start_date
    while current <= end_date:
        weight = 2.0 if current.weekday() in (5, 6) else 1.0
        if (current.month, current.day) in [(11, 27), (12, 24), (12, 31), (1, 1), (2, 14)]:
            weight += 1.0
        if current.month == 12:
            weight *= 1.20
        elif current.month == 1:
            weight *= 0.90
        dates.append(current)
        weights.append(weight)
        current += timedelta(days=1)
    return random.choices(dates, weights=weights, k=1)[0]


def hour_weighted_choice():
    hours = list(HOUR_WEIGHTS.keys())
    weights = list(HOUR_WEIGHTS.values())
    return random.choices(hours, weights=weights, k=1)[0]


def get_store_sales_weights(store_df: pd.DataFrame):
    weights = {}
    for _, row in store_df.iterrows():
        weights[int(row["store_id"])] = 1.25 if row["borough"] == "Brooklyn" else 1.00
    return weights


def basket_size_choice():
    return random.choices([1, 2, 3, 4, 5, 6], weights=[10, 20, 30, 20, 15, 5], k=1)[0]


def generate_store() -> pd.DataFrame:
    rows = []
    store_plan = [
        ("Queens", date(2020, 2, 15)),
        ("Queens", date(2020, 8, 20)),
        ("Brooklyn", date(2025, 1, 15)),
        ("Brooklyn", date(2025, 4, 10)),
        ("Brooklyn", date(2025, 7, 1)),
    ]

    for i, (borough, open_date) in enumerate(store_plan, start=1):
        rows.append({
            "store_id": i,
            "store_name": f"ABC Foodmart {borough[0]}{i}",
            "borough": borough,
            "street_address": BOROUGH_ADDRESSES[borough][(i - 1) % len(BOROUGH_ADDRESSES[borough])],
            "phone_number": us_phone(),
            "open_date": open_date,
            "store_status": "open",
        })
    return pd.DataFrame(rows)


def generate_department() -> pd.DataFrame:
    return pd.DataFrame([
        {"department_id": i, "department_name": name, "department_description": desc}
        for i, (name, desc) in enumerate(DEPARTMENTS, start=1)
    ])


def generate_product_category() -> pd.DataFrame:
    return pd.DataFrame({"category_id": list(range(1, len(PRODUCT_CATEGORIES) + 1)), "category_name": PRODUCT_CATEGORIES})


def generate_customer() -> pd.DataFrame:
    rows = []
    used_emails = set()
    for i in range(1, ROW_COUNTS["customer"] + 1):
        first = fake.first_name()
        last = fake.last_name()
        email = fake.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)
        segment = weighted_choice([("high", 0.20), ("medium", 0.50), ("low", 0.30)])
        rows.append({
            "customer_id": i,
            "first_name": first,
            "last_name": last,
            "phone_number": us_phone() if random.random() < 0.85 else None,
            "email_address": email,
            "join_date": random_date(date(2023, 1, 1), TODAY),
            "customer_segment": segment,
        })
    return pd.DataFrame(rows)


def generate_vendor() -> pd.DataFrame:
    rows = []
    names = VENDOR_NAMES_LOCAL + VENDOR_NAMES_NATIONAL
    regions = ["local"] * len(VENDOR_NAMES_LOCAL) + ["national"] * len(VENDOR_NAMES_NATIONAL)
    pairs = list(zip(names, regions))
    random.shuffle(pairs)
    for i, (name, region) in enumerate(pairs[:ROW_COUNTS["vendor"]], start=1):
        if region == "local":
            address = random.choice(["Brooklyn, NY", "Queens, NY", "Long Island City, NY", "Jersey City, NJ", "Bronx, NY"])
            phone = us_phone()
        else:
            address = random.choice(["Chicago, IL", "Atlanta, GA", "Dallas, TX", "Columbus, OH", "Philadelphia, PA"])
            phone = f"800-555-{random.randint(1000, 9999)}"
        email_domain = name.lower().replace(" ", "").replace(",", "")
        rows.append({
            "vendor_id": i,
            "vendor_name": name,
            "contact_name": fake.name(),
            "phone_number": phone,
            "email_address": f"contact{i}@{email_domain}.com",
            "vendor_address": address,
            "vendor_status": "active",
        })
    return pd.DataFrame(rows)


def generate_product(product_category_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    used_barcodes = set()
    category_name_to_id = dict(zip(product_category_df["category_name"], product_category_df["category_id"]))

    for i in range(1, ROW_COUNTS["product"] + 1):
        category_name = PRODUCT_CATEGORIES[(i - 1) % len(PRODUCT_CATEGORIES)]
        brand = random.choice(BRANDS)
        barcode = str(random.randint(100000000000, 999999999999))
        while barcode in used_barcodes:
            barcode = str(random.randint(100000000000, 999999999999))
        used_barcodes.add(barcode)

        if category_name in PRODUCT_TEMPLATES:
            template = random.choice(PRODUCT_TEMPLATES[category_name])
            package_size, unit_of_measure, price_range = random.choice(template["options"])
            product_base_name = template["name"]
            is_perishable = template["perishable"]
            current_unit_price = money(random.uniform(*price_range))
            product_status = random.choice(["active", "active", "active", "seasonal"])
        else:
            rule = CATEGORY_RULES[category_name]
            product_base_name = random.choice(rule["names"])
            package_size = "standard"
            unit_of_measure = random.choice(rule["units"])
            is_perishable = rule["perishable"]
            current_unit_price = money(random.uniform(*rule["price_range"]))
            product_status = random.choice(rule["statuses"])

        rows.append({
            "product_id": i,
            "category_id": category_name_to_id[category_name],
            "product_name": f"{brand} {product_base_name}",
            "brand_name": brand,
            "package_size": package_size,
            "unit_of_measure": unit_of_measure,
            "barcode": barcode,
            "is_perishable": is_perishable,
            "product_status": product_status,
            "current_unit_price": current_unit_price,
        })
    return pd.DataFrame(rows)


def generate_employee(store_df: pd.DataFrame, department_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    dept_ids = department_df["department_id"].tolist()
    dept_name_by_id = dict(zip(department_df["department_id"], department_df["department_name"]))
    store_open_by_id = dict(zip(store_df["store_id"], pd.to_datetime(store_df["open_date"]).dt.date))
    used_emails = set()
    employee_id = 1

    for store_id in store_df["store_id"].tolist():
        titles = ["Store Manager", "Assistant Manager"] + ["Department Manager"] * 7
        titles += random.choices(["Cashier", "Stock Associate"], weights=[4, 2], k=6)
        dept_manager_pool = dept_ids.copy()
        random.shuffle(dept_manager_pool)

        for title in titles:
            if title == "Department Manager":
                department_id = dept_manager_pool.pop()
            else:
                allowed_names = JOB_RULES[title]["departments"]
                eligible_dept_ids = [d for d in dept_ids if dept_name_by_id[d] in allowed_names]
                department_id = random.choice(eligible_dept_ids)

            first = fake.first_name()
            last = fake.last_name()
            email = f"{first.lower()}.{last.lower()}.{employee_id}@abcfoodmart.com"
            while email in used_emails:
                email = f"{first.lower()}.{last.lower()}.{employee_id}{random.randint(1,9)}@abcfoodmart.com"
            used_emails.add(email)

            if JOB_RULES[title]["pay_type"] == "hourly":
                hourly_rate = money(random.uniform(JOB_RULES[title]["hourly_min"], JOB_RULES[title]["hourly_max"]))
                annual_salary = None
            else:
                hourly_rate = None
                annual_salary = money(random.uniform(JOB_RULES[title]["salary_min"], JOB_RULES[title]["salary_max"]))

            rows.append({
                "employee_id": employee_id,
                "store_id": store_id,
                "department_id": department_id,
                "first_name": first,
                "last_name": last,
                "email_address": email,
                "phone_number": us_phone(),
                "hire_date": random_date(store_open_by_id[store_id], date(2025, 10, 31)),
                "employment_status": weighted_choice([("active", 0.82), ("inactive", 0.10), ("leave", 0.08)]),
                "job_title": title,
                "hourly_rate": hourly_rate,
                "annual_salary": annual_salary,
            })
            employee_id += 1

    return pd.DataFrame(rows)


def generate_store_department(store_df: pd.DataFrame, department_df: pd.DataFrame, employee_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    dept_managers = employee_df[employee_df["job_title"] == "Department Manager"]
    for store_id in store_df["store_id"]:
        for department_id in department_df["department_id"]:
            eligible = dept_managers[(dept_managers["store_id"] == store_id) & (dept_managers["department_id"] == department_id)]
            rows.append({
                "store_id": int(store_id),
                "department_id": int(department_id),
                "department_manager_id": int(eligible.iloc[0]["employee_id"]) if not eligible.empty else None,
            })
    return pd.DataFrame(rows)


def generate_vendor_product(vendor_df: pd.DataFrame, product_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    assigned_pairs = set()
    retail_price = dict(zip(product_df["product_id"], product_df["current_unit_price"]))
    for product_id in product_df["product_id"].tolist():
        vendor_ids = vendor_df["vendor_id"].tolist()
        vendor_count = 2 if random.random() < 0.67 else 1
        selected_vendors = random.sample(vendor_ids, k=vendor_count)
        preferred_index = random.randint(0, vendor_count - 1)
        for idx, vendor_id in enumerate(selected_vendors):
            assigned_pairs.add((vendor_id, product_id))
            rows.append({
                "vendor_id": vendor_id,
                "product_id": product_id,
                "vendor_product_code": f"VP-{vendor_id}-{product_id}",
                "unit_cost": money(float(retail_price[product_id]) * random.uniform(0.55, 0.80)),
                "lead_time_days": random.randint(2, 10),
                "is_preferred_vendor": idx == preferred_index,
            })
    while len(rows) < ROW_COUNTS["vendor_product"]:
        vendor_id = random.choice(vendor_df["vendor_id"].tolist())
        product_id = random.choice(product_df["product_id"].tolist())
        if (vendor_id, product_id) in assigned_pairs:
            continue
        assigned_pairs.add((vendor_id, product_id))
        rows.append({
            "vendor_id": vendor_id,
            "product_id": product_id,
            "vendor_product_code": f"VP-{vendor_id}-{product_id}",
            "unit_cost": money(float(retail_price[product_id]) * random.uniform(0.55, 0.80)),
            "lead_time_days": random.randint(2, 10),
            "is_preferred_vendor": False,
        })
    return pd.DataFrame(rows)


def generate_inventory(store_df: pd.DataFrame, product_df: pd.DataFrame, category_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    category_name_by_id = dict(zip(category_df["category_id"], category_df["category_name"]))
    store_open_by_id = dict(zip(store_df["store_id"], pd.to_datetime(store_df["open_date"]).dt.date))
    inventory_id = 1

    for store_id in store_df["store_id"]:
        store_open = store_open_by_id[int(store_id)]
        for _, product in product_df.iterrows():
            category_name = category_name_by_id[product["category_id"]]
            aisle_code, aisle_desc = AISLE_MAP[category_name]
            quantity = random.randint(20, 150) if bool(product["is_perishable"]) else random.randint(80, 500)
            if category_name in ["Produce", "Snacks", "Beverages", "Dairy"]:
                quantity = max(15, int(quantity * random.uniform(0.85, 1.00)))

            last_update_start = max(store_open, date(2025, 1, 1))
            rows.append({
                "inventory_id": inventory_id,
                "store_id": int(store_id),
                "product_id": int(product["product_id"]),
                "quantity_on_hand": quantity,
                "reorder_level": max(5, int(round(quantity * random.uniform(0.10, 0.20)))),
                "last_updated_at": datetime.combine(random_date(last_update_start, TODAY), datetime.min.time()) + timedelta(hours=random.randint(6, 20), minutes=random.randint(0, 59)),
                "aisle_code": aisle_code,
                "aisle_location_description": aisle_desc,
            })
            inventory_id += 1
    return pd.DataFrame(rows)


def generate_purchase_order(store_df: pd.DataFrame, vendor_df: pd.DataFrame, employee_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    managers = employee_df[employee_df["job_title"].isin(["Store Manager", "Assistant Manager", "Department Manager"])].copy()
    store_open_by_id = dict(zip(store_df["store_id"], pd.to_datetime(store_df["open_date"]).dt.date))
    po_id = 1

    for _ in range(ROW_COUNTS["purchase_order"]):
        store_id = int(random.choice(store_df["store_id"].tolist()))
        eligible = managers[managers["store_id"] == store_id]
        po_start = max(store_open_by_id[store_id], date(2025, 1, 1))
        po_date = random_date(po_start, TODAY)

        latest_expected = min(po_date + timedelta(days=10), TODAY)
        expected_delivery = random_date(po_date + timedelta(days=1), latest_expected)

        if expected_delivery < TODAY - timedelta(days=20):
            status = weighted_choice([("received", 0.70), ("cancelled", 0.08), ("shipped", 0.12), ("created", 0.10)])
        elif po_date < TODAY - timedelta(days=7):
            status = weighted_choice([("shipped", 0.42), ("created", 0.30), ("received", 0.20), ("cancelled", 0.08)])
        else:
            status = weighted_choice([("created", 0.72), ("shipped", 0.20), ("cancelled", 0.08)])

        rows.append({
            "purchase_order_id": po_id,
            "store_id": store_id,
            "vendor_id": int(random.choice(vendor_df["vendor_id"].tolist())),
            "created_by_employee_id": int(eligible.sample(1, random_state=random.randint(1, 10000)).iloc[0]["employee_id"]),
            "purchase_order_date": po_date,
            "expected_delivery_date": expected_delivery,
            "purchase_order_status": status,
        })
        po_id += 1
    return pd.DataFrame(rows)


def generate_shift_schedule(employee_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    shift_id = 1
    default_start = date(2025, 1, 1)
    end_date = TODAY

    for _, emp in employee_df.iterrows():
        emp_start = max(pd.to_datetime(emp["hire_date"]).date(), default_start)
        available_dates = [emp_start + timedelta(days=i) for i in range((end_date - emp_start).days + 1)] if emp_start <= end_date else [end_date]

        # Prefer variety across weeks when possible
        if len(available_dates) >= 28:
            week_groups = defaultdict(list)
            for d in available_dates:
                week_groups[d.isocalendar()[:2]].append(d)
            ordered_weeks = sorted(week_groups.keys())
            chosen_weeks = random.sample(ordered_weeks, k=min(6, len(ordered_weeks)))
            selected_dates = []
            for week_key in chosen_weeks:
                candidate_days = week_groups[week_key]
                if emp["job_title"] in ["Store Manager", "Assistant Manager", "Department Manager"]:
                    weekday_days = [d for d in candidate_days if d.weekday() < 5]
                    selected_dates.append(random.choice(weekday_days if weekday_days else candidate_days))
                else:
                    weekend_bias = [d for d in candidate_days if d.weekday() in [4, 5, 6]]
                    selected_dates.append(random.choice(weekend_bias if weekend_bias else candidate_days))
        else:
            # fallback if hire date is late in the year
            if len(available_dates) >= 6:
                selected_dates = sorted(random.sample(available_dates, 6))
            else:
                selected_dates = sorted(random.choices(available_dates, k=6))

        for shift_date in selected_dates:
            if emp["job_title"] in ["Cashier", "Stock Associate"]:
                start_hour = random.choice([9, 10, 11, 12, 13, 14, 15]) if shift_date.weekday() in [5, 6] else random.choice([7, 8, 9, 12, 13, 14, 15])
                length_hours = random.choice([6, 7, 8])
            else:
                start_hour = random.choice([7, 8, 9, 10])
                length_hours = random.choice([8, 9])

            shift_start = datetime(shift_date.year, shift_date.month, shift_date.day, start_hour, 0, 0)
            shift_end = shift_start + timedelta(hours=length_hours)
            status = "completed" if random.random() < 0.90 else "missed"

            rows.append({
                "shift_id": shift_id,
                "employee_id": int(emp["employee_id"]),
                "store_id": int(emp["store_id"]),
                "department_id": int(emp["department_id"]),
                "shift_start_date": shift_date,
                "shift_end_date": shift_date,
                "clock_in_time": shift_start + timedelta(minutes=random.randint(-5, 10)) if status == "completed" else None,
                "clock_out_time": shift_end + timedelta(minutes=random.randint(-10, 15)) if status == "completed" else None,
                "shift_status": status,
            })
            shift_id += 1

    return pd.DataFrame(rows).head(ROW_COUNTS["shift_schedule"]).copy()


def generate_payroll_record(employee_df: pd.DataFrame, shift_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    payroll_id = 1
    periods = [
        (date(2025, 10, 1), date(2025, 10, 31), date(2025, 11, 5)),
        (date(2025, 11, 1), date(2025, 11, 30), date(2025, 12, 5)),
    ]
    completed = shift_df[shift_df["shift_status"] == "completed"].copy()
    completed["hours"] = (pd.to_datetime(completed["clock_out_time"]) - pd.to_datetime(completed["clock_in_time"])).dt.total_seconds() / 3600.0

    for _, emp in employee_df.iterrows():
        hire_date = pd.to_datetime(emp["hire_date"]).date()
        emp_shifts = completed[completed["employee_id"] == emp["employee_id"]]

        for start_period, end_period, pay_date in periods:
            actual_start = max(start_period, hire_date)
            period_shifts = emp_shifts[
                (pd.to_datetime(emp_shifts["shift_start_date"]).dt.date >= actual_start) &
                (pd.to_datetime(emp_shifts["shift_start_date"]).dt.date <= end_period)
            ]
            hours_worked = round(period_shifts["hours"].sum(), 2)

            if pd.notna(emp["hourly_rate"]):
                gross_pay = money(hours_worked * float(emp["hourly_rate"]))
                reported_hours = hours_worked
            else:
                gross_pay = money(float(emp["annual_salary"]) / 12.0)
                reported_hours = None

            deduction_amount = money(gross_pay * random.uniform(0.10, 0.18))
            rows.append({
                "payroll_id": payroll_id,
                "employee_id": int(emp["employee_id"]),
                "store_id": int(emp["store_id"]),
                "period_start_date": actual_start,
                "period_end_date": end_period,
                "pay_date": pay_date,
                "gross_pay": gross_pay,
                "deduction_amount": deduction_amount,
                "net_pay": money(gross_pay - deduction_amount),
                "hours_worked": reported_hours,
            })
            payroll_id += 1

    return pd.DataFrame(rows)


def generate_purchase_order_line(purchase_order_df: pd.DataFrame, vendor_product_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    pol_id = 1
    products_by_vendor = defaultdict(list)
    vp_cost = {}
    for _, vp in vendor_product_df.iterrows():
        vendor_id = int(vp["vendor_id"])
        product_id = int(vp["product_id"])
        products_by_vendor[vendor_id].append(product_id)
        vp_cost[(vendor_id, product_id)] = float(vp["unit_cost"])

    for _, po in purchase_order_df.iterrows():
        vendor_id = int(po["vendor_id"])
        possible_products = products_by_vendor[vendor_id]
        selected_products = random.sample(possible_products, k=3) if len(possible_products) >= 3 else random.choices(possible_products, k=3)
        for product_id in selected_products:
            ordered_qty = random.randint(10, 120)
            rows.append({
                "purchase_order_line_id": pol_id,
                "purchase_order_id": int(po["purchase_order_id"]),
                "product_id": int(product_id),
                "ordered_quantity": ordered_qty,
                "unit_cost_at_order": money(vp_cost[(vendor_id, product_id)]),
                "received_quantity": 0,
            })
            pol_id += 1
    return pd.DataFrame(rows).head(ROW_COUNTS["purchase_order_line"]).copy()


def generate_delivery(purchase_order_df: pd.DataFrame, employee_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    final_po = purchase_order_df[purchase_order_df["purchase_order_status"].isin(["received", "cancelled"])].copy()
    candidate_po = purchase_order_df.copy() if len(final_po) < ROW_COUNTS["delivery"] else final_po.copy()
    delivery_po = candidate_po.sample(ROW_COUNTS["delivery"], random_state=SEED).sort_values("purchase_order_id")
    delivery_id = 1

    for _, po in delivery_po.iterrows():
        store_employees = employee_df[employee_df["store_id"] == po["store_id"]]
        receiver = int(store_employees.sample(1, random_state=random.randint(1, 10000)).iloc[0]["employee_id"])
        if po["purchase_order_status"] == "received":
            delivery_status = weighted_choice([("ontime", 0.60), ("delayed", 0.25), ("partial", 0.15)])
            if delivery_status == "ontime":
                delivery_date = po["expected_delivery_date"]; delay_days = 0; delay_reason = None
            elif delivery_status == "delayed":
                delay_days = random.randint(1, 3); delivery_date = min(po["expected_delivery_date"] + timedelta(days=delay_days), TODAY); delay_reason = random.choice(["traffic delay", "weather", "supplier backlog", "routing issue"])
            else:
                delay_days = random.choice([0, 1, 2]); delivery_date = min(po["expected_delivery_date"] + timedelta(days=delay_days), TODAY); delay_reason = "partial shipment"
            received_by_employee_id = receiver
        elif po["purchase_order_status"] == "cancelled":
            delivery_status = "cancelled"; delivery_date = None; delay_days = None; delay_reason = "order cancelled"; received_by_employee_id = None
        else:
            delivery_status = "cancelled"; delivery_date = None; delay_days = None; delay_reason = "not delivered"; received_by_employee_id = None

        rows.append({
            "delivery_id": delivery_id,
            "purchase_order_id": int(po["purchase_order_id"]),
            "vendor_id": int(po["vendor_id"]),
            "store_id": int(po["store_id"]),
            "received_by_employee_id": received_by_employee_id,
            "delivery_date": delivery_date,
            "delivery_status": delivery_status,
            "delay_days": delay_days,
            "delay_reason": delay_reason,
        })
        delivery_id += 1

    return pd.DataFrame(rows)


def apply_delivery_to_po_lines(purchase_order_line_df: pd.DataFrame, delivery_df: pd.DataFrame) -> pd.DataFrame:
    df = purchase_order_line_df.copy()
    delivery_status_by_po = dict(zip(delivery_df["purchase_order_id"], delivery_df["delivery_status"]))
    for idx, row in df.iterrows():
        po_id = int(row["purchase_order_id"])
        ordered_qty = int(row["ordered_quantity"])
        status = delivery_status_by_po.get(po_id)
        if status in ["ontime", "delayed"]:
            received_qty = ordered_qty
        elif status == "partial":
            received_qty = random.randint(1, max(1, ordered_qty - 1))
        else:
            received_qty = 0
        df.at[idx, "received_quantity"] = received_qty
    return df


def generate_sales_transaction(store_df: pd.DataFrame, customer_df: pd.DataFrame, employee_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    customer_df = customer_df.copy()
    high_ids = customer_df[customer_df["customer_segment"] == "high"]["customer_id"].tolist()
    medium_ids = customer_df[customer_df["customer_segment"] == "medium"]["customer_id"].tolist()
    low_ids = customer_df[customer_df["customer_segment"] == "low"]["customer_id"].tolist()
    store_weights = get_store_sales_weights(store_df)
    store_ids = store_df["store_id"].tolist()
    store_weight_values = [store_weights[int(s)] for s in store_ids]
    store_open_by_id = dict(zip(store_df["store_id"], pd.to_datetime(store_df["open_date"]).dt.date))

    for sale_id in range(1, ROW_COUNTS["sales_transaction"] + 1):
        store_id = int(random.choices(store_ids, weights=store_weight_values, k=1)[0])
        store_employees = employee_df[employee_df["store_id"] == store_id]
        eligible = store_employees[store_employees["job_title"].isin(["Cashier", "Assistant Manager", "Store Manager"])]
        if eligible.empty:
            eligible = store_employees

        sale_start = max(store_open_by_id[store_id], date(2025, 1, 1))
        sale_date = weekend_weighted_sale_date(sale_start, TODAY)
        sale_hour = hour_weighted_choice()
        attach_customer_prob = 0.68 + (0.04 if sale_date.weekday() in [5, 6] else 0) + (0.03 if sale_hour >= 17 else 0)

        if random.random() < attach_customer_prob:
            seg = random.choices(["high", "medium", "low"], weights=[30, 45, 25], k=1)[0]
            if seg == "high" and high_ids:
                customer_id = random.choice(high_ids)
            elif seg == "medium" and medium_ids:
                customer_id = random.choice(medium_ids)
            elif low_ids:
                customer_id = random.choice(low_ids)
            else:
                customer_id = random.choice(customer_df["customer_id"].tolist())
        else:
            customer_id = None

        rows.append({
            "sale_id": sale_id,
            "store_id": store_id,
            "customer_id": customer_id,
            "employee_id": int(eligible.sample(1, random_state=random.randint(1, 10000)).iloc[0]["employee_id"]),
            "sale_timestamp": datetime(sale_date.year, sale_date.month, sale_date.day, sale_hour, random.randint(0, 59), 0),
            "sales_subtotal": 0.00,
            "discount_total": 0.00,
            "tax_total": 0.00,
            "total_amount": 0.00,
            "points_earned": 0,
            "points_redeemed": 0,
        })
    return pd.DataFrame(rows)


def generate_sales_transaction_line(sales_df: pd.DataFrame, product_df: pd.DataFrame, customer_df: pd.DataFrame, store_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    line_id = 1

    customer_segment = dict(zip(customer_df["customer_id"], customer_df["customer_segment"]))
    store_borough = dict(zip(store_df["store_id"], store_df["borough"]))

    product_df = product_df.copy()
    category_id_to_name = dict(zip(range(1, len(PRODUCT_CATEGORIES) + 1), PRODUCT_CATEGORIES))
    product_df["category_name"] = product_df["category_id"].map(category_id_to_name)
    product_df["demand_weight"] = product_df["category_name"].map(CATEGORY_DEMAND_WEIGHT)

    for _, sale in sales_df.iterrows():
        sale_id = int(sale["sale_id"])
        store_id = int(sale["store_id"])
        customer_id = sale["customer_id"]

        if pd.notna(customer_id):
            seg = customer_segment.get(customer_id, "low")
        else:
            seg = "walkin"

        sale_products = product_df.copy()
        if store_borough[store_id] == "Brooklyn":
            sale_products.loc[
                sale_products["category_name"].isin(["Snacks", "Beverages", "Deli"]),
                "demand_weight"
            ] *= 1.15

        selected_products = sale_products.sample(
            n=3,
            weights=sale_products["demand_weight"],
            replace=False,
            random_state=random.randint(1, 100000)
        )

        for _, product in selected_products.iterrows():
            category_name = product["category_name"]
            unit_price = float(product["current_unit_price"])

            if seg == "high":
                quantity = random.choices([1, 2, 3, 4, 5], weights=[25, 25, 20, 15, 15], k=1)[0]
            elif seg == "medium":
                quantity = random.choices([1, 2, 3, 4], weights=[40, 30, 20, 10], k=1)[0]
            else:
                quantity = random.choices([1, 2, 3], weights=[65, 25, 10], k=1)[0]

            if category_name in ["Meat", "Seafood", "Household", "Personal Care"]:
                quantity = min(quantity, 2)

            gross_amount = unit_price * quantity

            discount_rate = 0.0
            if category_name in ["Snacks", "Beverages", "Frozen", "Bakery"]:
                if random.random() < 0.25:
                    discount_rate = random.choice([0.05, 0.10])
            elif seg == "high":
                if random.random() < 0.20:
                    discount_rate = random.choice([0.05, 0.10])

            discount_amount = money(gross_amount * discount_rate)
            line_total = money(gross_amount - discount_amount)

            rows.append({
                "sale_line_id": line_id,
                "sale_id": sale_id,
                "product_id": int(product["product_id"]),
                "quantity_sold": quantity,
                "unit_price": money(unit_price),
                "discount_amount": discount_amount,
                "line_total": line_total,
            })
            line_id += 1

    return pd.DataFrame(rows)


def finalize_sales_transactions(sales_df: pd.DataFrame, sales_line_df: pd.DataFrame) -> pd.DataFrame:
    sales = sales_df.copy()
    sales_line = sales_line_df.copy()
    sales_line["gross_line_amount"] = sales_line["unit_price"] * sales_line["quantity_sold"]
    grouped = sales_line.groupby("sale_id").agg(sales_subtotal=("gross_line_amount", "sum"), discount_total=("discount_amount", "sum"), net_sales=("line_total", "sum")).reset_index()
    sales = sales.drop(columns=["sales_subtotal", "discount_total", "tax_total", "total_amount", "points_earned", "points_redeemed"]).merge(grouped, on="sale_id", how="left")
    sales["sales_subtotal"] = sales["sales_subtotal"].fillna(0).round(2)
    sales["discount_total"] = sales["discount_total"].fillna(0).round(2)
    sales["net_sales"] = sales["net_sales"].fillna(0).round(2)
    sales["tax_total"] = (sales["net_sales"] * 0.08875).round(2)
    sales["points_earned"] = sales.apply(lambda row: int(row["net_sales"]) if pd.notna(row["customer_id"]) else 0, axis=1)
    sales["points_redeemed"] = sales.apply(lambda row: random.choice([0, 0, 0, 0, 10, 20, 30]) if pd.notna(row["customer_id"]) and row["net_sales"] >= 20 else 0, axis=1)
    sales["total_amount"] = (sales["net_sales"] - (sales["points_redeemed"] * 0.01) + sales["tax_total"]).round(2)
    sales.drop(columns=["net_sales"], inplace=True)
    return sales


def generate_payment(sales_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for payment_id, (_, sale) in enumerate(sales_df.iterrows(), start=1):
        method = weighted_choice([("cash", 0.18), ("credit_card", 0.54), ("debit_card", 0.28)])
        rows.append({
            "payment_id": payment_id,
            "sale_id": int(sale["sale_id"]),
            "payment_method": method,
            "payment_amount": money(sale["total_amount"]),
            "payment_timestamp": pd.to_datetime(sale["sale_timestamp"]) + timedelta(minutes=random.randint(0, 3)),
            "confirmation_code": None if method == "cash" else fake.bothify(text="????####????"),
        })
    return pd.DataFrame(rows)


def generate_customer_loyalty_account(customer_df: pd.DataFrame, sales_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    loyalty_customers = set(random.sample(customer_df["customer_id"].tolist(), ROW_COUNTS["customer_loyalty_account"]))
    sales_with_customer = sales_df[sales_df["customer_id"].notna()].copy()
    last_purchase = sales_with_customer.groupby("customer_id")["sale_timestamp"].max().to_dict()
    earned = sales_with_customer.groupby("customer_id")["points_earned"].sum().to_dict()
    redeemed = sales_with_customer.groupby("customer_id")["points_redeemed"].sum().to_dict()

    loyalty_id = 1
    for _, customer in customer_df.iterrows():
        customer_id = int(customer["customer_id"])
        if customer_id not in loyalty_customers:
            continue
        last_purchase_dt = last_purchase.get(customer_id)
        status = "active" if (last_purchase_dt is not None and pd.to_datetime(last_purchase_dt).date() >= (TODAY - timedelta(days=180))) else "inactive"
        rows.append({
            "loyalty_account_id": loyalty_id,
            "customer_id": customer_id,
            "points_balance": max(0, int(earned.get(customer_id, 0) - redeemed.get(customer_id, 0))),
            "account_status": status,
            "created_at": datetime.combine(customer["join_date"], datetime.min.time()) + timedelta(hours=random.randint(8, 18)),
        })
        loyalty_id += 1
    return pd.DataFrame(rows)


def generate_accounting_record(store_df: pd.DataFrame, sales_df: pd.DataFrame, purchase_order_df: pd.DataFrame, delivery_df: pd.DataFrame, po_line_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    record_id = 1
    for _, sale in sales_df.iterrows():
        sale_dt = pd.to_datetime(sale["sale_timestamp"])
        rows.append({
            "accounting_record_id": record_id,
            "store_id": int(sale["store_id"]),
            "sale_id": int(sale["sale_id"]),
            "purchase_order_id": None,
            "record_type": "revenue",
            "record_category": "sales",
            "amount": money(sale["total_amount"]),
            "record_date": sale_dt.date(),
            "description": f"Revenue from sale {int(sale['sale_id'])}",
            "fiscal_period": f"{sale_dt.year}-{sale_dt.month:02d}",
        })
        record_id += 1

    completed_delivery_po_ids = set(delivery_df[delivery_df["delivery_status"].isin(["ontime", "delayed", "partial"])]["purchase_order_id"].tolist())
    po_cost = (
        po_line_df[po_line_df["purchase_order_id"].isin(completed_delivery_po_ids)]
        .assign(total_cost=lambda df: df["received_quantity"] * df["unit_cost_at_order"])
        .groupby("purchase_order_id")["total_cost"].sum().to_dict()
    )
    po_lookup = purchase_order_df.set_index("purchase_order_id").to_dict("index")
    for po_id, cost in po_cost.items():
        po = po_lookup[po_id]
        rows.append({
            "accounting_record_id": record_id,
            "store_id": int(po["store_id"]),
            "sale_id": None,
            "purchase_order_id": int(po_id),
            "record_type": "expense",
            "record_category": "inventory_purchase",
            "amount": money(cost),
            "record_date": po["purchase_order_date"],
            "description": f"Expense for purchase order {int(po_id)}",
            "fiscal_period": f"{po['purchase_order_date'].year}-{po['purchase_order_date'].month:02d}",
        })
        record_id += 1

    while len(rows) < ROW_COUNTS["accounting_record"]:
        record_date = random_date(date(2025, 11, 1), TODAY)
        rows.append({
            "accounting_record_id": record_id,
            "store_id": int(random.choice(store_df["store_id"].tolist())),
            "sale_id": None,
            "purchase_order_id": None,
            "record_type": "expense",
            "record_category": random.choice(["utilities", "maintenance", "supplies"]),
            "amount": money(random.uniform(50, 1200)),
            "record_date": record_date,
            "description": "Store operating expense",
            "fiscal_period": f"{record_date.year}-{record_date.month:02d}",
        })
        record_id += 1

    return pd.DataFrame(rows[:ROW_COUNTS["accounting_record"]])


def apply_inventory_movements(inventory_df: pd.DataFrame, sales_line_df: pd.DataFrame, sales_df: pd.DataFrame, delivery_df: pd.DataFrame, po_line_df: pd.DataFrame, purchase_order_df: pd.DataFrame) -> pd.DataFrame:
    df = inventory_df.copy()
    index_lookup = {(int(row.store_id), int(row.product_id)): idx for idx, row in df.iterrows()}
    sales_store = dict(zip(sales_df["sale_id"], sales_df["store_id"]))
    for _, line in sales_line_df.iterrows():
        key = (int(sales_store[int(line["sale_id"])]), int(line["product_id"]))
        if key in index_lookup:
            i = index_lookup[key]
            df.at[i, "quantity_on_hand"] = max(0, int(df.at[i, "quantity_on_hand"]) - int(line["quantity_sold"]))

    completed_delivery_po_ids = set(delivery_df[delivery_df["delivery_status"].isin(["ontime", "delayed", "partial"])]["purchase_order_id"].tolist())
    po_store = dict(zip(purchase_order_df["purchase_order_id"], purchase_order_df["store_id"]))
    received_lines = po_line_df[po_line_df["purchase_order_id"].isin(completed_delivery_po_ids)]
    for _, line in received_lines.iterrows():
        key = (int(po_store[int(line["purchase_order_id"])]), int(line["product_id"]))
        if key in index_lookup:
            i = index_lookup[key]
            df.at[i, "quantity_on_hand"] = int(df.at[i, "quantity_on_hand"]) + int(line["received_quantity"])

    df["last_updated_at"] = datetime.combine(TODAY, datetime.min.time()) + timedelta(hours=18)
    return df


def validate_counts(dataframes: dict) -> None:
    print("Row count check")
    for name, expected in ROW_COUNTS.items():
        actual = len(dataframes[name])
        print(f"{name:25s} expected={expected:5d} actual={actual:5d} {'OK' if actual == expected else 'CHECK'}")


def validate_status_values(dataframes: dict) -> None:
    print("\nStatus value check")
    checks = {
        "store": (dataframes["store"]["store_status"], ALLOWED_STATUS["store"]),
        "vendor": (dataframes["vendor"]["vendor_status"], ALLOWED_STATUS["vendor"]),
        "product": (dataframes["product"]["product_status"], ALLOWED_STATUS["product"]),
        "employee": (dataframes["employee"]["employment_status"], ALLOWED_STATUS["employment"]),
        "shift": (dataframes["shift_schedule"]["shift_status"], ALLOWED_STATUS["shift"]),
        "purchase_order": (dataframes["purchase_order"]["purchase_order_status"], ALLOWED_STATUS["purchase_order"]),
        "delivery": (dataframes["delivery"]["delivery_status"], ALLOWED_STATUS["delivery"]),
        "loyalty": (dataframes["customer_loyalty_account"]["account_status"], ALLOWED_STATUS["account"]),
    }
    for name, (series, allowed) in checks.items():
        actual_values = set(series.dropna().unique())
        print(f"{name:25s} values={sorted(actual_values)} {'OK' if actual_values.issubset(allowed) else 'CHECK'}")


def validate_hire_dates(store_df: pd.DataFrame, employee_df: pd.DataFrame) -> None:
    print("\nHire date check")
    store_open = dict(zip(store_df["store_id"], pd.to_datetime(store_df["open_date"]).dt.date))
    ok = True
    for _, row in employee_df.iterrows():
        if row["hire_date"] < store_open[int(row["store_id"])]:
            ok = False; break
    print(f"store open before hire date: {'OK' if ok else 'CHECK'}")


def validate_delivery_logic(purchase_order_df: pd.DataFrame, delivery_df: pd.DataFrame, po_line_df: pd.DataFrame) -> None:
    print("\nDelivery logic check")
    po_status = dict(zip(purchase_order_df["purchase_order_id"], purchase_order_df["purchase_order_status"]))
    delivery_ok = True; partial_ok = True; date_ok = True
    for _, delivery in delivery_df.iterrows():
        po_id = int(delivery["purchase_order_id"])
        if delivery["delivery_status"] in ["ontime", "delayed", "partial"] and po_status[po_id] != "received":
            delivery_ok = False; break
        if delivery["delivery_status"] == "partial":
            lines = po_line_df[po_line_df["purchase_order_id"] == po_id]
            cond = ((lines["received_quantity"] > 0) & (lines["received_quantity"] < lines["ordered_quantity"]))
            if lines.empty or not cond.all():
                partial_ok = False; break

    po_dates = purchase_order_df.set_index("purchase_order_id")["purchase_order_date"].to_dict()
    for _, delivery in delivery_df[delivery_df["delivery_date"].notna()].iterrows():
        if pd.to_datetime(delivery["delivery_date"]).date() < po_dates[int(delivery["purchase_order_id"])]:
            date_ok = False; break
    print(f"delivery status vs PO status: {'OK' if delivery_ok else 'CHECK'}")
    print(f"partial delivery quantities: {'OK' if partial_ok else 'CHECK'}")
    print(f"purchase before delivery dates: {'OK' if date_ok else 'CHECK'}")


def validate_sales_logic(sales_df: pd.DataFrame, sales_line_df: pd.DataFrame) -> None:
    print("\nSales logic check")
    gross_by_sale = sales_line_df.assign(gross=lambda df: df["unit_price"] * df["quantity_sold"]).groupby("sale_id")["gross"].sum().round(2)
    discount_by_sale = sales_line_df.groupby("sale_id")["discount_amount"].sum().round(2)
    net_by_sale = sales_line_df.groupby("sale_id")["line_total"].sum().round(2)
    merged = sales_df.set_index("sale_id").copy()
    ok_subtotal = gross_by_sale.equals(merged["sales_subtotal"].round(2))
    ok_discount = discount_by_sale.equals(merged["discount_total"].round(2))
    ok_total = (((net_by_sale - (merged["points_redeemed"] * 0.01) + merged["tax_total"]).round(2)) == merged["total_amount"].round(2)).all()
    print(f"sales subtotal logic: {'OK' if ok_subtotal else 'CHECK'}")
    print(f"sales discount logic: {'OK' if ok_discount else 'CHECK'}")
    print(f"sales total logic: {'OK' if ok_total else 'CHECK'}")


def validate_payroll_logic(payroll_df: pd.DataFrame) -> None:
    print("\nPayroll logic check")
    ok = ((payroll_df["gross_pay"] - payroll_df["deduction_amount"]).round(2) == payroll_df["net_pay"].round(2)).all()
    date_ok = ((pd.to_datetime(payroll_df["period_start_date"]) < pd.to_datetime(payroll_df["period_end_date"])) & (pd.to_datetime(payroll_df["period_end_date"]) < pd.to_datetime(payroll_df["pay_date"]))).all()
    print(f"payroll net pay logic: {'OK' if ok else 'CHECK'}")
    print(f"payroll date order: {'OK' if date_ok else 'CHECK'}")


def validate_store_related_dates(store_df: pd.DataFrame, employee_df: pd.DataFrame, sales_df: pd.DataFrame, purchase_order_df: pd.DataFrame, delivery_df: pd.DataFrame, shift_df: pd.DataFrame, inventory_df: pd.DataFrame) -> None:
    print("\nStore-related date range check")
    store_open = dict(zip(store_df["store_id"], pd.to_datetime(store_df["open_date"]).dt.date))

    sales_bad = 0
    for _, row in sales_df.iterrows():
        if pd.to_datetime(row["sale_timestamp"]).date() < store_open[int(row["store_id"])]:
            sales_bad += 1

    po_bad = 0
    for _, row in purchase_order_df.iterrows():
        if pd.to_datetime(row["purchase_order_date"]).date() < store_open[int(row["store_id"])]:
            po_bad += 1

    delivery_bad = 0
    for _, row in delivery_df[delivery_df["delivery_date"].notna()].iterrows():
        if pd.to_datetime(row["delivery_date"]).date() < store_open[int(row["store_id"])]:
            delivery_bad += 1

    shift_bad = 0
    for _, row in shift_df.iterrows():
        if pd.to_datetime(row["shift_start_date"]).date() < store_open[int(row["store_id"])]:
            shift_bad += 1

    inventory_bad = 0
    for _, row in inventory_df.iterrows():
        if pd.to_datetime(row["last_updated_at"]).date() < store_open[int(row["store_id"])]:
            inventory_bad += 1

    print(f"sales after store open date: {'OK' if sales_bad == 0 else f'CHECK ({sales_bad})'}")
    print(f"purchase orders after store open date: {'OK' if po_bad == 0 else f'CHECK ({po_bad})'}")
    print(f"deliveries after store open date: {'OK' if delivery_bad == 0 else f'CHECK ({delivery_bad})'}")
    print(f"shifts after store open date: {'OK' if shift_bad == 0 else f'CHECK ({shift_bad})'}")
    print(f"inventory updates after store open date: {'OK' if inventory_bad == 0 else f'CHECK ({inventory_bad})'}")


def validate_loyalty_logic(loyalty_df: pd.DataFrame, sales_df: pd.DataFrame) -> None:
    print("\nLoyalty logic check")
    sales_with_customer = sales_df[sales_df["customer_id"].notna()].copy()
    last_purchase = sales_with_customer.groupby("customer_id")["sale_timestamp"].max().to_dict()
    ok = True
    for _, row in loyalty_df.iterrows():
        customer_id = row["customer_id"]
        expected = "inactive"
        last_purchase_dt = last_purchase.get(customer_id)
        if last_purchase_dt is not None and pd.to_datetime(last_purchase_dt).date() >= (TODAY - timedelta(days=180)):
            expected = "active"
        if row["account_status"] != expected:
            ok = False; break
    print(f"loyalty active/inactive logic: {'OK' if ok else 'CHECK'}")


def save_csvs(dataframes: dict) -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    ensure_dir(OUTPUT_DIR)
    for name, df in dataframes.items():
        export_df = df.drop(columns=["customer_segment"]).copy() if name == "customer" else df.copy()
        export_df.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)
    print(f"\nCSV files saved to: {OUTPUT_DIR.resolve()}")


def main() -> None:
    store_df = generate_store()
    department_df = generate_department()
    product_category_df = generate_product_category()
    customer_df = generate_customer()
    vendor_df = generate_vendor()

    product_df = generate_product(product_category_df)
    employee_df = generate_employee(store_df, department_df)
    store_department_df = generate_store_department(store_df, department_df, employee_df)

    vendor_product_df = generate_vendor_product(vendor_df, product_df)
    inventory_df = generate_inventory(store_df, product_df, product_category_df)
    purchase_order_df = generate_purchase_order(store_df, vendor_df, employee_df)
    shift_schedule_df = generate_shift_schedule(employee_df)
    payroll_record_df = generate_payroll_record(employee_df, shift_schedule_df)

    purchase_order_line_df = generate_purchase_order_line(purchase_order_df, vendor_product_df)
    delivery_df = generate_delivery(purchase_order_df, employee_df)
    purchase_order_line_df = apply_delivery_to_po_lines(purchase_order_line_df, delivery_df)

    sales_transaction_df = generate_sales_transaction(store_df, customer_df, employee_df)
    sales_transaction_line_df = generate_sales_transaction_line(sales_transaction_df, product_df, customer_df, store_df)
    sales_transaction_df = finalize_sales_transactions(sales_transaction_df, sales_transaction_line_df)
    payment_df = generate_payment(sales_transaction_df)
    customer_loyalty_account_df = generate_customer_loyalty_account(customer_df, sales_transaction_df)
    accounting_record_df = generate_accounting_record(store_df, sales_transaction_df, purchase_order_df, delivery_df, purchase_order_line_df)

    inventory_df = apply_inventory_movements(inventory_df, sales_transaction_line_df, sales_transaction_df, delivery_df, purchase_order_line_df, purchase_order_df)

    dataframes = {
        "store": store_df,
        "department": department_df,
        "product_category": product_category_df,
        "product": product_df,
        "vendor": vendor_df,
        "vendor_product": vendor_product_df,
        "customer": customer_df,
        "customer_loyalty_account": customer_loyalty_account_df,
        "employee": employee_df,
        "store_department": store_department_df,
        "inventory": inventory_df,
        "purchase_order": purchase_order_df,
        "purchase_order_line": purchase_order_line_df,
        "delivery": delivery_df,
        "sales_transaction": sales_transaction_df,
        "sales_transaction_line": sales_transaction_line_df,
        "payment": payment_df,
        "shift_schedule": shift_schedule_df,
        "payroll_record": payroll_record_df,
        "accounting_record": accounting_record_df,
    }


    save_csvs(dataframes)
    print("\nDone.")


if __name__ == "__main__":
    main()
