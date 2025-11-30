"""
Test weighted graph algorithms - Dijkstra vs A*
"""
import sys
sys.path.insert(0, 'src')

from algorithms.graph.dijkstra_weighted import dijkstra_weighted
from algorithms.graph.astar_weighted import astar_weighted


def test_weighted_graph_comparison():
    """Compare Dijkstra and A* on the same weighted graph"""
    print("="*70)
    print("Testing Dijkstra vs A* on Weighted Graph")
    print("="*70)

    test_arr = [15]  # Will generate ~5 nodes

    # Test Dijkstra
    print("\n1. Dijkstra's Algorithm:")
    print("-" * 70)
    dijkstra_gen = dijkstra_weighted(test_arr)

    dijkstra_stats = None
    dijkstra_graph = None

    for state in dijkstra_gen:
        if state['action'] == 'start':
            dijkstra_graph = {
                'nodes': state['nodes'],
                'edges': state['edges'],
                'start': state['start'],
                'end': state['end']
            }
            print(f"  Graph: {len(state['nodes'])} nodes, {len(state['edges'])} edges")
            print(f"  Start: {state['start']}, Goal: {state['end']}")
            print(f"  Edges with weights:")
            for edge in state['edges']:
                print(f"    {edge[0]} --[{edge[2]}]-- {edge[1]}")

        if state['action'] == 'done':
            dijkstra_stats = state['stats']

    if dijkstra_stats:
        print(f"\n  Results:")
        print(f"    Nodes Visited: {dijkstra_stats['nodes_visited']}")
        print(f"    Path Length: {dijkstra_stats['path_length']}")
        print(f"    Total Cost: {dijkstra_stats['total_cost']}")
        print(f"    Efficiency: {dijkstra_stats['path_length'] / dijkstra_stats['nodes_visited'] * 100:.1f}%")

    # Test A*
    print("\n2. A* Algorithm:")
    print("-" * 70)
    astar_gen = astar_weighted(test_arr)

    astar_stats = None

    for state in astar_gen:
        if state['action'] == 'done':
            astar_stats = state['stats']

    if astar_stats:
        print(f"  Results:")
        print(f"    Nodes Visited: {astar_stats['nodes_visited']}")
        print(f"    Path Length: {astar_stats['path_length']}")
        print(f"    Total Cost: {astar_stats['total_cost']}")
        print(f"    Efficiency: {astar_stats['path_length'] / astar_stats['nodes_visited'] * 100:.1f}%")

    # Comparison
    print("\n" + "="*70)
    print("Comparison:")
    print("="*70)

    if dijkstra_stats and astar_stats:
        # Check if they found the same path cost
        if dijkstra_stats['total_cost'] == astar_stats['total_cost']:
            print(f"[OK] Both found optimal path with cost: {dijkstra_stats['total_cost']}")
        else:
            print(f"[X] Different costs: Dijkstra={dijkstra_stats['total_cost']}, A*={astar_stats['total_cost']}")

        # Compare efficiency
        nodes_saved = dijkstra_stats['nodes_visited'] - astar_stats['nodes_visited']
        improvement = (nodes_saved / dijkstra_stats['nodes_visited']) * 100

        print(f"\nEfficiency:")
        print(f"  Dijkstra visited: {dijkstra_stats['nodes_visited']} nodes")
        print(f"  A* visited: {astar_stats['nodes_visited']} nodes")
        print(f"  A* saved: {nodes_saved} node visits ({improvement:.1f}% reduction)")

        if astar_stats['nodes_visited'] < dijkstra_stats['nodes_visited']:
            print(f"\n[***] A* is more efficient!")
        elif astar_stats['nodes_visited'] == dijkstra_stats['nodes_visited']:
            print(f"\n[=] Both visited the same number of nodes")

    print("\n" + "="*70)
    print("Key Differences:")
    print("  - Dijkstra: Explores uniformly in all directions")
    print("  - A*: Uses heuristic to guide search toward goal")
    print("  - Both guarantee optimal path in weighted graphs")
    print("="*70)


if __name__ == "__main__":
    test_weighted_graph_comparison()
