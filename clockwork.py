import os
import sys
import streamlit as st
from importlib import import_module

sys.path.append(os.path.dirname(__file__))

# Alle Seiten & Funktioneen
PAGES = {
    "🌱 Philosophy": "philosophy",
    "🔑 Registration": "registration",
    "🔓 Login": "login",
    "🤖 VeggieAI Chat": "veggieai",
    "🍽️ VeggieFinder Pro": "veggiefinder",
    "🧊 SmartFridge Match": "smartfridge",
    "🎲 Mystery Dish": "mystery",
    "👨‍🍳 Jaden’s Specials": "jadenspecials"
}

def switch_page(page_name):
    st.session_state["current_page"] = page_name

def main():
    logo_path = "veggiepics/logo.png"
    menu_path = "veggiepics/menu.png"

    # für Streamlit dann
    st.set_page_config(
        page_title="Veggiez App",
        page_icon=logo_path,
        layout="wide"
    )

    # Sidebar & Anpassung von Sidebar
    with st.sidebar:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; padding-right: 10px;">
                <img src="data:image/png;base64,{get_base64(menu_path)}" width="200px" />
            </div>
            """,
            unsafe_allow_html=True
        )

        # Standardseite
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = "🌱 Philosophy"

        # Buttons
        for page_name, module_name in PAGES.items():
            if st.button(page_name, use_container_width=True):
                switch_page(page_name)

    # Hauptseite + Logo
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; align-items:center; margin-top: 20px; margin-bottom: 20px;">
            <img src="data:image/png;base64,{get_base64(logo_path)}" width="300px" />
        </div>
        """,
        unsafe_allow_html=True
    )

    page_module = PAGES.get(st.session_state["current_page"], "philosophy")

    try:
        page = import_module(page_module)
        if hasattr(page, "run"):
            page.run()
        else:
            st.error(f"🚨 Error: `{page_module}.py` does not have a `run()` function!")
    except ModuleNotFoundError:
        st.error(f"🚨 Error: `{page_module}.py` not found! Ensure the file exists.")
    except Exception as e:
        st.error(f"🚨 Unexpected error: {e}")
        st.exception(e)

# Bilder in base64 konvertieren juhu
import base64
def get_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

if __name__ == "__main__":
    main()