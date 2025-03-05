#!/usr/bin/env python
"""
Einfacher Starter für den Development Plan Agent MCP-Server.
Dieser Skript kann direkt ausgeführt werden, um den MCP-Server zu starten.
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Stelle sicher, dass die Umgebungsvariablen geladen werden
load_dotenv()

def main():
    """Hauptfunktion zum Starten des MCP-Servers"""
    parser = argparse.ArgumentParser(description="Starte den Development Plan Agent MCP-Server")
    parser.add_argument("--port", type=int, default=int(os.getenv("SERVICE_PORT", "8200")),
                        help="Port für den FastAPI-Service (default: 8200 oder aus .env)")
    args = parser.parse_args()
    
    # Setze den Port in der Umgebung
    os.environ["SERVICE_PORT"] = str(args.port)
    
    # Importiere und starte den MCP-Server
    from dev_plan_mcp import mcp
    
    print(f"Starting Development Plan Agent MCP Server")
    print(f"FastAPI Service running on http://127.0.0.1:{args.port}")
    print("Use Ctrl+C to stop the server")
    
    # Starte den MCP-Server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
