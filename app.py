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

# --- CURATED GUIDEBOOK DATA ---
places = [
    {
        "title": "Kigali Genocide Memorial",
        "category": "Culture & History",
        "neighborhood": "Gisozi, Kigali",
        "desc": "A deeply moving site honoring victims and offering education on peace-building.",
        "tip": "Plan for 1.5 - 2 hours",
        "lat": -1.9306,
        "lon": 30.0606,
        "image": "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=600",
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Kigali+Genocide+Memorial"
    },
    {
        "title": "Inema Arts Center",
        "category": "Culture & History",
        "neighborhood": "Kacyiru, Kigali",
        "desc": "Vibrant contemporary African art center with live painting and events.",
        "tip": "Great happy hour on Thursdays",
        "lat": -1.9365,
        "lon": 30.0894,
        "image": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=600",
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Inema+Arts+Center+Kigali"
    },
    {
        "title": "Question Coffee Cafe",
        "category": "Coffee & Dining",
        "neighborhood": "Gishushu, Kigali",
        "desc": "Specialty Rwandan coffee supporting women coffee farmers across the country.",
        "tip": "Try the iced pour-over",
        "lat": -1.9512,
        "lon": 30.0965,
        "image": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600",
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Question+Coffee+Kigali"
    },
    {
        "title": "Kimironko Market",
        "category": "Shopping & Markets",
        "neighborhood": "Kimironko, Kigali",
        "desc": "The largest and most vibrant local market for fabrics, produce, and crafts.",
        "tip": "Tailors can make custom clothes in hours",
        "lat": -1.9447,
        "lon": 30.1256,
        "image": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?w=600",
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Kimironko+Market+Kigali"
    },
    {
        "title": "Volcanoes National Park",
        "category": "Nature & Wildlife",
        "neighborhood": "Musanze",
        "desc": "Home to the endangered mountain gorillas and majestic Virunga volcanoes.",
        "tip": "Book gorilla trekking permits well in advance",
        "lat": -1.4800,
        "lon": 29.5300,
        "image": "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=600",
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Volcanoes+National+Park+Rwanda"
    },
    {
        "title": "Akagera National Park",
        "category": "Nature & Wildlife",
        "neighborhood": "Kayonza",
        "desc": "Rwanda's Big Five savanna park with lions, elephants, rhinos, and lakes.",
        "tip": "Take a boat safari on Lake Ihema",
        "lat": -1.8800,
        "lon": 30.7000,
        "image": "https://images.unsplash.com/photo-1534567153574-2b12153a87f0?w=600",
        "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Akagera+National+Park+Rwanda"
    }
]

# --- NAVIGATION ---
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["📖 Guidebook & Explorer", "🤖 AI Concierge", "🗣️ Kinyarwanda Helper"])

# --- GUIDEBOOK & EXPLORER PAGE ---
if page == "📖 Guidebook & Explorer":
    st.title("🇷🇼 Welcome to Rwanda")
    st.header("Interactive Guidebook & Place Search")
    st.markdown("---")

    # Section 1: Custom Live Google Search
    st.subheader("🔍 Search Any Specific Place or Business in Rwanda")
    custom_search = st.text_input("Type any restaurant, hotel, supermarket, or landmark (e.g., Simba Supermarket, Kigali Heights, Hotel des Mille Collines):")

    if custom_search:
        encoded_query = urllib.parse.quote(f"{custom_search} Rwanda")
        maps_search_url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
        embed_map_url = f"https://maps.google.com/maps?q={encoded_query}&t=&z=14&ie=UTF8&iwloc=&output=embed"

        col_left, col_right = st.columns([1, 1.2])
        with col_left:
            st.success(f"Showing results for: **{custom_search}**")
            st.link_button(
                f"📍 Open '{custom_search}' in Google Maps App", 
                maps_search_url, 
                use_container_width=True,
                type="primary"
            )
        with col_right:
            st.components.v1.iframe(embed_map_url, height=350, scrolling=True)

    st.markdown("---")

    # Section 2: Interactive Country Map & Filtering
    st.subheader("🗺️ Recommended Destinations Map")
    
    col_cat, col_filter = st.columns(2)
    with col_cat:
        categories = ["All Categories"] + sorted(list(set(p["category"] for p in places)))
        selected_cat = st.selectbox("Filter Recommendations by Category", categories)
    with col_filter:
        card_search = st.text_input("Filter Cards Below")

    filtered_places = places
    if selected_cat != "All Categories":
        filtered_places = [p for p in filtered_places if p["category"] == selected_cat]
    if card_search:
        filtered_places = [p for p in filtered_places if card_search.lower() in p["title"].lower() or card_search.lower() in p["neighborhood"].lower()]

    with st.expander("🗺️ View Interactive Map View", expanded=True):
        if filtered_places:
            import folium
            from streamlit_folium import st_folium

            m = folium.Map(location=[-1.94, 29.87], zoom_start=8, tiles="OpenStreetMap")

            for place in filtered_places:
                popup_html = f"""
                <div style="width:160px;">
                    <img src="{place['image']}" style="width:100%; border-radius:6px; margin-bottom:5px;">
                    <b>{place['title']}</b><br>
                    <small>📍 {place['neighborhood']}</small><br>
                    <a href="{place['google_maps_url']}" target="_blank">Open in Google Maps</a>
                </div>
                """
                folium.Marker(
                    location=[place["lat"], place["lon"]],
                    popup=folium.Popup(popup_html, max_width=180),
                    tooltip=place["title"],
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(m)

            st_folium(m, width="100%", height=400, returned_objects=[])

    st.markdown("---")

    # Section 3: Curated Cards
    st.subheader("✨ Curated Spot Highlights")
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
                st.link_button("📍 Open in Google Maps", place["google_maps_url"], use_container_width=True)

# --- AI CONCIERGE PAGE ---
elif page == "🤖 AI Concierge":
    st.title("🤖 Rwanda Travel Concierge")
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