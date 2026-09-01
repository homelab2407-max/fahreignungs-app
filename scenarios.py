"""
scenarios.py - Vordefinierte Fallakten für die Schweizer Fahreignungsabklärung
Enthält realistische Szenarien gemäss den Kriterien der Schweizer Vereinigung für Verkehrspsychologie (VfV)
und den Richtlinien der kantonalen Strassenverkehrsämter (ASA).
"""

from typing import Dict, Any, List

SCENARIOS: Dict[str, Dict[str, Any]] = {
    "kokain": {
        "id": "kokain",
        "title": "Kokain – Positiver Befund bei Verkehrskontrolle",
        "case_number": "#2026-FK-89",
        "category": "Betäubungsmittel (Kokain)",
        "badge_color": "#f85149",
        "incident_date": "Vor 4 Monaten",
        "canton": "Zürich (StVA ZH)",
        "blood_values": "Kokain: 68 ng/ml, Benzoylecgonin: 540 ng/ml",
        "legal_basis": "SVG Art. 16d Abs. 1 lit. b (Fahruntüchtigkeit wg. Betäubungsmitteln) & VZV Art. 14 / 15e",
        "police_report": (
            "Anlässlich einer mobilen Verkehrskontrolle um 02:45 Uhr fiel der Proband durch unruhiges Verhalten "
            "und erweiterte Pupillen auf. Der Drogenschnelltest reagierte positiv auf Kokain. "
            "Die anschliessende Blut- und Urinuntersuchung am IRM bestätigte akuten und kürzlichen Konsum."
        ),
        "focus_areas": [
            "Konsummuster & Konsumfrequenz (Erstkonsum vs. Gewohnheit)",
            "Trennungsvermögen zwischen Konsum und Verkehrsteilnahme",
            "Motive für den Substanzkonsum (Stress, Party, Leistungsdruck)",
            "Glaubhaftigkeit der Abstinenzbehauptung & Urinscreenings",
            "Rückfallprophylaxe & Umgang mit risikoreichen Situationen"
        ],
        "initial_question": (
            "Grüezi. Ich bin Dr. Urs Meier, Ihr zuständiger Verkehrspsychologe. "
            "In den Akten des Strassenverkehrsamts liegt ein Vorfall vom März mit einem positiven Kokainbefund vor. "
            "Bitte schildern Sie mir aus Ihrer Sicht: Wie kam es damals zu diesem Konsum und der anschliessenden Fahrt?"
        ),
    },
    "alkohol": {
        "id": "alkohol",
        "title": "Alkohol 1.82‰ – Trunkenheitsfahrt mit Sachschaden",
        "case_number": "#2026-AL-42",
        "category": "Alkohol (Schwere Fahrunfähigkeit)",
        "badge_color": "#e3b341",
        "incident_date": "Vor 6 Monaten",
        "canton": "Bern (SVSA BE)",
        "blood_values": "Blutalkoholkonzentration (BAK): 1.82 Promille",
        "legal_basis": "SVG Art. 16c Abs. 1 lit. b (Qualifizierte Alkohol-Fahrunfähigkeit ≥ 1.6‰) & Art. 53 SVG",
        "police_report": (
            "Der Proband kollidierte um 23:15 Uhr beim Einbiegen in eine Kreuzung mit einem parkierten Fahrzeug. "
            "Es entstand erheblicher Sachschaden. Ein durchgeführter Atemalkoholtest sowie die Blutentnahme "
            "ergaben einen Wert von 1.82‰. Der Führerausweis wurde auf der Stelle vorsorglich entzogen."
        ),
        "focus_areas": [
            "Vorhandene Alkoholgewöhnung / hohe Alkoholverträglichkeit bei 1.82‰",
            "Trinkvorgeschichte & realistische Mengenanalyse",
            "Verharmlosungstendenz ('Habe mich noch völlig fit gefühlt')",
            "Kontrolliertes Trinken vs. strikte Abstinenz als Zukunftsstrategie",
            "Veränderungen im Alltag & Coping-Strategien bei Belastung"
        ],
        "initial_question": (
            "Guten Tag. Wir führen heute die Fahreignungsabklärung bezüglich Ihrer Trunkenheitsfahrt mit 1.82 Promille durch. "
            "Ein solcher Wert deutet auf eine deutliche Trinkgewöhnung hin. "
            "Erklären Sie mir bitte: Wie sah Ihr Alkoholkonsum an jenem Abend und im Vorfeld dieser Fahrt konkret aus?"
        ),
    },
    "cannabis": {
        "id": "cannabis",
        "title": "Cannabis – Verdacht auf regelmässigen Konsum & fehlendes Trennvermögen",
        "case_number": "#2026-THC-15",
        "category": "Betäubungsmittel (Cannabis / THC)",
        "badge_color": "#2ea043",
        "incident_date": "Vor 3 Monaten",
        "canton": "Aargau (StVA AG)",
        "blood_values": "Freies THC: 3.4 ng/ml, THC-COOH (Abbauprodukt): 72 ng/ml",
        "legal_basis": "SVG Art. 16d Abs. 1 lit. b & Nulltoleranz / Grenzwert VZV Art. 14 / 15e",
        "police_report": (
            "Der Lenker wurde wegen defekter Beleuchtung angehalten. Im Fahrzeuginneren war deutlicher Marihuanageruch wahrnehmbar. "
            "Der Proband gab an, 'nur am Vorabend' einen Joint geraucht zu haben. Der THC-COOH Wert von 72 ng/ml "
            "weist jedoch auf regelmässigen bzw. chronischen Konsum hin."
        ),
        "focus_areas": [
            "Widerspruch zwischen behauptetem Gelegenheitskonsum und Laborwerten",
            "Mangelndes Wissen über Halbwertszeiten & Nachweisbarkeit von THC",
            "Funktion des Konsums (Einschlafhilfe, Stressbewältigung, Freizeit)",
            "Gefahr des schleichenden Rückfalls in alte Gewohnheiten",
            "Konkrete Massnahmen zur dauerhaften Verhaltensänderung"
        ],
        "initial_question": (
            "Grüezi. Das Strassenverkehrsamt hat eine Abklärung angeordnet, da bei Ihnen aktives THC sowie ein erhöhter "
            "THC-COOH-Wert festgestellt wurden. "
            "Sie gaben bei der Polizei an, nur selten zu konsumieren. Wie passt das mit dem Laborbefund zusammen?"
        ),
    },
    "via_sicura": {
        "id": "via_sicura",
        "title": "Via Sicura – Raserdelikt (88 km/h in 30er-Zone innerorts)",
        "case_number": "#2026-VS-99",
        "category": "Via Sicura (Charakterliche Eignung / Raser)",
        "badge_color": "#a371f7",
        "incident_date": "Vor 8 Monaten",
        "canton": "Basel-Landschaft (MFK BL)",
        "blood_values": "Keine Substanzen. Gemessene Geschwindigkeit: 88 km/h (nach Abzug 83 km/h)",
        "legal_basis": "SVG Art. 90 Abs. 3 / 4 (Raserdelikt) & Art. 16c Abs. 2 lit. a bis SVG",
        "police_report": (
            "Mittels stationärer Geschwindigkeitsmessung wurde der Lenker mit 88 km/h in einer signalisierten 30 km/h-Zone "
            "in einem Wohngebiet erfasst. Gemäss Art. 90 Abs. 4 lit. a SVG liegt ein qualifiziertes Raserdelikt vor. "
            "Das Strassenverkehrsamt verlangt ein verkehrspsychologisches Gutachten zur charakterlichen Fahreignung."
        ),
        "focus_areas": [
            "Akzeptanz von Regeln, Gesetzen und Autoritäten",
            "Impulskontrolle, emotionale Selbstregulation & Frustrationstoleranz",
            "Verharmlosung des Risikos für schwächere Verkehrsteilnehmer (Kinder, Fussgänger)",
            "Geltungsbedürfnis, Dominanzverhalten oder Zeitdruck als Triebfeder",
            "Tatsächliche Einsicht in das Gefahrenpotenzial und künftige Selbstdisziplin"
        ],
        "initial_question": (
            "Grüezi. Wir befassen uns heute mit dem Vorfall in der 30er-Zone, bei dem Sie mit über 80 km/h gemessen wurden. "
            "Ein solches Tempo in einem Wohngebiet ist hochgradig gefährlich. "
            "Was ging in jenem Moment in Ihnen vor, und was hat Sie dazu bewogen, das Tempolimit so extrem zu missachten?"
        ),
    },
    "custom": {
        "id": "custom",
        "title": "Individueller Fall (Benutzerdefiniert)",
        "case_number": "#2026-CUSTOM",
        "category": "Individuelle Fragestellung",
        "badge_color": "#58a6ff",
        "incident_date": "Vor kurzem",
        "canton": "Kanton nach Wahl",
        "blood_values": "Benutzerdefiniert",
        "legal_basis": "Art. 16d SVG (Fahreignungsuntersuchung)",
        "police_report": "Benutzerdefinierter Sachverhalt gemäss Eingabe.",
        "focus_areas": [
            "Ursachen & Motive des Vorfalls",
            "Selbstreflexion & Einsicht",
            "Zukünftige Strategien zur Vermeidung"
        ],
        "initial_question": (
            "Grüezi. Ich begrüsse Sie zu Ihrer verkehrspsychologischen Fahreignungsabklärung. "
            "Bitte schildern Sie mir einleitend den Sachverhalt, der zu dieser behördlichen Untersuchung geführt hat."
        ),
    }
}


def get_scenario(scenario_id: str) -> Dict[str, Any]:
    """Liefert die Falldaten für die übergebene ID zurück."""
    return SCENARIOS.get(scenario_id, SCENARIOS["kokain"])


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Liefert alle vordefinierten Fälle als Liste zurück."""
    return list(SCENARIOS.values())
