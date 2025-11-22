"""
Graph Breadth-First Search (BFS)
"""
from collections import deque


def graph_bfs(arr, target=None):
    """
    Breadth-First Search on a graph

    Time Complexity: O(V + E)
    Space Complexity: O(V)

    Args:
        arr: Array to generate graph from
        target: Target node to search for (optional)

    Yields:
        Dictionary containing visualization state
    """
    if not arr:
        return

    # Generate graph from array
    nodes, edges, adj_list = _generate_graph(arr)

    if not nodes:
        return

    start_node = nodes[0]

    # Initial state
    yield {
        'action': 'start',
        'nodes': nodes,
        'edges': edges,
        'visited': [],
        'current_node': None,
        'highlighted_edges': [],
        'path_edges': [],
        'description': f'Starting BFS from node {start_node}',
        'line': 0
    }

    # BFS using queue
    queue = deque([start_node])
    visited = set([start_node])
    visited_order = []

    while queue:
        # Dequeue
        current = queue.popleft()
        visited_order.append(current)

        # Show current node being visited
        yield {
            'action': 'visit',
            'nodes': nodes,
            'edges': edges,
            'visited': list(visited),
            'current_node': current,
            'highlighted_edges': [],
            'path_edges': [],
            'description': f'Visiting node {current} (Queue: {list(queue)})',
            'line': 1
        }

        # Explore neighbors
        neighbors = sorted(adj_list.get(current, []))

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)

                # Highlight edge being explored
                yield {
                    'action': 'explore',
                    'nodes': nodes,
                    'edges': edges,
                    'visited': list(visited),
                    'current_node': current,
                    'highlighted_edges': [(current, neighbor)],
                    'path_edges': [],
                    'description': f'Exploring edge ({current}, {neighbor})',
                    'line': 2
                }

                queue.append(neighbor)

    # Done
    yield {
        'action': 'done',
        'nodes': nodes,
        'edges': edges,
        'visited': list(visited),
        'current_node': None,
        'highlighted_edges': [],
        'path_edges': [],
        'description': f'BFS complete. Visited order: {visited_order}',
        'line': 4
    }


def _generate_graph(arr):
    """
    Generate a graph from an array

    Args:
        arr: Input array

    Returns:
        Tuple of (nodes, edges, adjacency_list)
    """
    # Get unique nodes (limit to 8 for visualization)
    nodes = sorted(list(set(arr)))[:8]

    if len(nodes) < 2:
        return nodes, [], {}

    # Generate edges (connect consecutive elements in original array)
    edges = []
    adj_list = {node: [] for node in nodes}

    # Connect based on original array order
    for i in range(len(arr) - 1):
        if arr[i] in nodes and arr[i+1] in nodes:
            u, v = arr[i], arr[i+1]
            weight = abs(u - v)

            # Add edge (undirected)
            if (u, v, weight) not in edges and (v, u, weight) not in edges:
                edges.append((u, v, weight))
                adj_list[u].append(v)
                adj_list[v].append(u)

    # Ensure graph is connected by adding extra edges if needed
    if len(edges) < len(nodes) - 1:
        for i in range(len(nodes) - 1):
            u, v = nodes[i], nodes[i+1]
            weight = abs(u - v)
            if v not in adj_list[u]:
                edges.append((u, v, weight))
                adj_list[u].append(v)
                adj_list[v].append(u)

    return nodes, edges, adj_list


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': 'Graph BFS',
        'category': 'Graph Algorithms',
        'time_complexity': 'O(V + E)',
        'space_complexity': 'O(V)',
        'description': 'Breadth-first search traversal of a graph using a queue.',
        'code': '''def bfs(graph, start):
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited'''
    }
