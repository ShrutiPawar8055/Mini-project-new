"""Internationalisation for the Crop Recommendation System.

All user-facing copy lives here so the UI code stays free of hard-coded text.
Use `t(key)` for UI strings and `crop_name(crop)` for crop labels.
"""

import streamlit as st

DEFAULT_LANGUAGE = "en"

LANGUAGES = {
    "en": "English",
    "hi": "हिंदी",
    "mr": "मराठी",
}

# Crop labels per language, keyed by the model's class name.
CROP_NAMES = {
    "en": {
        "apple": "Apple",
        "banana": "Banana",
        "blackgram": "Black Gram",
        "chickpea": "Chickpea",
        "coconut": "Coconut",
        "coffee": "Coffee",
        "cotton": "Cotton",
        "grapes": "Grapes",
        "jute": "Jute",
        "kidneybeans": "Kidney Beans",
        "lentil": "Lentil",
        "maize": "Maize",
        "mango": "Mango",
        "mothbeans": "Moth Beans",
        "mungbean": "Mung Bean",
        "muskmelon": "Muskmelon",
        "orange": "Orange",
        "papaya": "Papaya",
        "pigeonpeas": "Pigeon Peas",
        "pomegranate": "Pomegranate",
        "rice": "Rice",
        "watermelon": "Watermelon",
    },
    "hi": {
        "apple": "सेब",
        "banana": "केला",
        "blackgram": "उड़द",
        "chickpea": "चना",
        "coconut": "नारियल",
        "coffee": "कॉफ़ी",
        "cotton": "कपास",
        "grapes": "अंगूर",
        "jute": "जूट",
        "kidneybeans": "राजमा",
        "lentil": "मसूर",
        "maize": "मक्का",
        "mango": "आम",
        "mothbeans": "मोठ",
        "mungbean": "मूंग",
        "muskmelon": "खरबूज़ा",
        "orange": "संतरा",
        "papaya": "पपीता",
        "pigeonpeas": "अरहर",
        "pomegranate": "अनार",
        "rice": "चावल",
        "watermelon": "तरबूज़",
    },
    "mr": {
        "apple": "सेब",
        "banana": "केळी",
        "blackgram": "उडीद",
        "chickpea": "हरभरा",
        "coconut": "नारळ",
        "coffee": "कॉफी",
        "cotton": "कापूस",
        "grapes": "द्राक्षे",
        "jute": "ताग",
        "kidneybeans": "राजमा",
        "lentil": "मसूर",
        "maize": "मका",
        "mango": "आंबा",
        "mothbeans": "मटकी",
        "mungbean": "मूग",
        "muskmelon": "खरबूज",
        "orange": "संत्रा",
        "papaya": "पपई",
        "pigeonpeas": "तूर",
        "pomegranate": "डाळिंब",
        "rice": "भात",
        "watermelon": "टरबूज",
    },
}

# Emojis are language independent.
CROP_EMOJI = {
    "apple": "🍎",
    "banana": "🍌",
    "blackgram": "🫘",
    "chickpea": "🫘",
    "coconut": "🥥",
    "coffee": "☕",
    "cotton": "☁️",
    "grapes": "🍇",
    "jute": "🌿",
    "kidneybeans": "🫘",
    "lentil": "🫘",
    "maize": "🌽",
    "mango": "🥭",
    "mothbeans": "🫘",
    "mungbean": "🫛",
    "muskmelon": "🍈",
    "orange": "🍊",
    "papaya": "🍈",
    "pigeonpeas": "🫛",
    "pomegranate": "🍎",
    "rice": "🌾",
    "watermelon": "🍉",
}

