import matplotlib.pyplot as plt
import networkx as nx
import os
fig_root = os.curdir
# Define the imports and their dependencies
dependencies = {
    "numpy": [],
    "pandas": [],
    "sklearn.datasets": ["make_classification"],
    "sklearn.preprocessing": ["MinMaxScaler"],
    "joblib": [],
    "datetime": [],
    "os": [],
    "matplotlib.pyplot": [],
    "seaborn": [],
    "django.conf": ["settings"],
    "time": [],
    "geopy.exc": ["geo"],
    "requests": [],
    "geopy.geocoders": ["Geocodio", "GoogleV3", "Nominatim", "OpenCage"],
    "json": [],
    "pathlib": ["Path"],
    "get_coordinates": ["get_latitude_longitude"],
    "configparser": []
}

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for parent, children in dependencies.items():
    G.add_node(parent)
    for child in children:
        G.add_edge(parent, child)

# Draw the graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="lightblue", font_weight="bold", node_size=3000, font_size=10, edge_color="gray")
plt.title("Dependencies Graph for the Given Imports", fontsize=14)
plt.show()
plt.savefig(os.path.join(fig_root, 'dep_graph.png'))
