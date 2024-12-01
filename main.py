import argparse
from utils.config import load_env
from utils.neo4j_recommender import RecommenderSystem
import json

def json_format(results) :
    print("\nCollaborative Filtering Recommendations:")
    print(json.dumps(results, indent=4))


def list_random_users(recommender, limit=5):
    """List random users from the database."""
    print("\nListing Random Users:")
    users = recommender.list_users(limit)
    for user in users:
        print(f"- User ID: {user['user_id']}, Items Count: {user.get('items_count', 'N/A')}")


def get_user_info(recommender, user_id):
    """Fetch detailed information about a specific user."""
    print(f"\nFetching Information for User ID: {user_id}")
    user_info = recommender.get_user_info(user_id)
    if not user_info:
        print(f"No information found for User ID: {user_id}")
    else:
        print("User Information:")
        print(f"- User ID: {user_info['user_id']}")
        print(f"- Items Count: {user_info.get('items_count', 'N/A')}")
        print(f"- Played Games: {user_info.get('played_games', 'N/A')}")
        print(f"- Total Playtime: {user_info.get('total_playtime', 'N/A')} hours\n")
        print("Games Played (sorted by playtime):")

        for game in user_info.get("games", []):
            # Determine Player Bin
            playtime = game["playtime"] or 0
            max_bins = game["max_bin"]
            player_bin = 1
            player_bin = next((i + 1 for i, max_value in enumerate(max_bins) if playtime <= max_value), len(max_bins) + 1)

            print(f"  [{game['rank']}] {game['name']} (ID: {game['game_id']})")
            print(
                f"      Playtime: {playtime}h | Player Count: {game['player_count']} | Max Bins: {max_bins} | Player Bin: {player_bin}"
            )
            print(f"      Review: {game['review'] or 'No review'}")
        print("\n--- End of User Information ---")


def has_relevant_arguments(args):
    """Check if relevant arguments (beyond defaults) are provided."""
    return any([args.list_users, args.user_info, args.type, args.user_id])


def run():
    # Load environment variables
    env_config = load_env()
    DATABASE_URI = env_config["uri"]
    USERNAME = env_config["username"]
    PASSWORD = env_config["password"]

    # Initialize the recommender system
    recommender = RecommenderSystem(uri=DATABASE_URI, user=USERNAME, password=PASSWORD)

    parser = argparse.ArgumentParser(
        description="Recommendation System CLI",
        usage="""
        python main.py [OPTIONS]

        Options:
          --list_users                     List random users from the database.
          --user_info USER_ID              Fetch detailed information about a specific user.
          --type {collaborative,content,hybrid,bins} 
                                           Specify the type of recommendation.
          --user_id USER_ID                Specify the user ID for recommendations.
          --limit NUMBER                   Limit the number of results (default: 5).
          --bin_threshold NUMBER           Threshold for bin-based recommendations (default: 1).

        Examples:
          List random users:
            python main.py --list_users --limit 5

          Get user info:
            python main.py --user_info 76561197970982479

          Collaborative filtering recommendations:
            python main.py --type collaborative --user_id 76561197970982479 --limit 5

          Content-based recommendations:
            python main.py --type content --user_id 76561197970982479 --limit 5

          Hybrid recommendations:
            python main.py --type hybrid --user_id 76561197970982479 --limit 5

          Recommendations using bins:
            python main.py --type bins --user_id 76561197970982479 --bin_threshold 2 --limit 5
        """
    )
    parser.add_argument("--user_id", type=str, help="Specify the user ID for recommendations")
    parser.add_argument("--type", type=str, choices=["collaborative", "content", "hybrid", "bins"],
                        help="Type of recommendation (collaborative, content, hybrid, bins)")
    parser.add_argument("--list_users", action="store_true", help="List random users")
    parser.add_argument("--user_info", type=str, help="Fetch information about a specific user")
    parser.add_argument("--limit", type=int, default=5, help="Limit the number of recommendations or users")
    parser.add_argument("--bin_threshold", type=int, default=1, help="Threshold for bin-based recommendations")

    args = parser.parse_args()

    # Check for relevant arguments
    if not has_relevant_arguments(args):
        parser.print_help()
        return

    try:
        if args.list_users:
            list_random_users(recommender, limit=args.limit)

        elif args.user_info:
            get_user_info(recommender, args.user_info)

        elif args.type and args.user_id:
            user_id = args.user_id
            rec_type = args.type.lower()

            if rec_type == "collaborative":
                print("\nCollaborative Filtering Recommendations:")
                print(json.dumps(recommender.collaborative_filtering(user_id, top_n=args.limit), indent=4))

            elif rec_type == "content":
                print("\nContent-Based Filtering Recommendations:")
                print(json.dumps(recommender.content_based_filtering(user_id, top_n=args.limit), indent=4))

            elif rec_type == "hybrid":
                print("\nHybrid Recommendations:")
                print(json.dumps(recommender.hybrid_recommendation(user_id, top_n=args.limit), indent=4))

            elif rec_type == "bins":
                print("\nRecommendations Using Bins:")
                print(json.dumps(recommender.recommend_by_bins(user_id, bin_threshold=args.bin_threshold, top_n=args.limit), indent=4))

            else:
                print(f"Unknown recommendation type: {rec_type}")

    finally:
        recommender.close()


if __name__ == "__main__":
    run()
