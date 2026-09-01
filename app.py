"""
app.py - Schweizer Fahreignungsabklärung Live-Simulator
Interaktives verkehrspsychologisches Audiosystem im Auftrag des kantonalen Strassenverkehrsamts.
"""

import base64
import os
import streamlit as st

from scenarios import get_all_scenarios, get_scenario, SCENARIOS
from assessment_engine import (
    get_gemini_client,
    generate_psychologist_turn,
    generate_final_report,
    generate_tts_audio,
    TTS_VOICES,
)
from streamlit_mic_recorder import speech_to_text

# 1. Page Configuration
st.set_page_config(
    page_title="CH Fahreignungsabklärung | Live-Simulator",
    page_icon="🇨🇭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 2. Lokale PNG-Datei zuverlässig als Base64 laden
def load_local_image_base64(file_name: str) -> str:
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""


demon_logo_src = load_local_image_base64("Dodge-Demon-Logo.png")

# 3. Styling & Custom CSS
st.markdown(
    """
<style>
    /* Dark Mode Basis */
    .stApp {
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d !important;
    }

    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 24px;
        background: linear-gradient(90deg, #161b22 0%, #1c2128 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .swiss-flag {
        width: 38px;
        height: 38px;
        background-color: #d52b1e;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 10px rgba(213, 43, 30, 0.6);
    }

    .demon-logo-img {
        height: 48px;
        width: auto;
        object-fit: contain;
        filter: invert(27%) sepia(91%) saturate(6295%) hue-rotate(352deg) brightness(98%) contrast(117%);
    }

    .hero-box {
        background: linear-gradient(135deg, #1f2937 0%, #0d1117 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 22px 26px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .hero-box::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #d52b1e 0%, #38bdf8 50%, #58a6ff 100%);
    }

    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    
    .metric-card:hover {
        border-color: #58a6ff;
        transform: translateY(-1px);
    }

    .metric-title { 
        font-size: 11px; 
        color: #8b949e; 
        text-transform: uppercase; 
        font-weight: 700; 
        letter-spacing: 0.5px;
    }
    
    .metric-val-blue { font-size: 19px; font-weight: 700; color: #58a6ff; }
    .metric-val-red { font-size: 17px; font-weight: 700; color: #f85149; }
    .metric-val-green { font-size: 17px; font-weight: 700; color: #2ea043; }
    .metric-val-yellow { font-size: 17px; font-weight: 700; color: #e3b341; }

    .chat-bubble-gutachter {
        background: linear-gradient(135deg, #1c2128 0%, #161b22 100%);
        border-left: 4px solid #58a6ff;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
        color: #f0f6fc;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }

    .chat-bubble-user {
        background: linear-gradient(135deg, #21262d 0%, #1a1e24 100%);
        border-left: 4px solid #2ea043;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 16px;
        color: #c9d1d9;
    }

    .obs-note {
        background-color: #12161c;
        border: 1px dashed #30363d;
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 12px;
        color: #8b949e;
        margin-bottom: 8px;
    }

    .badge {
        display: inline-block;
        padding: 3px 8px;
        font-size: 11px;
        font-weight: 600;
        border-radius: 12px;
        text-transform: uppercase;
    }
    
    .report-container {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 30px;
        margin-top: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 4. Session State Initialisierung
if "scenario_id" not in st.session_state:
    st.session_state.scenario_id = "kokain"

if "session_active" not in st.session_state:
    st.session_state.session_active = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "scores" not in st.session_state:
    st.session_state.scores = {
        "einsicht": 35,
        "transparenz": 25,
        "problembewusstsein": 30,
        "risiko": "Mittel",
    }

if "observations" not in st.session_state:
    st.session_state.observations = []

if "current_phase" not in st.session_state:
    st.session_state.current_phase = "Phase 1/5: Rekonstruktion & Vorfall"

if "latest_audio_b64" not in st.session_state:
    st.session_state.latest_audio_b64 = None

if "show_report" not in st.session_state:
    st.session_state.show_report = False

if "final_report_data" not in st.session_state:
    st.session_state.final_report_data = None


# 5. Top-Bar mit Schweizer-Kreuz & rotem Demon-Logo
st.markdown(
    f"""
<div class="top-bar">
    <div style="display: flex; align-items: center; gap: 15px;">
        <div class="swiss-flag">
            <svg width="22" height="22" viewBox="0 0 20 20" fill="none">
                <rect x="8.5" y="3" width="3" height="14" fill="white"/>
                <rect x="3" y="8.5" width="14" height="3" fill="white"/>
            </svg>
        </div>
        <div>
            <div style="font-size: 14px; font-weight: 700; color: #f0f6fc; letter-spacing: 0.5px;">SCHWEIZERISCHE EIDGENOSSENSCHAFT</div>
            <div style="font-size: 11px; color: #8b949e;">Kantonale Fahreignungsabklärung • Strassenverkehrsamt</div>
        </div>
    </div>
    <div>
        <img src="{demon_logo_src}" class="demon-logo-img" alt="Dodge Demon Logo">
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# 6. API-Key Ermittlung (aus Environment oder Sidebar)
env_api_key = os.environ.get("GEMINI_API_KEY", "")
gemini_client = get_gemini_client(env_api_key)

# 7. Sidebar - Konfiguration & Gutachter-Panel
with st.sidebar:
    st.markdown("<h3 style='color: #f0f6fc; margin-bottom: 12px;'>📋 Gutachter-Panel</h3>", unsafe_allow_html=True)
    
    # API Key Einstellung falls in Umgebung nicht gesetzt
    if not gemini_client:
        with st.expander("🔑 Gemini API-Key Konfiguration", expanded=True):
            user_key = st.text_input("Gemini API Key:", type="password", help="Wird für die Live-Evaluation benötigt")
            if user_key:
                gemini_client = get_gemini_client(user_key)
                if gemini_client:
                    st.success("API Key aktiv!")
    
    # Audio-Einstellungen
    with st.expander("🔊 Audio- & Stimm-Optionen", expanded=False):
        tts_enabled = st.checkbox("Sprachausgabe (TTS) aktiv", value=True)
        selected_voice = st.selectbox(
            "Gutachter-Stimme:",
            options=list(TTS_VOICES.keys()),
            index=0
        )
    
    # Aktuelles Szenario laden
    current_scenario = get_scenario(st.session_state.scenario_id)
    
    # Dossier-Info Box
    st.markdown(
        f"""
    <div class="metric-card">
        <div class="metric-title">Fall-Akte</div>
        <div class="metric-val-blue">{current_scenario['case_number']}</div>
        <div style="font-size: 12px; color: #8b949e; margin-top: 4px;">{current_scenario.get('canton', 'Kanton ZH')}</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Delikt-Kategorie</div>
        <div style="font-size: 15px; font-weight: 700; color: {current_scenario.get('badge_color', '#f85149')}; margin-top: 2px;">
            {current_scenario['category']}
        </div>
        <div style="font-size: 11px; color: #8b949e; margin-top: 4px;">{current_scenario.get('blood_values', '')}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    # Live-Scores
    st.markdown("<div style='font-size: 13px; font-weight: 700; color: #f0f6fc; margin: 15px 0 8px 0;'>Live Psychometrie</div>", unsafe_allow_html=True)
    
    einsicht = st.session_state.scores.get("einsicht", 35)
    st.caption(f"Einsichtsfähigkeit ({einsicht}%):")
    st.progress(einsicht / 100.0)
    
    transparenz = st.session_state.scores.get("transparenz", 25)
    st.caption(f"Transparenz & Offenheit ({transparenz}%):")
    st.progress(transparenz / 100.0)
    
    problembewusstsein = st.session_state.scores.get("problembewusstsein", 30)
    st.caption(f"Problembewusstsein ({problembewusstsein}%):")
    st.progress(problembewusstsein / 100.0)
    
    risiko = st.session_state.scores.get("risiko", "Mittel")
    risiko_color_class = "metric-val-red" if risiko == "Hoch" else ("metric-val-yellow" if risiko == "Mittel" else "metric-val-green")
    
    st.markdown(
        f"""
    <div class="metric-card" style="margin-top: 10px;">
        <div class="metric-title">Rückfallgefahr</div>
        <div class="{risiko_color_class}">{risiko}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    # Gutachter-Notizbuch (Beobachtungen)
    if st.session_state.observations:
        with st.expander(f"📝 Psychologische Notizen ({len(st.session_state.observations)})", expanded=False):
            for obs in reversed(st.session_state.observations[-6:]):
                st.markdown(f"<div class='obs-note'>• {obs}</div>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: #30363d; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Aktionen
    if st.session_state.session_active and not st.session_state.show_report:
        if st.button("⏹ Assessment Beenden & Gutachten Generieren", type="primary", use_container_width=True):
            st.session_state.show_report = True
            with st.spinner("Dr. Urs Meier erstellt das offizielle Gutachten nach ASA/VfV Richtlinien..."):
                if gemini_client:
                    report_result = generate_final_report(
                        client=gemini_client,
                        scenario=current_scenario,
                        history=st.session_state.messages,
                        scores=st.session_state.scores,
                        observations=st.session_state.observations,
                    )
                else:
                    report_result = {
                        "markdown": "# 📋 Gutachten (Demo-Modus)\nFahreignung beurteilt.",
                        "status": "BEDINGT BEFÜRWORTET"
                    }
                st.session_state.final_report_data = report_result
            st.rerun()

    if st.button("🔄 Neues Szenario / Reset", use_container_width=True):
        st.session_state.session_active = False
        st.session_state.show_report = False
        st.session_state.messages = []
        st.session_state.observations = []
        st.session_state.latest_audio_b64 = None
        st.session_state.final_report_data = None
        st.session_state.scores = {"einsicht": 35, "transparenz": 25, "problembewusstsein": 30, "risiko": "Mittel"}
        st.rerun()


# 8. Hauptbereich

# A. SZENARIO-AUSWAHL (Wenn Session noch nicht aktiv)
if not st.session_state.session_active and not st.session_state.show_report:
    st.markdown(
        """
    <div class="hero-box">
        <h1 style="margin:0; font-size: 26px; font-weight: 700; color: #f0f6fc;">
            CH Fahreignungsabklärung <span style="color: #58a6ff;">Live-Simulator</span>
        </h1>
        <p style="margin: 8px 0 0 0; color: #8b949e; font-size: 14px;">
            Interaktive verkehrspsychologische Exploration nach Schweizer SVG/VZV-Richtlinien mit KI-Gutachter Dr. phil. Urs Meier.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    st.subheader("📂 Fallakte & Delikt-Szenario auswählen")
    
    all_scenarios = get_all_scenarios()
    scenario_titles = [f"{s['case_number']} – {s['title']}" for s in all_scenarios]
    
    selected_index = st.selectbox(
        "Wählen Sie das zu simulierende Verfahren:",
        range(len(all_scenarios)),
        format_func=lambda i: scenario_titles[i],
        index=0
    )
    
    chosen_scenario = all_scenarios[selected_index]
    st.session_state.scenario_id = chosen_scenario["id"]
    
    # Detailkarte zum gewählten Fall
    st.markdown(
        f"""
    <div style="background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 20px; margin-top: 15px;">
        <div style="display:flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="font-size: 18px; font-weight: 700; color: #f0f6fc;">{chosen_scenario['title']}</span>
            <span style="background-color: {chosen_scenario['badge_color']}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;">
                {chosen_scenario['category']}
            </span>
        </div>
        <p style="color: #c9d1d9; font-size: 14px; margin-bottom: 8px;"><strong>Sachverhalt gemäss Polizei/Akten:</strong> {chosen_scenario['police_report']}</p>
        <p style="color: #8b949e; font-size: 13px; margin-bottom: 6px;"><strong>Messwerte / Labor:</strong> <code style="color: #58a6ff;">{chosen_scenario['blood_values']}</code></p>
        <p style="color: #8b949e; font-size: 13px; margin-bottom: 12px;"><strong>Rechtliche Grundlage:</strong> {chosen_scenario['legal_basis']}</p>
        <div style="margin-top: 10px;">
            <strong style="font-size: 13px; color: #f0f6fc;">Schwerpunkte der psychologischen Untersuchung:</strong>
            <ul style="margin-top: 6px; font-size: 13px; color: #8b949e;">
                {''.join(f'<li>{f}</li>' for f in chosen_scenario['focus_areas'])}
            </ul>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    st.write("")
    if st.button("▶ Fahreignungsabklärung & Befragung starten", type="primary", use_container_width=True):
        st.session_state.session_active = True
        st.session_state.messages = [
            {"role": "assistant", "content": chosen_scenario["initial_question"]}
        ]
        st.session_state.current_phase = "Phase 1/5: Vorfall & Vorgeschichte"
        st.session_state.observations = ["Eröffnung des Explorationsgesprächs durch den Gutachter."]
        
        # Audio für die Begrüssung generieren
        if tts_enabled:
            with st.spinner("Stimme des Gutachters wird initialisiert..."):
                tts_result = generate_tts_audio(chosen_scenario["initial_question"], selected_voice)
                if tts_result:
                    _, st.session_state.latest_audio_b64 = tts_result
        
        st.rerun()


# B. ABSCHLUSSGUTACHTEN-ANSICHT
elif st.session_state.show_report and st.session_state.final_report_data:
    st.markdown(
        """
    <div class="hero-box">
        <h1 style="margin:0; font-size: 26px; font-weight: 700; color: #f0f6fc;">
            Offizielles Verkehrspsychologisches Gutachten
        </h1>
        <p style="margin: 8px 0 0 0; color: #8b949e; font-size: 14px;">
            Erstellt für das kantonale Strassenverkehrsamt nach den Kriterien der Schweizer Vereinigung für Verkehrspsychologie (VfV).
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    rep_status = st.session_state.final_report_data.get("status", "BEDINGT BEFÜRWORTET")
    status_bg = "#2ea043" if "BEFÜRWORTET" == rep_status else ("#f85149" if "ABGELEHNT" in rep_status else "#e3b341")
    
    st.markdown(
        f"""
    <div style="background-color: #161b22; border: 2px solid {status_bg}; border-radius: 10px; padding: 18px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div style="font-size: 12px; color: #8b949e; text-transform: uppercase; font-weight: 700;">Formelles Gesamturteil</div>
            <div style="font-size: 22px; font-weight: 800; color: {status_bg};">{rep_status}</div>
        </div>
        <div style="text-align: right; font-size: 13px; color: #8b949e;">
            <div>Dossier: <strong>{current_scenario['case_number']}</strong></div>
            <div>Gutachter: <strong>Dr. phil. Urs Meier</strong></div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    st.markdown('<div class="report-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.final_report_data["markdown"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📥 Gutachten als Markdown herunterladen",
            data=st.session_state.final_report_data["markdown"],
            file_name=f"Fahreignungsgutachten_{current_scenario['case_number'].replace('#','')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col_dl2:
        if st.button("⬅️ Zurück zum Gesprächsverlauf", use_container_width=True):
            st.session_state.show_report = False
            st.rerun()


# C. LIVE-EXPLORATION (DIALOG)
else:
    # Phase & Status Header
    st.markdown(
        f"""
    <div style="background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 14px 20px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <span style="font-size: 12px; color: #8b949e; text-transform: uppercase; font-weight: 700;">Status:</span>
            <span style="color: #58a6ff; font-weight: 600; margin-left: 8px;">{st.session_state.current_phase}</span>
        </div>
        <div>
            <span style="font-size: 12px; color: #8b949e;">Akte: <strong style="color: #f0f6fc;">{current_scenario['case_number']}</strong> ({current_scenario['category']})</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    # Audio Player für die letzte Gutachter-Antwort
    if st.session_state.latest_audio_b64 and tts_enabled:
        st.markdown(
            f"""
        <div style="background-color: #1c2128; border: 1px solid #38bdf8; border-radius: 8px; padding: 12px 18px; margin-bottom: 18px; display: flex; align-items: center; gap: 15px;">
            <span style="font-size: 18px;">🗣️</span>
            <div style="flex-grow: 1;">
                <div style="font-size: 12px; color: #8b949e; font-weight: 600;">Stimme Dr. Urs Meier:</div>
                <audio controls autoplay style="width: 100%; height: 35px; margin-top: 4px;">
                    <source src="data:audio/mp3;base64,{st.session_state.latest_audio_b64}" type="audio/mp3">
                </audio>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    
    # Bisheriger Dialogverlauf
    st.markdown("<div style='margin-bottom: 15px;'>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.markdown(
                f"""
            <div class="chat-bubble-gutachter">
                <div style="font-size: 12px; font-weight: 700; color: #58a6ff; margin-bottom: 4px;">👨‍⚕️ Dr. phil. Urs Meier (Verkehrspsychologe):</div>
                <div style="font-size: 15px; line-height: 1.5;">{msg['content']}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
            <div class="chat-bubble-user">
                <div style="font-size: 12px; font-weight: 700; color: #2ea043; margin-bottom: 4px;">👤 Sie (Proband):</div>
                <div style="font-size: 15px; line-height: 1.5;">{msg['content']}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Eingabebereich: Spracheingabe & Texteingabe
    st.markdown("---")
    st.markdown("<h4 style='color: #f0f6fc; font-size: 15px;'>Ihre Antwort auf die Frage des Gutachters:</h4>", unsafe_allow_html=True)
    
    col_mic, col_txt = st.columns([1, 2])
    
    spoken_text = None
    with col_mic:
        st.caption("🎙️ Per Mikrofon antworten:")
        spoken_text = speech_to_text(
            start_prompt="🎙️ Aufnehmen & Sprechen",
            stop_prompt="⏹ Fertig & Absenden",
            language="de",
            key="live_audio_stream",
        )
    
    with col_txt:
        st.caption("⌨️ Oder als Text eingeben:")
        text_input = st.text_input("Antwort tippen:", key="text_reply_input", placeholder="Schildern Sie Ihre Sichtweise...")
        send_text_clicked = st.button("Antwort senden", key="send_text_btn")
    
    # Wenn eine Antwort einging (per Sprache oder Text)
    user_reply = spoken_text if spoken_text else (text_input if send_text_clicked and text_input.strip() else None)
    
    if user_reply:
        # User-Nachricht anhängen
        st.session_state.messages.append({"role": "user", "content": user_reply})
        
        with st.spinner("Dr. Urs Meier analysiert Ihre Aussage und formuliert die Nachfrage..."):
            if gemini_client:
                turn_result = generate_psychologist_turn(
                    client=gemini_client,
                    scenario=current_scenario,
                    history=st.session_state.messages[:-1],
                    user_response=user_reply,
                    current_scores=st.session_state.scores,
                )
            else:
                turn_result = {
                    "gutachter_antwort": f"Sie erklärten '{user_reply}'. Wie schätzen Sie rückblickend die Gefährdung ein?",
                    "einsicht_score": min(100, st.session_state.scores.get("einsicht", 35) + 10),
                    "transparenz_score": min(100, st.session_state.scores.get("transparenz", 25) + 5),
                    "problembewusstsein_score": min(100, st.session_state.scores.get("problembewusstsein", 30) + 8),
                    "risiko_stufe": "Mittel",
                    "beobachtung": "Antwort registriert.",
                    "gespraechs_phase": "Phase 2/5: Reflexion & Ursachen",
                    "frage_nummer": len(st.session_state.messages) // 2 + 1
                }
            
            # Scores & Phase aktualisieren
            st.session_state.scores["einsicht"] = turn_result["einsicht_score"]
            st.session_state.scores["transparenz"] = turn_result["transparenz_score"]
            st.session_state.scores["problembewusstsein"] = turn_result["problembewusstsein_score"]
            st.session_state.scores["risiko"] = turn_result["risiko_stufe"]
            st.session_state.current_phase = turn_result["gespraechs_phase"]
            
            if turn_result["beobachtung"]:
                st.session_state.observations.append(turn_result["beobachtung"])
            
            # Gutachter-Antwort hinzufügen
            gutachter_reply = turn_result["gutachter_antwort"]
            st.session_state.messages.append({"role": "assistant", "content": gutachter_reply})
            
            # Audio generieren
            if tts_enabled:
                tts_res = generate_tts_audio(gutachter_reply, selected_voice)
                if tts_res:
                    _, st.session_state.latest_audio_b64 = tts_res
                else:
                    st.session_state.latest_audio_b64 = None
        
        st.rerun()
