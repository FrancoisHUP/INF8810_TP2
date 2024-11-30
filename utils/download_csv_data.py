import requests
import gzip
import shutil
import os

# URLs to download files
users_games="https://drive.usercontent.google.com/download?id=1hRLeEYdTVhZrCnk21ZOdE-Lg6CPqUrfr&export=download&authuser=0&confirm=t&uuid=f0a8a4ff-8bd5-4b7d-b0d2-5dc93ef288d0&at=AENtkXYDy9IDqO9t0KxXi9hq51dG:1732900404333"
games_data_bins="https://drive.usercontent.google.com/download?id=1F831wIF1-kfBotke1l6oA-FdbaIqDOo4&export=download&authuser=0&confirm=t&uuid=138f6b8c-b486-4653-8287-69673f107f65&at=AENtkXYzYTcbIo5cw6yHnEu4qTp4:1732900466945"
aus_reviews="https://drive.usercontent.google.com/download?id=1IneVMe_-dYxfDZDtaH3rgQFV0wAwq1ow&export=download&authuser=0&confirm=t&uuid=3af45070-d53d-4250-ab9b-09e258f77ae6&at=AENtkXbK_QfWsfp98NUX1PpIHhf5:1732900505238"
users_data="https://drive.usercontent.google.com/download?id=1LoaDJDZzugQt7kk7jnnj8-NKa6IjH45x&export=download&authuser=0&confirm=t&uuid=7e98bcf5-0c24-4945-a4fd-0241f925a1a2&at=AENtkXYwDPrP-AWJeZmwiInKlO2C:1732900542349"

# Directory to store data
data_folder = "data_csv"

# Ensure the data/ folder exists
os.makedirs(data_folder, exist_ok=True)

# Filenames for extracted files
users_games_file = os.path.join(data_folder, "users_games.csv")
games_data_bins_file = os.path.join(data_folder, "games_data_bins.csv")
aus_reviews_file = os.path.join(data_folder, "aus_reviews.csv")
users_data_file = os.path.join(data_folder, "users_data.csv")

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
download_file(users_games, users_games_file)
download_file(games_data_bins, games_data_bins_file)
download_file(aus_reviews, aus_reviews_file)
download_file(users_data, users_data_file)