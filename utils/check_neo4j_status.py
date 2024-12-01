from neo4j import GraphDatabase
from config import load_env  

# Load environment variables from the .env file
load_env()

# Load environment variables
env_config = load_env()
DATABASE_URI = env_config["uri"]
USERNAME = env_config["username"]
PASSWORD = env_config["password"]

# Connect to the database
driver = GraphDatabase.driver(DATABASE_URI, auth=(USERNAME, PASSWORD))

def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Connection Successful!' AS message")
        print(result.single()["message"])

test_connection()
driver.close()
