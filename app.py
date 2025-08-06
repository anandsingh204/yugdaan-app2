
import streamlit as st
from gtts import gTTS
from io import BytesIO

# Expanded crop guide data (3 crops, Hindi + English)
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
}

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

st.set_page_config(page_title="Yugdaan Crop Guide", page_icon="🌾", layout="centered")

st.title("🌾 Yugdaan Crop Guide Prototype")
st.markdown("A simple, farmer-friendly crop guide with audio and photo help.")

# Select crop and language
crop = st.selectbox("Select Crop", list(crop_guides.keys()), format_func=lambda x: crop_guides[x]['en']['title'])
lang = st.selectbox("Select Language / भाषा चुनें", ["en", "hi"], format_func=lambda x: "English" if x == "en" else "हिंदी")

guide = crop_guides[crop][lang]

st.header(guide["title"])
st.write(guide["description"])
st.markdown(f"**Sowing / बुवाई:** {guide['sowing']}")
st.markdown(f"**Irrigation / सिंचाई:** {guide['irrigation']}")
st.markdown(f"**Fertilizer / उर्वरक:** {guide['fertilizer']}")
st.markdown(f"**Harvest / कटाई:** {guide['harvest']}")

# Text-to-speech button
if st.button("Listen to Crop Guide / सुनें"):
    text_content = """
".join([
        guide["title"],
        guide["description"],
        f"Sowing: {guide['sowing']}",
        f"Irrigation: {guide['irrigation']}",
        f"Fertilizer: {guide['fertilizer']}",
        f"Harvest: {guide['harvest']}",
    ])
    audio_fp = text_to_speech(text_content, lang=lang)
    audio_bytes = audio_fp.read()
    st.audio(audio_bytes, format="audio/mp3")

# Photo upload section
st.header("Upload Photo for Help / मदद के लिए फोटो अपलोड करें")
uploaded_file = st.file_uploader("Upload a photo of your crop or soil / अपने खेत या फसल की फोटो अपलोड करें", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image / अपलोड की गई फोटो", use_column_width=True)
    st.success("Photo received! Our experts will get back to you soon. / फोटो प्राप्त हो गई है! हमारे विशेषज्ञ जल्द संपर्क करेंगे।")
