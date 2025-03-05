import os
import logging
import warnings
from dotenv import load_dotenv
import openai
from pydantic_ai import Agent

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Ensure OpenAI API key is set
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable in your .env file")

openai.api_key = openai_api_key

class FinancialTrackerAgent(Agent):
    def __init__(self):
        from agent_prompts import SYSTEM_PROMPT
        super().__init__(
            model='openai:gpt-4o-mini',  # Specify the OpenAI model
            system_prompt=SYSTEM_PROMPT
        )
    
    def generate_plan(self, user_needs: str):
        try:
            logger.info(f"Processing request: {user_needs}")
            plan = self.run_sync(user_needs)
            logger.info("Development plan generated successfully")
            return plan
        except Exception as e:
            logger.error(f"Error generating development plan: {str(e)}")
            raise

if __name__ == "__main__":
    agent = FinancialTrackerAgent()
    plan = agent.generate_plan("Generate a comprehensive software development plan for a financial tracker app.")
    print(plan.data)