TRANSLATIONS = {
    "en": {
        "app_title": "Crop Recommendation System",
        "language": "Language",
        "welcome": "Signed in as **{name}**",
        "logout": "Log out",
        # Auth
        "auth_action": "Sign in or create an account",
        "auth_signin": "Log in",
        "auth_signup": "Sign up",
        "email": "Email",
        "password": "Password",
        "confirm_password": "Confirm password",
        "login_button": "Log in",
        "signup_button": "Create account",
        "login_hero_subtitle": "Sign in to get crop recommendations for your field.",
        "login_error": "Incorrect email or password.",
        "login_empty": "Please enter your email and password.",
        "signup_empty": "Please enter an email and a password.",
        "signup_mismatch": "The passwords do not match.",
        "signup_weak": "Use a password of at least 6 characters.",
        "signup_confirm_email": "Account created. Confirm your address at {email}, then log in.",
        "signup_error": "Could not create the account: {message}",
        "auth_not_configured": "Authentication is not configured. Set SUPABASE_URL and SUPABASE_KEY.",
        "auth_offline": "Cannot reach the sign-in service. Please try again.",
        # Sidebar
        "about": "About",
        "about_text": (
            "This app recommends the crop best suited to your soil and "
            "climate, using a machine learning model trained on the "
            "Kaggle Crop Recommendation dataset."
        ),
        "how_it_works": "How it works",
        "step_1": "Enter your soil nutrients and climate conditions",
        "step_2": "Click **Recommend Crop**",
        "step_3": "Review the best crop and the alternatives",
        "model": "Model",
        "algorithm": "Algorithm",
        "crops": "Crops",
        "inputs": "Inputs",
        "inputs_value": "7 soil & climate features",
        "preprocessing": "Preprocessing",
        "preprocessing_value": "IQR capping + standard scaling",
        "dataset_link": "Dataset on Kaggle",
        # Hero
        "hero_title": "Crop Recommendation System",
        "hero_subtitle": (
            "Find the most suitable crop for your field from soil nutrients "
            "and climate conditions, powered by <b>{model}</b>."
        ),
        # Form
        "field_conditions": "Field Conditions",
        "example_label": "Try an example from the test set",
        "custom_values": "Custom values",
        "example_option": "Example: {crop}",
        "soil": "Soil",
        "climate": "Climate",
        "recommend_button": "Recommend Crop",
        # Result
        "recommendation": "Recommendation",
        "empty_info": (
            "Enter your field conditions on the left, or pick an example, "
            "then click **Recommend Crop** to see the best crop for your field."
        ),
        "recommended_crop": "Recommended crop",
        "confidence": "Confidence",
        "top_crops": "Top 3 crops",
        "tab_probabilities": "Probabilities",
        "tab_inputs": "Your Inputs",
        "probability": "Probability",
        "probabilities_caption": "Crops with a probability above 0%, up to the top 10.",
        "parameter": "Parameter",
        "value": "Value",
        "unit": "Unit",
        "footer": "Powered by {model} · Walchand College of Engineering, Sangli",
        # History
        "history_title": "Prediction History",
        "history_empty": "No predictions yet. Your recommendations will be saved here.",
        "history_total": "Total predictions",
        "history_top_crop": "Most recommended",
        "history_avg_confidence": "Average confidence",
        "history_date": "Date & time",
        "history_download": "Download CSV",
        "history_clear": "Clear history",
        # Feature labels
        "feat_N": "Nitrogen (N)",
        "help_N": "Nitrogen content in the soil",
        "feat_P": "Phosphorus (P)",
        "help_P": "Phosphorus content in the soil",
        "feat_K": "Potassium (K)",
        "help_K": "Potassium content in the soil",
        "feat_ph": "Soil pH",
        "help_ph": "Acidity of the soil: below 7 is acidic, above 7 is alkaline",
        "feat_temperature": "Temperature (°C)",
        "help_temperature": "Average temperature during the growing season",
        "feat_humidity": "Humidity (%)",
        "help_humidity": "Average relative humidity",
        "feat_rainfall": "Rainfall (mm)",
        "help_rainfall": "Average rainfall",
    },
    "hi": {
        "app_title": "फसल अनुशंसा प्रणाली",
        "language": "भाषा",
        "welcome": "**{name}** के रूप में साइन इन",
        "logout": "लॉग आउट",
        # Auth
        "auth_action": "साइन इन करें या खाता बनाएँ",
        "auth_signin": "लॉग इन",
        "auth_signup": "साइन अप",
        "email": "ईमेल",
        "password": "पासवर्ड",
        "confirm_password": "पासवर्ड की पुष्टि करें",
        "login_button": "लॉग इन करें",
        "signup_button": "खाता बनाएँ",
        "login_hero_subtitle": "अपने खेत के लिए फसल सुझाव पाने हेतु साइन इन करें।",
        "login_error": "ईमेल या पासवर्ड गलत है।",
        "login_empty": "कृपया अपना ईमेल और पासवर्ड दर्ज करें।",
        "signup_empty": "कृपया ईमेल और पासवर्ड दर्ज करें।",
        "signup_mismatch": "पासवर्ड मेल नहीं खाते।",
        "signup_weak": "कम से कम 6 अक्षरों का पासवर्ड रखें।",
        "signup_confirm_email": "खाता बन गया। {email} पर अपना पता सत्यापित करें, फिर लॉग इन करें।",
        "signup_error": "खाता नहीं बन सका: {message}",
        "auth_not_configured": "प्रमाणीकरण कॉन्फ़िगर नहीं है। SUPABASE_URL और SUPABASE_KEY सेट करें।",
        "auth_offline": "साइन इन सेवा से संपर्क नहीं हो सका। कृपया पुनः प्रयास करें।",
        # Sidebar
        "about": "परिचय",
        "about_text": (
            "यह ऐप Kaggle क्रॉप रेकमेंडेशन डेटासेट पर प्रशिक्षित मशीन लर्निंग "
            "मॉडल का उपयोग करके आपकी मिट्टी और जलवायु के लिए सबसे उपयुक्त "
            "फसल की सिफारिश करता है।"
        ),
        "how_it_works": "यह कैसे काम करता है",
        "step_1": "अपनी मिट्टी के पोषक तत्व और जलवायु स्थितियाँ दर्ज करें",
        "step_2": "**फसल की सिफारिश करें** पर क्लिक करें",
        "step_3": "सर्वोत्तम फसल और विकल्पों की समीक्षा करें",
        "model": "मॉडल",
        "algorithm": "एल्गोरिदम",
        "crops": "फसलें",
        "inputs": "इनपुट",
        "inputs_value": "7 मिट्टी और जलवायु विशेषताएँ",
        "preprocessing": "प्रीप्रोसेसिंग",
        "preprocessing_value": "IQR कैपिंग + मानक स्केलिंग",
        "dataset_link": "Kaggle पर डेटासेट",
        # Hero
        "hero_title": "फसल अनुशंसा प्रणाली",
        "hero_subtitle": (
            "मिट्टी के पोषक तत्वों और जलवायु स्थितियों से अपने खेत के लिए "
            "सबसे उपयुक्त फसल खोजें, <b>{model}</b> द्वारा संचालित।"
        ),
        # Form
        "field_conditions": "खेत की स्थितियाँ",
        "example_label": "परीक्षण सेट से एक उदाहरण आज़माएँ",
        "custom_values": "कस्टम मान",
        "example_option": "उदाहरण: {crop}",
        "soil": "मिट्टी",
        "climate": "जलवायु",
        "recommend_button": "फसल की सिफारिश करें",
        # Result
        "recommendation": "सिफारिश",
        "empty_info": (
            "बाईं ओर अपनी खेत की स्थितियाँ दर्ज करें, या कोई उदाहरण चुनें, "
            "फिर **फसल की सिफारिश करें** पर क्लिक करके अपने खेत के लिए "
            "सर्वोत्तम फसल देखें।"
        ),
        "recommended_crop": "अनुशंसित फसल",
        "confidence": "विश्वास",
        "top_crops": "शीर्ष 3 फसलें",
        "tab_probabilities": "संभावनाएँ",
        "tab_inputs": "आपके इनपुट",
        "probability": "संभावना",
        "probabilities_caption": "0% से अधिक संभावना वाली फसलें, अधिकतम शीर्ष 10।",
        "parameter": "पैरामीटर",
        "value": "मान",
        "unit": "इकाई",
        "footer": "{model} द्वारा संचालित · वालचंद कॉलेज ऑफ इंजीनियरिंग, सांगली",
        # History
        "history_title": "पूर्वानुमान इतिहास",
        "history_empty": "अभी तक कोई पूर्वानुमान नहीं। आपकी सिफारिशें यहाँ सहेजी जाएँगी।",
        "history_total": "कुल पूर्वानुमान",
        "history_top_crop": "सबसे अधिक सुझाई गई",
        "history_avg_confidence": "औसत विश्वास",
        "history_date": "दिनांक और समय",
        "history_download": "CSV डाउनलोड करें",
        "history_clear": "इतिहास मिटाएँ",
        # Feature labels
        "feat_N": "नाइट्रोजन (N)",
        "help_N": "मिट्टी में नाइट्रोजन की मात्रा",
        "feat_P": "फॉस्फोरस (P)",
        "help_P": "मिट्टी में फॉस्फोरस की मात्रा",
        "feat_K": "पोटैशियम (K)",
        "help_K": "मिट्टी में पोटैशियम की मात्रा",
        "feat_ph": "मिट्टी का pH",
        "help_ph": "मिट्टी की अम्लता: 7 से कम अम्लीय, 7 से अधिक क्षारीय",
        "feat_temperature": "तापमान (°C)",
        "help_temperature": "बढ़ते मौसम के दौरान औसत तापमान",
        "feat_humidity": "आर्द्रता (%)",
        "help_humidity": "औसत सापेक्ष आर्द्रता",
        "feat_rainfall": "वर्षा (mm)",
        "help_rainfall": "औसत वर्षा",
    },
    "mr": {
        "app_title": "पीक शिफारस प्रणाली",
        "language": "भाषा",
        "welcome": "**{name}** म्हणून साइन इन",
        "logout": "लॉग आउट",
        # Auth
        "auth_action": "साइन इन करा किंवा खाते तयार करा",
        "auth_signin": "लॉग इन",
        "auth_signup": "साइन अप",
        "email": "ईमेल",
        "password": "पासवर्ड",
        "confirm_password": "पासवर्डची पुष्टी करा",
        "login_button": "लॉग इन करा",
        "signup_button": "खाते तयार करा",
        "login_hero_subtitle": "तुमच्या शेतासाठी पीक शिफारस मिळवण्यासाठी साइन इन करा.",
        "login_error": "ईमेल किंवा पासवर्ड चुकीचा आहे.",
        "login_empty": "कृपया तुमचा ईमेल आणि पासवर्ड भरा.",
        "signup_empty": "कृपया ईमेल आणि पासवर्ड भरा.",
        "signup_mismatch": "पासवर्ड जुळत नाहीत.",
        "signup_weak": "किमान 6 अक्षरांचा पासवर्ड वापरा.",
        "signup_confirm_email": "खाते तयार झाले. {email} वर तुमचा पत्ता सत्यापित करा, नंतर लॉग इन करा.",
        "signup_error": "खाते तयार करता आले नाही: {message}",
        "auth_not_configured": "प्रमाणीकरण कॉन्फिगर केलेले नाही. SUPABASE_URL आणि SUPABASE_KEY सेट करा.",
        "auth_offline": "साइन इन सेवेशी संपर्क होऊ शकला नाही. कृपया पुन्हा प्रयत्न करा.",
        # Sidebar
        "about": "विषयी",
        "about_text": (
            "हे ॲप Kaggle क्रॉप रेकमेंडेशन डेटासेटवर प्रशिक्षित मशीन लर्निंग "
            "मॉडेल वापरून तुमच्या माती आणि हवामानासाठी सर्वात योग्य पिकाची "
            "शिफारस करते."
        ),
        "how_it_works": "हे कसे कार्य करते",
        "step_1": "तुमच्या मातीतील पोषकद्रव्ये आणि हवामानाची स्थिती भरा",
        "step_2": "**पीक शिफारस करा** वर क्लिक करा",
        "step_3": "सर्वोत्तम पीक आणि पर्यायांचे पुनरावलोकन करा",
        "model": "मॉडेल",
        "algorithm": "अल्गोरिदम",
        "crops": "पिके",
        "inputs": "इनपुट",
        "inputs_value": "7 माती व हवामान वैशिष्ट्ये",
        "preprocessing": "प्रीप्रोसेसिंग",
        "preprocessing_value": "IQR कॅपिंग + मानक स्केलिंग",
        "dataset_link": "Kaggle वर डेटासेट",
        # Hero
        "hero_title": "पीक शिफारस प्रणाली",
        "hero_subtitle": (
            "मातीतील पोषकद्रव्ये आणि हवामानाच्या स्थितीवरून तुमच्या शेतासाठी "
            "सर्वात योग्य पीक शोधा, <b>{model}</b> द्वारे समर्थित."
        ),
        # Form
        "field_conditions": "शेताची परिस्थिती",
        "example_label": "चाचणी संचातील उदाहरण वापरून पहा",
        "custom_values": "स्वतःची मूल्ये",
        "example_option": "उदाहरण: {crop}",
        "soil": "माती",
        "climate": "हवामान",
        "recommend_button": "पीक शिफारस करा",
        # Result
        "recommendation": "शिफारस",
        "empty_info": (
            "डावीकडे तुमच्या शेताची परिस्थिती भरा, किंवा उदाहरण निवडा, "
            "नंतर **पीक शिफारस करा** वर क्लिक करून तुमच्या शेतासाठी "
            "सर्वोत्तम पीक पहा."
        ),
        "recommended_crop": "शिफारस केलेले पीक",
        "confidence": "विश्वास",
        "top_crops": "अव्वल 3 पिके",
        "tab_probabilities": "संभाव्यता",
        "tab_inputs": "तुमचे इनपुट",
        "probability": "संभाव्यता",
        "probabilities_caption": "0% पेक्षा जास्त संभाव्यता असलेली पिके, कमाल अव्वल 10.",
        "parameter": "पॅरामीटर",
        "value": "मूल्य",
        "unit": "एकक",
        "footer": "{model} द्वारे समर्थित · वालचंद कॉलेज ऑफ इंजिनिअरिंग, सांगली",
        # History
        "history_title": "अंदाज इतिहास",
        "history_empty": "अद्याप कोणताही अंदाज नाही. तुमच्या शिफारसी येथे जतन केल्या जातील.",
        "history_total": "एकूण अंदाज",
        "history_top_crop": "सर्वाधिक शिफारस केलेले",
        "history_avg_confidence": "सरासरी विश्वास",
        "history_date": "दिनांक व वेळ",
        "history_download": "CSV डाउनलोड करा",
        "history_clear": "इतिहास साफ करा",
        # Feature labels
        "feat_N": "नायट्रोजन (N)",
        "help_N": "मातीतील नायट्रोजनचे प्रमाण",
        "feat_P": "फॉस्फरस (P)",
        "help_P": "मातीतील फॉस्फरसचे प्रमाण",
        "feat_K": "पोटॅशियम (K)",
        "help_K": "मातीतील पोटॅशियमचे प्रमाण",
        "feat_ph": "मातीचा pH",
        "help_ph": "मातीची आम्लता: 7 पेक्षा कमी आम्लीय, 7 पेक्षा जास्त क्षारीय",
        "feat_temperature": "तापमान (°C)",
        "help_temperature": "वाढीच्या हंगामातील सरासरी तापमान",
        "feat_humidity": "आर्द्रता (%)",
        "help_humidity": "सरासरी सापेक्ष आर्द्रता",
        "feat_rainfall": "पाऊस (mm)",
        "help_rainfall": "सरासरी पाऊस",
    },
}


def current_language():
    return st.session_state.get("language", DEFAULT_LANGUAGE)


def t(key, **values):
    """Translate `key`, falling back to English and then to the key itself."""
    language = current_language()
    text = (
        TRANSLATIONS.get(language, {}).get(key)
        or TRANSLATIONS[DEFAULT_LANGUAGE].get(key)
        or key
    )
    return text.format(**values) if values else text


def crop_name(crop):
    names = CROP_NAMES.get(current_language(), CROP_NAMES[DEFAULT_LANGUAGE])
    return names.get(crop, crop.title())


def crop_emoji(crop):
    return CROP_EMOJI.get(crop, "🌱")


def language_selector():
    """Sidebar widget that switches the UI language."""
    st.selectbox(
        t("language"),
        list(LANGUAGES),
        format_func=lambda code: LANGUAGES[code],
        key="language",
    )
