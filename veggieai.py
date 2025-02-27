import streamlit as st
import openai

# Open-AI Key
api_key = st.secrets["openai_api_key"]

def generate_response(prompt):
    try:
        client = openai.Client(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant specializing in vegetarian recipes and dietary advice."},
                      {"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.5  # fir creativity-level
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def run():
    st.title("🤖 VeggieAI Chat")
    st.write("Ask me about vegetarian alternatives, recipes, or cooking tips! 🥦🍽️")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Ask a question (e.g., 'How can I replace ground meat?')")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.write(user_input)

        # AI-response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(user_input)
                st.session_state.chat_history.append(("assistant", response))
                st.write(response)

    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

if __name__ == "__main__":
    run()