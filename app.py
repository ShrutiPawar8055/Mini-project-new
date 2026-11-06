import altair as alt
import joblib
import pandas as pd
import streamlit as st

from app_auth import require_login, sign_out
from db import clear_predictions, get_predictions, save_prediction
from tts import listen_button, result_text  # optional voice feature
from i18n import (
    DEFAULT_LANGUAGE,
    crop_emoji,
    crop_name,
    language_selector,
    t,
)


st.set_page_config(
    page_title=t("app_title"),
    page_icon="🌱",
    layout="wide"
)


FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

MODEL_NAMES = {
    "RandomForestClassifier": "Random Forest",
    "SVC": "Support Vector Machine",
    "KNeighborsClassifier": "K-Nearest Neighbours",
    "DecisionTreeClassifier": "Decision Tree",
}

# feature: (unit, min, max, step, display format); labels/help come from i18n
INPUTS = {
    "N": ("kg/ha", 0.0, 150.0, 1.0, "%.0f"),
    "P": ("kg/ha", 0.0, 150.0, 1.0, "%.0f"),
    "K": ("kg/ha", 0.0, 210.0, 1.0, "%.0f"),
    "ph": ("pH", 0.0, 14.0, 0.1, "%.1f"),
    "temperature": ("°C", -10.0, 60.0, 0.1, "%.1f"),
    "humidity": ("%", 0.0, 100.0, 0.1, "%.1f"),
    "rainfall": ("mm", 0.0, 500.0, 1.0, "%.1f"),
}

DEFAULTS = {
    "N": 50.0, "P": 50.0, "K": 50.0, "temperature": 25.0,
    "humidity": 70.0, "ph": 6.5, "rainfall": 100.0,
}

# Real samples from the unseen test set (notebook section 3.5)
EXAMPLES = {
    "rice": [60, 49, 44, 20.8, 84.5, 6.2, 240.1],
    "cotton": [140, 38, 15, 24.1, 75.9, 6.0, 69.9],
    "maize": [71, 54, 16, 22.6, 63.7, 5.7, 87.8],
    "chickpea": [25, 68, 77, 20.1, 15.1, 7.7, 85.7],
    "apple": [0, 133, 200, 23.7, 90.5, 5.7, 104.2],
    "coffee": [109, 31, 27, 23.1, 50.4, 7.0, 164.5],
}


st.session_state.setdefault("language", DEFAULT_LANGUAGE)


