"""
Test tree structure for Dijkstra and A*
"""
import sys
sys.path.insert(0, 'src')

from algorithms.graph.dijkstra_weighted import dijkstra_weighted
from algorithms.graph.astar_weighted import astar_weighted


def test_tree_structure():
    """Test that the graph is generated as a tree"""
    print("="*70)
    print("Testing Tree Structure for Weighted Pathfinding")
    print("="*70)

    test_arr = [20]  # Will determine depth

    # Test Dijkstra to see the tree structure
    print("\nGenerating tree structure...")
    dijkstra_gen = dijkstra_weighted(test_arr)

    tree_info = None
    dijkstra_stats = None

    for state in dijkstra_gen:
        if state['action'] == 'start':
            tree_info = {
                'nodes': state['nodes'],
                'edges': state['edges'],
                'start': state['start'],
                'end': state['end']
            }

        if state['action'] == 'done':
            dijkstra_stats = state['stats']
            dijkstra_path = state.get('path', [])

    if tree_info:
        print(f"\nTree Statistics:")
        print(f"  Total Nodes: {len(tree_info['nodes'])}")
        print(f"  Total Edges: {len(tree_info['edges'])}")
        print(f"  Root Node: {tree_info['start']}")
        print(f"  Goal Node (Leaf): {tree_info['end']}")

        # Analyze tree structure
        children_count = {}
        for node in tree_info['nodes']:
            children_count[node] = 0

        for edge in tree_info['edges']:
            parent, child = edge[0], edge[1]
            # Count based on direction (lower number = parent)
            if parent < child:
                children_count[parent] = children_count.get(parent, 0) + 1

        # Find leaf nodes (nodes with no children in tree structure)
        leaf_nodes = [node for node, count in children_count.items() if count == 0 and node != tree_info['start']]

        print(f"\n  Leaf Nodes: {len(leaf_nodes)}")
        print(f"  Max branching factor: {max(children_count.values())}")

        # Calculate tree depth
        print(f"\nTree Edges with weights:")
        edges_by_level = {}
        for edge in tree_info['edges']:
            parent, child, weight = edge
            if parent < child:  # Tree edge (parent -> child)
                level = parent // 3  # Approximate level
                if level not in edges_by_level:
                    edges_by_level[level] = []
                edges_by_level[level].append((parent, child, weight))

        for level in sorted(edges_by_level.keys())[:3]:  # Show first 3 levels
            print(f"\n  Level {level}:")
            for parent, child, weight in edges_by_level[level][:5]:  # Show first 5
                print(f"    {parent} --[{weight}]-> {child}")
            if len(edges_by_level[level]) > 5:
                print(f"    ... and {len(edges_by_level[level]) - 5} more")

    # Test both algorithms
    print("\n" + "="*70)
    print("Comparison: Dijkstra vs A*")
    print("="*70)

    # Run A*
    astar_gen = astar_weighted(test_arr)
    astar_stats = None

    for state in astar_gen:
        if state['action'] == 'done':
            astar_stats = state['stats']

    if dijkstra_stats and astar_stats:
        print(f"\nDijkstra's Algorithm:")
        print(f"  Nodes Visited: {dijkstra_stats['nodes_visited']}")
        print(f"  Path Length: {dijkstra_stats['path_length']}")
        print(f"  Total Cost: {dijkstra_stats['total_cost']}")

        print(f"\nA* Algorithm:")
        print(f"  Nodes Visited: {astar_stats['nodes_visited']}")
        print(f"  Path Length: {astar_stats['path_length']}")
        print(f"  Total Cost: {astar_stats['total_cost']}")

        if dijkstra_stats['total_cost'] == astar_stats['total_cost']:
            print(f"\n[OK] Both found optimal path with cost: {dijkstra_stats['total_cost']}")
        else:
            print(f"\n[!] Different costs found")

        nodes_saved = dijkstra_stats['nodes_visited'] - astar_stats['nodes_visited']
        if nodes_saved > 0:
            improvement = (nodes_saved / dijkstra_stats['nodes_visited']) * 100
            print(f"\nEfficiency Improvement:")
            print(f"  A* visited {nodes_saved} fewer nodes ({improvement:.1f}% reduction)")
        elif nodes_saved < 0:
            print(f"\n[!] A* visited more nodes (unusual)")
        else:
            print(f"\n[=] Both visited same number of nodes")

    print("\n" + "="*70)
    print("Tree Structure Benefits:")
    print("  - Clear visual hierarchy (root at top, leaves at bottom)")
    print("  - Easy to see path from root to goal leaf")
    print("  - Alternative paths via cross-edges")
    print("  - Weighted edges show different costs")
    print("="*70)


if __name__ == "__main__":
    test_tree_structure()
