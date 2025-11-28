"""
Test 100x100 grid generation for graph algorithms
"""
import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from algorithms.graph.graph_dfs import graph_dfs
from algorithms.graph.graph_bfs import graph_bfs


def test_grid_size(size):
    """Test grid generation and algorithm execution for a given size"""
    print(f"\n{'='*60}")
    print(f"Testing {size}x{size} Grid")
    print(f"{'='*60}")

    test_array = [size]

    # Test DFS
    print(f"\n[1/2] Testing Graph DFS with {size}x{size} grid...")
    try:
        start_time = time.time()
        states = list(graph_dfs(test_array))
        elapsed = time.time() - start_time

        print(f"[OK] DFS completed successfully!")
        print(f"  - Total steps: {len(states)}")
        print(f"  - Time taken: {elapsed:.2f} seconds")
        print(f"  - Grid size: {len(states[0]['grid'])}x{len(states[0]['grid'][0])}")

        # Verify grid structure
        if states:
            grid = states[0]['grid']
            if len(grid) == size and len(grid[0]) == size:
                print(f"  - Grid dimensions verified: {size}x{size}")
            else:
                print(f"  - WARNING: Grid dimensions mismatch!")
                return False
    except Exception as e:
        print(f"[FAIL] DFS failed: {str(e)}")
        return False

    # Test BFS
    print(f"\n[2/2] Testing Graph BFS with {size}x{size} grid...")
    try:
        start_time = time.time()
        states = list(graph_bfs(test_array))
        elapsed = time.time() - start_time

        print(f"[OK] BFS completed successfully!")
        print(f"  - Total steps: {len(states)}")
        print(f"  - Time taken: {elapsed:.2f} seconds")
        print(f"  - Grid size: {len(states[0]['grid'])}x{len(states[0]['grid'][0])}")

        # Verify grid structure
        if states:
            grid = states[0]['grid']
            if len(grid) == size and len(grid[0]) == size:
                print(f"  - Grid dimensions verified: {size}x{size}")
            else:
                print(f"  - WARNING: Grid dimensions mismatch!")
                return False
    except Exception as e:
        print(f"[FAIL] BFS failed: {str(e)}")
        return False

    return True


def main():
    """Test multiple grid sizes including 100x100"""
    print("Grid Size Test Suite")
    print("Testing graph algorithms with various grid sizes")

    test_sizes = [10, 20, 50, 100]
    results = {}

    for size in test_sizes:
        results[size] = test_grid_size(size)

    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")

    all_passed = True
    for size, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{size}x{size} grid:".ljust(20) + status)
        if not passed:
            all_passed = False

    print(f"{'='*60}")
    if all_passed:
        print("[OK] All grid sizes tested successfully!")
        print("[OK] 100x100 grid support confirmed!")
    else:
        print("[FAIL] Some tests failed!")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
