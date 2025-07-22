import streamlit as st
from main import chat_with_tools  # Import from your chatbot logic file

st.set_page_config(page_title="AI Tool Assistant", page_icon="🤖")

st.title("🤖 Tool-Enabled AI Assistant")
st.markdown("Ask about the weather, currency conversion, time, coordinates, or search the web.")

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Input form
with st.form("chat_form"):
    user_input = st.text_input("Enter your query", placeholder="e.g. What's the weather in Paris?")
    submitted = st.form_submit_button("Send")

# Process input
if submitted and user_input.strip():
    with st.spinner("Thinking..."):
        try:
            response = chat_with_tools(user_input)
            # Store in session state
            st.session_state.history.append(("You", user_input))
            st.session_state.history.append(("Bot", response))
            # Show answer directly below the form
            st.markdown(f"**🧠 Answer:** {response}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Optional dropdown for chat history
with st.expander("💬 View Chat History"):
    for role, msg in st.session_state.history:
        icon = "🧑‍💻" if role == "You" else "🤖"
        st.markdown(f"**{icon} {role}:** {msg}")
