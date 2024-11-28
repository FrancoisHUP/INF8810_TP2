import requests
import gzip
import shutil
import os

# URLs to download files
reviews_url = "https://datarepo.eng.ucsd.edu/mcauley_group/data/steam/australian_user_reviews.json.gz"
items_url = "https://datarepo.eng.ucsd.edu/mcauley_group/data/steam/australian_users_items.json.gz"

# Directory to store data
data_folder = "data"

# Ensure the data/ folder exists
os.makedirs(data_folder, exist_ok=True)

# Filenames for downloaded files
reviews_file_gz = os.path.join(data_folder, "australian_user_reviews.json.gz")
items_file_gz = os.path.join(data_folder, "australian_users_items.json.gz")

# Filenames for extracted files
reviews_file = os.path.join(data_folder, "australian_user_reviews.json")
items_file = os.path.join(data_folder, "australian_users_items.json")

def download_file(url, output_path):
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        print(f"Downloaded {output_path}.")
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")

def extract_gz_file(input_path, output_path):
    print(f"Extracting {input_path}...")
    with gzip.open(input_path, 'rb') as gz_file:
        with open(output_path, 'wb') as out_file:
            shutil.copyfileobj(gz_file, out_file)
    print(f"Extracted {output_path}.")

# Download the files into the data/ folder
download_file(reviews_url, reviews_file_gz)
download_file(items_url, items_file_gz)

# Extract the files into the data/ folder
extract_gz_file(reviews_file_gz, reviews_file)
extract_gz_file(items_file_gz, items_file)

