"""
Test that all grid-based algorithms use the same grid
"""
import sys
sys.path.insert(0, 'src')

from algorithms.graph.graph_dfs import graph_dfs
from algorithms.graph.graph_bfs import graph_bfs
from algorithms.graph.dijkstra_grid import dijkstra_grid
from algorithms.graph.astar_grid import astar_grid


def get_initial_grid(algorithm_func, arr):
    """Get the initial grid from an algorithm"""
    gen = algorithm_func(arr)
    first_state = next(gen)
    return first_state['grid'], first_state['start'], first_state['end']


def test_grid_consistency():
    """Test that all algorithms generate the same grid for the same input"""
    test_size = [20]  # 20x20 grid

    print("Testing grid consistency across algorithms...")
    print(f"Grid size: {test_size[0]}x{test_size[0]}\n")

    # Get grids from each algorithm
    dfs_grid, dfs_start, dfs_end = get_initial_grid(graph_dfs, test_size)
    bfs_grid, bfs_start, bfs_end = get_initial_grid(graph_bfs, test_size)
    dijkstra_grid_data, dijkstra_start, dijkstra_end = get_initial_grid(dijkstra_grid, test_size)
    astar_grid_data, astar_start, astar_end = get_initial_grid(astar_grid, test_size)

    # Check if grids are identical
    grids_match = (dfs_grid == bfs_grid == dijkstra_grid_data == astar_grid_data)
    starts_match = (dfs_start == bfs_start == dijkstra_start == astar_start)
    ends_match = (dfs_end == bfs_end == dijkstra_end == astar_end)

    print(f"[OK] Grids match: {grids_match}")
    print(f"[OK] Start positions match: {starts_match} - {dfs_start}")
    print(f"[OK] End positions match: {ends_match} - {dfs_end}")

    if grids_match and starts_match and ends_match:
        print("\n[SUCCESS] All algorithms use the same grid!")
        print(f"Grid dimensions: {len(dfs_grid)}x{len(dfs_grid[0])}")

        # Count walls
        wall_count = sum(sum(row) for row in dfs_grid)
        total_cells = len(dfs_grid) * len(dfs_grid[0])
        print(f"Walls: {wall_count}/{total_cells} ({wall_count/total_cells*100:.1f}%)")
    else:
        print("\n[FAILED] Grids don't match!")
        if not grids_match:
            print("  - Grid layouts are different")
        if not starts_match:
            print(f"  - Start positions differ: DFS={dfs_start}, BFS={bfs_start}, Dijkstra={dijkstra_start}, A*={astar_start}")
        if not ends_match:
            print(f"  - End positions differ: DFS={dfs_end}, BFS={bfs_end}, Dijkstra={dijkstra_end}, A*={astar_end}")

    return grids_match and starts_match and ends_match


if __name__ == "__main__":
    test_grid_consistency()
