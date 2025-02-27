import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import random
import datetime
import calendar

@st.cache_resource
def connect_to_mongo():
    try:
        user = st.secrets["username"]
        db_password = st.secrets["password"]
        uri = f"mongodb+srv://{user}:{db_password}@veggiez.kq0vj.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
        client = MongoClient(uri, server_api=ServerApi('1'))
        return client
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        raise e

client = connect_to_mongo()

def format_ingredients(ingredients):
    if not ingredients:
        return "No ingredients available."
    if isinstance(ingredients[0], dict):
        return ", ".join([f"{item['quantity']} {item['unit']} {item['name']}" for item in ingredients])
    else:
        return ", ".join(ingredients)

def get_random_recipe(tags=[]):
    db = client["veggiez"]
    collection = db["recipes"]
    query = {"tags": {"$in": tags}} if tags else {}
    recipes = list(collection.find(query))
    return random.choice(recipes) if recipes else None

def get_seasonal_tags(month):
    seasonal_tags = {
        1: ["Brussels Sprouts", "Kale", "Leek"],
        2: ["Brussels Sprouts", "Kale", "Leek"],
        3: ["Asparagus", "Wild Garlic", "Spring Onion"],
        4: ["Asparagus", "Wild Garlic", "Spring Onion"],
        5: ["Asparagus", "Rhubarb", "Spring Vegetables"],
        6: ["Tomato", "Zucchini", "Basil"],
        7: ["Tomato", "Zucchini", "Basil"],
        8: ["Tomato", "Zucchini", "Basil"],
        9: ["Pumpkin", "Mushrooms", "Leafy Greens"],
        10: ["Pumpkin", "Mushrooms", "Leafy Greens"],
        11: ["Cabbage", "Brussels Sprouts", "Root Vegetables"],
        12: ["Cabbage", "Brussels Sprouts", "Root Vegetables"],
    }
    return seasonal_tags.get(month, [])

def get_random_seasonal_recipe():
    db = client["veggiez"]
    collection = db["seasonal_dish"]
    current_month = datetime.datetime.now().month
    tags = get_seasonal_tags(current_month)
    query = {"tags": {"$in": tags}}
    recipes = list(collection.find(query))
    return random.choice(recipes) if recipes else None

def run():
    st.title("🎲 Mystery Dish")
    st.write("Get surprised! Discover a random vegetarian dish.")

    db = client["veggiez"]
    collection = db["recipes"]
    all_tags = set()
    for recipe in collection.find():
        if "tags" in recipe:
            all_tags.update(recipe["tags"])

    selected_tags = st.multiselect("🔍 Filter by tags:", sorted(all_tags), key="mystery_dish_tags")

    if st.button("🔄 Generate Mystery Dish", key="generate_mystery_dish"):
        recipe = get_random_recipe(selected_tags)
        if recipe:
            st.subheader(f"🎉 Your Mystery Dish: {recipe.get('dish_name', 'Unknown')}")
            st.write(f"**Meat Alternative:** {recipe.get('meat_alternative', 'N/A')}")
            st.write(f"**Ingredients:** {format_ingredients(recipe.get('ingredients', []))}")
            st.write(f"**Instructions:** {recipe.get('instructions', 'No instructions available.')}")
        else:
            st.error("⚠️ No matching recipe found. Try different tags!")

    st.markdown("---")

    st.title("🎲 Mystery Seasonal Dish")
    st.write("Discover a seasonal, delicious, and simple vegetarian recipe based on the current seasonal fruits and vegetables in Germany.")

    if st.button("🔄 Generate Seasonal Mystery Dish", key="generate_seasonal_mystery_dish"):
        current_month = datetime.datetime.now().month
        month_name = calendar.month_name[current_month]
        seasonal_ingredients = get_seasonal_tags(current_month)

        st.info(f"Oh, it's the month of {month_name}! Seasonal ingredients include: {', '.join(seasonal_ingredients)}")

        recipe = get_random_seasonal_recipe()
        if recipe:
            st.subheader(f"🎉 Your Seasonal Mystery Dish: {recipe.get('dish_name', 'Unknown')}")
            st.write(f"**Meat Alternative:** {recipe.get('meat_alternative', 'N/A')}")
            st.write(f"**Ingredients:** {format_ingredients(recipe.get('ingredients', []))}")
            st.write(f"**Instructions:** {recipe.get('instructions', 'No instructions available.')}")
        else:
            st.error("⚠️ No seasonal recipe found. Please add more seasonal recipes!")

run()