import os
import sys
import json
import subprocess
import time
import requests

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import write_to_log

def test_mcp_client():
    """
    Test the Development Plan Agent through the MCP server.
    This simulates how an external system would interact with the agent.
    """
    # Start the MCP server in a separate process
    mcp_process = subprocess.Popen(
        ["python", "dev_plan_mcp.py"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Give the server time to start
    time.sleep(5)
    
    try:
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
        innerhalb von 8 Monaten fertigstellen. Die Hauptherausforderung besteht darin, 
        die komplexen Finanzberechnungen korrekt zu implementieren und eine intuitive 
        Benutzeroberfläche zu schaffen, die auch für nicht-technikaffine Kunden leicht 
        verständlich ist.
        """
        
        print("\n=== Testing Development Plan MCP Client ===\n")
        
        # Create a thread
        create_thread_request = {
            "jsonrpc": "2.0",
            "method": "create_thread",
            "params": {},
            "id": 1
        }
        
        # Send the request to the MCP server
        mcp_process.stdin.write(json.dumps(create_thread_request) + "\n")
        mcp_process.stdin.flush()
        
        # Read the response
        response_line = mcp_process.stdout.readline()
        thread_response = json.loads(response_line)
        thread_id = thread_response.get("result")
        
        print(f"Created thread: {thread_id}")
        
        # Run the agent with the project description
        run_agent_request = {
            "jsonrpc": "2.0",
            "method": "run_agent",
            "params": {
                "thread_id": thread_id,
                "user_input": project_description
            },
            "id": 2
        }
        
        print("Sending project description to agent...")
        
        # Send the request to the MCP server
        mcp_process.stdin.write(json.dumps(run_agent_request) + "\n")
        mcp_process.stdin.flush()
        
        # Read the response (this may take some time)
        response_line = mcp_process.stdout.readline()
        agent_response = json.loads(response_line)
        
        print("\n=== Agent Response ===\n")
        print(agent_response.get("result"))
        
        # Simulate user feedback
        user_feedback = """
        Danke für den Plan! Könntest du bitte mehr Details zur Datensicherheit und zum Datenschutz hinzufügen? 
        Die finanziellen Daten unserer Kunden sind sehr sensibel. Außerdem würde ich gerne wissen, 
        wie wir die Implementierung der Investmentstrategien und Finanzberechnungen priorisieren sollten, 
        da diese das Herzstück der Anwendung sind.
        """
        
        print("\n=== Sending User Feedback ===\n")
        print(user_feedback)
        
        # Run the agent with the user feedback
        feedback_request = {
            "jsonrpc": "2.0",
            "method": "run_agent",
            "params": {
                "thread_id": thread_id,
                "user_input": user_feedback
            },
            "id": 3
        }
        
        # Send the request to the MCP server
        mcp_process.stdin.write(json.dumps(feedback_request) + "\n")
        mcp_process.stdin.flush()
        
        # Read the response
        response_line = mcp_process.stdout.readline()
        feedback_response = json.loads(response_line)
        
        print("\n=== Agent Response to Feedback ===\n")
        print(feedback_response.get("result"))
        
        print("\n=== Test Complete ===\n")
        
    finally:
        # Terminate the MCP server
        mcp_process.terminate()
        mcp_process.wait()

if __name__ == "__main__":
    test_mcp_client()
