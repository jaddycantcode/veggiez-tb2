import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fuzzywuzzy import process  # for missspelling
import random
import streamlit.components.v1 as components


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


# Search-Function
def search_recipe(query, recipes):
    choices = [recipe["meat_alternative"] for recipe in recipes if "meat_alternative" in recipe]

    if not choices:
        return []

    best_matches = process.extract(query, choices, limit=3)
    return [match[0] for match in best_matches if match[1] > 60]  # Only results above 60% similarity


# MAIN
def run():
    st.title("🍽️ VeggieFinder Pro")
    st.write("Find vegetarian alternatives for your favorite dishes!")

    # cooking tipsss
    tips = [
        "Try roasting your vegetables with a drizzle of olive oil and your favorite herbs for an extra burst of flavor.",
        "Add a splash of lemon juice to your greens to enhance their natural taste.",
        "Experiment with different spice blends to discover new flavors in your vegetarian dishes.",
        "Use nutritional yeast as a cheesy topping for a vegan-friendly flavor boost.",
        "Incorporate seasonal produce to make your dishes both fresh and nutritious.",
        "When sautéing greens, add a pinch of salt at the end to preserve their vibrant color.",
        "For a creamier texture, blend cooked vegetables into soups or sauces.",
        "Marinate tofu for at least 30 minutes to absorb more flavor.",
        "Sprinkle toasted sesame seeds on top of stir-fried veggies for added crunch and flavor.",
        "Try grilling your vegetables for a smoky taste that enhances their natural sweetness.",
        "Use a mix of different colored bell peppers to create visually appealing and nutritious meals.",
        "It's the easiest to crack an egg on a smooth surface!",
        "For an extra kick, add a dash of chili flakes to your vegetarian pasta dishes.",
        "Cook rice using the fingertip trick: when the water level reaches your fingertip, you've got the perfect ratio.",
        "Mix herbs like basil and oregano into your tomato sauce for a fresh twist on classic recipes.",
        "Replace cream with coconut milk in curries for a lighter, dairy-free alternative."
    ]
    tip = random.choice(tips)
    tip_html = f"""
    <html>
    <head>
    <style>
    .fixed-tip {{
      position: fixed;
      top: 5px;
      right: 10px;
      background-color: #f0f0f0;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
      z-index: 1000;
      width: 300px;
      font-family: sans-serif;
      font-size: 14px;
    }}
    </style>
    </head>
    <body>
    <div class="fixed-tip">
      <strong>Cooking Tip:</strong> {tip}
    </div>
    </body>
    </html>
    """
    components.html(tip_html, height=120)

    db = client["veggiez"]
    collection = db["recipes"]

    user_query = st.text_input("Enter your meat-based dish (e.g., 'Schnitzel'):")
    search_button = st.button("🔍 Start Search")

    if search_button and user_query:
        recipes = list(collection.find())

        if not recipes:
            st.error("⚠️ No recipes found in the database!")
            return

        # Alternativen.suche
        matches = search_recipe(user_query, recipes)

        if matches:
            for match in matches:
                recipe = collection.find_one({"meat_alternative": match})

                if recipe:
                    st.subheader(f"🌱 Alternative found for '{match}'!")
                    st.write(f"**Vegetarian Dish:** {recipe['dish_name']}")
                    st.write(f"**Ingredients:** {', '.join(recipe['ingredients'])}")
                    st.write(f"**Instructions:** {recipe['instructions']}")
                else:
                    st.warning(f"No recipe found for '{match}'.")
        else:
            st.error("❌ No matching alternatives found. Try a different search term!")


if __name__ == "__main__":
    client = connect_to_mongo()
    run()