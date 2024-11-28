from dotenv import load_dotenv
import os
from neo4j import GraphDatabase

# Load environment variables from the .env file
load_dotenv()

# Retrieve variables
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

# Connect to the database
driver = GraphDatabase.driver(uri, auth=(username, password))

def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Connection Successful!' AS message")
        print(result.single()["message"])

test_connection()
driver.close()
