# Development Plan Agent

Ein Agent, der einen detaillierten Entwicklungsplan für Softwareprojekte erstellt. Der Agent nutzt einen Reasoner, um die Projektanforderungen zu analysieren, und einen Planner, um einen strukturierten Entwicklungsplan zu erstellen. Der Agent unterstützt sowohl Deutsch als auch Englisch und kann auf Feedback in beiden Sprachen reagieren.

## Architektur

Der Development Plan Agent besteht aus drei Hauptkomponenten:

1. **dev_plan_graph.py**: Definiert den Workflow des Agenten mit LangGraph
   - Reasoner-Node: Analysiert die Projektanforderungen
   - Planner-Node: Erstellt den Entwicklungsplan
   - Refiner-Node: Verfeinert den Plan basierend auf Feedback

2. **dev_plan_service.py**: FastAPI-Service, der den Agenten-Workflow ausführt
   - Stellt einen `/invoke`-Endpunkt bereit
   - Verarbeitet Anfragen und gibt Antworten zurück

3. **dev_plan_mcp.py**: MCP-Server, der als Brücke zu externen Systemen dient
   - Stellt Tools wie `create_thread()` und `run_agent()` bereit
   - Verwaltet Gesprächs-IDs und leitet Anfragen weiter

## Installation

### Voraussetzungen

- Python 3.10 oder höher
- pip (Python Package Installer)

### Methode 1: Direkte Installation

1. Klone das Repository:
   ```bash
   git clone https://github.com/yourusername/dev-plan-agent.git
   cd dev-plan-agent
   ```

2. Erstelle eine virtuelle Umgebung:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unter Windows: venv\Scripts\activate
   ```

3. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

4. Kopiere die `.env.example` Datei zu `.env` und füge deine API-Schlüssel ein:
   ```bash
   cp .env.example .env
   ```

5. Bearbeite die `.env` Datei und füge deine OpenAI und/oder Anthropic API-Schlüssel ein.

### Methode 2: Installation als Paket

1. Installiere das Paket direkt von GitHub:
   ```bash
   pip install git+https://github.com/yourusername/dev-plan-agent.git
   ```

2. Erstelle eine `.env` Datei in deinem Arbeitsverzeichnis mit den erforderlichen API-Schlüsseln.

## Verwendung

### Starten des MCP-Servers

```bash
python -m dev_plan_agent.run_mcp
```

Oder wenn du das Repository direkt geklont hast:

```bash
python run_mcp.py
```

### Testen des Agenten

Du kannst den Agenten mit dem mitgelieferten Testskript testen:

```bash
python test_mcp.py
```

### Integration in eigene Anwendungen

Verwende die bereitgestellten MCP-Tools in deiner Anwendung:

```python
# Beispiel für die Integration in eine eigene Anwendung
import json
import subprocess

# Starte den MCP-Server (oder starte ihn separat)
mcp_process = subprocess.Popen(
    ["python", "-m", "dev_plan_agent.run_mcp"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

# Erstelle einen Thread
create_thread_request = {
    "jsonrpc": "2.0",
    "method": "create_thread",
    "params": {},
    "id": 1
}
mcp_process.stdin.write(json.dumps(create_thread_request) + "\n")
mcp_process.stdin.flush()
response = json.loads(mcp_process.stdout.readline())
thread_id = response.get("result")

# Sende eine Anfrage an den Agenten
run_agent_request = {
    "jsonrpc": "2.0",
    "method": "run_agent",
    "params": {
        "thread_id": thread_id,
        "user_input": "Beschreibe dein Projekt hier..."
    },
    "id": 2
}
mcp_process.stdin.write(json.dumps(run_agent_request) + "\n")
mcp_process.stdin.flush()
response = json.loads(mcp_process.stdout.readline())
print(response.get("result"))
```

## Workflow

1. Der Benutzer beschreibt sein Softwareprojekt
2. Der Reasoner analysiert die Anforderungen und definiert den Projektumfang
3. Der Planner erstellt einen detaillierten Entwicklungsplan
4. Der Benutzer kann Feedback geben, um den Plan zu verfeinern
5. Der Agent gibt den endgültigen Plan zurück

## Beispiel

```
Benutzer: "Ich möchte eine Web-App für Finanzberatung entwickeln, die den aktuellen Excel-basierten Prozess ersetzt. Die App soll Kundendaten verwalten, Finanzanalysen durchführen und personalisierte Investmentstrategien vorschlagen."

Agent: [Analysiert die Anforderungen und erstellt einen detaillierten Entwicklungsplan mit Phasen, Meilensteinen, Aufgaben und Ressourcenzuweisung]

Benutzer: "Könntest du bitte mehr Details zur Datensicherheit und zum Datenschutz hinzufügen?"

Agent: [Verfeinert den Plan mit zusätzlichen Details zu Datensicherheit und Datenschutz]
```

## Lizenz

MIT

## Beitragen

Beiträge sind willkommen! Bitte erstelle einen Fork des Repositories und reiche einen Pull Request ein.
