from neo4j import GraphDatabase

class RecommenderSystem:
    def __init__(self, uri, user, password):
        """Initialize the connection to the Neo4j database."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        """Close the connection to the Neo4j database."""
        self.driver.close()
    
    def collaborative_filtering(self, user_id, top_n=5):
        """Recommend games based on collaborative filtering."""
        query = """
        MATCH (target:User {user_id: $user_id})-[:PLAYS]->(g:Game)<-[:PLAYS]-(similar:User)
        WITH target, similar, COUNT(g) AS shared_games
        ORDER BY shared_games DESC
        LIMIT 10
        MATCH (similar)-[:PLAYS]->(recommended:Game)
        WHERE NOT (target)-[:PLAYS]->(recommended)  // Ensure 'target' is carried over from WITH
        RETURN recommended.game_id AS game_id, recommended.name AS name, COUNT(*) AS popularity
        ORDER BY popularity DESC, recommended.name
        LIMIT $top_n
        """
        with self.driver.session() as session:
            results = session.run(query, user_id=user_id, top_n=top_n)
            return [{"game_id": record["game_id"], "name": record["name"], "popularity": record["popularity"]} for record in results]
    
    
    def recommend_by_bins(self, user_id, top_n=5, bin_threshold=1):
        """Recommend games based on bin popularity."""
        query = """
        MATCH (target:User {user_id: $user_id})-[:PLAYS]->(g:Game)
        WITH target, g
        MATCH (recommended:Game)
        WHERE recommended.game_id <> g.game_id
        AND recommended.max_bin_1 >= $bin_threshold
        AND NOT (target)-[:PLAYS]->(recommended)
        RETURN DISTINCT recommended.game_id AS game_id, recommended.name AS name, recommended.max_bin_1 AS bin_score
        ORDER BY bin_score DESC
        LIMIT $top_n
        """
        with self.driver.session() as session:
            results = session.run(query, user_id=user_id, top_n=top_n, bin_threshold=bin_threshold)
            return [{"game_id": record["game_id"], "name": record["name"], "bin_score": record["bin_score"]} for record in results]
        
    def list_users(self, limit=5):
        """List random users."""
        query = """
        MATCH (u:User)
        RETURN u.user_id AS user_id, u.items_count AS items_count
        ORDER BY rand()
        LIMIT $limit;
        """
        with self.driver.session() as session:
            results = session.run(query, limit=limit)
            return [{"user_id": record["user_id"], "items_count": record.get("items_count")} for record in results]

    def get_user_info(self, user_id):
        """Fetch detailed information about a specific user."""
        query = """
        MATCH (u:User {user_id: $user_id})-[p:PLAYS]->(g:Game)
        OPTIONAL MATCH (u)-[r:REVIEWS]->(g)
        RETURN u.user_id AS user_id, 
            u.items_count AS items_count,
            u.played_games AS played_games, 
            u.total_playtime AS total_playtime,
            g.game_id AS game_id,
            g.name AS game_name,
            p.playtime AS playtime,
            g.max_bin_1 AS max_bin_1,
            g.max_bin_2 AS max_bin_2,
            g.max_bin_3 AS max_bin_3,
            g.max_bin_4 AS max_bin_4,
            g.max_bin_5 AS max_bin_5,
            g.player_count AS player_count,
            r.review AS review
        ORDER BY p.playtime DESC;
        """
        with self.driver.session() as session:
            results = session.run(query, user_id=user_id)
            user_info = None
            games = []

            for record in results:
                if not user_info:
                    user_info = {
                        "user_id": record["user_id"],
                        "items_count": record["items_count"],
                        "played_games": record["played_games"],
                        "total_playtime": record["total_playtime"],
                    }
                games.append({
                    "game_id": record["game_id"],
                    "name": record["game_name"],
                    "playtime": record["playtime"],  # Correctly fetch playtime from the PLAYS relationship
                    "max_bin": [record["max_bin_1"], record["max_bin_2"], record["max_bin_3"], record["max_bin_4"], record["max_bin_5"]],
                    "player_count": record["player_count"],
                    "review": record["review"]
                })

            # Add rank to each game
            for idx, game in enumerate(games, start=1):
                game["rank"] = idx

            if user_info:
                user_info["games"] = games

            return user_info


if __name__ == "__main__" : 

    from config import load_env  
    # Load environment variables
    env_config = load_env()
    DATABASE_URI = env_config["uri"]
    USERNAME = env_config["username"]
    PASSWORD = env_config["password"]

    # Initialize the recommender system
    recommender = RecommenderSystem(uri=DATABASE_URI, user=USERNAME, password=PASSWORD)

    try:
        user_id = "76561197970982479"  # Example user ID

        # Collaborative filtering recommendations
        print("Collaborative Filtering Recommendations:")
        collab_recommendations = recommender.collaborative_filtering(user_id)
        print(collab_recommendations)

        # Content-based filtering recommendations
        print("\nContent-Based Filtering Recommendations:")
        content_recommendations = recommender.content_based_filtering(user_id)
        print(content_recommendations)

        # Hybrid recommendations
        print("\nHybrid Recommendations:")
        hybrid_recommendations = recommender.hybrid_recommendation(user_id)
        print(hybrid_recommendations)

        # Recommendations using bins
        print("\nRecommendations Using Bins:")
        bin_recommendations = recommender.recommend_by_bins(user_id, bin_threshold=2)
        print(bin_recommendations)

    finally:
        recommender.close()