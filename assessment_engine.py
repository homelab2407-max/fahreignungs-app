"""
assessment_engine.py - KI-Engine & Verkehrspsychologischer Gutachter-Simulator
Verwaltet Gemini-API-Aufrufe, psychologische Analyse, dynamisches Scoring,
Abschlussgutachten-Erstellung und Text-to-Speech (TTS).
"""

import asyncio
import base64
import json
import os
import re
from typing import Dict, Any, List, Optional, Tuple

from google import genai
from google.genai import types

# Standard-Modell
GEMINI_MODEL = "gemini-2.5-flash"

# Verfügbare TTS-Stimmen via edge-tts
TTS_VOICES = {
    "Schweizerdeutsch / Akzent (Jan)": "de-CH-JanNeural",
    "Schweizerdeutsch / Akzent (Leni)": "de-CH-LeniNeural",
    "Hochdeutsch (Conrad - Seriös)": "de-DE-ConradNeural",
    "Hochdeutsch (Katja - Klar)": "de-DE-KatjaNeural",
}


def get_gemini_client(api_key: Optional[str] = None) -> Optional[genai.Client]:
    """Initialisiert den Gemini Client mit dem angegebenen Key oder aus der Umgebung."""
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    try:
        return genai.Client(api_key=key)
    except Exception:
        return None


def build_system_prompt(scenario: Dict[str, Any]) -> str:
    """Erstellt den verkehrspsychologischen System-Prompt für das gewählte Szenario."""
    focus_list = "\n".join(f"- {f}" for f in scenario.get("focus_areas", []))
    
    return f"""Du bist Dr. phil. Urs Meier, ein erfahrener und anerkannter Fachpsychologe für Verkehrspsychologie FSP in der Schweiz.
Du führst im Auftrag des kantonalen Strassenverkehrsamts ({scenario.get('canton', 'Kantonales Strassenverkehrsamt')}) eine offizielle verkehrspsychologische Fahreignungsabklärung durch.

AKTENLAGE DES FALLS:
- Fall-Nummer: {scenario.get('case_number')}
- Delikt / Kategorie: {scenario.get('category')}
- Datum / Vorfall: {scenario.get('incident_date')}
- Messwerte / Labor: {scenario.get('blood_values')}
- Rechtliche Grundlage: {scenario.get('legal_basis')}
- Polizeibericht / Sachverhalt: {scenario.get('police_report')}

DEINE AUFGABE & VERHALTEN:
1. Du führst ein professionelles, strukturiertes, kritisches und zugleich sachliches Explorationsgespräch auf Deutsch (mit leichtem, höflichem Schweizer Bezug wie 'Grüezi', 'Verkehrsamt', 'Führerausweis', 'Billet').
2. Du glaubst dem Probanden nicht einfach Ausreden, Schutzbehauptungen oder Bagatellisierungen (z.B. "Ich war nur müde", "War nur ein einmaliger Ausrutscher", "Habe mich fit gefühlt", "Freunde haben mich überredet").
3. Du hakst sofort präzise nach, wenn Widersprüche zwischen den Akten/Messwerten und den Aussagen des Probanden auftreten.
4. Du prüfst schrittweise die 5 Phasen der verkehrspsychologischen Exploration:
   - Phase 1: Rekonstruktion des Vorfalls & Vorgeschichte
   - Phase 2: Motive, Konsummuster bzw. Fahrverhalten & Ursachen
   - Phase 3: Problembewusstsein & Reflexion über Gefahren
   - Phase 4: Nachweisbare Verhaltensänderungen, Coping-Strategien & Vermeidungsstrategie
   - Phase 5: Rückfallprophylaxe & Fazit
5. Schwerpunkte dieses Falls:
{focus_list}

WICHTIGE ANTWORTSTRUKTUR:
Du MUSST deine Antwort IMMER als valides JSON im folgenden Format zurückgeben (kein Markdown-Block darum herum, nur pures JSON):
{{
  "gutachter_antwort": "Der Text, den du direkt an den Probanden sprichst (1-3 gezielte Sätze, analytisch und fordernd).",
  "einsicht_score": 45,
  "transparenz_score": 30,
  "problembewusstsein_score": 40,
  "risiko_stufe": "Mittel",
  "beobachtung": "Kurze, prägnante psychologische Notiz über die letzte Antwort des Probanden für das Gutachterprotokoll (max. 2 Sätze).",
  "gespraechs_phase": "Phase 2/5: Ursachen & Konsummuster",
  "frage_nummer": 3
}}

Hinweise zu den Scores:
- einsicht_score: 0 bis 100 (wie gut sieht der Proband eigene Fehler und Gefahren ein?)
- transparenz_score: 0 bis 100 (wie ehrlich, offen und frei von Schutzbehauptungen ist der Proband?)
- problembewusstsein_score: 0 bis 100 (versteht der Proband die tieferen Ursachen und Mechanismen?)
- risiko_stufe: "Gering", "Mittel" oder "Hoch" (Rückfallgefahr bezüglich künftiger Verkehrsgefährdung)
"""


