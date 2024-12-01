from neo4j import GraphDatabase
import csv
from tqdm import tqdm
from config import load_env  

class Neo4jimporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print(f"=== Connected as user : {user} ===")

        self.metrics = {
            "games_added": 0,
            "users_added": 0,
            "relationships_added": 0,
            "reviews_added": 0,
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
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file: # file == "data_csv/games_data_bins.csv"
                csv_reader = csv.DictReader(file)
                total_games = count_rows(file_path)
                for row in tqdm(csv_reader, total=total_games, desc="Games Progress"):
                    session.run("""
                        MERGE (g:Game {game_id: $game_id})
                        ON CREATE SET g.name = $name,
                                      g.time_played = toInteger($time_played),
                                      g.player_count = toInteger($player_count),
                                      g.median_time_played = toInteger($median_time_played),
                                      g.max_bin_1 = toInteger($max_bin_1),
                                      g.max_bin_2 = toInteger($max_bin_2),
                                      g.max_bin_3 = toInteger($max_bin_3),
                                      g.max_bin_4 = toInteger($max_bin_4),
                                      g.max_bin_5 = toInteger($max_bin_5)
                    """, game_id=row['game_id'], name=row['name'],
                       time_played=row['time_played'], player_count=row['player_count'],
                       median_time_played=row['median_time_played'], max_bin_1=row['max_bin_1'],
                       max_bin_2=row['max_bin_2'], max_bin_3=row['max_bin_3'],
                       max_bin_4=row['max_bin_4'], max_bin_5=row['max_bin_5'])
                    self.metrics["games_added"] += 1

    def load_users(self, file_path):
        print("Loading users...")
        with self.driver.session() as session:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                csv_reader = csv.DictReader(file)
                total_users = count_rows(file_path)
                for row in tqdm(csv_reader, total=total_users, desc="Users Progress"):
                    session.run("""
                        MERGE (u:User {user_id: $user_id})
                        ON CREATE SET u.items_count = toInteger($items_count),
                                      u.played_games = toInteger($played_games),
                                      u.total_playtime = toInteger($total_playtime),
                                      u.most_played_game_id = $most_played_game_id
                    """, user_id=row['user_id'], items_count=row['items_count'],
                       played_games=row['played_games'], total_playtime=row['total_playtime'],
                       most_played_game_id=row['most_played_game_id'])
                    self.metrics["users_added"] += 1

    def load_user_game_relationships(self, file_path):
        print("Loading user-game relationships...")
        with self.driver.session() as session:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                csv_reader = csv.DictReader(file)
                total_relationships = count_rows(file_path)
                for row in tqdm(csv_reader, total=total_relationships, desc="Relationships Progress"):
                    session.run("""
                        MERGE (u:User {user_id: $user_id})
                        MERGE (g:Game {game_id: $game_id})
                        MERGE (u)-[r:PLAYS]->(g)
                        ON CREATE SET r.playtime = toInteger($playtime),
                                    r.active = $active
                    """, user_id=row['user_id'], game_id=row['game_id'],
                    playtime=row['playtime'], active=row['active'])
                    self.metrics["relationships_added"] += 1

    def load_reviews(self, file_path):
        print("Loading reviews...")
        with self.driver.session() as session:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                csv_reader = csv.DictReader(file)
                total_reviews = count_rows(file_path)
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
    
    def import_all_data(self, games_path, users_path, users_games_path, reviews_path):
        print("\n=== File Summary ===")
        print(f"Games file: {games_path}, Rows: {count_rows(games_path)}")
        print(f"Users file: {users_path}, Rows: {count_rows(users_path)}")
        print(f"User-Game Relationships file: {users_games_path}, Rows: {count_rows(users_games_path)}")
        print(f"Reviews file: {reviews_path}, Rows: {count_rows(reviews_path)}")
        print("=====================")

        self.create_constraints()
        self.load_games(games_path)
        self.load_users(users_path)
        self.load_user_game_relationships(users_games_path)
        self.load_reviews(reviews_path)

    def print_metrics(self):
        print("\n=== Metrics Report ===")
        print(f"Games added: {self.metrics['games_added']}")
        print(f"Users added: {self.metrics['users_added']}")
        print(f"Relationships added: {self.metrics['relationships_added']}")
        print(f"Reviews added: {self.metrics['reviews_added']}")
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

    # Load environment variables
    env_config = load_env()
    DATABASE_URI = env_config["uri"]
    USERNAME = env_config["username"]
    PASSWORD = env_config["password"]
    
    # Define paths to the CSV files
    GAMES_FILE =  "data_csv/games_data_bins.csv"
    USER_GAME_FILE = "data_csv/users_games.csv"
    REVIEWS_FILE = "data_csv/aus_reviews.csv"
    USER_FILE = "data_csv/users_data.csv"

    print("Starting data imporing process...")

    # Initialize Neo4jimporer
    importer = Neo4jimporter(DATABASE_URI, USERNAME, PASSWORD)

    try:
        # Load all data into Neo4j
        importer.import_all_data(GAMES_FILE, USER_FILE, USER_GAME_FILE, REVIEWS_FILE)

        # Fetch and print sample data
        importer.fetch_sample_data()

        # Print metrics
        importer.print_metrics()

        print("Data successfully loaded into Neo4j!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        importer.close()

    
    