"""
Test stack display order
"""
import sys
sys.path.insert(0, 'src')

from algorithms.graph.graph_dfs import graph_dfs


def test_stack_display():
    """Test that stack displays items in correct order"""
    print("Testing DFS stack display order...")
    print("Expected: Top of stack should be the last item added\n")

    # Generate DFS
    arr = [10]  # Small 10x10 grid
    gen = graph_dfs(arr)

    # Get first few states
    for i, state in enumerate(gen):
        if i > 5:  # Just check first few steps
            break

        stack_state = state.get('stack_queue')
        if stack_state and stack_state.get('items'):
            items = stack_state['items']
            print(f"Step {i}: Stack = {items}")
            print(f"  -> Last added (should be Top): {items[-1]}")
            print(f"  -> First added (should be Bottom): {items[0]}")

            # In Python list used as stack:
            # - append() adds to end (items[-1])
            # - pop() removes from end (items[-1])
            # So items[-1] is the TOP of the stack

            if len(items) > 1:
                print(f"  -> Stack visualization should show {items[-1]} at TOP")
                print(f"  -> Stack visualization should show {items[0]} at BOTTOM")
            print()

    print("Verification:")
    print("- In the GUI, the TOPMOST box in the stack should show items[-1]")
    print("- In the GUI, the BOTTOMMOST box in the stack should show items[0]")
    print("- The '← Top' arrow should point to items[-1]")


if __name__ == "__main__":
    test_stack_display()
