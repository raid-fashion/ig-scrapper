from pyvis.network import Network

net = Network(directed=True)

example_dict = {
    "dani": [
        "luisa",
        "vale",
        "rosalía"
    ],
    "vale": [
        "luisa",
        "dani",
        "sebas",
        "jose"
    ],
    "sebas": [
        "vale",
        "jose"
    ],
    "jose": [
        "vale"
    ],

}

example_dict2 = {
    'a': [
        'b', 'c', 'd'
    ]
}


def add_follower(username, followers):
    net.add_node(username, label=username)
    for follower in followers:
        net.add_node(follower, label=follower)
        net.add_edge(username, follower)


def build_graph(dict_to_graph):
    for username, followers in dict_to_graph.items():
        add_follower(username, followers)
    net.show('mygraph.html')



