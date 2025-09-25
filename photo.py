import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


def get_names():
    file = "names.csv"
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f]
    return []


def rule(img: Image.Image):
    return img.width > img.height


def search_image(query):
    search_url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to search {query}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    # Skip the first one (Google logo), start from 1
    for img_tag in img_tags[1:]:
        url = img_tag.get("src")
        if not url:
            continue

        # Try downloading to check dimensions
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                img = Image.open(BytesIO(r.content))
                if rule(img):  # check landscape rule
                    return url
        except Exception as e:
            print(f"Error checking image: {e}")
            continue

    return None  # no image passed the rule


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.save(filename)
        print(f"Saved {filename}")
    else:
        print(f"Failed to download {url}")


def main():
    if not os.path.exists("pics"):
        os.makedirs("pics")
    names = get_names()
    for name in names:
        search_query = f"რესტორანი {name}"
        image_url = search_image(search_query)
        if image_url:
            download_image(image_url, f"pics/{name}.png")


if __name__ == "__main__":
    main()
