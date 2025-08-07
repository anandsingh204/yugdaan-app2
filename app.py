import streamlit as st
from io import BytesIO
from gtts import gTTS
import datetime
import requests

# --- Sample Crop Guides (All crops combined) ---
crop_guides = {
    # Wheat, Rice, Potato plus Luxury Crops examples
    "wheat": {
        "en": {
            "title": "Wheat Crop Guide",
            "description": "Wheat grows best in cool climates with moderate rainfall. It requires well-drained soil and proper irrigation.",
            "sowing": "Sow seeds in November. Prepare the land well before sowing.",
            "irrigation": "Irrigate at 15-20 days after sowing and again during flowering.",
            "fertilizer": "Use nitrogen-rich fertilizer for better yield.",
            "harvest": "Harvest in April when grains are golden and hard.",
        },
        "hi": {
            "title": "गेहूं की खेती",
            "description": "गेहूं ठंडे मौसम और मध्यम वर्षा में अच्छी तरह उगता है। इसके लिए अच्छी जल निकासी वाली मिट्टी और सही सिंचाई जरूरी है।",
            "sowing": "बीज नवंबर में बोएं। बोने से पहले जमीन अच्छी तरह तैयार करें।",
            "irrigation": "बीज बोने के 15-20 दिन बाद सिंचाई करें और फूल आने के समय भी सिंचाई करें।",
            "fertilizer": "अच्छा उत्पादन के लिए नाइट्रोजन युक्त उर्वरक का उपयोग करें।",
            "harvest": "जब दाने सुनहरे और कड़े हो जाएं तब अप्रैल में फसल काटें।",
        },
    },
    "rice": {
        "en": {
            "title": "Rice Crop Guide",
            "description": "Rice requires a warm climate with abundant water. It grows well in clayey soils and needs standing water during most of its growth period.",
            "sowing": "Sow seeds in June-July after land preparation and puddling.",
            "irrigation": "Maintain water level of 5-10 cm throughout the growing period.",
            "fertilizer": "Apply nitrogen, phosphorus, and potassium as per soil test.",
            "harvest": "Harvest when grains are mature and moisture content is low.",
        },
        "hi": {
            "title": "चावल की खेती",
            "description": "चावल को गर्म जलवायु और भरपूर पानी की आवश्यकता होती है। यह चिकनी मिट्टी में अच्छी तरह उगता है और इसके विकास के दौरान पानी जमा रहना चाहिए।",
            "sowing": "जून-जुलाई में भूमि की तैयारी और पल्लींग के बाद बीज बोएं।",
            "irrigation": "पूरे विकास काल में 5-10 सेमी पानी रखें।",
            "fertilizer": "मिट्टी परीक्षण के अनुसार नाइट्रोजन, फॉस्फोरस और पोटैशियम दें।",
            "harvest": "जब दाने पक जाएं और नमी कम हो तब फसल काटें।",
        },
    },
    "potato": {
        "en": {
            "title": "Potato Crop Guide",
            "description": "Potatoes grow best in cool climates with well-drained sandy loam soil.",
            "sowing": "Plant seed potatoes in February-March after soil preparation.",
            "irrigation": "Water regularly but avoid waterlogging.",
            "fertilizer": "Use balanced NPK fertilizers according to soil tests.",
            "harvest": "Harvest when plants start to yellow and die back.",
        },
        "hi": {
            "title": "आलू की खेती",
            "description": "आलू ठंडे मौसम और अच्छी जल निकासी वाली दोमट मिट्टी में अच्छी तरह उगता है।",
            "sowing": "फरवरी-मार्च में मिट्टी तैयार करने के बाद आलू के बीज बोएं।",
            "irrigation": "नियमित सिंचाई करें लेकिन जल जमाव से बचें।",
            "fertilizer": "मिट्टी परीक्षण के अनुसार संतुलित NPK उर्वरक का उपयोग करें।",
            "harvest": "जब पौधे पीले होने लगें और सूख जाएं तब फसल काटें।",
        },
    },
    "avocado": {
        "en": {
            "title": "Avocado Crop Guide",
            "description": "Avocado requires warm climate with well-drained soil. It has high market value and good returns.",
            "sowing": "Plant seedlings in well-prepared soil during spring.",
            "irrigation": "Regular watering during dry spells is important.",
            "fertilizer": "Use organic compost and balanced NPK fertilizers.",
            "harvest": "Harvest fruits after 6-8 months of flowering.",
        },
        "hi": {
            "title": "एवोकाडो की खेती",
            "description": "एवोकाडो को गर्म जलवायु और अच्छी जल निकासी वाली मिट्टी की आवश्यकता होती है। इसका बाजार मूल्य उच्च है।",
            "sowing": "वसंत में अच्छी तरह तैयार मिट्टी में पौधे लगाएं।",
            "irrigation": "सूखे समय में नियमित सिंचाई करें।",
            "fertilizer": "कार्बनिक खाद और संतुलित NPK उर्वरक का उपयोग करें।",
            "harvest": "फूल आने के 6-8 महीने बाद फल काटें।",
        },
    },
}

