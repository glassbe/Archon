import os
import warnings
from dotenv import load_dotenv
import openai
from agent import FinancialTrackerAgent

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable in your .env file")

openai.api_key = openai_api_key

def main():
    print("=" * 50)
    print("Financial Tracker Development Plan Generator")
    print("=" * 50)
    
    # Create an instance of the Financial Tracker Agent
    agent = FinancialTrackerAgent()
    
    # Generate a development plan for the financial tracker app
    plan = agent.generate_plan(
        "Create a comprehensive software development plan for a modern financial tracker web application. "
        "The application should help users track income, manage expenses, and monitor investment portfolios. "
        "Key requirements include secure user authentication, responsive design, real-time financial insights, "
        "and the ability to connect multiple financial accounts. The target users are young professionals "
        "and small business owners who want a comprehensive financial management solution. "
        "Provide a detailed plan covering technology stack, architecture, features, development phases, "
        "security considerations, and scalability strategies."
    )
    
    # Print the generated plan
    print("Financial Tracker Development Plan:")
    print(plan.data)
    
    # Write the output also in a markdown file
    with open("FinancialTrackerDevelopmentPlan.md", "w") as f:
        f.write("# Financial Tracker Development Plan\n\n")
        f.write(plan.data)

if __name__ == "__main__":
    main()
