import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from time import sleep

# Create logos directory if not exists
if not os.path.exists("logos"):
    os.makedirs("logos")

def get_names():
    file = "names.csv"
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f]
    return []

def search_image(query):
    search_url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to search {query}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    # First image is usually Google's logo, so take the second one
    if len(img_tags) > 1:
        return img_tags[1]["src"]
    return None

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.save(filename)
        print(f"Saved {filename}")
    else:
        print(f"Failed to download {url}")

def main():
    names = get_names()
    for idx, name in enumerate(names, start=1):
        search_query = f"{name}"
        image_url = search_image(search_query)
        if image_url:
            download_image(image_url, f"logos/{name}.png")
        
        # sleep(1)

if __name__ == "__main__":
    main()
