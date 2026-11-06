"""Local hashed authentication for the Crop Recommendation System.

Accounts are stored in `users.json` with bcrypt-hashed passwords.
Session persistence is handled via a browser cookie.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import bcrypt
import extra_streamlit_components as stx
import streamlit as st

from i18n import language_selector, t

COOKIE_NAME = "crop_auth_user"
COOKIE_DAYS = 30
MIN_PASSWORD_LENGTH = 6
USERS_FILE = Path(__file__).parent / "users.json"

_LOGIN_HERO = """
<div class="hero">
    <div class="hero-title">🌱 {title}</div>
    <div class="hero-subtitle">{subtitle}</div>
</div>
"""

def _load_users():
    if not USERS_FILE.exists():
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def _hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def _check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def _cookies():
    """Single cookie component per session, reused across runs."""
    if "_cookie_manager" not in st.session_state:
        st.session_state["_cookie_manager"] = stx.CookieManager(key="auth_cookies")
    return st.session_state["_cookie_manager"]

def _clear_cookie(cookies):
    try:
        cookies.delete(COOKIE_NAME)
    except Exception:
        pass

def _start_session(email, cookies):
    st.session_state["authentication_status"] = True
    st.session_state["user_email"] = email
    cookies.set(
        COOKIE_NAME,
        email,
        expires_at=datetime.now() + timedelta(days=COOKIE_DAYS),
    )

def _restore_session(cookies):
    email = st.context.cookies.get(COOKIE_NAME)
    if not email:
        return
    users = _load_users()
    if email in users:
        st.session_state["authentication_status"] = True
        st.session_state["user_email"] = email

def _sign_in_form(cookies):
    with st.form("sign_in"):
        email = st.text_input(t("email"))
        password = st.text_input(t("password"), type="password")
        submitted = st.form_submit_button(
            t("login_button"), type="primary", width="stretch"
        )

    if not submitted:
        return

    if not email or not password:
        st.error(t("login_empty"))
        return

    users = _load_users()
    if email in users and _check_password(password, users[email]["hashed_password"]):
        _start_session(email, cookies)
        st.rerun()
    else:
        st.error(t("login_error"))

def _sign_up_form(cookies):
    with st.form("sign_up"):
        email = st.text_input(t("email"))
        password = st.text_input(t("password"), type="password")
        confirm = st.text_input(t("confirm_password"), type="password")
        submitted = st.form_submit_button(
            t("signup_button"), type="primary", width="stretch"
        )

    if not submitted:
        return

    if not email or not password:
        st.error(t("signup_empty"))
        return

    if password != confirm:
        st.error(t("signup_mismatch"))
        return

    if len(password) < MIN_PASSWORD_LENGTH:
        st.error(t("signup_weak"))
        return

    users = _load_users()
    if email in users:
        st.error(t("signup_error", message="User already exists"))
        return

    users[email] = {
        "hashed_password": _hash_password(password),
        "created_at": datetime.now().isoformat()
    }
    _save_users(users)
    _start_session(email, cookies)
    st.rerun()

def _render_auth_screen(cookies):
    """The centred log in / sign up screen."""
    _, column, _ = st.columns([1, 1.1, 1])
    with column:
        language_selector()
        st.markdown(
            _LOGIN_HERO.format(
                title=t("hero_title"),
                subtitle=t("login_hero_subtitle"),
            ),
            unsafe_allow_html=True,
        )
        action = st.radio(
            t("auth_action"),
            ["signin", "signup"],
            format_func=lambda name: t(f"auth_{name}"),
            horizontal=True,
            label_visibility="collapsed",
        )

        if action == "signin":
            _sign_in_form(cookies)
        else:
            _sign_up_form(cookies)

def require_login():
    """Gate the app, stopping the script while signed out."""
    cookies = _cookies()

    if not st.session_state.get("authentication_status"):
        _restore_session(cookies)

    if st.session_state.get("authentication_status"):
        return None  # No client needed for local auth

    _render_auth_screen(cookies)
    st.stop()

def sign_out(client=None):
    """Clear the local session and cookie."""
    st.session_state["authentication_status"] = False
    st.session_state.pop("user_email", None)
    _clear_cookie(_cookies())
    st.rerun()
