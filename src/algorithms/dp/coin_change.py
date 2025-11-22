"""
Coin Change Problem using Dynamic Programming
"""


def coin_change(arr, target=None):
    """
    Coin Change Problem - Minimum coins needed

    Time Complexity: O(n * amount)
    Space Complexity: O(amount)

    Args:
        arr: Coin denominations
        target: Target amount (if None, uses sum(arr)//2)

    Yields:
        Dictionary containing visualization state
    """
    if not arr:
        return

    coins = sorted(set(arr))  # Remove duplicates and sort
    coins = coins[:6]  # Limit to 6 coin types
    amount = target if target is not None else sum(arr) // 2
    amount = max(1, min(amount, 50))  # Limit amount

    # Initialize DP table (2D for visualization)
    # Row 0: amount values, Row 1: min coins needed
    dp = [[i for i in range(amount + 1)],
          [float('inf')] * (amount + 1)]
    dp[1][0] = 0

    # Initial state
    yield {
        'action': 'start',
        'indices': [],
        'array': arr.copy(),
        'dp_table': [row[:] for row in dp],
        'current_cell': None,
        'problem': 'Coin Change',
        'description': f'Coins: {coins}, Target: {amount}',
        'line': 0
    }

    # Build table
    for coin in coins:
        for amt in range(coin, amount + 1):
            # Show current computation
            yield {
                'action': 'compute',
                'indices': [coins.index(coin)] if coins.index(coin) < len(arr) else [],
                'array': arr.copy(),
                'dp_table': [row[:] for row in dp],
                'current_cell': (1, amt),
                'problem': 'Coin Change',
                'description': f'Using coin {coin} for amount {amt}',
                'line': 2
            }

            if dp[1][amt - coin] != float('inf'):
                dp[1][amt] = min(dp[1][amt], dp[1][amt - coin] + 1)

            # Show computed value
            result = dp[1][amt] if dp[1][amt] != float('inf') else 'inf'
            yield {
                'action': 'computed',
                'indices': [],
                'array': arr.copy(),
                'dp_table': [row[:] for row in dp],
                'current_cell': (1, amt),
                'problem': 'Coin Change',
                'description': f'Min coins for {amt}: {result}',
                'line': 3
            }

    # Done
    result = dp[1][amount] if dp[1][amount] != float('inf') else 'Impossible'
    yield {
        'action': 'done',
        'indices': [],
        'array': arr.copy(),
        'dp_table': [row[:] for row in dp],
        'current_cell': (1, amount),
        'problem': 'Coin Change',
        'description': f'Minimum coins for {amount}: {result}',
        'line': 5
    }


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Coin Change',
        'category': 'Dynamic Programming',
        'time_complexity': 'O(n × amount)',
        'space_complexity': 'O(amount)',
        'description': 'Find minimum number of coins needed to make a given amount.',
        'code': '''def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1'''
    }
