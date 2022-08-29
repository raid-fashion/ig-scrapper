import pickle

from cleaner import SocialNetworkMatrix
from plotter import Plotter


dictionary = pickle.load(open("tree.pickle", "rb"))
username_images = {}
for username, followers in dictionary.items():
    for follower in followers:
        username_images[follower['username']] = follower['image']

snm = SocialNetworkMatrix.build_from_dict(dictionary)

filtered_df = snm.df[snm.df.apply(lambda x: x.sum(), axis=1) > 1]

plotter = Plotter(username_images=username_images)

for username, row in filtered_df.iterrows():
    followers = filtered_df.loc[username].dropna().index.tolist()
    plotter.add_follower(username, followers)

plotter.build_graph()
