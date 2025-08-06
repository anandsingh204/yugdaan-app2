import streamlit as st
from io import BytesIO
from gtts import gTTS
import datetime
import requests

# -------------------
# Sample Data & Constants
# -------------------

# Crop guides for demo (simplified)
crop_guides = {
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
    }
}

# Sample soil report data
soil_report = {
    "pH": {"value": 7.0, "ideal": "6.5 - 7.5", "rating": "Normal"},
    "Soil Salinity": {"value": 0.84, "ideal": "< 1", "rating": "Normal"},
    "Organic Carbon": {"value": 1.44, "ideal": "0.50 - 0.75", "rating": "High"},
    "Organic Matter": {"value": 2.48, "ideal": "0.89 - 1.29", "rating": "High"},
}

# Sample crop health overlays per date (simulated)
farm_health_data = {
    "2025-07-01": {"green": 70, "yellow": 20, "red": 10},
    "2025-07-08": {"green": 60, "yellow": 30, "red": 10},
    "2025-07-15": {"green": 55, "yellow": 35, "red": 10},
}

# Marketplace demo products
marketplace_products = [
    {"name": "Starter Fertilizer", "price": 225, "unit": "1 kg", "description": "Balanced nutrients for initial growth."},
    {"name": "DWS-777 Pesticide", "price": 225, "unit": "1 L", "description": "Effective pest control spray."},
]

# Crop insurance sample policies
insurance_policies = [
    {"name": "Basic Crop Cover", "premium": 500, "coverage": "Covers damage from drought and flood."},
    {"name": "Premium Crop Cover", "premium": 1500, "coverage": "Covers pests, drought, flood and other calamities."},
]

# Mandi price sample data
mandi_prices = {
    "Wheat": {"price": 2026.83, "unit": "quintal", "last_update": "2025-08-06"},
    "Mustard": {"price": 3500, "unit": "quintal", "last_update": "2025-08-05"},
}

# Weather API Setup (Replace YOUR_API_KEY with actual OpenWeatherMap API key)
OPENWEATHER_API_KEY = "cce8745e8f0664cd77af8b135789fe54"
DEFAULT_LOCATION = "Patna,IN"

# -------------------
# Helper functions
# -------------------

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

def get_weather(location=DEFAULT_LOCATION):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return None
        weather_desc = data['weather'][0]['description'].title()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return {
            "description": weather_desc,
            "temperature": temp,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "location": location
        }
    except Exception:
        return None

# -------------------
# Streamlit UI
# -------------------

st.set_page_config(page_title="Yugdaan Farm Assistant", page_icon="🌾", layout="wide")

st.title("🌾 Yugdaan Farm Assistant Prototype")

# Sidebar navigation
module = st.sidebar.selectbox("Select Module", [
    "Crop Guide",
    "Soil Testing",
    "Farm Tagging",
    "Crop Health Report",
    "Weather Alerts",
    "Marketplace",
    "Connect with Experts",
    "Crop Insurance",
    "Mandi Prices"
])

# Module: Crop Guide
if module == "Crop Guide":
    st.header("Crop Guide")
    crop = st.selectbox("Select Crop", list(crop_guides.keys()))
    lang = st.selectbox("Select Language", ["English", "Hindi"])
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

# Module: Soil Testing
elif module == "Soil Testing":
    st.header("Soil Testing Report")
    st.write("Upload your soil test report document (image/pdf) or enter parameters below.")
    uploaded_file = st.file_uploader("Upload Soil Report", type=["jpg", "jpeg", "png", "pdf"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Soil Report")
    st.subheader("Soil Parameters")
    for param, details in soil_report.items():
        st.markdown(f"**{param}**: {details['value']} (Ideal: {details['ideal']}) — Rating: {details['rating']}")

# Module: Farm Tagging
elif module == "Farm Tagging":
    st.header("Farm Tagging & Satellite Monitoring")
    st.write("This is a demo map with sample farm boundaries and crop health zones.")
    # Sample static map embed (replace with real Google Maps or Leaflet in real app)
    st.markdown("""
    ![Farm Map](https://upload.wikimedia.org/wikipedia/commons/6/62/Google_Maps_logo.svg)
    """)
    st.info("Interactive farm map with satellite overlays and health zones will appear here.")

# Module: Crop Health Report
elif module == "Crop Health Report":
    st.header("Crop Health Report")
    st.write("Sample crop health status with detected issues and recommendations.")
    st.markdown("""
    - **Date:** 2025-08-05  
    - **Crop:** Wheat  
    - **Status:** Moderate pest infestation detected  
    - **Recommendation:** Apply Neem oil spray within 3 days  
    """)
    st.button("Contact Expert")

# Module: Weather Alerts
elif module == "Weather Alerts":
    st.header("Weather Alerts & Forecast")
    location = st.text_input("Enter Location", DEFAULT_LOCATION)
    weather = get_weather(location)
    if weather:
        st.subheader(f"Weather in {weather['location']}")
        st.write(f"Description: {weather['description']}")
        st.write(f"Temperature: {weather['temperature']} °C")
        st.write(f"Humidity: {weather['humidity']}%")
        st.write(f"Wind Speed: {weather['wind_speed']} m/s")
    else:
        st.error("Could not fetch weather data. Check your API key and internet connection.")

# Module: Marketplace
elif module == "Marketplace":
    st.header("Quality Input Marketplace")
    for product in marketplace_products:
        st.subheader(product["name"])
        st.write(f"Price: ₹{product['price']} per {product['unit']}")
        st.write(product["description"])
        st.button(f"Add {product['name']} to Cart")

# Module: Connect with Experts
elif module == "Connect with Experts":
    st.header("Connect with Experts")
    st.write("Chat with agri experts to solve your problems faster.")
    st.text_area("Type your message here", placeholder="Describe your farm issue or ask a question...")

# Module: Crop Insurance
elif module == "Crop Insurance":
    st.header("Crop Insurance")
    for policy in insurance_policies:
        st.subheader(policy["name"])
        st.write(f"Premium: ₹{policy['premium']}")
        st.write(policy["coverage"])

# Module: Mandi Prices
elif module == "Mandi Prices":
    st.header("Mandi Rate & Market Linkage")
    for crop, info in mandi_prices.items():
        st.subheader(crop)
        st.write(f"Price: ₹{info['price']} per {info['unit']}")
        st.write(f"Last updated: {info['last_update']}")

