import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Load API key if present in .env
load_dotenv()
env_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Kigali Edge AI", page_icon="🇷🇼", layout="wide")

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["📖 Digital Guidebook", "🤖 AI Assistant"])

# Optional API key override in sidebar
with st.sidebar:
    st.markdown("---")
    st.subheader("Settings")
    api_key_input = st.text_input("Gemini API Key", value=env_key if env_key else "", type="password")

api_key = api_key_input or env_key

# --- GUIDEBOOK DATA ---
places = [
    {
        "title": "Kigali Genocide Memorial",
        "category": "Culture & History",
        "neighborhood": "Gisozi",
        "desc": "A deeply moving site honoring victims and offering education on peace-building.",
        "tip": "Plan for 1.5 - 2 hours"
    },
    {
        "title": "Inema Arts Center",
        "category": "Culture & History",
        "neighborhood": "Kacyiru",
        "desc": "Vibrant contemporary African art center with live painting and events.",
        "tip": "Great happy hour on Thursdays"
    },
    {
        "title": "Niyo Arts Gallery",
        "category": "Culture & History",
        "neighborhood": "Kacyiru",
        "desc": "Social impact art space supporting local youth through creative programs.",
        "tip": "Traditional drumming displays"
    },
    {
        "title": "Question Coffee Cafe",
        "category": "Coffee & Dining",
        "neighborhood": "Gishushu",
        "desc": "Specialty Rwandan coffee supporting women coffee farmers across the country.",
        "tip": "Try the iced pour-over"
    },
    {
        "title": "Inzora Rooftop Cafe",
        "category": "Coffee & Dining",
        "neighborhood": "Kacyiru",
        "desc": "Cozy rooftop spot with amazing sunset views over the hills of Kigali.",
        "tip": "Perfect spot for remote work"
    },
    {
        "title": "Heaven Restaurant",
        "category": "Coffee & Dining",
        "neighborhood": "Kiyovu",
        "desc": "Upscale modern African cuisine with fresh organic local ingredients.",
        "tip": "Great cocktail menu"
    },
    {
        "title": "Kimironko Market",
        "category": "Shopping & Markets",
        "neighborhood": "Kimironko",
        "desc": "The largest and most vibrant local market for fabrics, produce, and crafts.",
        "tip": "Tailors can make custom clothes in hours"
    },
    {
        "title": "Caplaki Crafts Village",
        "category": "Shopping & Markets",
        "neighborhood": "Rugunga",
        "desc": "Collection of wooden huts selling traditional Rwandan crafts and carvings.",
        "tip": "Friendly bargaining is expected"
    },
    {
        "title": "Kigali Heights",
        "category": "Shopping & Markets",
        "neighborhood": "Kimihurura",
        "desc": "Modern shopping and commercial complex with dining, supermarkets, and cafes.",
        "tip": "Located right next to the Convention Center"
    }
]

# --- PAGE 1: DIGITAL GUIDEBOOK ---
if page == "📖 Digital Guidebook":
    st.title("🇷🇼 Welcome to Kigali")
    st.subheader("Your Curated Interactive City Guide")
    st.write("Explore top spots across the city with quick highlights and local tips!")
    st.markdown("---")

    # Filter Bar
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_cat = st.selectbox("Filter by Category", ["All Categories", "Culture & History", "Coffee & Dining", "Shopping & Markets"])
    with col_filter2:
        search_query = st.text_input("Search by spot name or neighborhood", "")

    # Filter Logic
    filtered_places = places
    if selected_cat != "All Categories":
        filtered_places = [p for p in filtered_places if p["category"] == selected_cat]
    if search_query:
        filtered_places = [p for p in filtered_places if search_query.lower() in p["title"].lower() or search_query.lower() in p["neighborhood"].lower()]

    st.write("")

    # Display Cards in Grid
    if not filtered_places:
        st.info("No places found matching your search.")
    else:
        cols = st.columns(3)
        for index, place in enumerate(filtered_places):
            col = cols[index % 3]
            with col:
                with st.container(border=True):
                    st.markdown(f"#### {place['title']}")
                    st.caption(f"📁 {place['category']} | 📍 {place['neighborhood']}")
                    st.write(place["desc"])
                    st.caption(f"💡 **Tip:** {place['tip']}")

# --- PAGE 2: AI ASSISTANT ---
elif page == "🤖 AI Assistant":
    st.title("🤖 Kigali AI Assistant")
    st.write("Ask anything about Kigali—travel spots, local tips, or general advice!")

    # Session State for User Prompt
    if "prompt_input" not in st.session_state:
        st.session_state["prompt_input"] = ""

    st.markdown("##### 💡 Quick Prompts:")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("☕ Best quiet cafes for remote work?"):
            st.session_state["prompt_input"] = "What are the best quiet cafes for remote work in Kigali?"
    with btn_col2:
        if st.button("🍲 Popular local Rwandan dishes to try?"):
            st.session_state["prompt_input"] = "What are popular local Rwandan dishes and where can I try them in Kigali?"
    with btn_col3:
        if st.button("🚕 Best way to get around Kigali?"):
            st.session_state["prompt_input"] = "What is the safest and best way to get around Kigali as a visitor?"

    user_query = st.text_input("What would you like to know about Kigali?", value=st.session_state["prompt_input"])

    if st.button("Ask AI", type="primary"):
        if not api_key:
            st.warning("Please enter your Gemini API Key in the sidebar first!")
        elif not user_query:
            st.warning("Please type a question first.")
        else:
            try:
                client = genai.Client(api_key=api_key)
                with st.spinner("Thinking..."):
                    prompt = f"You are an expert local Kigali tour guide and concierge. Answer helpful and concise: {user_query}"
                    response = client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=prompt,
                    )
                    st.success("Response:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")