st.markdown(
    """
    <style>
    .hero {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 55%, #66bb6a 100%);
        color: #ffffff;
        padding: 1.75rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.25rem;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        margin-top: 0.4rem;
        opacity: 0.92;
    }
    .result-card {
        display: flex;
        align-items: center;
        gap: 1.25rem;
        background: linear-gradient(135deg, #1b5e20 0%, #43a047 100%);
        color: #ffffff;
        padding: 1.5rem 1.75rem;
        border-radius: 16px;
        margin-bottom: 1rem;
    }
    .result-emoji {
        font-size: 3.5rem;
        line-height: 1;
    }
    .result-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.85;
    }
    .result-crop {
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .result-pill {
        display: inline-block;
        margin-top: 0.4rem;
        padding: 0.2rem 0.75rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.2);
        font-size: 0.9rem;
        font-weight: 600;
    }
    .rank-card {
        text-align: center;
    }
    .rank-emoji {
        font-size: 2rem;
    }
    .rank-crop {
        font-weight: 600;
        font-size: 1.05rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Everything below requires an authenticated session
client = require_login()


# Artifacts saved by Smart_Crop_Recommendation.ipynb (section 2.5)
@st.cache_resource
def load_model():
    model = joblib.load("best_model.pkl")
    scaler = joblib.load("scaler.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    cap_bounds = joblib.load("cap_bounds.pkl")
    return model, scaler, label_encoder, cap_bounds


model, scaler, label_encoder, cap_bounds = load_model()

model_name = MODEL_NAMES.get(type(model).__name__, type(model).__name__)


def preprocess(raw_df):
    # Same steps as training: IQR capping, then standard scaling
    capped = raw_df.copy()
    for feature in FEATURES:
        low, high = cap_bounds[feature]
        capped[feature] = capped[feature].clip(low, high)
    return scaler.transform(capped[FEATURES])


for feature in FEATURES:
    st.session_state.setdefault(feature, DEFAULTS[feature])


def load_example():
    example = st.session_state.example
    if example in EXAMPLES:
        values = dict(zip(FEATURES, EXAMPLES[example]))
    else:
        values = DEFAULTS
    for feature in FEATURES:
        st.session_state[feature] = float(values[feature])


def number_input(feature):
    _, min_value, max_value, step, display_format = INPUTS[feature]
    return st.number_input(
        t(f"feat_{feature}"),
        min_value=min_value,
        max_value=max_value,
        step=step,
        format=display_format,
        help=t(f"help_{feature}"),
        key=feature
    )


with st.sidebar:
    language_selector()
    st.caption(t("welcome", name=st.session_state.get("user_email") or ""))
    if st.button(t("logout"), width="stretch"):
        sign_out(client)
    st.divider()

    st.header(f"🌱 {t('about')}")
    st.write(t("about_text"))

    st.subheader(t("how_it_works"))
    st.markdown(
        f"1. {t('step_1')}\n"
        f"2. {t('step_2')}\n"
        f"3. {t('step_3')}"
    )
    listen_button(
        f"{t('about')}. {t('about_text')} {t('how_it_works')}. "
        f"1. {t('step_1')}. 2. {t('step_2')}. 3. {t('step_3')}.",
        key="about",
    )

    st.subheader(t("model"))
    st.markdown(
        f"- **{t('algorithm')}:** {model_name}\n"
        f"- **{t('crops')}:** {len(label_encoder.classes_)}\n"
        f"- **{t('inputs')}:** {t('inputs_value')}\n"
        f"- **{t('preprocessing')}:** {t('preprocessing_value')}"
    )

    st.markdown(
        f"[{t('dataset_link')}]"
        "(https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)"
    )


st.markdown(
    f"""
    <div class="hero">
        <div class="hero-title">🌱 {t('hero_title')}</div>
        <div class="hero-subtitle">
            {t('hero_subtitle', model=model_name)}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


input_col, result_col = st.columns([5, 7], gap="large")

with input_col:

    st.subheader(f"🌾 {t('field_conditions')}")

    st.selectbox(
        t("example_label"),
        ["custom"] + list(EXAMPLES),
        format_func=lambda crop: (
            f"✏️ {t('custom_values')}" if crop == "custom"
            else t("example_option", crop=f"{crop_emoji(crop)} {crop_name(crop)}")
        ),
        key="example",
        on_change=load_example
    )

    with st.form("conditions", border=False):

        with st.container(border=True):
            st.markdown(f"**🧪 {t('soil')}**")
            soil_col1, soil_col2 = st.columns(2)
            with soil_col1:
                number_input("N")
                number_input("K")
            with soil_col2:
                number_input("P")
                number_input("ph")

        with st.container(border=True):
            st.markdown(f"**🌦️ {t('climate')}**")
            climate_col1, climate_col2 = st.columns(2)
            with climate_col1:
                number_input("temperature")
                number_input("rainfall")
            with climate_col2:
                number_input("humidity")

        submitted = st.form_submit_button(
            f"🔍 {t('recommend_button')}",
            type="primary",
            width="stretch"
        )


with result_col:

    st.subheader(f"🌿 {t('recommendation')}")

    if not submitted:

        st.info(t("empty_info"))
        listen_button(t("empty_info"), key="instructions")

    else:

        values = {feature: st.session_state[feature] for feature in FEATURES}

        input_data = pd.DataFrame([values], columns=FEATURES)

        model_input = preprocess(input_data)

        predicted_class = model.predict(model_input)[0]

        predicted_crop = label_encoder.inverse_transform(
            [predicted_class]
        )[0]

        probabilities = model.predict_proba(model_input)[0]

        probability_df = pd.DataFrame({
            "crop": label_encoder.classes_,
            "Probability": probabilities
        }).sort_values(
            by="Probability",
            ascending=False
        ).reset_index(drop=True)

        probability_df["Crop"] = probability_df["crop"].map(crop_name)

        confidence = probability_df.iloc[0]["Probability"]

        # Store the inputs and the model output in SQLite
        save_prediction(
            st.session_state.get("user_email") or "anonymous",
            values,
            predicted_crop,
            confidence,
            probability_df.head(3)[["crop", "Probability"]].values.tolist(),
        )

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-emoji">{crop_emoji(predicted_crop)}</div>
                <div>
                    <div class="result-label">{t('recommended_crop')}</div>
                    <div class="result-crop">{crop_name(predicted_crop)}</div>
                    <span class="result-pill">
                        {t('confidence')} · {confidence * 100:.1f}%
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        listen_button(
            result_text(
                crop_name(predicted_crop),
                confidence,
                [crop_name(crop) for crop in probability_df["crop"].iloc[1:3]],
            ),
            key="result",
        )

        st.markdown(f"**🏆 {t('top_crops')}**")

        medals = ["🥇", "🥈", "🥉"]

        for rank_col, medal, (_, row) in zip(
            st.columns(3), medals, probability_df.head(3).iterrows()
        ):
            with rank_col:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div class="rank-card">
                            <div class="rank-emoji">{medal} {crop_emoji(row["crop"])}</div>
                            <div class="rank-crop">{row["Crop"]}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.progress(
                        float(row["Probability"]),
                        text=f"{row['Probability'] * 100:.1f}%"
                    )

        chart_tab, input_tab = st.tabs(
            [f"📊 {t('tab_probabilities')}", f"🧾 {t('tab_inputs')}"]
        )

        with chart_tab:

            chart_data = probability_df[
                probability_df["Probability"] > 0
            ].head(10).copy()

            chart_data["Type"] = [
                "Recommended" if i == 0 else "Other"
                for i in range(len(chart_data))
            ]

            chart = alt.Chart(chart_data).mark_bar(
                cornerRadiusEnd=4
            ).encode(
                x=alt.X(
                    "Probability:Q",
                    title=t("probability"),
                    axis=alt.Axis(format="%"),
                    scale=alt.Scale(domain=[0, 1])
                ),
                y=alt.Y("Crop:N", sort="-x", title=None),
                color=alt.Color(
                    "Type:N",
                    scale=alt.Scale(
                        domain=["Recommended", "Other"],
                        range=["#2e7d32", "#a5d6a7"]
                    ),
                    legend=None
                ),
                tooltip=[
                    alt.Tooltip("Crop:N"),
                    alt.Tooltip("Probability:Q", format=".1%")
                ]
            ).properties(
                height=max(120, 34 * len(chart_data))
            )

            st.altair_chart(chart)

            st.caption(t("probabilities_caption"))

        with input_tab:

            input_display = pd.DataFrame({
                t("parameter"): [t(f"feat_{feature}") for feature in FEATURES],
                t("value"): [values[feature] for feature in FEATURES],
                t("unit"): [INPUTS[feature][0] for feature in FEATURES],
            })

            st.dataframe(
                input_display,
                width="stretch",
                hide_index=True
            )


# Prediction history stored in SQLite (db.py)
st.divider()

st.subheader(f"📜 {t('history_title')}")

user_email = st.session_state.get("user_email") or "anonymous"
history = get_predictions(user_email)

if history.empty:

    st.info(t("history_empty"))

else:

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    top_crop = history["predicted_crop"].mode()[0]
    stat_col1.metric(t("history_total"), len(history))
    stat_col2.metric(
        t("history_top_crop"),
        f"{crop_emoji(top_crop)} {crop_name(top_crop)}"
    )
    stat_col3.metric(
        t("history_avg_confidence"),
        f"{history['confidence'].mean() * 100:.1f}%"
    )

    history_display = pd.DataFrame({
        t("history_date"): history["created_at"],
        **{t(f"feat_{feature}"): history[feature] for feature in FEATURES},
        t("recommended_crop"): [
            f"{crop_emoji(crop)} {crop_name(crop)}"
            for crop in history["predicted_crop"]
        ],
        t("confidence"): history["confidence"] * 100,
    })

    st.dataframe(
        history_display,
        width="stretch",
        hide_index=True,
        column_config={
            t("confidence"): st.column_config.ProgressColumn(
                t("confidence"), format="%.1f%%", min_value=0, max_value=100
            ),
        },
    )

    download_col, clear_col = st.columns(2)

    with download_col:
        st.download_button(
            f"⬇️ {t('history_download')}",
            history.drop(columns=["user_email"]).to_csv(index=False),
            file_name="prediction_history.csv",
            mime="text/csv",
            width="stretch",
        )

    with clear_col:
        if st.button(f"🗑️ {t('history_clear')}", width="stretch"):
            clear_predictions(user_email)
            st.rerun()


st.divider()

st.caption(
    f"🌱 {t('app_title')} · {t('footer', model=model_name)}"
)
