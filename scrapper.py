import logging
import os
import pickle
import time

from PIL import Image
from io import BytesIO

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from hashlib import md5

MAIN_URL = "http://instagram.com"
FOLLOWER_CLASS_SELECTOR = ""
USERNAME_CLASS_SELECTOR = ""

usernames = [
    'albamelendo',
    'erinwalshstyle',
    'nickyygood',
    'mrenriquemelendez',
    'jessicamulroney',
    'laura.cardenasz',
    'cristianbaena_art',
    'antobella_',
    # plus size
    'heensie',
    'melissajadestyle',
    'moniquedoy',
    'nicolettemason',
    # black
    'henson',
    'zoedupree'
]

def build_profile_url(username: str):
    return f"{MAIN_URL}/{username}"

def download_image(image_url, file_path):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.resize((572, 572))
    img.save(file_path+".png", format="png")
    return

class Scrapper:
    def __init__(self):

        options = FirefoxOptions()
        # options.add_argument("--headless")

        self.main_driver = webdriver.Firefox(options=options)
        return
    
    def quit(self):
        self.main_driver.quit()
        return

    def build_login(self):
        self.main_driver.get(MAIN_URL)
        return

    def scrap(self, username: str, n_scrolls=20):
        logging.info(f"Getting followers of {username}")
        self.main_driver.get(build_profile_url(username))
        time.sleep(5)

        body = self.main_driver.find_element(By.TAG_NAME, "body")
        # Scroll over followers panel
        for i in range(n_scrolls):
            body.send_keys(Keys.END)
            time.sleep(1)
        time.sleep(2)

        grid_class = "x1iyjqo2"
        grid = self.main_driver.find_element(By.TAG_NAME, "article")
        posts = grid.find_elements(By.CLASS_NAME, "x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd")
        logging.info(f"Found {len(posts)} posts")

        for post in posts:
            image_url = post.find_element(By.TAG_NAME, "img").get_attribute("src")
            download_image(image_url, f"images/{md5(image_url.encode()).hexdigest()}")
            logging.info(f"Downloaded image {image_url}")

        return


def main():
    scrapper = Scrapper()
    scrapper.build_login()
    for username in usernames:
        scrapper.scrap(username=username, n_scrolls=1)
    scrapper.quit()
    return


if __name__ == "__main__":
    main()
