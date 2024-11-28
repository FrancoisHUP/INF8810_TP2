from neo4j import GraphDatabase
import csv
import os 
from tqdm import tqdm
from dotenv import load_dotenv

class Neo4jLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.metrics = {
            "games_added": 0,
            "games_skipped": 0,
            "users_added": 0,
            "users_skipped": 0,
            "reviews_added": 0,
            "reviews_skipped": 0,
        }
    
    def close(self):
        self.driver.close()
    
    def create_constraints(self):
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.user_id IS UNIQUE;")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (g:Game) REQUIRE g.game_id IS UNIQUE;")

    def load_games(self, file_path):
        print("Loading games...")
        with self.driver.session() as session:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                csv_reader = csv.DictReader(file)
                total_games = sum(1 for _ in open(file_path, 'r', encoding='utf-8', errors='replace')) - 1
                file.seek(0)
                for row in tqdm(csv_reader, total=total_games, desc="Games Progress"):
                    session.run("""
                        MERGE (g:Game {game_id: $game_id})
                        ON CREATE SET g.name = $name
                    """, game_id=row['game_id'], name=row['name'])
                    self.metrics["games_added"] += 1  # Assume games are added without skip logic

    def load_users_and_playtime(self, file_path):
        print("Loading users and playtime...")
        with self.driver.session() as session:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                csv_reader = csv.DictReader(file)
                total_users = sum(1 for _ in open(file_path, 'r', encoding='utf-8', errors='replace')) - 1
                file.seek(0)
                for row in tqdm(csv_reader, total=total_users, desc="Users Progress"):
                    session.run("""
                        MERGE (u:User {user_id: $user_id})
                        MERGE (g:Game {game_id: $game_id})
                        MERGE (u)-[r:PLAYS]->(g)
                        ON CREATE SET r.playtime = toInteger($playtime), r.active = $active
                    """, user_id=row['user_id'], game_id=row['game_id'],
                       playtime=row['playtime'], active=row['active'])
                    self.metrics["users_added"] += 1

    def load_reviews(self, file_path):
        print("Loading reviews...")
        with self.driver.session() as session:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                csv_reader = csv.DictReader(file)
                total_reviews = sum(1 for _ in open(file_path, 'r', encoding='utf-8', errors='replace')) - 1
                file.seek(0)
                for row in tqdm(csv_reader, total=total_reviews, desc="Reviews Progress"):
                    session.run("""
                        MERGE (u:User {user_id: $user_id})
                        MERGE (g:Game {game_id: $item_id})
                        MERGE (u)-[r:REVIEWS {funny: $funny, posted: $posted, 
                                             last_edited: $last_edited, helpful: $helpful, 
                                             recommend: $recommend, review: $review}]->(g)
                    """, user_id=row['user_id'], item_id=row['item_id'],
                       funny=row['funny'], posted=row['posted'], last_edited=row['last_edited'],
                       helpful=row['helpful'], recommend=row['recommend'], review=row['review'])
                    self.metrics["reviews_added"] += 1
                    
    def load_all_data(self, games_path, user_game_path, reviews_path):
        print("\n=== File Summary ===")
        games_count = count_rows(games_path)
        users_count = count_rows(user_game_path)
        reviews_count = count_rows(reviews_path)
        print(f"Games file: {games_path}, Rows: {games_count}")
        print(f"Users/Playtime file: {user_game_path}, Rows: {users_count}")
        print(f"Reviews file: {reviews_path}, Rows: {reviews_count}")
        print("=====================")

        self.create_constraints()
        self.load_games(games_path)
        self.load_users_and_playtime(user_game_path)
        self.load_reviews(reviews_path)
        self.print_metrics()

    def print_metrics(self):
        print("\n=== Metrics Report ===")
        print(f"Games added: {self.metrics['games_added']}")
        print(f"Games skipped (already exists): {self.metrics['games_skipped']}")
        print(f"Users added: {self.metrics['users_added']}")
        print(f"Users skipped (already exists): {self.metrics['users_skipped']}")
        print(f"Reviews added: {self.metrics['reviews_added']}")
        print(f"Reviews skipped (already exists): {self.metrics['reviews_skipped']}")
        print("======================")

    def fetch_sample_data(self):
        with self.driver.session() as session:
            print("\n=== Sample Games ===")
            games = session.run("MATCH (g:Game) RETURN g.game_id AS game_id, g.name AS name LIMIT 5")
            for record in games:
                print(f"Game ID: {record['game_id']}, Name: {record['name']}")

            print("\n=== Sample Users ===")
            users = session.run("MATCH (u:User) RETURN u.user_id AS user_id LIMIT 5")
            for record in users:
                print(f"User ID: {record['user_id']}")

            print("\n=== Sample Reviews ===")
            reviews = session.run("""
                MATCH (u:User)-[r:REVIEWS]->(g:Game)
                RETURN u.user_id AS user_id, g.game_id AS game_id, r.review AS review LIMIT 5
            """)
            for record in reviews:
                print(f"User ID: {record['user_id']}, Game ID: {record['game_id']}, Review: {record['review']}")

def count_rows(file_path):
    """Count the number of rows in a CSV file (excluding the header)."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return sum(1 for _ in file) - 1  # Subtract 1 for the header
    
if __name__ == "__main__":
    # Load environment variables from the .env file
    load_dotenv()
    
    # Configuration for Neo4j connection
    DATABASE_URI = os.getenv("NEO4J_URI")
    USERNAME = os.getenv("NEO4J_USERNAME")
    PASSWORD = os.getenv("NEO4J_PASSWORD")

    # Define paths to the CSV files
    GAMES_FILE =  "data_csv/games_names.csv"
    USER_GAME_FILE = "data_csv/user_game.csv"
    REVIEWS_FILE = "data_csv/aus_reviews.csv"

    print("Starting data loading process...")

    # Initialize Neo4jLoader
    loader = Neo4jLoader(DATABASE_URI, USERNAME, PASSWORD)

    try:
        # Load all data into Neo4j
        loader.load_all_data(GAMES_FILE, USER_GAME_FILE, REVIEWS_FILE)

        # Fetch and print sample data
        loader.fetch_sample_data()

        # Print metrics
        loader.print_metrics()

        print("Data successfully loaded into Neo4j!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        loader.close()

    