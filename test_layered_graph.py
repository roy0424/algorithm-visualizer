"""
Test layered graph structure (neural network style)
"""
import sys
sys.path.insert(0, 'src')

from algorithms.graph.dijkstra_weighted import dijkstra_weighted
from algorithms.graph.astar_weighted import astar_weighted


def test_layered_structure():
    """Test that the graph is generated in layered structure"""
    print("="*70)
    print("Testing Layered Graph Structure (Neural Network Style)")
    print("="*70)

    test_arr = [30]  # Will determine number of layers

    # Test Dijkstra to see the layer structure
    print("\nGenerating layered graph...")
    dijkstra_gen = dijkstra_weighted(test_arr)

    graph_info = None
    dijkstra_stats = None

    for state in dijkstra_gen:
        if state['action'] == 'start':
            graph_info = {
                'nodes': state['nodes'],
                'edges': state['edges'],
                'start': state['start'],
                'end': state['end']
            }

        if state['action'] == 'done':
            dijkstra_stats = state['stats']
            dijkstra_path = state.get('path', [])

    if graph_info:
        print(f"\nGraph Structure:")
        print(f"  Total Nodes: {len(graph_info['nodes'])}")
        print(f"  Total Edges: {len(graph_info['edges'])}")
        print(f"  Start Node: {graph_info['start']}")
        print(f"  Goal Node: {graph_info['end']}")

        # Analyze layer structure
        layers = {}
        for node in graph_info['nodes']:
            if isinstance(node, tuple):
                layer_id = node[0]
                if layer_id not in layers:
                    layers[layer_id] = []
                layers[layer_id].append(node)

        print(f"\n  Layers: {len(layers)}")
        for layer_id in sorted(layers.keys()):
            nodes_in_layer = layers[layer_id]
            print(f"    Layer {layer_id}: {len(nodes_in_layer)} nodes - {nodes_in_layer}")

        # Show some edges
        print(f"\n  Sample Edges (with weights):")
        for i, edge in enumerate(graph_info['edges'][:10]):
            source, target, weight = edge
            print(f"    {source} --[{weight}]--> {target}")
        if len(graph_info['edges']) > 10:
            print(f"    ... and {len(graph_info['edges']) - 10} more edges")

    # Test both algorithms
    print("\n" + "="*70)
    print("Comparison: Dijkstra vs A* (Layered Graph)")
    print("="*70)

    # Run A*
    astar_gen = astar_weighted(test_arr)
    astar_stats = None
    astar_path = None

    for state in astar_gen:
        if state['action'] == 'done':
            astar_stats = state['stats']
            astar_path = state.get('path', [])

    if dijkstra_stats and astar_stats:
        print(f"\nDijkstra's Algorithm:")
        print(f"  Nodes Visited: {dijkstra_stats['nodes_visited']}")
        print(f"  Path Length: {dijkstra_stats['path_length']}")
        print(f"  Total Cost: {dijkstra_stats['total_cost']}")
        if dijkstra_path:
            print(f"  Path: {' -> '.join([str(n) for n in dijkstra_path[:5]])}{'...' if len(dijkstra_path) > 5 else ''}")

        print(f"\nA* Algorithm:")
        print(f"  Nodes Visited: {astar_stats['nodes_visited']}")
        print(f"  Path Length: {astar_stats['path_length']}")
        print(f"  Total Cost: {astar_stats['total_cost']}")
        if astar_path:
            print(f"  Path: {' -> '.join([str(n) for n in astar_path[:5]])}{'...' if len(astar_path) > 5 else ''}")

        if dijkstra_stats['total_cost'] == astar_stats['total_cost']:
            print(f"\n[OK] Both found optimal path with cost: {dijkstra_stats['total_cost']}")
        else:
            print(f"\n[!] Different costs: Dijkstra={dijkstra_stats['total_cost']}, A*={astar_stats['total_cost']}")

        nodes_saved = dijkstra_stats['nodes_visited'] - astar_stats['nodes_visited']
        if nodes_saved > 0:
            improvement = (nodes_saved / dijkstra_stats['nodes_visited']) * 100
            print(f"\nEfficiency Improvement:")
            print(f"  A* visited {nodes_saved} fewer nodes ({improvement:.1f}% reduction)")
            print(f"  [***] A* is more efficient!")
        elif nodes_saved < 0:
            print(f"\n[!] A* visited {-nodes_saved} more nodes")
        else:
            print(f"\n[=] Both visited same number of nodes")

    print("\n" + "="*70)
    print("Layered Graph Benefits:")
    print("  - Clear left-to-right progression (Start -> Goal)")
    print("  - Multiple paths through different layer nodes")
    print("  - Skip connections for alternative routes")
    print("  - Weighted edges show cost differences")
    print("  - Like a neural network visualization!")
    print("="*70)


if __name__ == "__main__":
    test_layered_structure()