# Simple user database (in-memory)
users = {}

# For farm activity log per user (in-memory)
farm_activities = {}

# --- Helper Functions ---

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

# --- Streamlit UI ---

st.set_page_config(page_title="Yugdaan MVP Farm App", page_icon="🌾")

st.title("🌾 Yugdaan MVP Farm Assistant")

# User onboarding
if "user" not in st.session_state:
    st.header("Welcome! Please Register")
    name = st.text_input("Your Name")
    location = st.text_input("Your Location (City/District)")
    land_size = st.selectbox("Your Land Size (in acres)", ["<1", "1-5", ">5"])
    if st.button("Register"):
        if name and location and land_size:
            st.session_state.user = {"name": name, "location": location, "land_size": land_size}
            farm_activities[name] = []
            st.success(f"Welcome {name}! You are now registered.")
        else:
            st.error("Please fill all fields.")

else:
    user = st.session_state.user
    st.sidebar.header(f"Hello, {user['name']}")

    # Navigation
    menu = st.sidebar.selectbox("Menu", [
        "Crop Guide", "Farm Activity Log", "Photo Upload", "Weather Info", "Marketplace", "Contact Expert"
    ])

    if menu == "Crop Guide":
        st.header("Crop Guide")
        crop = st.selectbox("Select Crop", list(crop_guides.keys()), index=0, format_func=lambda c: crop_guides[c]['en']['title'])
        lang = st.selectbox("Language", ["English", "Hindi"])
        lang_code = "en" if lang == "English" else "hi"
        guide = crop_guides[crop][lang_code]

        st.subheader(guide["title"])
        st.write(guide["description"])
        st.markdown(f"**Sowing:** {guide['sowing']}")
        st.markdown(f"**Irrigation:** {guide['irrigation']}")
        st.markdown(f"**Fertilizer:** {guide['fertilizer']}")
        st.markdown(f"**Harvest:** {guide['harvest']}")

        if st.button("Listen to Guide"):
            text = f"{guide['title']}. {guide['description']}. Sowing: {guide['sowing']}. Irrigation: {guide['irrigation']}. Fertilizer: {guide['fertilizer']}. Harvest: {guide['harvest']}."
            audio_fp = text_to_speech(text, lang=lang_code)
            st.audio(audio_fp.read(), format="audio/mp3")

    elif menu == "Farm Activity Log":
        st.header("Farm Activity Log")
        st.write("Log your farm activities and get next-step recommendations.")
        activity = st.selectbox("Select Activity", ["Sowing", "Irrigation", "Fertilizing", "Harvesting"])
        date = st.date_input("Date", datetime.date.today())
        notes = st.text_area("Notes (optional)")

        if st.button("Add Activity"):
            entry = {"activity": activity, "date": date, "notes": notes}
            farm_activities[user["name"]].append(entry)
            st.success("Activity logged!")

        st.subheader("Your Farm Activities")
        for i, act in enumerate(farm_activities.get(user["name"], []), 1):
            st.write(f"{i}. {act['activity']} on {act['date']}. Notes: {act['notes']}")

        if farm_activities.get(user["name"]):
            st.info("Next Step Recommendation: \nBased on your recent activities, remember to monitor crop growth and prepare for pest management.")

    elif menu == "Photo Upload":
        st.header("Upload Photo for Expert Help")
        uploaded_file = st.file_uploader("Upload photo of your crop or soil", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            st.success("Photo received! Our experts will contact you soon.")

    elif menu == "Weather Info":
        st.header("Weather Information")
        location = user["location"]
        st.write(f"Showing weather for {location} (Static demo)")
        # For demo, static weather info
        st.write("Temperature: 32 °C")
        st.write("Humidity: 60%")
        st.write("Wind Speed: 10 km/h")
        st.write("Conditions: Clear Sky")

    elif menu == "Marketplace":
        st.header("Marketplace - Seeds, Fertilizers, Pesticides")
        products = [
            {"name": "Starter Fertilizer", "price": 225, "unit": "1 kg"},
            {"name": "Neem Oil Spray", "price": 300, "unit": "500 ml"},
            {"name": "High Yield Wheat Seeds", "price": 500, "unit": "1 kg"},
        ]
        for p in products:
            st.subheader(p["name"])
            st.write(f"Price: ₹{p['price']} per {p['unit']}")
            st.button(f"Add {p['name']} to Cart")

    elif menu == "Contact Expert":
        st.header("Contact Expert")
        st.write("Ask your farming questions and get expert advice.")
        user_query = st.text_area("Write your question here")
        if st.button("Send Question"):
            if user_query.strip():
                st.success("Your question has been sent! Our expert will reply soon.")
            else:
                st.error("Please enter your question.")

