import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Print environment variables
print("Environment Variables:")
print(f"BASE_URL: {os.getenv('BASE_URL', 'Not set')}")
print(f"LLM_API_KEY: {'Set' if os.getenv('LLM_API_KEY') else 'Not set'}")
print(f"REASONER_MODEL: {os.getenv('REASONER_MODEL', 'Not set')}")
print(f"PRIMARY_MODEL: {os.getenv('PRIMARY_MODEL', 'Not set')}")
print(f"EMBEDDING_MODEL: {os.getenv('EMBEDDING_MODEL', 'Not set')}")
print(f"OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL', 'Not set')}")
print(f"SUPABASE_SERVICE_KEY: {'Set' if os.getenv('SUPABASE_SERVICE_KEY') else 'Not set'}")

# Check Python path
print("\nPython Path:")
for path in sys.path:
    print(path)
