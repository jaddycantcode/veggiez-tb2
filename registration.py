import streamlit as st
import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

@st.cache_resource
def connect_to_mongo():
    try:
        user = st.secrets["username"]
        db_password = st.secrets["password"]
        uri = f"mongodb+srv://{user}:{db_password}@veggiez.kq0vj.mongodb.net/?retryWrites=true&w=majority&appName=veggiez"
        client = MongoClient(uri, tlsAllowInvalidCertificates=True, server_api=ServerApi('1'))
        return client
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        raise e

client = connect_to_mongo()

def run():
    placeholder = st.empty()

    with placeholder.form("registration_form"):
        st.subheader("Register for VEGGIEZ")

        user_name = st.text_input("Username*")
        password = st.text_input("Password*", type="password")
        age = st.number_input("Age", min_value=12, step=1)
        favorite_food = st.text_input("Favorite Dish")
        cooking_skill = st.selectbox("Your Cooking Skills", ["Beginner", "Intermediate", "Expert"])
        reason = st.selectbox("Why are you here?", ["Already vegetarian", "Just curious", "I want to become a vegetarian"])

        submit_button = st.form_submit_button("Register")

    if submit_button:
        try:
            db = client["veggiez"]
            collection = db["users"]

            if not user_name:
                st.error("Please enter a username.", icon="⚠️")
            elif collection.find_one({"username": user_name}):
                st.error("Username already exists.", icon="⚠️")
            elif age < 12:
                st.error("Age must be at least 12.")
            else:
                # Passwort verdaddeln mit HASH
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                document = {
                    "username": user_name,
                    "password": hashed_password,
                    "age": age,
                    "favorite_food": favorite_food,
                    "cooking_skill": cooking_skill,
                    "reason": reason,
                    "created_at": datetime.datetime.now()
                }

                collection.insert_one(document)

                st.success("Registration successful! Welcome to VEGGIEZ 🥦")
                placeholder.empty()

                st.session_state["current_page"] = "🌱 Philosophy"

        except Exception as e:
            st.error(f"An error occurred: {e}")