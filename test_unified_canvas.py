"""
Test that Dijkstra and A* provide statistics correctly
"""
import sys
sys.path.insert(0, 'src')

from algorithms.graph.dijkstra_grid import dijkstra_grid
from algorithms.graph.astar_grid import astar_grid


def test_statistics_in_state():
    """Test that Dijkstra and A* include statistics in their state"""
    print("Testing Dijkstra and A* statistics output...")
    print("="*60)

    # Test Dijkstra
    print("\nDijkstra's Algorithm:")
    dijkstra_gen = dijkstra_grid([15])
    has_stats = False
    final_stats = None

    for state in dijkstra_gen:
        if 'stats' in state:
            has_stats = True
            final_stats = state['stats']

    print(f"  Has 'stats' in state: {has_stats}")
    if final_stats:
        print(f"  Final stats: {final_stats}")
        print(f"    - Nodes Visited: {final_stats.get('nodes_visited', 'N/A')}")
        print(f"    - Path Length: {final_stats.get('path_length', 'N/A')}")
        print(f"    - Steps: {final_stats.get('steps', 'N/A')}")

    # Test A*
    print("\nA* Algorithm:")
    astar_gen = astar_grid([15])
    has_stats = False
    final_stats = None

    for state in astar_gen:
        if 'stats' in state:
            has_stats = True
            final_stats = state['stats']

    print(f"  Has 'stats' in state: {has_stats}")
    if final_stats:
        print(f"  Final stats: {final_stats}")
        print(f"    - Nodes Visited: {final_stats.get('nodes_visited', 'N/A')}")
        print(f"    - Path Length: {final_stats.get('path_length', 'N/A')}")
        print(f"    - Steps: {final_stats.get('steps', 'N/A')}")

    print("\n" + "="*60)
    print("Verification:")
    print("- Both algorithms should have 'stats' in their state")
    print("- GraphCanvas will display these stats in the top-right panel")
    print("- DFS/BFS show stack/queue, Dijkstra/A* show statistics")


if __name__ == "__main__":
    test_statistics_in_state()
