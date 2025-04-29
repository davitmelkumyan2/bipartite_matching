import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_graph_with_matching(G, matching, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    try:
        top, bottom = nx.bipartite.sets(G)
    except:
        raise ValueError("Graph is not bipartite")

    pos = {}
    top_nodes = sorted(top)
    bottom_nodes = sorted(bottom)

    max_len = max(len(top_nodes), len(bottom_nodes))
    x_step = 1.5 / (max_len + 1)

    for i, node in enumerate(top_nodes):
        pos[node] = ((i + 1) * x_step, 1)
    for i, node in enumerate(bottom_nodes):
        pos[node] = ((i + 1 + (max_len - len(bottom_nodes)) / 2) * x_step, 0)

    fig, ax = plt.subplots(figsize=(14, 8))

    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1, ax=ax)
    if matching:
        nx.draw_networkx_edges(G, pos, edgelist=matching, edge_color='red', width=3, ax=ax)

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', ax=ax, node_size=500)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12)

    for (u, v), d in G.edges.items():
        weight = d['weight']
        weight_text = f"{int(weight)}" if weight.is_integer() else f"{weight:.1f}".rstrip('0').rstrip('.')

        x = pos[u][0] + (pos[v][0] - pos[u][0]) * 0.6
        y = pos[u][1] + (pos[v][1] - pos[u][1]) * 0.6

        x_offset = 0.02 if pos[u][1] > pos[v][1] else -0.02
        y_offset = 0.02 if pos[u][0] < pos[v][0] else -0.02

        ax.text(x + x_offset, y + y_offset, weight_text,
                ha='center', va='center',
                fontsize=11,
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=0.3))

    ax.set_title("Bipartite Graph Matching", fontsize=14, pad=10)
    ax.axis('off')
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)