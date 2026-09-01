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
    "mischkonsum": {
        "id": "mischkonsum",
        "title": "Mischkonsum – Alkohol (0.95‰) & Kokain bei Nachtkontrolle",
        "case_number": "#2026-MK-63",
        "category": "Mischkonsum (Alkohol & Kokain)",
        "badge_color": "#f0883e",
        "incident_date": "Vor 4 Monaten",
        "canton": "Luzern (DVS LU)",
        "blood_values": "BAK: 0.95 Promille, Kokain: 42 ng/ml, Benzoylecgonin: 380 ng/ml",
        "legal_basis": "SVG Art. 16c Abs. 1 lit. b & Art. 16d Abs. 1 lit. b (Kumulative Fahrunfähigkeit bei Mischkonsum)",
        "police_report": (
            "Anlässlich einer mobilen Schwerpunktkontrolle 'Nachtleben' um 03:20 Uhr in Luzern fiel der Lenker durch "
            "überhöhte Innerorts-Geschwindigkeit und verzögerte Reaktion an einer Lichtsignalanlage auf. "
            "Der Atemalkoholtest ergab 0.95‰. Aufgrund von auffälliger motorischer Unruhe und verlangsamter Pupillenreaktion "
            "wurde ein Drogenschnelltest durchgeführt, welcher positiv auf Kokain reagierte. "
            "Die anschliessende Blutuntersuchung am IRM bestätigte den gleichzeitigen Mischkonsum."
        ),
        "focus_areas": [
            "Wechselwirkungen & gefährliche Risikoverstärkung (Kokain dämpft subjektive Alkoholwahrnehmung)",
            "Trennungsvermögen und Planungsverhalten bei Abenden im Nachtleben",
            "Motive und Frequenz des parallelen Konsums im Freundeskreis",
            "Verharmlosungstendenz bezüglich der kumulativen Fahruntüchtigkeit",
            "Konkretes Vermeidungs- und Notfallkonzept für künftige Ausgangssituationen"
        ],
        "initial_question": (
            "Grüezi. Anlässlich der Luzerner Polizeikontrolle wurden bei Ihnen gleichzeitig 0.95 Promille Alkohol "
            "sowie aktives Kokain im Blut nachgewiesen. Durch diesen Mischkonsum entsteht eine massive Selbstüberschätzung bei "
            "gleichzeitig gravierend vermindertem Reaktionsvermögen. "
            "Wie kam es zu dieser folgenschweren Entscheidung, sich trotz beider Substanzen ans Steuer zu setzen?"
        ),
    },
    "mdma_speed": {
        "id": "mdma_speed",
        "title": "Amphetamin & MDMA – Anhaltung nach Musikfestival am Sonntagmorgen",
        "case_number": "#2026-MD-27",
        "category": "Betäubungsmittel (Amphetamin / MDMA)",
        "badge_color": "#db61a2",
        "incident_date": "Vor 5 Monaten",
        "canton": "St. Gallen (StVA SG)",
        "blood_values": "MDMA (Ecstasy): 140 ng/ml, Amphetamin (Speed): 38 ng/ml",
        "legal_basis": "SVG Art. 16d Abs. 1 lit. b & VZV Art. 14 / 15e (Nulltoleranz-Grenzwert für Designerdrogen)",
        "police_report": (
            "Auf der Autobahn A1 bei der Raststätte St. Margrethen wurde der Lenker um 08:15 Uhr anlässlich einer "
            "morgendlichen Nachfahrkontrolle angehalten. Die Patrouille stellte stark zittrige Hände, motorische Hyperaktivität "
            "und trotz Tageslichts maximal erweiterte Pupillen fest. Der Proband gab an, von einem Wochenendfestival "
            "heimzureisen und sich nach zweistündigem Zeltschlaf 'wieder völlig fahrfähig und wach' gefühlt zu haben."
        ),
        "focus_areas": [
            "Mangelndes Wissen über Halbwertszeiten und neurotoxische Nachwirkungen von Stimulanzien",
            "Gefährliche Kombination aus Schlafmangel, Erschöpfung und 'Rebound'-Effekt",
            "Funktion von Partydrogen im Freizeitverhalten und Gruppendruck",
            "Glaubhaftigkeit bezüglich früherer Konsumerfahrungen und Konsumhäufigkeit",
            "Nachweisbare Distanzierung vom konsumierenden Umfeld und Eventmilieu"
        ],
        "initial_question": (
            "Guten Tag. Bei der Autobahnkontrolle um 8 Uhr morgens wurden in Ihrem Blut hohe Konzentrationen von MDMA und "
            "Amphetamin gemessen. Sie gaben damals an, nach zwei Stunden Schlaf wieder fit gewesen zu sein. "
            "Wie beurteilen Sie rückblickend diese Selbsteinschätzung und das damit verbundene Gefahrenpotenzial?"
        ),
    },
    "medikamente": {
        "id": "medikamente",
        "title": "Medikamente – Schlangenlinienfahrt unter Benzodiazepinen & Zolpidem",
        "case_number": "#2026-MED-54",
        "category": "Arzneimittel / Psychotrope Stoffe",
        "badge_color": "#79c0ff",
        "incident_date": "Vor 3 Monaten",
        "canton": "Solothurn (MFK SO)",
        "blood_values": "Zolpidem: 115 ng/ml (übertherapeutisch), Diazepam: 240 ng/ml, Nordazepam: 320 ng/ml",
        "legal_basis": "SVG Art. 16d Abs. 1 lit. b & Art. 2 Abs. 2 VRV (Fahrunfähigkeit infolge Arzneimitteleinwirkung)",
        "police_report": (
            "Aufgrund einer Meldung über einen Lenker mit extrem unsicherer Fahrweise und wiederholtem Überfahren der "
            "Sicherheitslinie auf der Kantonsstrasse stoppte die Polizei das Fahrzeug um 14:15 Uhr. "
            "Der Lenker wies verwaschene Sprache, verengte Augen und starke Gangunsicherheiten auf. "
            "Der Atemalkoholtest verlief negativ (0.0‰). Die toxikologische Analyse am Institut für Rechtsmedizin "
            "wies stark übertherapeutische Spiegel von Schlaf- und Beruhigungsmitteln nach."
        ),
        "focus_areas": [
            "Missachtung von ärztlichen Warnungen und Beipackzetteln bezüglich Fahrfähigkeit",
            "Entwicklung einer Medikamententoleranz, Dosissteigerung und psychische Gewöhnung",
            "Motive der Selbstmedikation (Schlafstörungen, Angst, beruflicher Druck)",
            "Zusammenarbeit mit behandelnden Fachärzten und Umstellung der Medikation",
            "Dauerhafte Gewährleistung der Fahrfähigkeit ohne sedierende Substanzen"
        ],
        "initial_question": (
            "Grüezi. Sie wurden am frühen Nachmittag wegen massiver Fahruntüchtigkeit angehalten. Das toxikologische "
            "Gutachten ergab Schlaf- und Beruhigungsmittel weit über der therapeutischen Norm. "
            "Wie kam es zu dieser starken Überdosierung am hellichten Tag und weshalb haben Sie dennoch ein Fahrzeug gelenkt?"
        ),
    },
    "flucht_verweigerung": {
        "id": "flucht_verweigerung",
        "title": "Kontrollverweigerung – Flucht vor Kontrollstelle & Blutprobe verweigert",
        "case_number": "#2026-VF-12",
        "category": "Vereitelung von Massnahmen (SVG 91a)",
        "badge_color": "#ff7b72",
        "incident_date": "Vor 6 Monaten",
        "canton": "Wallis (DSI / SAN VS)",
        "blood_values": "Messung vereitelt / verweigert (Rechtlich qualifizierter Fahrunfähigkeit gleichgestellt)",
        "legal_basis": "SVG Art. 91a Abs. 1 (Vereitelung von Massnahmen zur Feststellung der Fahrunfähigkeit) & Art. 16c Abs. 1 lit. d SVG",
        "police_report": (
            "Um 23:45 Uhr missachtete der Lenker die Halteaufforderung an einem stationären Kontrollposten und versuchte, "
            "sich der Kontrolle durch rasches Abbiegen und Beschleunigen in eine Seitenstrasse zu entziehen. "
            "Nach kurzer Nachfahrt konnte das Fahrzeug gestoppt werden. Der Proband trat verbal aggressiv auf, roch stark nach Alkohol "
            "und verweigerte sowohl den Atemalkoholtest als auch die im Spital ärztlich angeordnete Blut- und Urinprobe."
        ),
        "focus_areas": [
            "Motive für die Kontrollflucht und die strikte Verweigerung der behördlichen Massnahme",
            "Ehrliche Aufarbeitung des tatsächlichen Konsums am Vorfallsabend",
            "Impulsive Vermeidungsreaktionen und mangelhafte Impulskontrolle unter Stress",
            "Haltung gegenüber Verkehrsregeln, Polizei und staatlichen Institutionen",
            "Übernahme persönlicher Verantwortung ohne Schuldverschiebung auf die Einsatzkräfte"
        ],
        "initial_question": (
            "Guten Tag. Sie haben sich einer regulären Polizeikontrolle durch Flucht entzogen und anschliessend jede "
            "Blutentnahme verweigert. Das Gesetz stellt dies einer schweren Trunkenheitsfahrt gleich. "
            "Warum haben Sie damals so drastisch reagiert, und was genau wollten Sie vor den Polizeibeamten verbergen?"
        ),
    },
    "aggressiv_noetigung": {
        "id": "aggressiv_noetigung",
        "title": "Aggressives Fahrverhalten – Dichtes Auffahren & Rechtsüberholen auf Autobahn",
        "case_number": "#2026-AG-77",
        "category": "Charakterliche Eignung (Aggression / Nötigung)",
        "badge_color": "#d29922",
        "incident_date": "Vor 7 Monaten",
        "canton": "Zürich (Kantonspolizei ZH / StVA ZH)",
        "blood_values": "Keine Substanzen (Alkohol 0.0‰, Drogenschnelltest negativ)",
        "legal_basis": "SVG Art. 90 Abs. 2 (Grobe Verkehrsregelverletzung), Art. 34 Abs. 4 SVG (Abstand) & Art. 35 Abs. 1 SVG",
        "police_report": (
            "Eine zivile Video-Patrouille der Kantonspolizei dokumentierte auf der A3 über 4 Kilometer ein massiv aggressives "
            "Fahrverhalten: Der Proband fuhr bei 120 km/h mit weniger als 4 Metern Abstand auf vorausfahrende Fahrzeuge auf, "
            "betätigte dauerhaft die Lichthupe, überholte verbotswidrig rechts über den Pannenstreifen und bremste ein anderes "
            "Fahrzeug nach dem Wiedereinbiegen mutwillig aus ('Road Rage')."
        ),
        "focus_areas": [
            "Emotionsregulation, Impulsdurchbrüche und Frustrationstoleranz am Steuer",
            "Mangelndes Empathievermögen für schwächere und verunsicherte Verkehrsteilnehmer",
            "Auslöser und Triebfedern (beruflicher Stress, Zeitnot, Geltungsdrang, Aggressionsstau)",
            "Erkennen und Abbauen von Selbstjustiz- und Belehrmustern im Strassenverkehr",
            "Praktische Deeskalations- und Selbstberuhigungsstrategien für Konfliktsituationen"
        ],
        "initial_question": (
            "Grüezi. Die Videoaufzeichnung der Autobahnpolizei zeigt ein hochriskantes Verhalten: Drängeln mit wenigen Metern "
            "Abstand, Lichthupe, Rechtsüberholen und Ausbremsen. Ein solches Verhalten gefährdet Menschenleben direkt. "
            "Was ging in jenem Moment in Ihnen vor, und wie erklären Sie sich diesen extremen Kontrollverlust?"
        ),
    },
    "wiederholungstaeter": {
        "id": "wiederholungstaeter",
        "title": "Mehrfachdelinquenz – Wiederholte Geschwindigkeits- & Regelmissachtungen",
        "case_number": "#2026-WD-18",
        "category": "Charakterliche Eignung (Mehrfachtäter / Kaskade)",
        "badge_color": "#bc8cff",
        "incident_date": "Vor 4 Monaten",
        "canton": "Bern (SVSA BE)",
        "blood_values": "Keine Substanzen. Festgestellte Delikthäufung im Führerausweisregister (ADMAS)",
        "legal_basis": "SVG Art. 16c Abs. 2 lit. c / Art. 16d Abs. 1 lit. c (Charakterliche Nichteignung wegen unbelehrbaren Verhaltens)",
        "police_report": (
            "Anlässlich einer routinemässigen Verkehrskontrolle in Bern wurde festgestellt, dass der Lenker innerhalb von 24 Monaten "
            "bereits zum dritten Mal wegen grober Verkehrsregelverletzungen (wiederholte Geschwindigkeitsüberschreitungen >25 km/h, "
            "Mobiltelefonbedienung bei Autobahnfahrt und Vortrittsmissachtung mit Beinahe-Kollision) aufgefallen ist. "
            "Das SVSA ordnete wegen mangelnder Regeleinsicht und Rückfallgefahr ein verkehrspsychologisches Fahreignungsgutachten an."
        ),
        "focus_areas": [
            "Grundsätzliche Einstellung zu Rechtsnormen, Limits und Verkehrssicherheit",
            "Ursachen der chronischen Verharmlosung ('Geht doch jedem so', 'Abzocke der Behörden')",
            "Mangelnde Lernfähigkeit trotz vorangegangener Ausweisentzüge und Bussen",
            "Zusammenhang zwischen Zeitmanagement, Alltagshektik und Verkehrsdelinquenz",
            "Entwicklung eines verbindlichen Verhaltenskodex zur strikten Regeltreue"
        ],
        "initial_question": (
            "Guten Tag. Das Strassenverkehrsamt hat dieses Gutachten angeordnet, weil Sie innerhalb von zwei Jahren bereits zum "
            "dritten Mal schwerwiegend gegen Verkehrsregeln verstossen haben. Vorherige Verwarnungen und Entzüge blieben offenbar wirkungslos. "
            "Warum fällt es Ihnen so schwer, sich dauerhaft an die geltenden Verkehrsregeln zu halten?"
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
