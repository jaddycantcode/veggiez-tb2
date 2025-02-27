import streamlit as st
import os
import base64
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# für Mongooo
@st.cache_resource
def connect_to_mongo():
    try:
        user = st.secrets["username"]
        db_password = st.secrets["password"]
        uri = f"mongodb+srv://{user}:{db_password}@veggiez.kq0vj.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
        client = MongoClient(uri, server_api=ServerApi("1"))
        return client
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        raise e

client = connect_to_mongo()

# Ingredients Liste (:
def format_ingredients(ingredients):
    if not ingredients:
        return ""
    if isinstance(ingredients[0], dict):
        return ", ".join([f"{item['quantity']} {item['unit']} {item['name']}" for item in ingredients])
    else:
        return ", ".join(ingredients)

# Randomizen!
def get_random_recipe(special_type):
    db = client["veggiez"]
    collection = db["jadenspezial"]
    query = {"special_type": special_type}
    recipes = list(collection.find(query))
    if recipes:
        return random.choice(recipes)
    else:
        return None

def get_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def run():
    st.title("👨‍🍳 Jaden’s Specials")

    # Jaden-Sektion Bild usw
    with st.expander("Who's even Jaden?"):
        image_path = "veggiepics/jaden.png"  # Relativer Bildpfad
        if os.path.exists(image_path):
            image_base64 = get_base64(image_path)
            st.markdown(
                f'<img src="data:image/png;base64,{image_base64}" width="300px"/>',
                unsafe_allow_html=True
            )
        else:
            st.error("Bild nicht gefunden! Bitte sicherstellen, dass das Bild im 'veggiepics'-Ordner liegt.")

        st.write("""
        Hi there! I'm Jaden, a 22-year-old student who built this site because I know firsthand how challenging it can be to embrace a vegetarian lifestyle. Although I'm not a professional chef, my Asian heritage has exposed me to a myriad of culinary traditions from an early age. As a passionate home cook—and now, living with my vegetarian girlfriend—I’ve immersed myself in the world of delicious, budget-friendly vegetarian cooking. Welcome to my culinary journey, where I share recipes crafted with heart and a love for food!
        """)

    st.write("Discover my personal recipes: Chef's Choice and Tenner for Two, specially curated for you!")

    special_option = st.selectbox("Choose a special recipe:",
                                  ["Chef's Choice: Recipe of the Week", "Tenner for Two"])

    if special_option == "Chef's Choice: Recipe of the Week":
        special_type = "chef_choice"
        st.subheader("Chef's Choice: Recipe of the Week")
        st.write("Enjoy my hand-picked recipe that I love the most this week!")
    else:
        special_type = "tenner_for_two"
        st.subheader("Tenner for Two")
        st.write("A budget-friendly recipe for students: serves at least 2 people and costs under €10.")

    if st.button("Show Recipe"):
        recipe = get_random_recipe(special_type)
        if recipe:
            st.subheader(f"Your Recipe: {recipe.get('dish_name', 'Unknown Recipe')}")
            st.write(f"**Ingredients:** {format_ingredients(recipe.get('ingredients', []))}")
            st.write(f"**Instructions:** {recipe.get('instructions', 'No instructions provided.')}")
        else:
            st.error("⚠️ No recipe found for this special type. Please add recipes to the 'jadenspezial' collection!")

if __name__ == "__main__":
    run()