import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt


# For da connection
@st.cache_resource
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


def run():
    st.title("Login to VEGGIEZ")

    username = st.text_input("Username*")
    password = st.text_input("Password*", type="password")

    if st.button("Log in"):
        try:
            db = client["veggiez"]
            collection = db["users"]

            # Username, Passwort usw.
            user = collection.find_one({"username": username})
            if user:
                if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
                    st.session_state["username"] = username
                    # zurück zu SmartFridge
                    st.session_state["current_page"] = "🧊 SmartFridge Match"
                    st.success("Successfully logged in!")
                else:
                    st.error("Incorrect password!")
            else:
                st.error("Username does not exist!")
        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    run()