import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from pyvis.network import Network
import logging

MAIN_URL = "http://instagram.com"


def build_followers_url(username: str):
    return f"{MAIN_URL}/{username}/followers"


class Scrapper:
    def __init__(self, username):
        self.username = username
        self.followers_tree = {}
        self.main_driver = webdriver.Firefox()
        return

    def start_and_log(self):
        self.main_driver.get(MAIN_URL)
        return

    def get_follower_usernames(self, username: str, n_scrolls=2):
        logging.info(f"Getting followers of {username}")
        self.main_driver.get(build_followers_url(username))
        time.sleep(2)

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
        follower_panels = followers_panel.find_elements(By.CSS_SELECTOR,
                                                 "._ab8w._ab94._ab97._ab9f._ab9k._ab9p._ab9-._aba8._abcm")
        print(f"{len(follower_panels)} followers were found for {username}")
        followers = []
        for follower_panel in follower_panels:
            follower_username = follower_panel.find_element(By.CSS_SELECTOR, "._aacl._aaco._aacu._aacx._aada").text
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
        """
        Generate followers tree given a user, that is to say, generates a tree of followers and its followers of depth 'depth'.
        :param username:
        :param depth: Depth of the tree
        :param n_scrolls:
        :return:
        """

        if depth < 1:
            return

        followers = self.get_follower_usernames(username, n_scrolls=n_scrolls)
        follower_usernames = [follower["username"] for follower in followers]
        self.followers_tree[username] = followers
        for follower_username in follower_usernames:
            self.generate_followers_tree(follower_username, depth=depth-1, n_scrolls=n_scrolls)


def main():
    scrapper = Scrapper("baru.derama")
    scrapper.start_and_log()
    scrapper.generate_followers_tree(scrapper.username, depth=2, n_scrolls=40)
    pickle.dump(scrapper.followers_tree, open("followers_tree_baruderama.pickle", "wb+"))
    return


if __name__ == "__main__":
    main()
