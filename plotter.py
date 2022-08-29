from pyvis.network import Network


class Plotter:
    def __init__(self, username_images=None):
        self.username_images = username_images
        self.net = Network(directed=True)

    def add_follower(self, username, followers):
        self.net.add_node(username, label=username, shape='circularImage', image=self.username_images.get(username, None))
        for follower in followers:
            self.net.add_node(follower, label=follower)
            self.net.add_edge(follower, username)

    def build_graph(self):
        self.net.show('mygraph.html')



