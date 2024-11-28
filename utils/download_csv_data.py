import requests
import gzip
import shutil
import os

# URLs to download files
aus_reviews_url = "https://drive.usercontent.google.com/download?id=1KJVwUXOAEb-6FB7RPI4PMT0OoExt5zx7&export=download&authuser=0&confirm=t&uuid=238b5b2a-1a32-4c2f-b8c7-132c7ae7244f&at=AENtkXaIE5VOQJdZUViOkGU89y0i:1732827472145"
games_names_url = "https://drive.usercontent.google.com/download?id=1tXkhXo_JlbdMQyiyzbPEjCopICyccZfH&export=download&authuser=0&confirm=t&uuid=6832b865-7e9d-4c99-a8e0-4c848d20b2cf&at=AENtkXZmxqZZCuldoJyVAN1Y_0Tc:1732827494889"
user_game_url = "https://drive.usercontent.google.com/download?id=1nIUzmc0zyJlkoZrpxPoSTOlj8OaoE-X4&export=download&authuser=0&confirm=t&uuid=b6cd4744-e14f-40dd-9988-979889aa60e5&at=AENtkXYRPaRJkFQasxqLjJQZ5vx-:1732827531068"
# Directory to store data
data_folder = "data_csv"

# Ensure the data/ folder exists
os.makedirs(data_folder, exist_ok=True)

# Filenames for extracted files
aus_reviews_file = os.path.join(data_folder, "aus_reviews.csv")
games_names_file = os.path.join(data_folder, "games_names.csv")
user_game_file = os.path.join(data_folder, "user_game.csv")

def download_file(url, output_path):
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        print(f"Downloaded {output_path}.")
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")

# Download the files into the data/ folder
download_file(aus_reviews_url, aus_reviews_file)
download_file(games_names_url, games_names_file)
download_file(user_game_url, user_game_file)