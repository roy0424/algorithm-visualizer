"""
Test script to verify graph algorithm integration
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from algorithms.graph.graph_dfs import graph_dfs, get_algorithm_info as dfs_info
from algorithms.graph.graph_bfs import graph_bfs, get_algorithm_info as bfs_info
from algorithms.graph.dijkstra import dijkstra, get_algorithm_info as dijkstra_info
from algorithms.graph.prim import prim, get_algorithm_info as prim_info
from algorithms.graph.kruskal import kruskal, get_algorithm_info as kruskal_info


def test_algorithm(name, algo_func, info_func, test_array):
    """Test a single graph algorithm"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")

    info = info_func()
    print(f"Time Complexity: {info['time_complexity']}")
    print(f"Space Complexity: {info['space_complexity']}")
    print(f"Description: {info['description']}\n")

    # Run algorithm and collect states
    states = []
    for state in algo_func(test_array):
        states.append(state)

    print(f"Total steps: {len(states)}")

    if states:
        # Show first and last state
        print(f"\nFirst state:")
        print(f"  Action: {states[0].get('action')}")
        print(f"  Nodes: {states[0].get('nodes', [])}")
        print(f"  Edges: {len(states[0].get('edges', []))} edges")
        print(f"  Description: {states[0].get('description', 'N/A')}")

        print(f"\nLast state:")
        print(f"  Action: {states[-1].get('action')}")
        print(f"  Visited: {states[-1].get('visited', [])}")
        print(f"  Description: {states[-1].get('description', 'N/A')}")

        return True
    else:
        print("ERROR: No states generated!")
        return False


def main():
    """Run all graph algorithm tests"""
    print("Graph Algorithm Integration Test")
    print("="*60)

    # Test array
    test_array = [5, 10, 3, 8, 15, 7, 12, 9]
    print(f"Test array: {test_array}")

    results = {}

    # Test DFS
    results['DFS'] = test_algorithm(
        "Graph DFS",
        graph_dfs,
        dfs_info,
        test_array
    )

    # Test BFS
    results['BFS'] = test_algorithm(
        "Graph BFS",
        graph_bfs,
        bfs_info,
        test_array
    )

    # Test Dijkstra
    results['Dijkstra'] = test_algorithm(
        "Dijkstra's Algorithm",
        dijkstra,
        dijkstra_info,
        test_array
    )

    # Test Prim
    results['Prim'] = test_algorithm(
        "Prim's Algorithm",
        prim,
        prim_info,
        test_array
    )

    # Test Kruskal
    results['Kruskal'] = test_algorithm(
        "Kruskal's Algorithm",
        kruskal,
        kruskal_info,
        test_array
    )

    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")

    all_passed = True
    for algo, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{algo:20s}: {status}")
        if not passed:
            all_passed = False

    print(f"{'='*60}")
    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed!")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
