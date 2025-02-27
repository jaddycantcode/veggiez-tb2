import streamlit as st


def run():
    st.title("🌱 Behind the Veggiez")

    # dicke Überschrift
    st.markdown("""
        ### **Why Veggiez?**
        We aim to make living vegetarian **easier**, **funnier** and **tastier** than ever before! 🎉  
    """)

    st.success("💡 Quickly find foolproof vegetarian alternatives for your favorite dishes.")
    st.info("🍳 Explore cheap, easy and student-friendly recipes.")
    st.warning("💰 Avoid substitute products whenever possible.")

    st.markdown("### **What inspired us?**")
    st.write("""
        Many people face challenges transitioning to vegetarianism, such as:
    """)

    # Die HERAUSFORDERUNGEN!
    st.markdown("""
        - ❓ **Lack of knowledge** about vegetarian alternatives.  
        - 💸 **Expensive replacement products** that don’t fit the budget.  
        - ⏳ **Extra effort** required for meal preparation.  
        - 🍖 The belief that **meat dishes taste better**.  
    """)

    st.markdown("""
        **Let’s change that together with Veggiez!**  
        🥦 Making vegetarian living accessible, fun and delicious for everyone.  
    """)

    st.markdown("## Get to know the Veggiez Functions!")

    with st.expander("🔑 Registration & Login"):
        st.write("""
            **Unlock SmartFridge Features!**  
            Seamlessly linked with our login system, this function lets you register to gain exclusive access to the SmartFridge. Secure and easy, it’s your gateway to personalized recipe recommendations.
        """)

    with st.expander("🤖 VeggieAI Chat"):
        st.write("""
            **Your AI Culinary Assistant**  
            Got questions about vegetarian recipes? Chat with VeggieAI and get instant, expert advice on ingredient swaps, cooking tips, and more. It’s like having a gourmet chef on call!
        """)

    with st.expander("🍽️ VeggieFinder Pro"):
        st.write("""
            **From Meat to Marvel**  
            Input any meat-based dish and let VeggieFinder Pro work its magic by suggesting a foolproof vegetarian alternative. Discover new flavors while keeping your meals exciting and wholesome.
        """)

    with st.expander("🧊 SmartFridge Match"):
        st.write("""
            **Smart Cooking with Your Fridge**  
            Once you’re registered and logged in, simply enter your current fridge contents. SmartFridge Match will curate recipes based on what you have, complete with estimated preparation times.
        """)

    with st.expander("🎲 Mystery Dish"):
        st.write("""
            **Adventure in Every Bite**  
            Feeling spontaneous? Choose tags like snack, vegan, or Asian and let Mystery Dish surprise you with a randomly selected, delicious recipe. Every dish is a new adventure!
        """)

    with st.expander("👨‍🍳 Jaden’s Specials"):
        st.write("""
            **Personal Touch by Jaden**  
            In this section, I share my handpicked recipes that truly reflect my passion for vegetarian cooking:

            - **Chef's Choice: Recipe of the Week**  
              Every week, I select a standout recipe that embodies creativity and culinary excellence.

            - **Tenner for Two**  
              A budget-friendly recipe designed especially for students—costing no more than €10 and serving at least 2 people.

            Enjoy these personal specialties that blend gourmet flair with practical, everyday cooking!
        """)


if __name__ == "__main__":
    run()