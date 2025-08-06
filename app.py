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
            "sowing": "जून-
