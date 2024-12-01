import os
from dotenv import load_dotenv

def load_env():
    """Load environment variables from the .env file."""
    # Clear existing env variables for Neo4j connection (optional)
    os.environ.pop("NEO4J_URI", None)
    os.environ.pop("NEO4J_USERNAME", None)
    os.environ.pop("NEO4J_PASSWORD", None)
    
    # Load environment variables from the .env file
    load_dotenv()
    
    # Return Neo4j configuration
    return {
        "uri": os.getenv("NEO4J_URI"),
        "username": os.getenv("NEO4J_USERNAME"),
        "password": os.getenv("NEO4J_PASSWORD"),
    }