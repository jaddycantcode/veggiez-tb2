import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def connect_to_mongo():
    try:
        user = st.secrets["username"]
        db_password = st.secrets["password"]
        uri = f"mongodb+srv://{user}:{db_password}@veggiez.kq0vj.mongodb.net/?retryWrites=true&w=majority&appName=veggiez"
        client = MongoClient(uri, tlsAllowInvalidCertificates=True, server_api=ServerApi("1"))
        return client
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        raise e

client = connect_to_mongo()

# vorgefertigten Ingredients
PREDEFINED_INGREDIENTS = {
    "vegetables": [
        "tomato", "cucumber", "carrot", "pepper", "lettuce",
        "eggplant", "zucchini", "broccoli", "spinach", "onion", "cauliflower"
    ],
    "grains": ["rice", "pasta", "quinoa", "oat"],
    "proteins": ["tofu", "bean", "lentil", "chickpea", "seitan", "egg"],
    "freezer": ["pea", "corn", "mixed vegetable"],
    "liquids & condiments": ["tomato sauce", "pesto", "cream", "butter", "olive oil", "soy sauce"]
}

def get_unit(category, ingredient):
    """
    Returns the measurement unit for the given ingredient.
    - Vegetables and eggs are measured in pieces.
    - Liquids & condiments are measured in ml.
    - Everything else is measured in grams.
    """
    if category == "vegetables" or ingredient.lower() in ["tofu", "egg"]:
        return "pieces"
    elif category == "liquids & condiments":
        return "ml"
    else:
        return "g"

def run():
    st.title("🧊 SmartFridge Match")

    # tutorial-timee
    with st.expander("📖 How to use SmartFridge"):
        st.write("""
        - **Step 1:** Add ingredients from your fridge by adjusting their quantities.
        - **Step 2:** Click 'Update Inventory' to save your selection.
        - **Step 3:** Choose a cooking time limit and press 'Find Recipes!'.
        - **Step 4:** See matching recipes based on at least **3 ingredients** you have.
        - **Step 5:** Missing ingredients will be shown so you can decide what to buy.
        - **Step 6:** Just give it a try!
        """)

    username = st.session_state.get("username")
    if not username:
        st.error("Please log in to continue.")
        return

    db = client["veggiez"]
    fridge_collection = db["fridges"]

    # Fridge-individuell laden
    fridge = fridge_collection.find_one({"username": username})
    stored_inventory = fridge.get("fridge", {}) if fridge else {}

    st.subheader("Adjust Your Fridge Inventory")
    # neues Inventar wird gebaut!
    inventory = {}

    for category, ingredients in PREDEFINED_INGREDIENTS.items():
        with st.expander(category.capitalize(), expanded=True):
            inventory[category] = {}
            for ingredient in ingredients:
                unit = get_unit(category, ingredient)
                default_qty = stored_inventory.get(category, {}).get(ingredient, 0)
                qty = st.number_input(
                    f"{ingredient.capitalize()} (in {unit})",
                    min_value=0,
                    value=default_qty,
                    key=f"{category}_{ingredient}"
                )
                inventory[category][ingredient] = qty

    # Inventar speochern
    if st.button("Update Inventory"):
        fridge_data = {"username": username, "fridge": inventory}
        fridge_collection.update_one({"username": username}, {"$set": fridge_data}, upsert=True)
        st.success("Your fridge inventory has been updated!")

    st.markdown("---")
    st.subheader("Recipe Search")
    # Time-Folter
    time_filter = st.selectbox("Maximum cooking time (in minutes):", [15, 30, 60])

    if st.button("Find Recipes!"):
        st.subheader("Matching Recipes")
        recipe_collection = db["fridge_recipes"]

        available_ingredients = []
        for cat, ing_dict in inventory.items():
            for ingredient, qty in ing_dict.items():
                if qty > 0:
                    available_ingredients.append(ingredient)

        query = {"time": {"$lte": time_filter}}
        recipes = recipe_collection.find(query)

        found_recipe = False
        for recipe in recipes:
            if "ingredient_names" in recipe:
                recipe_ingredients = recipe["ingredient_names"]
            else:
                try:
                    recipe_ingredients = [ing["name"] for ing in recipe["ingredients"]]
                except Exception:
                    recipe_ingredients = recipe["ingredients"]

            matching_ingredients = [ing for ing in recipe_ingredients if ing in available_ingredients]
            # mindestens 3 Zutaten matchen
            if len(matching_ingredients) >= 3:
                found_recipe = True
                st.write(f"**{recipe['title']}**")
                st.write("Ingredients: " + ", ".join(recipe_ingredients))
                st.write("Instructions: " + recipe.get("instructions", "No instructions provided"))
                st.write(f"Cooking Time: {recipe['time']} minutes")

                missing_ingredients = [ing for ing in recipe_ingredients if ing not in available_ingredients]
                if missing_ingredients:
                    st.write("Missing ingredients: " + ", ".join(missing_ingredients))

                if st.button(f"Cook {recipe['title']}", key=f"cook_{recipe['_id']}"):
                    for ing in recipe_ingredients:
                        for cat in inventory:
                            if ing in inventory[cat] and inventory[cat][ing] > 0:
                                inventory[cat][ing] = max(0, inventory[cat][ing] - 1)
                    fridge_collection.update_one(
                        {"username": username}, {"$set": {"fridge": inventory}}, upsert=True
                    )
                    st.success(f"Ingredients for {recipe['title']} have been updated!")

        if not found_recipe:
            st.write("No matching recipes found!")

run()