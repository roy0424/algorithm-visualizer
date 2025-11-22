"""
Quick test script to verify all algorithms can be imported and run
"""
import sys
sys.path.insert(0, 'src')

from algorithms.algorithm_registry import ALGORITHMS

def test_all_algorithms():
    """Test that all algorithms can be initialized"""
    print("Testing Algorithm Visualizer - All Algorithms\n")
    print("=" * 60)

    total_algorithms = 0
    successful = 0
    failed = []

    for category, algorithms in ALGORITHMS.items():
        print(f"\n{category}:")
        print("-" * 60)

        for name, algo_data in algorithms.items():
            total_algorithms += 1
            try:
                # Get the function and info
                func = algo_data['function']
                info = algo_data['info']

                # Try to initialize the generator
                test_array = [5, 2, 8, 1, 9]
                gen = func(test_array)

                # Get first state
                first_state = next(gen)

                print(f"  [OK] {name:30} - {info['time_complexity']}")
                successful += 1

            except Exception as e:
                print(f"  [FAIL] {name:30} - ERROR: {str(e)}")
                failed.append((category, name, str(e)))

    print("\n" + "=" * 60)
    print(f"\nResults:")
    print(f"  Total: {total_algorithms}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {len(failed)}")

    if failed:
        print(f"\nFailed algorithms:")
        for cat, name, error in failed:
            print(f"  - {cat} > {name}: {error}")
        return False
    else:
        print(f"\n[SUCCESS] All {total_algorithms} algorithms working correctly!")
        return True

if __name__ == "__main__":
    success = test_all_algorithms()
    sys.exit(0 if success else 1)
