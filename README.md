# 🇨🇭 Schweizer Fahreignungsabklärung – Live-Simulator

Ein interaktives verkehrspsychologisches Explorations- und Simulationssystem im Auftrag kantonaler Strassenverkehrsämter (ASA / VfV Kriterien).

Ermöglicht das Training und die Vorbereitung auf Fahreignungsuntersuchungen (MPU-Äquivalent in der Schweiz) bei Betäubungsmittel-, Alkohol- und Raserdelikten (Via Sicura).

---

## ✨ Features

1. **KI-Verkehrspsychologe (Dr. phil. Urs Meier):**
   - Fachpsychologe für Verkehrspsychologie FSP.
   - Realistischer, fordernder Interviewstil zur Aufdeckung von Schutzbehauptungen, Bagatellisierungen und Widersprüchen zu den Akten.
   - Basiert auf dem modernen `google-genai` SDK mit Gemini 2.5 Flash.

2. **Dynamisches Live-Scoring & Psychometrie:**
   - **Einsichtsfähigkeit** (0–100%)
   - **Transparenz & Offenheit** (0–100%)
   - **Problembewusstsein** (0–100%)
   - **Rückfallrisiko** (Gering / Mittel / Hoch)
   - **Psychologisches Gutachter-Notizbuch:** Laufende Zwischenprotokolle und Beobachtungen in der Sidebar.

3. **Sprachinteraktion (Audio & TTS):**
   - 🎙️ **Spracheingabe:** Direkte Aufnahme per Mikrofon via Web-Speech / `streamlit-mic-recorder`.
   - 🗣️ **Sprachausgabe:** Realistische Sprachgenerierung mit `edge-tts` (u.a. Schweizer Akzent `de-CH-JanNeural`, `de-CH-LeniNeural` oder Hochdeutsch `de-DE-ConradNeural`).

4. **Offizielles Abschlussgutachten:**
   - Erstellt auf Knopfdruck einen vollständigen, formellen Befundbericht nach Schweizer ASA/VfV-Kriterien.
   - Eindeutige Empfehlung ans Strassenverkehrsamt:
     - 🟢 **Befürwortet**
     - 🟡 **Bedingt befürwortet mit Auflagen** (z.B. 6 Monate Abstinenzscreenings / Haaranalysen)
     - 🔴 **Abgelehnt**
   - Download als formatiertes Markdown (`.md`).

5. **Fallakten & Szenarien (Polizeikontrollen & Delikte):**
   - **Kokain (Erstbefund)** – Fall `#2026-FK-89` (StVA Zürich)
   - **Alkohol 1.82‰ (Fahrunfähigkeit)** – Fall `#2026-AL-42` (SVSA Bern)
   - **Cannabis & Trennvermögen** – Fall `#2026-THC-15` (StVA Aargau)
   - **Via Sicura / Raserdelikt** – Fall `#2026-VS-99` (MFK Basel-Landschaft)
   - **Mischkonsum (Alkohol & Kokain)** – Fall `#2026-MK-63` (DVS Luzern)
   - **MDMA & Amphetamin (Festival-Rückreise)** – Fall `#2026-MD-27` (StVA St. Gallen)
   - **Medikamente & Psychotrope Stoffe (Zolpidem/Diazepam)** – Fall `#2026-MED-54` (MFK Solothurn)
   - **Kontrollverweigerung / Vereitelung (Art. 91a SVG)** – Fall `#2026-VF-12` (SAN Wallis)
   - **Aggressive Nötigung & Road Rage** – Fall `#2026-AG-77` (StVA Zürich)
   - **Mehrfachdelinquenz / Kaskadentäter** – Fall `#2026-WD-18` (SVSA Bern)
   - **Individueller Fall** (Benutzerdefiniert)

---

## 📁 Projektstruktur

```
fahreignungs-app/
├── app.py                   # Haupt-UI (Streamlit, Audio-Recorder, Score-Visualisierung)
├── assessment_engine.py     # Gemini-Anbindung, Prompt-Logik, Scoring & Edge-TTS
├── scenarios.py             # Falldefinitionen, Grenzwerte, Akten & Rechtsgrundlagen
├── requirements.txt         # Python-Abhängigkeiten
├── Dodge-Demon-Logo.png     # Logo-Asset
├── .streamlit/
│   └── config.toml          # Dark-Mode Styling
├── .gitignore
└── README.md
```

---

## 🚀 Schnelleinstieg / Starten

### 1. Virtuelle Umgebung aktivieren & Abhängigkeiten installieren
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Gemini API-Key setzen (Optional)
```bash
export GEMINI_API_KEY="DEIN_GEMINI_API_KEY"
```
*(Alternativ kann der Key auch direkt in der Streamlit-Sidebar im Eingabefeld hinterlegt werden.)*

### 3. Anwendung starten
```bash
streamlit run app.py
```
Die App öffnet sich unter **`http://localhost:8501`**.
