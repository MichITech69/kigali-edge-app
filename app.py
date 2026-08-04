import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# --- INITIAL SETUP ---
load_dotenv()
st.set_page_config(page_title="RW Welcome to Kigali", page_icon="🇷🇼", layout="wide")

# --- API KEY HANDLING ---
env_key = os.getenv("GEMINI_API_KEY", "")

with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input("Gemini API Key", value=env_key, type="password")

api_key = api_key_input or env_key

# --- GUIDEBOOK DATA WITH IMAGES & COORDINATES ---
places = [
    {
        "title": "Kigali Genocide Memorial",
        "category": "Culture & History",
        "neighborhood": "Gisozi",
        "desc": "A deeply moving site honoring victims and offering education on peace-building.",
        "tip": "Plan for 1.5 - 2 hours",
        "lat": -1.9306,
        "lon": 30.0606,
        "image": "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=600"
    },
    {
        "title": "Inema Arts Center",
        "category": "Culture & History",
        "neighborhood": "Kacyiru",
        "desc": "Vibrant contemporary African art center with live painting and events.",
        "tip": "Great happy hour on Thursdays",
        "lat": -1.9365,
        "lon": 30.0894,
        "image": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=600"
    },
    {
        "title": "Niyo Arts Gallery",
        "category": "Culture & History",
        "neighborhood": "Kacyiru",
        "desc": "Social impact art space supporting local youth through creative programs.",
        "tip": "Traditional drumming displays",
        "lat": -1.9328,
        "lon": 30.0877,
        "image": "https://images.unsplash.com/photo-1561214115-f2f134cc4912?w=600"
    },
    {
        "title": "Question Coffee Cafe",
        "category": "Coffee & Dining",
        "neighborhood": "Gishushu",
        "desc": "Specialty Rwandan coffee supporting women coffee farmers across the country.",
        "tip": "Try the iced pour-over",
        "lat": -1.9512,
        "lon": 30.0965,
        "image": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600"
    },
    {
        "title": "Inzora Rooftop Cafe",
        "category": "Coffee & Dining",
        "neighborhood": "Kacyiru",
        "desc": "Cozy rooftop spot with amazing sunset views over the hills of Kigali.",
        "tip": "Perfect spot for remote work",
        "lat": -1.9421,
        "lon": 30.0883,
        "image": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=600"
    },
    {
        "title": "Heaven Restaurant",
        "category": "Coffee & Dining",
        "neighborhood": "Kiyovu",
        "desc": "Upscale modern African cuisine with fresh organic local ingredients.",
        "tip": "Great cocktail menu",
        "lat": -1.9567,
        "lon": 30.0642,
        "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600"
    },
    {
        "title": "Kimironko Market",
        "category": "Shopping & Markets",
        "neighborhood": "Kimironko",
        "desc": "The largest and most vibrant local market for fabrics, produce, and crafts.",
        "tip": "Tailors can make custom clothes in hours",
        "lat": -1.9447,
        "lon": 30.1256,
        "image": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?w=600"
    },
    {
        "title": "Caplaki Crafts Village",
        "category": "Shopping & Markets",
        "neighborhood": "Rugunga",
        "desc": "Collection of wooden huts selling traditional Rwandan crafts and carvings.",
        "tip": "Friendly bargaining is expected",
        "lat": -1.9628,
        "lon": 30.0673,
        "image": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600"
    },
    {
        "title": "Kigali Heights",
        "category": "Shopping & Markets",
        "neighborhood": "Kimihurura",
        "desc": "Modern shopping and commercial complex with dining, supermarkets, and cafes.",
        "tip": "Located right next to the Convention Center",
        "lat": -1.9536,
        "lon": 30.0931,
        "image": "https://images.unsplash.com/photo-1567449303078-57ad995bd301?w=600"
    }
]

# --- NAVIGATION ---
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["📖 Digital Guidebook", "🤖 AI Assistant", "🗣️ Kinyarwanda Helper"])

