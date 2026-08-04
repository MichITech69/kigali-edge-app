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
    # --- KIGALI ---
    {
        "title": "Kigali Genocide Memorial",
        "category": "Culture & History",
        "neighborhood": "Gisozi, Kigali",
        "desc": "A deeply moving site honoring victims and offering education on peace-building.",
        "tip": "Plan for 1.5 - 2 hours",
        "lat": -1.9306,
        "lon": 30.0606,
        "image": "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=600"
    },
    {
        "title": "Inema Arts Center",
        "category": "Culture & History",
        "neighborhood": "Kacyiru, Kigali",
        "desc": "Vibrant contemporary African art center with live painting and events.",
        "tip": "Great happy hour on Thursdays",
        "lat": -1.9365,
        "lon": 30.0894,
        "image": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=600"
    },
    # --- NORTHERN PROVINCE ---
    {
        "title": "Volcanoes National Park",
        "category": "Nature & Wildlife",
        "neighborhood": "Musanze",
        "desc": "Home to the endangered mountain gorillas and majestic Virunga volcanoes.",
        "tip": "Book gorilla trekking permits well in advance",
        "lat": -1.4800,
        "lon": 29.5300,
        "image": "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=600"
    },
    # --- WESTERN PROVINCE ---
    {
        "title": "Lake Kivu Boardwalk & Beaches",
        "category": "Nature & Wildlife",
        "neighborhood": "Rubavu / Gisenyi",
        "desc": "Scenic lakeside resort town perfect for boat tours, relaxation, and water sports.",
        "tip": "Great evening sunset views over Lake Kivu",
        "lat": -1.7003,
        "lon": 29.2562,
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600"
    },
    # --- SOUTHERN PROVINCE ---
    {
        "title": "King's Palace Museum",
        "category": "Culture & History",
        "neighborhood": "Nyanza",
        "desc": "Traditional royal residence showcasing royal Inyambo long-horned cattle.",
        "tip": "Listen to traditional praise singers tending to the cattle",
        "lat": -2.3510,
        "lon": 29.7505,
        "image": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600"
    },
    {
        "title": "Nyungwe National Park",
        "category": "Nature & Wildlife",
        "neighborhood": "Rusizi",
        "desc": "Ancient montane rainforest featuring chimpanzees and a high-canopy walkway.",
        "tip": "Experience the famous Canopy Walkway",
        "lat": -2.4883,
        "lon": 29.2314,
        "image": "https://images.unsplash.com/photo-1511497584788-876761c119ef?w=600"
    },
    # --- EASTERN PROVINCE ---
    {
        "title": "Akagera National Park",
        "category": "Nature & Wildlife",
        "neighborhood": "Kayonza",
        "desc": "Rwanda's Big Five savanna park with lions, elephants, rhinos, and lakes.",
        "tip": "Take a boat safari on Lake Ihema",
        "lat": -1.8800,
        "lon": 30.7000,
        "image": "https://images.unsplash.com/photo-1534567153574-2b12153a87f0?w=600"
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
    # Map View (Interactive 3D / Pan / Zoom Map)
    # Map View (Countrywide Interactive View)
    # Map View (Countrywide Interactive View)
    # Map View (Countrywide Interactive View)
    # Map View (Rich Interactive Explorer)
    with st.expander("🗺️ Countrywide Travel Explorer Map", expanded=True):
        if filtered_places:
            import folium
            from streamlit_folium import st_folium

            # Create base map centered on Rwanda
            m = folium.Map(location=[-1.94, 29.87], zoom_start=9, tiles="OpenStreetMap")

            # Add Satellite / Street view toggle
            folium.TileLayer("cartodbpositron", name="Light Map").add_to(m)
            folium.TileLayer(
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                attr="Esri",
                name="Satellite View"
            ).add_to(m)

            # Add markers for all spots
            for place in filtered_places:
                popup_html = f"""
                <div style="width:180px;">
                    <img src="{place['image']}" style="width:100%; border-radius:6px; margin-bottom:5px;">
                    <b>{place['title']}</b><br>
                    <small>📍 {place['neighborhood']}</small><br>
                    <small>📁 {place['category']}</small>
                </div>
                """
                folium.Marker(
                    location=[place["lat"], place["lon"]],
                    popup=folium.Popup(popup_html, max_width=200),
                    tooltip=place["title"],
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(m)

            folium.LayerControl().add_to(m)
            st_folium(m, width="100%", height=450, returned_objects=[])
        else:
            st.info("No locations match current search criteria.")
            
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