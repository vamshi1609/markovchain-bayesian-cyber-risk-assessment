"""Core algorithms for the cyber‑risk evaluation modules described by the
user.

Each function corresponds roughly to one of the seven modules in the
specification.  They operate on Django model objects defined in
`risk.models` and return plain Python data structures that can be
rendered or persisted by the calling view/command.
"""

import networkx as nx
import numpy as np
from .models import Asset, Vulnerability, AssetDependency


# 1. Vulnerability Likelihood Estimation Module
# ------------------------------------------------
# For the sake of the example we provide a stub that either looks up an
# external EPSS value or generates a random probability.  In a production
# system you would call the official EPSS API or a local model.

def compute_epss(vulns=None):
    if vulns is None:
        vulns = Vulnerability.objects.all()
    for v in vulns:
        if v.epss_score is None:
            # placeholder: random in [0,1)
            v.epss_score = np.random.rand()
            v.save()
    return vulns


# 2. Asset Dependency Modeling Module
# ------------------------------------------------

def build_asset_graph():
    """Return a directed graph where nodes are asset primary keys and edges
    encode dependencies (with an optional weight attribute)."""

    G = nx.DiGraph()
    for a in Asset.objects.all():
        G.add_node(a.pk, criticality=a.criticality, name=a.name)
    for dep in AssetDependency.objects.all():
        G.add_edge(dep.source.pk, dep.target.pk, weight=dep.weight)
    return G


# 3. Attack Path Identification Module
# ------------------------------------------------

def find_attack_paths(G, start_nodes, goal_nodes):
    """Depth‑first traversal collecting all simple paths from any start node
    to any goal node."""

    paths = []

    def dfs(current, path):
        if current in goal_nodes:
            paths.append(path.copy())
            return
        for succ in G.successors(current):
            if succ not in path:  # avoid cycles
                path.append(succ)
                dfs(succ, path)
                path.pop()

    for s in start_nodes:
        dfs(s, [s])
    return paths


# 4. Probabilistic Risk Evaluation Module
# ------------------------------------------------

def risk_markov(paths, G):
    """Combine a set of attack paths into a simple absorbing Markov chain.
    Return a dictionary mapping end node -> probability of reaching it.
    """

    # build transition matrix
    nodes = list(G.nodes)
    idx = {n: i for i, n in enumerate(nodes)}
    P = np.zeros((len(nodes), len(nodes)))
    # for simplicity, assume epss_score on vulnerability is the edge
    # transition probability between assets (could be more complex).
    for u, v in G.edges():
        # default weight if not specified
        w = G[u][v].get("weight", 1.0)
        P[idx[u], idx[v]] = w
    # normalise rows
    row_sums = P.sum(axis=1)
    for i, s in enumerate(row_sums):
        if s > 0:
            P[i, :] /= s

    # use paths to compute absorption probabilities; this is a heuristic
    distribution = {}
    for path in paths:
        end = path[-1]
        # product of transition probabilities along the path
        prob = 1.0
        for u, v in zip(path, path[1:]):
            prob *= P[idx[u], idx[v]]
        distribution[end] = distribution.get(end, 0.0) + prob
    # normalise
    total = sum(distribution.values())
    if total > 0:
        for k in distribution:
            distribution[k] /= total
    return distribution


# 5. Impact Assessment Module
# ------------------------------------------------

def assess_impact(distribution, G=None):
    """Given a probability distribution over asset nodes, weight by
    criticality to compute aggregate risk."""

    impact = 0.0
    if G is None:
        G = build_asset_graph()
    for node, prob in distribution.items():
        crit = G.nodes[node].get("criticality", 0)
        impact += prob * crit
    return impact


# 6. Attack Progression Analysis Module
# ------------------------------------------------

def progression_analysis(paths, time_map=None):
    """Return a dict mapping each path (tuple of nodes) to an estimated
    time‑to‑compromise. ``time_map`` is a dict of (u,v)-> latency.
    """

    if time_map is None:
        time_map = {}
    metrics = {}
    for path in paths:
        total = 0.0
        for u, v in zip(path, path[1:]):
            total += time_map.get((u, v), 1.0)
        metrics[tuple(path)] = total
    return metrics


# 7. Decision Support & Visualization Module
# ------------------------------------------------
from django.template.loader import render_to_string


def make_dashboard(context):
    """Produce rendered HTML for inclusion in an existing template or
    as a standalone page."""

    return render_to_string("risk/dashboard.html", context)
