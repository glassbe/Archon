#!/bin/bash

# Aktiviere die virtuelle Umgebung
source venv/bin/activate

# Führe den Test aus
python test_agent.py

# Deaktiviere die virtuelle Umgebung
deactivate
