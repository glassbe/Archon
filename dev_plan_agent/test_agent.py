import os
import sys
import asyncio
import json
import uuid
from dotenv import load_dotenv
from langgraph.types import Command
from langchain_core.tracers.langchain import wait_for_all_tracers

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import write_to_log

# Load environment variables
load_dotenv()

async def test_dev_plan_agent():
    """
    Test the Development Plan Agent directly without using MCP.
    This is useful for debugging and testing the agent workflow.
    """
    from dev_plan_graph import dev_plan_flow
    
    # Finanzberatungs-Projekt Beschreibung
    project_description = """
    Ich möchte eine Web-App für Finanzberatung entwickeln, die den aktuellen Excel-basierten Prozess ersetzt. 
    Die App soll folgende Funktionen haben:
    
    1. Kunden können ihre finanzielle Ist-Situation eintragen (Einkommen, Ausgaben, Vermögen, Schulden)
    2. Finanzberater können die Daten einsehen und analysieren
    3. Basierend auf der Analyse können Finanzberater personalisierte Investmentstrategien vorschlagen
    4. Ziel ist die finanzielle Freiheit der Kunden, sodass ihre Investments die Fixkosten decken können
    5. Berechnung und Visualisierung von Investmentraten und Wachstumsszenarien
    6. Dashboard für Finanzberater mit Übersicht aller Kunden und deren Status
    7. Automatische Benachrichtigungen bei wichtigen Meilensteinen oder notwendigen Anpassungen
    8. Versionierung der Finanzpläne, um Fortschritte zu verfolgen
    9. Sichere Datenspeicherung und Benutzerauthentifizierung
    
    Wir haben ein Team von 4 Entwicklern (2 Frontend, 2 Backend) und möchten die App 
    innerhalb von 6 Monaten fertigstellen. Die Hauptherausforderung besteht darin, 
    die komplexen Finanzberechnungen korrekt zu implementieren und eine intuitive 
    Benutzeroberfläche zu schaffen, die auch für nicht-technikaffine Kunden leicht 
    verständlich ist.
    """
    
    print("\n=== Testing Development Plan Agent ===\n")
    print("Project Description:")
    print(project_description)
    print("\n=== Agent Response ===\n")
    
    # Run the agent with the project description
    run_id = str(uuid.uuid4())
    config = {
        "configurable": {"thread_id": "test-thread"},
        "metadata": {"run_id": run_id}
    }
    response = ""
    
    # Prepare initial state
    initial_state = {
        "latest_user_message": project_description,
        "messages": [],
        "project_scope": "",
        "development_plan": ""
    }
    
    # Print LangSmith URL if available
    from dev_plan_graph import get_langsmith_url
    langsmith_url = get_langsmith_url(run_id)
    if langsmith_url:
        print(f"\n=== LangSmith Trace URL ===\n{langsmith_url}\n")
    
    # First message
    async for msg in dev_plan_flow.astream(
        initial_state, 
        config,
        stream_mode="custom"
    ):
        chunk = str(msg)
        response += chunk
        print(chunk, end="", flush=True)
    
    print("\n\n=== First Response Complete ===\n")
    
    # Simulate user feedback
    user_feedback = """
    Danke für den Plan! Könntest du bitte mehr Details zur Datensicherheit und zum Datenschutz hinzufügen? 
    Die finanziellen Daten unserer Kunden sind sehr sensibel. Außerdem würde ich gerne wissen, 
    wie wir die Implementierung der Investmentstrategien und Finanzberechnungen priorisieren sollten, 
    da diese das Herzstück der Anwendung sind.
    """
    
    print("User Feedback:")
    print(user_feedback)
    print("\n=== Agent Response to Feedback ===\n")
    
    # Process feedback
    feedback_run_id = str(uuid.uuid4())
    feedback_config = {
        "configurable": {"thread_id": "test-thread"},
        "metadata": {"run_id": feedback_run_id}
    }
    
    async for msg in dev_plan_flow.astream(
        Command(resume=user_feedback),
        feedback_config,
        stream_mode="custom"
    ):
        chunk = str(msg)
        print(chunk, end="", flush=True)
    
    # Print LangSmith URL for feedback if available
    feedback_langsmith_url = get_langsmith_url(feedback_run_id)
    if feedback_langsmith_url:
        print(f"\n\n=== Feedback LangSmith Trace URL ===\n{feedback_langsmith_url}\n")
    
    # Wait for tracers to finish
    if os.getenv("LANGCHAIN_API_KEY"):
        wait_for_all_tracers()
    
    print("\n\n=== Test Complete ===\n")

if __name__ == "__main__":
    asyncio.run(test_dev_plan_agent())
