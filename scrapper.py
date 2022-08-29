from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from pyvis.network import Network

username = ""


def build_url_followers(username):
    return f"{main_url}/{username}/followers"


main_driver = webdriver.Firefox()
main_url = "http://instagram.com"

main_driver.get(main_url)

followers_dict = {}


def get_followers(username, depth=3, n_scrolls=2):
    print(f"Getting followers of {username}")
    if depth < 1:
        print(f"Depth reached for {username}")
        return
    main_driver.get(build_url_followers(username))
    time.sleep(5)

    followers_dict[username] = followers_dict.get(username, [])
    try:
        followers_pane = main_driver.find_element(By.CSS_SELECTOR, "._aano")
    except:
        print(f"Account {username} seems to be private")
        return

    for i in range(n_scrolls):
        followers_pane.send_keys(Keys.END)
        time.sleep(3)

    # TODO: Following and followers
    # TODO: Take children of first child in order to avoid suggestions
    followers = followers_pane.find_elements(By.CSS_SELECTOR, "._ab8w._ab94._ab97._ab9f._ab9k._ab9p._ab9-._aba8._abcm")
    print(f"{len(followers)} followers were found for {username}")
    follower_usernames = []
    for follower_item in followers:
        follower_username = follower_item.find_element(By.CSS_SELECTOR, "._aacl._aaco._aacu._aacx._aada").text
        if follower_username:
            follower_usernames.append(follower_username)
            followers_dict[username].append(follower_username)
        else:
            print(f"An username is missing in the panel of {username}")
    for follower_username in follower_usernames:
        get_followers(follower_username, depth=depth-1, n_scrolls=n_scrolls)


get_followers(username, depth=2, n_scrolls=2)
followers_dict
#main_driver.close()

pd.pivot_table(df.reset_index(), aggfunc='count', index=['index'])