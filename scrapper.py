import logging
import os
import pickle
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions

MAIN_URL = "http://instagram.com"
FOLLOWER_CLASS_SELECTOR = ""
USERNAME_CLASS_SELECTOR = ""


def build_followers_url(username: str):
    return f"{MAIN_URL}/{username}/followers"


def download_image(image_url, file_path):
    response = requests.get(image_url)
    open(file_path+".png", "wb").write(response.content)
    return


class Scrapper:
    def __init__(self, username):
        self.username = username
        self.followers_tree = {}

        options = FirefoxOptions()
        # options.add_argument("--headless")

        self.main_driver = webdriver.Firefox(options=options)
        return

    def start_and_log(self):
        self.main_driver.get(MAIN_URL)
        return

    def get_follower_usernames(self, username: str, n_scrolls=2):
        logging.info(f"Getting followers of {username}")
        self.main_driver.get(build_followers_url(username))
        time.sleep(5)

        # Looks for followers panel
        try:
            followers_panel = self.main_driver.find_element(By.CSS_SELECTOR, "._aano")
        except:
            print(f"Account {username} seems to be private")
            return []

        # Scroll over followers panel
        for i in range(n_scrolls):
            followers_panel.send_keys(Keys.END)
            time.sleep(1)
        time.sleep(2)

        # TODO: Following and followers
        # TODO: Take children of first child in order to avoid suggestions

        follower_panels = followers_panel.find_elements(By.CLASS_NAME,
                                    FOLLOWER_CLASS_SELECTOR.replace(" ", "."))

        print(f"{len(follower_panels)} followers were found for {username}")
        followers = []
        for follower_panel in follower_panels:
            follower_username = follower_panel.find_element(By.CLASS_NAME, USERNAME_CLASS_SELECTOR.replace(" ", ".")).text
            try:
                follower_image = follower_panel.find_element(By.TAG_NAME, "img").get_attribute("src")
            except NoSuchElementException:
                follower_image = None
            if follower_username:
                followers.append({
                    "username": follower_username,
                    "image": follower_image
                })
            else:
                print(f"An username is missing in the panel of {username}")
        return followers

    def generate_followers_tree(self, username: str, depth=3, n_scrolls=2):
        if depth < 1:
            return

        followers = self.get_follower_usernames(username, n_scrolls=n_scrolls)
        follower_usernames = [follower["username"] for follower in followers]
        self.followers_tree[username] = followers
        for follower_username in follower_usernames:
            self.generate_followers_tree(follower_username, depth=depth-1, n_scrolls=n_scrolls)


def main():
    user = "valentinafeve"
    scrapper = Scrapper(user)
    scrapper.start_and_log()
    scrapper.generate_followers_tree(scrapper.username, depth=2, n_scrolls=30)
    pickle.dump(scrapper.followers_tree, open(f"followers_tree_{user}.pickle", "wb+"))
    return


if __name__ == "__main__":
    main()
