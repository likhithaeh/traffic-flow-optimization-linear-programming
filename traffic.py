import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import linprog

SCENARIO_TO_DRAW = "Peak Hour"   # Normal / Peak Hour / Road Closure / Reduced Capacity
SCENARIOS = ["Normal", "Peak Hour", "Road Closure", "Reduced Capacity"]

# (from, to, capacity in cars/hour)
ROADS = [("A","B",500), ("A","C",400), ("B","D",600), ("C","D",300), ("B","E",400),
         ("C","F",500), ("D","E",600), ("D","F",400), ("E","F",700)]
NODES = ["A", "B", "C", "D", "E", "F"]
POS = {"A": (0,1), "B": (1,2), "C": (1,0), "D": (2,1), "E": (3,2), "F": (3,0)}


def build(name):
    """Make the road network for a scenario. Returns (graph, cars per hour A->F)."""
    g = nx.DiGraph()
    for u, v, cap in ROADS:
        g.add_edge(u, v, capacity=cap)
    demand = 770
    if name == "Peak Hour":
        demand = 850
    elif name == "Road Closure":
        g.remove_edge("B", "D")
    elif name == "Reduced Capacity":
        g["D"]["E"]["capacity"] = 250
    return g, demand


def before(g, demand):
    """Simple rule: every intersection splits its cars evenly among its roads."""
    arriving = {n: 0 for n in NODES}
    arriving["A"] = demand
    flows = {}
    for n in NODES:
        out = list(g.successors(n))
        for m in out:
            flows[(n, m)] = arriving[n] / len(out)
            arriving[m] += arriving[n] / len(out)
    return flows


def after(g, demand):
    """Linear program: make the busiest road as empty as possible."""
    edges = list(g.edges())
    n = len(edges)
    cap = [g[u][v]["capacity"] for u, v in edges]

    # variables: flow on each road (n of them) + z (busiest road's utilisation)
    # 1) cars in = cars out at every intersection
    A_eq = np.zeros((len(NODES), n + 1))
    for j, (u, v) in enumerate(edges):
        A_eq[NODES.index(u), j] = 1
        A_eq[NODES.index(v), j] = -1
    b_eq = np.zeros(len(NODES))
    b_eq[0], b_eq[-1] = demand, -demand          # A sends cars, F receives them

    # 2) flow <= z * capacity   (so z = worst utilisation)
    A_ub = np.zeros((n, n + 1))
    for j in range(n):
        A_ub[j, j] = 1
        A_ub[j, n] = -cap[j]

    # goal: minimise z (tiny extra cost on flow avoids pointless loops)
    c = np.append(np.full(n, 1e-4), 1.0)
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(n), A_eq=A_eq, b_eq=b_eq,
                  bounds=[(0, None)] * (n + 1), method="highs")
    return {e: res.x[j] for j, e in enumerate(edges)}


def draw(g, b, a, title):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for ax, flows, name in zip(axes, [b, a], ["Before", "After"]):
        ax.set_title(name + " Optimization", fontsize=14, fontweight="bold")
        colors, labels = [], {}
        for u, v in g.edges():
            f, cap = flows[(u, v)], g[u][v]["capacity"]
            colors.append("red" if f > cap else "orange" if f >= 0.8 * cap else "green")
            labels[(u, v)] = f"{f:.0f}/{cap}"
        nx.draw_networkx_nodes(g, POS, ax=ax, node_color="skyblue", node_size=1200)
        nx.draw_networkx_labels(g, POS, ax=ax, font_weight="bold")
        nx.draw_networkx_edges(g, POS, ax=ax, edge_color=colors, width=2.5, arrowsize=20)
        nx.draw_networkx_edge_labels(g, POS, edge_labels=labels, ax=ax, font_size=9)
        ax.axis("off")
    plt.suptitle(title + "\n(green = ok, orange = >=80% full, red = over capacity)", fontsize=14)
    plt.tight_layout()
    plt.savefig("traffic_result.png", dpi=150)


def worst(g, flows):
    return max(flows[e] / g[e[0]][e[1]]["capacity"] for e in g.edges())


def excess(g, flows):
    return sum(max(0, flows[e] - g[e[0]][e[1]]["capacity"]) for e in g.edges())


print(f"{'Scenario':<18}{'Demand':>7}{'Worst before':>14}{'Worst after':>13}{'Excess before':>15}{'Excess after':>14}")
print("-" * 81)
for name in SCENARIOS:
    g, demand = build(name)
    b, a = before(g, demand), after(g, demand)
    print(f"{name:<18}{demand:>7}{worst(g,b)*100:>13.0f}%{worst(g,a)*100:>12.0f}%"
          f"{excess(g,b):>15.0f}{excess(g,a):>14.0f}")
    if name == SCENARIO_TO_DRAW:
        draw(g, b, a, f"Traffic Flow Optimization - {name}")

print("\n(Worst = busiest road's utilisation. Excess = cars/hr above capacity.)")
plt.show()