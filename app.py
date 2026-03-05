import math
import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "inventory_manager_key"

# =============================
# Upload configuration
# =============================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =============================
# MongoDB
# =============================

client = MongoClient(
    "mongodb+srv://groceryadmin:grocery123@cluster0.ba9oamp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client["grocery_store"]
inventory_col = db["inventory"]

ADMIN_PASSWORD = "1234567@"
LOW_STOCK_THRESHOLD = 5

# =============================
# Helper
# =============================

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# =============================
# React Landing Page
# =============================

@app.route("/")
def landing():
    return send_from_directory("static/landing", "index.html")

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('static/landing/assets', filename)


# =============================
# Store Page
# =============================

@app.route("/store")
def index():

    q = request.args.get("q", "")
    page = int(request.args.get("page", 1))

    per_page = 20

    query = {
        "$or": [
            {"item": {"$regex": q, "$options": "i"}},
            {"category": {"$regex": q, "$options": "i"}},
        ]
    } if q else {}

    total_items = inventory_col.count_documents(query)
    total_pages = math.ceil(total_items / per_page)

    raw_items = list(
        inventory_col.find(query)
        .sort("category", 1)
        .skip((page - 1) * per_page)
        .limit(per_page)
    )

    grouped_items = {}

    for i in raw_items:
        cat = i.get("category", "General")

        if cat not in grouped_items:
            grouped_items[cat] = []

        grouped_items[cat].append(i)

    return render_template(
        "index.html",
        grouped_items=grouped_items,
        page=page,
        total_pages=total_pages,
        q=q,
    )


# =============================
# Admin Panel
# =============================

@app.route("/admin")
def admin():

    if "logged_in" not in session:
        return redirect(url_for("login"))

    q = request.args.get("q", "")
    page = int(request.args.get("page", 1))

    per_page = 25

    query = {
        "$or": [
            {"item": {"$regex": q, "$options": "i"}},
            {"category": {"$regex": q, "$options": "i"}},
        ]
    } if q else {}

    total_items = inventory_col.count_documents(query)
    total_pages = math.ceil(total_items / per_page)

    items = list(
        inventory_col.find(query)
        .skip((page - 1) * per_page)
        .limit(per_page)
    )

    low_stock = list(
        inventory_col.find({"stock": {"$lt": LOW_STOCK_THRESHOLD}})
    )

    return render_template(
        "admin.html",
        items=items,
        low_stock_items=low_stock,
        page=page,
        total_pages=total_pages,
        q=q,
        threshold=LOW_STOCK_THRESHOLD,
    )


# =============================
# Add Item
# =============================

@app.route("/add_item", methods=["POST"])
def add_item():

    if "logged_in" not in session:
        return redirect(url_for("admin"))

    image_filename = ""

    if "image" in request.files:
        file = request.files["image"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(
                os.path.join(app.config["UPLOAD_FOLDER"], filename)
            )

            image_filename = filename

    new_item = {
        "item": request.form["item"],
        "category": request.form["category"],
        "size": request.form["size"],
        "price": float(request.form["price"]),
        "stock": int(request.form["stock"]),
        "image": image_filename,
        "last_updated": datetime.now().strftime("%d %b, %H:%M"),
    }

    inventory_col.insert_one(new_item)

    return redirect(url_for("admin"))


# =============================
# Edit Item
# =============================

@app.route("/edit_item/<id>", methods=["GET", "POST"])
def edit_item(id):

    if "logged_in" not in session:
        return redirect(url_for("admin"))

    item = inventory_col.find_one({"_id": ObjectId(id)})

    if request.method == "POST":

        update_data = {
            "item": request.form["item"],
            "category": request.form["category"],
            "size": request.form["size"],
            "price": float(request.form["price"]),
            "stock": int(request.form["stock"]),
        }

        if "image" in request.files:

            file = request.files["image"]

            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)

                file.save(
                    os.path.join(app.config["UPLOAD_FOLDER"], filename)
                )

                update_data["image"] = filename

        inventory_col.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data},
        )

        return redirect(url_for("admin"))

    return render_template("edit.html", item=item)


# =============================
# Update Stock
# =============================

@app.route("/update_stock", methods=["POST"])
def update_stock():

    item_id = request.form["item_id"]
    new_stock = int(request.form["new_stock"])

    now = datetime.now().strftime("%d %b, %H:%M")

    inventory_col.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": {"stock": new_stock, "last_updated": now}},
    )

    return redirect(url_for("admin"))


# =============================
# Delete Item
# =============================

@app.route("/delete_item/<id>")
def delete_item(id):

    if "logged_in" not in session:
        return redirect(url_for("admin"))

    inventory_col.delete_one({"_id": ObjectId(id)})

    return redirect(url_for("admin"))


# =============================
# Login
# =============================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        if request.form.get("password") == ADMIN_PASSWORD:

            session["logged_in"] = True
            return redirect(url_for("admin"))

    return render_template("login.html")


# =============================
# Logout
# =============================

@app.route("/logout")
def logout():

    session.pop("logged_in", None)

    return redirect(url_for("landing"))


# =============================
# Run Server
# =============================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")