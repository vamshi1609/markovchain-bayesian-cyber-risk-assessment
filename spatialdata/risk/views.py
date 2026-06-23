from django.shortcuts import render

from . import services
from .models import Asset, Vulnerability


def risk_dashboard(request):
    # ensure EPSS scores are available
    services.compute_epss()

    G = services.build_asset_graph()
    # for demonstration assume every asset with a vuln is a start node
    start_nodes = list(
        Asset.objects.filter(vulnerability__isnull=False).values_list("pk", flat=True)
    )
    # assume assets with highest criticality are goals
    goal_nodes = list(
        Asset.objects.order_by("-criticality").values_list("pk", flat=True)[:3]
    )
    paths = services.find_attack_paths(G, start_nodes, goal_nodes)
    dist = services.risk_markov(paths, G)
    impact = services.assess_impact(dist, G)
    prog = services.progression_analysis(paths)
    context = {
        "paths": paths,
        "distribution": dist,
        "impact": impact,
        "progression": prog,
    }
    return render(request, "risk/dashboard.html", context)