def generate_psychologist_turn(
    client: genai.Client,
    scenario: Dict[str, Any],
    history: List[Dict[str, str]],
    user_response: str,
    current_scores: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Sendet den Dialogverlauf an Gemini und holt die nächste Gutachter-Antwort
    inklusive aktualisierter psychologischer Scores und Notizen ab.
    """
    system_prompt = build_system_prompt(scenario)
    
    # Dialogverlauf für Prompt aufbauen
    dialogue_context = "Bisheriger Gesprächsverlauf:\n"
    for turn in history:
        role = "Gutachter Dr. Meier" if turn["role"] == "assistant" else "Proband (Klient)"
        dialogue_context += f"{role}: {turn['content']}\n"
    
    dialogue_context += f"Proband (Klient): {user_response}\n\n"
    dialogue_context += (
        f"Aktuelle bisherige Scores: Einsicht={current_scores.get('einsicht', 35) if current_scores else 35}, "
        f"Transparenz={current_scores.get('transparenz', 25) if current_scores else 25}. "
        f"Bewerte die Probanden-Aussage psychologisch und formuliere deine nächste Frage oder Erwiderung als JSON."
    )
    
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=f"{system_prompt}\n\n{dialogue_context}")]
                )
            ],
            config=types.GenerateContentConfig(
                temperature=0.4,
                response_mime_type="application/json",
            )
        )
        
        raw_text = response.text.strip()
        # Säubern falls Codeblock
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()
        
        data = json.loads(raw_text)
        return {
            "gutachter_antwort": data.get("gutachter_antwort", "Bitte führen Sie das noch etwas genauer aus."),
            "einsicht_score": max(0, min(100, int(data.get("einsicht_score", 35)))),
            "transparenz_score": max(0, min(100, int(data.get("transparenz_score", 25)))),
            "problembewusstsein_score": max(0, min(100, int(data.get("problembewusstsein_score", 30)))),
            "risiko_stufe": data.get("risiko_stufe", "Mittel"),
            "beobachtung": data.get("beobachtung", "Proband antwortet auf die Fragestellung."),
            "gespraechs_phase": data.get("gespraechs_phase", "Laufende Exploration"),
            "frage_nummer": int(data.get("frage_nummer", len(history) // 2 + 1))
        }
    except Exception as e:
        # Intelligenter Fallback bei API-Fehler
        return {
            "gutachter_antwort": (
                f"Ich verstehe Ihre Schilderung. Doch wenn wir auf die Aktenlage blicken: "
                f"Was haben Sie seither konkret unternommen, um eine Wiederholung auszuschliessen?"
            ),
            "einsicht_score": current_scores.get("einsicht", 40) if current_scores else 40,
            "transparenz_score": current_scores.get("transparenz", 30) if current_scores else 30,
            "problembewusstsein_score": current_scores.get("problembewusstsein", 35) if current_scores else 35,
            "risiko_stufe": "Mittel",
            "beobachtung": f"Antwort verarbeitet ({str(e)[:40]}).",
            "gespraechs_phase": "Phase 3/5: Verhaltensreflexion",
            "frage_nummer": len(history) // 2 + 1
        }


def generate_final_report(
    client: genai.Client,
    scenario: Dict[str, Any],
    history: List[Dict[str, str]],
    scores: Dict[str, Any],
    observations: List[str]
) -> Dict[str, Any]:
    """
    Erstellt ein offizielles, strukturiertes Schweizer Verkehrspsychologisches Gutachten
    basierend auf dem vollständigen Gesprächsverlauf und den Bewertungs-Scores.
    """
    dialog_text = "\n".join([
        f"[{m['role'].upper()}]: {m['content']}" for m in history
    ])
    
    obs_text = "\n".join([f"- {o}" for o in observations]) if observations else "Keine spezifischen Notizen."
    
    prompt = f"""Du bist Dr. phil. Urs Meier, Leitender Fachpsychologe für Verkehrspsychologie FSP.
Erstelle nun das offizielle VERKEHRSPSYCHOLOGISCHE GUTACHTEN zur Fahreignung für das {scenario.get('canton', 'Strassenverkehrsamt')}.

DATEN ZUR PERSON & ZUM FALL:
- Fall-Nummer: {scenario.get('case_number')}
- Delikt / Anlass: {scenario.get('category')}
- Datum / Messwerte: {scenario.get('blood_values')}
- Rechtliche Grundlage: {scenario.get('legal_basis')}

ASSESSMENT-ERGEBNISSE AUS DEM SIMULATOR:
- Einsichtsfähigkeit: {scores.get('einsicht', 50)}%
- Transparenz & Offenheit: {scores.get('transparenz', 50)}%
- Problembewusstsein: {scores.get('problembewusstsein', 50)}%
- Geschätztes Rückfallrisiko: {scores.get('risiko', 'Mittel')}

MITSCHRIFT & EXPLORATIONSPROTOKOLL:
{dialog_text}

PSYCHOLOGISCHE BEOBACHTUNGEN WÄHREND DES GESPRÄCHS:
{obs_text}

FORMATIERUNGSANFORDERUNG:
Erstelle ein fundiertes, hochprofessionelles Gutachten im Markdown-Format nach den ASA-Richtlinien der Vereinigung für Verkehrspsychologie.
Verwende exakt folgende Gliederung:

# 📋 VERKEHRSPSYCHOLOGISCHES GUTACHTEN
**Auftraggeber:** {scenario.get('canton', 'Kantonales Strassenverkehrsamt')} • Abteilung Administrativmassnahmen  
**Gutachter:** Dr. phil. Urs Meier, Fachpsychologe für Verkehrspsychologie FSP  
**Dossier-Nr.:** {scenario.get('case_number')} • **Status:** Abgeschlossen  

---

## 1. Anlass & Untersuchungsauftrag
(Zusammenfassung des Sachverhalts, Delikt, rechtliche Einordnung gemäss SVG/VZV)

## 2. Zusammenfassung der Exploration
(Wie schilderte der Proband den Vorfall? Welche Motive wurden genannt? Gibt es Widersprüche zur Aktenlage?)

## 3. Verkehrspsychologische Würdigung & Kriterienprüfung
- **3.1 Problembewusstsein & Einsichtsfähigkeit:** (Detaillierte Analyse)
- **3.2 Glaubhaftigkeit & Transparenz:** (Bewertung der Offenheit vs. Bagatellisierung)
- **3.3 Verhaltensänderung & Stabilität:** (Coping-Strategien, gelebte Veränderungen)
- **3.4 Rückfallprophylaxe:** (Umgang mit Risikofaktoren)

## 4. Prognose & Rückfallrisiko
(Einschätzung der künftigen Verkehrssicherheit)

---

## 5. Formelles Fazit & Empfehlung ans Strassenverkehrsamt

Gib hier eine unmissverständliche Empfehlung ab. Wähle basierend auf dem Gespräch eines der 3 Ergebnisse:
- 🟢 **BEFÜRWORTET:** Die Fahreignung aus verkehrspsychologischer Sicht ist gegeben.
- 🟡 **BEDINGT BEFÜRWORTET (MIT AUFLAGEN):** Fahreignung kann befürwortet werden unter Auflagen (z.B. 6-12 Monate forensische Abstinenzkontrollen, Alkoholsperre oder therapeutische Begleitung).
- 🔴 **ABGELEHNT:** Die Fahreignung ist zum jetzigen Zeitpunkt nicht gegeben. Eine Wiedererteilung wird nicht empfohlen.

(Begründe die Entscheidung in 3-4 klaren Sätzen und liste allfällige behördliche Auflagen auf.)
"""
    
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(
                temperature=0.3,
            )
        )
        report_markdown = response.text
        
        # Bestimme Empfehlung für UI-Badge
        status = "BEDINGT BEFÜRWORTET"
        if "🟢 **BEFÜRWORTET" in report_markdown or "🟢 BEFÜRWORTET" in report_markdown or "befürwortet" in report_markdown.lower() and "nicht befürwortet" not in report_markdown.lower() and scores.get('einsicht', 50) >= 70:
            status = "BEFÜRWORTET"
        elif "🔴 **ABGELEHNT" in report_markdown or "🔴 ABGELEHNT" in report_markdown or scores.get('einsicht', 50) < 40 or scores.get('risiko') == "Hoch":
            status = "ABGELEHNT"
            
        return {
            "markdown": report_markdown,
            "status": status
        }
    except Exception as e:
        fallback_md = f"""# 📋 VERKEHRSPSYCHOLOGISCHES GUTACHTEN (Vorläufig)
**Dossier-Nr.:** {scenario.get('case_number')}  
**Anlass:** {scenario.get('category')}  
**Hinweis:** Automatische Generierung via API ({str(e)}).

## 1. Aktenlage & Vorfall
Der Proband wurde anlässlich des Delikts {scenario.get('category')} begutachtet.

## 2. Psychologischer Befund
- Einsichtsfähigkeit: {scores.get('einsicht', 0)}%
- Transparenz: {scores.get('transparenz', 0)}%
- Problembewusstsein: {scores.get('problembewusstsein', 0)}%

## 3. Empfehlung ans Strassenverkehrsamt
🟡 **BEDINGT BEFÜRWORTET MIT AUFLAGEN**: Zur Sicherung der Abstinenz und Festigung der Verhaltensänderung werden 6 Monate forensische Kontrollen empfohlen.
"""
        return {
            "markdown": fallback_md,
            "status": "BEDINGT BEFÜRWORTET"
        }


async def _async_edge_tts(text: str, voice: str) -> bytes:
    """Erzeugt Audiodaten asynchron mit edge-tts."""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    audio_data = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
    return bytes(audio_data)


def generate_tts_audio(text: str, voice_name: str = "Schweizerdeutsch / Akzent (Jan)") -> Optional[Tuple[bytes, str]]:
    """
    Generiert MP3-Audiodaten für den übergebenen Text.
    Gibt ein Tupel (audio_bytes, base64_str) zurück.
    """
    # Text bereinigen (keine Regieanweisungen, JSON oder Sternchen sprechen)
    cleaned_text = re.sub(r'[\*\#\_\"\[\]\(\)]', ' ', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    if not cleaned_text:
        return None
        
    voice = TTS_VOICES.get(voice_name, "de-CH-JanNeural")
    
    try:
        # Erst edge-tts probieren
        audio_bytes = asyncio.run(_async_edge_tts(cleaned_text, voice))
        b64 = base64.b64encode(audio_bytes).decode("utf-8")
        return audio_bytes, b64
    except Exception:
        try:
            # Fallback zu gTTS
            from gtts import gTTS
            import io
            tts = gTTS(text=cleaned_text, lang="de", tld="ch")
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_bytes = fp.read()
            b64 = base64.b64encode(audio_bytes).decode("utf-8")
            return audio_bytes, b64
        except Exception:
            return None