# --- DIGITAL GUIDEBOOK PAGE ---
if page == "📖 Digital Guidebook":
    st.title("🇷🇼 Welcome to Kigali")
    st.header("Your Curated Interactive City Guide")
    st.write("Explore top spots across the city with quick highlights and local tips!")
    st.markdown("---")

    col_cat, col_search = st.columns(2)
    with col_cat:
        categories = ["All Categories"] + sorted(list(set(p["category"] for p in places)))
        selected_cat = st.selectbox("Filter by Category", categories)
    with col_search:
        search_query = st.text_input("Search by spot name or neighborhood")

    filtered_places = places
    if selected_cat != "All Categories":
        filtered_places = [p for p in filtered_places if p["category"] == selected_cat]
    if search_query:
        filtered_places = [p for p in filtered_places if search_query.lower() in p["title"].lower() or search_query.lower() in p["neighborhood"].lower()]

    # Map View
    with st.expander("🗺️ View Interactive Map of Spots", expanded=True):
        if filtered_places:
            map_data = [{"lat": p["lat"], "lon": p["lon"]} for p in filtered_places]
            st.map(map_data)
        else:
            st.info("No locations on map for current filter.")

    st.write("")

    cols = st.columns(3)
    for index, place in enumerate(filtered_places):
        col = cols[index % 3]
        with col:
            with st.container(border=True):
                st.image(place["image"], use_container_width=True)
                st.markdown(f"#### {place['title']}")
                st.caption(f"📁 {place['category']} | 📍 {place['neighborhood']}")
                st.write(place["desc"])
                st.caption(f"💡 **Tip:** {place['tip']}")

# --- AI ASSISTANT PAGE ---
elif page == "🤖 AI Assistant":
    st.title("🤖 Kigali Travel Concierge")
    st.write("Ask anything about traveling, transport, dining, or culture in Kigali!")
    st.markdown("---")

    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar or setup your .env file to use the AI assistant.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if user_prompt := st.chat_input("Ask a question about Kigali..."):
                st.session_state.messages.append({"role": "user", "content": user_prompt})
                with st.chat_message("user"):
                    st.markdown(user_prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        system_context = "You are an expert local guide for Kigali, Rwanda. Provide helpful, accurate, and welcoming advice."
                        full_prompt = f"{system_context}\n\nUser Question: {user_prompt}"
                        response = model.generate_content(full_prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

# --- KINYARWANDA HELPER PAGE ---
elif page == "🗣️ Kinyarwanda Helper":
    st.title("🗣️ Kinyarwanda Phrasebook")
    st.write("Essential phrases to connect with locals in Kigali!")
    st.markdown("---")

    phrases = [
        {"english": "Hello / Good day", "kinyarwanda": "Muraho", "pronunciation": "Moo-rah-ho", "usage": "General greeting anytime"},
        {"english": "Thank you", "kinyarwanda": "Murakoze", "pronunciation": "Moo-rah-koh-zeh", "usage": "Showing gratitude"},
        {"english": "How are you?", "kinyarwanda": "Amakuru?", "pronunciation": "Ah-mah-koo-roo", "usage": "Friendly check-in"},
        {"english": "I am fine / Good", "kinyarwanda": "Ni meza", "pronunciation": "Nee meh-zah", "usage": "Response to Amakuru"},
        {"english": "Yes", "kinyarwanda": "Yego", "pronunciation": "Yeh-go", "usage": "Affirmation"},
        {"english": "No", "kinyarwanda": "Oya", "pronunciation": "Oh-yah", "usage": "Negation"},
        {"english": "How much is this?", "kinyarwanda": "Ni angahe?", "pronunciation": "Nee ahn-gah-heh", "usage": "At market or shops"},
        {"english": "Goodbye", "kinyarwanda": "Mwirirwe", "pronunciation": "Mwee-reer-weh", "usage": "Daytime farewell"}
    ]

    for p in phrases:
        with st.container(border=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader(p["kinyarwanda"])
                st.caption(f"🗣️ Pronounced: *{p['pronunciation']}*")
            with col2:
                st.write(f"**English:** {p['english']}")
                st.caption(f"💡 Context: {p['usage']}")