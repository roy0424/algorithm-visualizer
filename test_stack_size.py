"""
Test stack/queue size during DFS/BFS execution
"""
import sys
sys.path.insert(0, 'src')

from algorithms.graph.graph_dfs import graph_dfs
from algorithms.graph.graph_bfs import graph_bfs


def test_stack_queue_sizes():
    """Test maximum stack/queue sizes during algorithm execution"""
    test_sizes = [20, 30, 50]

    for size in test_sizes:
        print(f"\n{'='*60}")
        print(f"Testing with {size}x{size} grid")
        print(f"{'='*60}")

        # Test DFS
        print("\nDFS (Stack):")
        dfs_gen = graph_dfs([size])
        max_stack_size = 0
        for state in dfs_gen:
            stack_state = state.get('stack_queue')
            if stack_state:
                items = stack_state.get('items', [])
                max_stack_size = max(max_stack_size, len(items))

        print(f"  Max stack size: {max_stack_size}")
        if max_stack_size > 6:
            print(f"  -> Will show 6 items + '{max_stack_size - 6} more'")
        else:
            print(f"  -> Will show all {max_stack_size} items")

        # Test BFS
        print("\nBFS (Queue):")
        bfs_gen = graph_bfs([size])
        max_queue_size = 0
        for state in bfs_gen:
            queue_state = state.get('stack_queue')
            if queue_state:
                items = queue_state.get('items', [])
                max_queue_size = max(max_queue_size, len(items))

        print(f"  Max queue size: {max_queue_size}")
        if max_queue_size > 6:
            print(f"  -> Will show 6 items + '{max_queue_size - 6} more'")
        else:
            print(f"  -> Will show all {max_queue_size} items")

    print(f"\n{'='*60}")
    print("Summary:")
    print("- Max display limit: 6 items")
    print("- Overflow shown as: '... +N more'")
    print("- This prevents UI overflow on large grids")
    print(f"{'='*60}")


if __name__ == "__main__":
    test_stack_queue_sizes()
