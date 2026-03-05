import json
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["grocery_store"]
inventory_col = db["inventory"]

# Full list of 100 essential Indian grocery items
essential_inventory = [
    # 1. Grains & Flour (10)
    {"item": "Wheat Flour (Atta)", "category": "Grains & Flour", "brand": "Aashirvaad", "size": "5kg", "price": 280, "stock": 50},
    {"item": "Maida", "category": "Grains & Flour", "brand": "Fortune", "size": "1kg", "price": 45, "stock": 30},
    {"item": "Semolina (Sooji/Rava)", "category": "Grains & Flour", "brand": "Rajdhani", "size": "500g", "price": 35, "stock": 25},
    {"item": "Besan (Gram Flour)", "category": "Grains & Flour", "brand": "Tata Sampann", "size": "1kg", "price": 95, "stock": 20},
    {"item": "Corn Flour", "category": "Grains & Flour", "brand": "Weikfield", "size": "100g", "price": 30, "stock": 15},
    {"item": "Rice Flour", "category": "Grains & Flour", "brand": "MTR", "size": "500g", "price": 40, "stock": 15},
    {"item": "Poha", "category": "Grains & Flour", "brand": "Rajdhani", "size": "500g", "price": 45, "stock": 20},
    {"item": "Vermicelli (Seviyan)", "category": "Grains & Flour", "brand": "Bambino", "size": "200g", "price": 25, "stock": 20},
    {"item": "Oats", "category": "Grains & Flour", "brand": "Quaker", "size": "400g", "price": 99, "stock": 15},
    {"item": "Daliya (Broken Wheat)", "category": "Grains & Flour", "brand": "Patanjali", "size": "500g", "price": 40, "stock": 10},

    # 2. Rice (5)
    {"item": "Basmati Rice", "category": "Rice", "brand": "India Gate", "size": "1kg", "price": 120, "stock": 40},
    {"item": "Sona Masoori Rice", "category": "Rice", "brand": "Daawat", "size": "5kg", "price": 350, "stock": 20},
    {"item": "Kolam Rice", "category": "Rice", "brand": "Local", "size": "5kg", "price": 320, "stock": 15},
    {"item": "Brown Rice", "category": "Rice", "brand": "24 Mantra", "size": "1kg", "price": 110, "stock": 10},
    {"item": "Idli Rice", "category": "Rice", "brand": "MTR", "size": "1kg", "price": 60, "stock": 15},

    # 3. Pulses / Dal (10)
    {"item": "Toor Dal", "category": "Pulses / Dal", "brand": "Tata Sampann", "size": "1kg", "price": 160, "stock": 35},
    {"item": "Moong Dal", "category": "Pulses / Dal", "brand": "Organic Tattva", "size": "500g", "price": 85, "stock": 25},
    {"item": "Masoor Dal", "category": "Pulses / Dal", "brand": "Rajdhani", "size": "1kg", "price": 110, "stock": 20},
    {"item": "Chana Dal", "category": "Pulses / Dal", "brand": "Tata Sampann", "size": "1kg", "price": 100, "stock": 20},
    {"item": "Urad Dal", "category": "Pulses / Dal", "brand": "Fortune", "size": "500g", "price": 90, "stock": 20},
    {"item": "Whole Moong", "category": "Pulses / Dal", "brand": "Local", "size": "500g", "price": 75, "stock": 15},
    {"item": "Kabuli Chana", "category": "Pulses / Dal", "brand": "Tata Sampann", "size": "500g", "price": 80, "stock": 15},
    {"item": "Black Chana", "category": "Pulses / Dal", "brand": "Rajdhani", "size": "500g", "price": 60, "stock": 20},
    {"item": "Rajma", "category": "Pulses / Dal", "brand": "Chitra", "size": "500g", "price": 95, "stock": 15},
    {"item": "Lobia (Black Eyed Peas)", "category": "Pulses / Dal", "brand": "Local", "size": "500g", "price": 70, "stock": 10},

    # 4. Cooking Oils & Ghee (6)
    {"item": "Mustard Oil", "category": "Cooking Oils & Ghee", "brand": "Fortune", "size": "1L", "price": 145, "stock": 50},
    {"item": "Sunflower Oil", "category": "Cooking Oils & Ghee", "brand": "Saffola", "size": "1L", "price": 160, "stock": 40},
    {"item": "Groundnut Oil", "category": "Cooking Oils & Ghee", "brand": "Engine", "size": "1L", "price": 190, "stock": 20},
    {"item": "Refined Oil", "category": "Cooking Oils & Ghee", "brand": "Fortune", "size": "1L", "price": 135, "stock": 40},
    {"item": "Olive Oil", "category": "Cooking Oils & Ghee", "brand": "Figaro", "size": "500ml", "price": 650, "stock": 10},
    {"item": "Desi Ghee", "category": "Cooking Oils & Ghee", "brand": "Amul", "size": "500ml", "price": 310, "stock": 15},

    # 5. Salt & Sugar (4)
    {"item": "Iodized Salt", "category": "Salt & Sugar", "brand": "Tata Salt", "size": "1kg", "price": 28, "stock": 100},
    {"item": "Rock Salt (Sendha Namak)", "category": "Salt & Sugar", "brand": "Patanjali", "size": "1kg", "price": 60, "stock": 30},
    {"item": "Sugar", "category": "Salt & Sugar", "brand": "Uttam", "size": "1kg", "price": 45, "stock": 100},
    {"item": "Jaggery (Gud)", "category": "Salt & Sugar", "brand": "Local", "size": "500g", "price": 50, "stock": 25},

    # 6. Spices / Masala (15)
    {"item": "Turmeric Powder", "category": "Spices / Masala", "brand": "MDH", "size": "200g", "price": 55, "stock": 60},
    {"item": "Red Chilli Powder", "category": "Spices / Masala", "brand": "Everest", "size": "200g", "price": 75, "stock": 50},
    {"item": "Coriander Powder", "category": "Spices / Masala", "brand": "Catch", "size": "200g", "price": 50, "stock": 40},
    {"item": "Cumin Seeds", "category": "Spices / Masala", "brand": "Local", "size": "100g", "price": 80, "stock": 30},
    {"item": "Mustard Seeds", "category": "Spices / Masala", "brand": "Local", "size": "100g", "price": 30, "stock": 30},
    {"item": "Garam Masala", "category": "Spices / Masala", "brand": "Everest", "size": "100g", "price": 90, "stock": 40},
    {"item": "Chaat Masala", "category": "Spices / Masala", "brand": "MDH", "size": "100g", "price": 70, "stock": 30},
    {"item": "Black Pepper", "category": "Spices / Masala", "brand": "Local", "size": "50g", "price": 60, "stock": 20},
    {"item": "Cloves", "category": "Spices / Masala", "brand": "Local", "size": "50g", "price": 80, "stock": 15},
    {"item": "Cardamom", "category": "Spices / Masala", "brand": "Local", "size": "50g", "price": 200, "stock": 10},
    {"item": "Cinnamon", "category": "Spices / Masala", "brand": "Local", "size": "50g", "price": 50, "stock": 15},
    {"item": "Bay Leaf", "category": "Spices / Masala", "brand": "Local", "size": "20g", "price": 20, "stock": 20},
    {"item": "Fenugreek Seeds", "category": "Spices / Masala", "brand": "Local", "size": "100g", "price": 40, "stock": 20},
    {"item": "Fennel Seeds", "category": "Spices / Masala", "brand": "Local", "size": "100g", "price": 50, "stock": 20},
    {"item": "Asafoetida (Hing)", "category": "Spices / Masala", "brand": "Catch", "size": "50g", "price": 65, "stock": 25},

    # 7. Dairy Products (6)
    {"item": "Milk", "category": "Dairy Products", "brand": "Amul Gold", "size": "1L", "price": 66, "stock": 40},
    {"item": "Curd (Dahi)", "category": "Dairy Products", "brand": "Mother Dairy", "size": "400g", "price": 40, "stock": 30},
    {"item": "Paneer", "category": "Dairy Products", "brand": "Amul", "size": "200g", "price": 85, "stock": 20},
    {"item": "Butter", "category": "Dairy Products", "brand": "Amul", "size": "100g", "price": 56, "stock": 50},
    {"item": "Cheese", "category": "Dairy Products", "brand": "Britannia", "size": "200g", "price": 130, "stock": 20},
    {"item": "Buttermilk", "category": "Dairy Products", "brand": "Amul Masti", "size": "200ml", "price": 15, "stock": 40},

    # 8. Tea & Coffee (4)
    {"item": "Tea Leaves", "category": "Tea & Coffee", "brand": "Red Label", "size": "500g", "price": 250, "stock": 30},
    {"item": "Tea Bags", "category": "Tea & Coffee", "brand": "Taj Mahal", "size": "25 bags", "price": 80, "stock": 15},
    {"item": "Instant Coffee", "category": "Tea & Coffee", "brand": "Nescafe", "size": "50g", "price": 160, "stock": 25},
    {"item": "Filter Coffee", "category": "Tea & Coffee", "brand": "Bru", "size": "200g", "price": 180, "stock": 15},

    # 9. Breakfast Items (5)
    {"item": "Cornflakes", "category": "Breakfast Items", "brand": "Kellogg's", "size": "475g", "price": 195, "stock": 20},
    {"item": "Muesli", "category": "Breakfast Items", "brand": "Bagrry's", "size": "400g", "price": 350, "stock": 10},
    {"item": "Instant Oats", "category": "Breakfast Items", "brand": "Saffola Masala", "size": "40g", "price": 15, "stock": 50},
    {"item": "Peanut Butter", "category": "Breakfast Items", "brand": "Dr. Oetker", "size": "340g", "price": 170, "stock": 15},
    {"item": "Bread", "category": "Breakfast Items", "brand": "Harvest Gold", "size": "400g", "price": 45, "stock": 20},

    # 10. Snacks & Biscuits (10)
    {"item": "Parle-G Biscuits", "category": "Snacks & Biscuits", "brand": "Parle", "size": "800g", "price": 80, "stock": 100},
    {"item": "Marie Biscuits", "category": "Snacks & Biscuits", "brand": "Britannia", "size": "250g", "price": 35, "stock": 50},
    {"item": "Good Day Biscuits", "category": "Snacks & Biscuits", "brand": "Britannia", "size": "600g", "price": 120, "stock": 40},
    {"item": "Cream Biscuits", "category": "Snacks & Biscuits", "brand": "Sunfeast", "size": "100g", "price": 20, "stock": 40},
    {"item": "Cookies", "category": "Snacks & Biscuits", "brand": "Unibic", "size": "150g", "price": 40, "stock": 30},
    {"item": "Potato Chips", "category": "Snacks & Biscuits", "brand": "Lay's", "size": "50g", "price": 20, "stock": 60},
    {"item": "Namkeen", "category": "Snacks & Biscuits", "brand": "Haldiram's", "size": "200g", "price": 45, "stock": 50},
    {"item": "Kurkure", "category": "Snacks & Biscuits", "brand": "PepsiCo", "size": "90g", "price": 20, "stock": 60},
    {"item": "Khakhra", "category": "Snacks & Biscuits", "brand": "Local", "size": "200g", "price": 60, "stock": 20},
    {"item": "Roasted Peanuts", "category": "Snacks & Biscuits", "brand": "Haldiram's", "size": "100g", "price": 40, "stock": 30},

    # 11. Instant Food (5)
    {"item": "Instant Noodles", "category": "Instant Food", "brand": "Maggi", "size": "70g", "price": 14, "stock": 150},
    {"item": "Pasta", "category": "Instant Food", "brand": "Bambino", "size": "500g", "price": 70, "stock": 25},
    {"item": "Instant Soup", "category": "Instant Food", "brand": "Knorr", "size": "45g", "price": 55, "stock": 40},
    {"item": "Ready Poha Mix", "category": "Instant Food", "brand": "MTR", "size": "60g", "price": 25, "stock": 30},
    {"item": "Ready Upma Mix", "category": "Instant Food", "brand": "MTR", "size": "60g", "price": 25, "stock": 30},

    # 12. Sauces & Condiments (6)
    {"item": "Tomato Ketchup", "category": "Sauces & Condiments", "brand": "Kissan", "size": "950g", "price": 140, "stock": 25},
    {"item": "Mayonnaise", "category": "Sauces & Condiments", "brand": "FunFoods", "size": "250g", "price": 85, "stock": 20},
    {"item": "Soy Sauce", "category": "Sauces & Condiments", "brand": "Chings", "size": "200g", "price": 55, "stock": 15},
    {"item": "Vinegar", "category": "Sauces & Condiments", "brand": "Chings", "size": "200ml", "price": 45, "stock": 15},
    {"item": "Green Chilli Sauce", "category": "Sauces & Condiments", "brand": "Chings", "size": "200g", "price": 50, "stock": 15},
    {"item": "Schezwan Sauce", "category": "Sauces & Condiments", "brand": "Chings", "size": "250g", "price": 90, "stock": 20},

    # 13. Dry Fruits & Nuts (6)
    {"item": "Almonds", "category": "Dry Fruits & Nuts", "brand": "Happilo", "size": "200g", "price": 250, "stock": 15},
    {"item": "Cashews", "category": "Dry Fruits & Nuts", "brand": "Happilo", "size": "200g", "price": 300, "stock": 15},
    {"item": "Raisins", "category": "Dry Fruits & Nuts", "brand": "Happilo", "size": "200g", "price": 120, "stock": 20},
    {"item": "Pistachios", "category": "Dry Fruits & Nuts", "brand": "Happilo", "size": "200g", "price": 350, "stock": 10},
    {"item": "Walnuts", "category": "Dry Fruits & Nuts", "brand": "Happilo", "size": "200g", "price": 400, "stock": 10},
    {"item": "Peanuts", "category": "Dry Fruits & Nuts", "brand": "Local", "size": "500g", "price": 80, "stock": 30},

    # 14. Pickles & Papad (3)
    {"item": "Mango Pickle", "category": "Pickles & Papad", "brand": "Mother's Recipe", "size": "400g", "price": 110, "stock": 20},
    {"item": "Mixed Pickle", "category": "Pickles & Papad", "brand": "Priya", "size": "300g", "price": 90, "stock": 20},
    {"item": "Papad", "category": "Pickles & Papad", "brand": "Lijjat", "size": "200g", "price": 70, "stock": 50},

    # 15. Baking Items (5)
    {"item": "Baking Soda", "category": "Baking Items", "brand": "Weikfield", "size": "100g", "price": 25, "stock": 20},
    {"item": "Baking Powder", "category": "Baking Items", "brand": "Weikfield", "size": "100g", "price": 40, "stock": 20},
    {"item": "Cocoa Powder", "category": "Baking Items", "brand": "Cadbury", "size": "50g", "price": 90, "stock": 15},
    {"item": "Custard Powder", "category": "Baking Items", "brand": "Weikfield", "size": "100g", "price": 45, "stock": 15},
    {"item": "Yeast", "category": "Baking Items", "brand": "Urban Platter", "size": "50g", "price": 150, "stock": 10},
]

def migrate():
    now = datetime.now().strftime("%d %b, %H:%M")
    for item in essential_inventory:
        item["last_updated"] = now
    
    inventory_col.delete_many({}) # Clear existing
    inventory_col.insert_many(essential_inventory)
    print(f"✅ Successfully migrated {len(essential_inventory)} essential items to MongoDB!")

if __name__ == '__main__':
    migrate()