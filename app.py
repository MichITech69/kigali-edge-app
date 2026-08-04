import os
import urllib.parse
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# --- INITIAL SETUP ---
load_dotenv()
st.set_page_config(page_title="RW Welcome to Rwanda", page_icon="🇷🇼", layout="wide")

# --- API KEY HANDLING ---
env_key = os.getenv("GEMINI_API_KEY", "")

with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input("Gemini API Key", value=env_key, type="password")

api_key = api_key_input or env_key

# --- NAVIGATION ---
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["🗺️ Google Maps Explorer", "🤖 AI Concierge", "🗣️ Kinyarwanda Helper"])

# --- GOOGLE MAPS SEARCH PAGE ---
if page == "🗺️ Google Maps Explorer":
    st.title("🇷🇼 Rwanda Place & Itinerary Explorer")
    st.write("Search for **any venue, hotel, restaurant, market, or stadium** across Rwanda!")

    # Search Bar Input
    search_query = st.text_input("🔍 Search anything (e.g. Simba Supermarket, Kigali Heights, Musanze Hotel, Nyungwe)", value="Simba Supermarket Kigali")

    if search_query:
        encoded_query = urllib.parse.quote(search_query)
        maps_search_url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
        embed_map_url = f"https://maps.google.com/maps?q={encoded_query}&t=&z=13&ie=UTF8&iwloc=&output=embed"

        col_left, col_right = st.columns([1, 1.2])

        with col_left:
            st.subheader(f"Results for: '{search_query}'")
            st.write("Click below to get directions, reviews, and turn-by-turn navigation directly inside Google Maps:")
            
            # Direct Navigation Link
            st.link_button(
                f"📍 Open '{search_query}' in Google Maps App", 
                maps_search_url, 
                use_container_width=True,
                type="primary"
            )

            st.info("💡 **Tip for Visitors:** Clicking the button above will launch the native Google Maps app on mobile or desktop with directions, phone numbers, and opening hours.")

        with col_right:
            st.subheader("🗺️ Live Map Preview")
            # Embed Interactive Google Map frame
            st.components.v1.iframe(embed_map_url, height=450, scrolling=True)

# --- AI ASSISTANT PAGE ---
elif page == "🤖 AI Concierge":
    st.title("🤖 Kigali & Rwanda Travel Concierge")
    st.write("Ask anything about traveling, transport, dining, or culture in Rwanda!")
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

            if user_prompt := st.chat_input("Ask a question about Rwanda..."):
                st.session_state.messages.append({"role": "user", "content": user_prompt})
                with st.chat_message("user"):
                    st.markdown(user_prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        system_context = "You are an expert local guide for Rwanda. Provide helpful, accurate, and welcoming advice."
                        full_prompt = f"{system_context}\n\nUser Question: {user_prompt}"
                        response = model.generate_content(full_prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

# --- KINYARWANDA HELPER PAGE ---
elif page == "🗣️ Kinyarwanda Helper":
    st.title("🗣️ Kinyarwanda Phrasebook")
    st.write("Essential phrases to connect with locals in Rwanda!")
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