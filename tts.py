"""Text-to-speech "Listen" buttons, so farmers who cannot read can hear the text.

Uses gTTS (Google Text-to-Speech), which needs an internet connection and
speaks English, Hindi and Marathi. The voice follows the language picked
in the app.

This feature is fully self-contained:
  * Turn it off:  set ENABLED = False below (buttons disappear).
  * Remove it:    delete this file, the `from tts import ...` line and the
                  `listen_button(...)` calls in app.py, and `gTTS` in
                  requirements.txt. Nothing else depends on it.
  * New language: add it to GTTS_LANGUAGES and LABELS.
"""

import io
import re

import streamlit as st

from i18n import current_language

ENABLED = True

# App language code -> (gTTS language, Google domain for the accent)
GTTS_LANGUAGES = {
    "en": ("en", "co.in"),  # English with an Indian accent
    "hi": ("hi", "com"),
    "mr": ("mr", "com"),
}

LABELS = {
    "en": {
        "listen": "🔊 Listen",
        "loading": "Preparing audio...",
        "error": "Audio is not available right now. Please check the internet connection.",
        "result": (
            "The recommended crop is {crop}, with {confidence} percent "
            "confidence. Other options are {others}."
        ),
    },
    "hi": {
        "listen": "🔊 सुनें",
        "loading": "ऑडियो तैयार हो रहा है...",
        "error": "ऑडियो अभी उपलब्ध नहीं है। कृपया इंटरनेट कनेक्शन जांचें।",
        "result": (
            "सुझाई गई फसल {crop} है, {confidence} प्रतिशत विश्वास के साथ। "
            "अन्य विकल्प हैं {others}।"
        ),
    },
    "mr": {
        "listen": "🔊 ऐका",
        "loading": "ऑडिओ तयार होत आहे...",
        "error": "ऑडिओ सध्या उपलब्ध नाही. कृपया इंटरनेट कनेक्शन तपासा.",
        "result": (
            "शिफारस केलेले पीक {crop} आहे, {confidence} टक्के विश्वासासह. "
            "इतर पर्याय आहेत {others}."
        ),
    },
}


def _label(key, language):
    return LABELS.get(language, LABELS["en"])[key]


def _clean(text):
    """Strip Markdown/HTML so the voice does not read symbols aloud."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[*_`#>]", "", text)
    return re.sub(r"\s+", " ", text).strip()


@st.cache_data(show_spinner=False, max_entries=256)
def synthesize(text, language):
    """Return MP3 bytes for `text`. Cached, so each text is fetched once."""
    from gtts import gTTS  # imported here so the app runs even without gTTS

    lang, tld = GTTS_LANGUAGES.get(language, GTTS_LANGUAGES["en"])
    buffer = io.BytesIO()
    gTTS(text=text, lang=lang, tld=tld).write_to_fp(buffer)
    return buffer.getvalue()


@st.fragment
def _player(text, language, key):
    # A fragment reruns only itself on click, so the rest of the page
    # (for example the prediction result) stays on screen.
    if st.button(_label("listen", language), key=f"tts_{key}"):
        try:
            with st.spinner(_label("loading", language)):
                audio = synthesize(text, language)
            st.audio(audio, format="audio/mp3", autoplay=True)
        except Exception:
            st.warning(_label("error", language))


def listen_button(text, key):
    """Show a "Listen" button that reads `text` aloud in the current language."""
    if not ENABLED or not text:
        return
    _player(_clean(text), current_language(), key)


def result_text(crop, confidence, alternatives):
    """Spoken summary of a prediction, in the current language."""
    return _label("result", current_language()).format(
        crop=crop,
        confidence=f"{confidence * 100:.0f}",
        others=", ".join(alternatives),
    )
