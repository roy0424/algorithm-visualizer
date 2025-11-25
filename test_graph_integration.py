#!/usr/bin/env python3
"""
Test script to verify graph algorithm integration
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_graph_algorithms_import():
    """Test that graph algorithms can be imported"""
    print("Testing graph algorithm imports...")
    try:
        from algorithms.graph.graph_bfs import graph_bfs, get_algorithm_info as bfs_info
        from algorithms.graph.graph_dfs import graph_dfs, get_algorithm_info as dfs_info
        print("✓ Graph algorithms imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import graph algorithms: {e}")
        return False

def test_graph_canvas_import():
    """Test that graph canvas can be imported"""
    print("\nTesting graph canvas import...")
    try:
        # This will fail on macOS < 13.0 due to PyQt6 requirements
        # But we can at least check the file exists
        canvas_path = os.path.join(os.path.dirname(__file__), 'src', 'gui', 'graph_canvas.py')
        if os.path.exists(canvas_path):
            print("✓ Graph canvas file exists")
            return True
        else:
            print("✗ Graph canvas file not found")
            return False
    except Exception as e:
        print(f"✗ Error checking graph canvas: {e}")
        return False

def test_algorithm_registry():
    """Test that graph algorithms are registered"""
    print("\nTesting algorithm registry...")
    try:
        from algorithms.algorithm_registry import get_algorithm, get_all_algorithms_in_category

        # Get graph algorithms
        graph_algos = get_all_algorithms_in_category("Graph Algorithms")
        print(f"  Available graph algorithms: {graph_algos}")

        # Test getting Graph BFS
        bfs_func, bfs_info = get_algorithm("Graph Algorithms", "Graph BFS")
        if bfs_func and bfs_info:
            print(f"  ✓ Graph BFS: {bfs_info['name']}")
            print(f"    Time complexity: {bfs_info['time_complexity']}")
            print(f"    Space complexity: {bfs_info['space_complexity']}")
        else:
            print("  ✗ Graph BFS not found in registry")
            return False

        # Test getting Graph DFS
        dfs_func, dfs_info = get_algorithm("Graph Algorithms", "Graph DFS")
        if dfs_func and dfs_info:
            print(f"  ✓ Graph DFS: {dfs_info['name']}")
            print(f"    Time complexity: {dfs_info['time_complexity']}")
            print(f"    Space complexity: {dfs_info['space_complexity']}")
        else:
            print("  ✗ Graph DFS not found in registry")
            return False

        print("✓ Algorithm registry test passed")
        return True
    except Exception as e:
        print(f"✗ Algorithm registry test failed: {e}")
        return False

def test_graph_algorithm_execution():
    """Test that graph algorithms can execute"""
    print("\nTesting graph algorithm execution...")
    try:
        from algorithms.graph.graph_bfs import graph_bfs
        from algorithms.graph.graph_dfs import graph_dfs

        # Test array
        test_array = [5, 3, 8, 1, 9, 2]

        # Test BFS
        print("  Testing BFS execution...")
        bfs_gen = graph_bfs(test_array)
        step_count = 0
        for state in bfs_gen:
            step_count += 1
            if step_count == 1:  # Check first state
                if 'action' in state and 'nodes' in state and 'edges' in state:
                    print(f"    ✓ BFS yields valid state: action={state['action']}, nodes={len(state['nodes'])}, edges={len(state['edges'])}")
                else:
                    print(f"    ✗ BFS first state missing required fields")
                    return False
        print(f"    ✓ BFS completed in {step_count} steps")

        # Test DFS
        print("  Testing DFS execution...")
        dfs_gen = graph_dfs(test_array)
        step_count = 0
        for state in dfs_gen:
            step_count += 1
            if step_count == 1:  # Check first state
                if 'action' in state and 'nodes' in state and 'edges' in state:
                    print(f"    ✓ DFS yields valid state: action={state['action']}, nodes={len(state['nodes'])}, edges={len(state['edges'])}")
                else:
                    print(f"    ✗ DFS first state missing required fields")
                    return False
        print(f"    ✓ DFS completed in {step_count} steps")

        print("✓ Graph algorithm execution test passed")
        return True
    except Exception as e:
        print(f"✗ Graph algorithm execution test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_graph_canvas_interface():
    """Test that graph canvas has required methods"""
    print("\nTesting graph canvas interface...")
    try:
        # Read the graph_canvas.py file to check for required methods
        canvas_path = os.path.join(os.path.dirname(__file__), 'src', 'gui', 'graph_canvas.py')
        with open(canvas_path, 'r') as f:
            content = f.read()

        required_methods = ['def set_state', 'def update_state', 'def reset', 'def set_array']
        for method in required_methods:
            if method in content:
                print(f"  ✓ {method}() found")
            else:
                print(f"  ✗ {method}() not found")
                return False

        print("✓ Graph canvas interface test passed")
        return True
    except Exception as e:
        print(f"✗ Graph canvas interface test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Graph Algorithm Integration Test")
    print("=" * 60)

    results = []
    results.append(("Import Test", test_graph_algorithms_import()))
    results.append(("Canvas File Test", test_graph_canvas_import()))
    results.append(("Registry Test", test_algorithm_registry()))
    results.append(("Execution Test", test_graph_algorithm_execution()))
    results.append(("Canvas Interface Test", test_graph_canvas_interface()))

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:30} {status}")

    all_passed = all(result for _, result in results)
    print("=" * 60)
    if all_passed:
        print("All tests passed! ✓")
    else:
        print("Some tests failed. ✗")
    print("=" * 60)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
