import argparse
import networkx as nx
import matplotlib.pyplot as plt
import os


def load_graph(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")
    try:
        G = nx.read_gml(file_path)
    except Exception as e:
        raise ValueError(f"Error reading GML file: {e}")
    return G


def plot_graph(G, preferences=None, title="Market Graph"):
    pos = nx.spring_layout(G, seed=42)
    labels = {
        node: f"{node}\n${G.nodes[node].get('price', '')}" if G.nodes[node].get("bipartite") == 0 else f"{node}"
        for node in G.nodes
    }
    edge_labels = {(u, v): f"{d['valuation']}" for u, v, d in G.edges(data=True)}

    nx.draw(G, pos, with_labels=True, labels=labels, node_color='skyblue', edge_color='gray', node_size=1500)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.show()


def market_clearing_algorithm(G, interactive=False):
    A = [n for n, d in G.nodes(data=True) if d.get('bipartite') == 0]
    B = [n for n, d in G.nodes(data=True) if d.get('bipartite') == 1]

    round_num = 1
    while round_num <= 4:
        preferences = {}
        for b in B:
            neighbors = list(G[b])
            if not neighbors:
                continue
            best_seller = max(neighbors, key=lambda a: G[b][a]['valuation'] - G.nodes[a]['price'])
            preferences[b] = best_seller

        demand = {a: 0 for a in A}
        for a in preferences.values():
            demand[a] += 1

        constricted = [a for a in demand if demand[a] > 1]
        if interactive:
            print(f"Round {round_num}: Constricted set = {constricted}, prices before update = {[G.nodes[a]['price'] for a in A]}")

        for a in constricted:
            G.nodes[a]['price'] += 1

        if interactive:
            print(f"Round {round_num}: Prices after update = {[G.nodes[a]['price'] for a in A]}\n")

        round_num += 1

    return G


def main():
    parser = argparse.ArgumentParser(description="Market Clearing Strategy")
    parser.add_argument("file", help="Path to market GML file")
    parser.add_argument("--plot", action="store_true", help="Plot the graph")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode showing each round")
    args = parser.parse_args()

    try:
        G = load_graph(args.file)
    except Exception as e:
        print(e)
        return

    G = market_clearing_algorithm(G, interactive=args.interactive)

    if args.plot:
        plot_graph(G, title="Final Market Graph")


if __name__ == "__main__":
    main()