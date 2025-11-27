"""
Kruskal's Minimum Spanning Tree Algorithm
"""


class UnionFind:
    """Union-Find (Disjoint Set Union) data structure"""

    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node):
        """Find root of node with path compression"""
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        """Union two sets by rank"""
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 == root2:
            return False

        # Union by rank
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1

        return True


def kruskal(arr, target=None):
    """
    Kruskal's algorithm for finding Minimum Spanning Tree

    Time Complexity: O(E log E)
    Space Complexity: O(V)

    Args:
        arr: Array to generate graph from
        target: Not used (for consistency)

    Yields:
        Dictionary containing visualization state
    """
    if not arr:
        return

    # Generate graph from array
    nodes, edges, adj_list = _generate_graph(arr)

    if not nodes or not edges:
        return

    # Initialize Union-Find
    uf = UnionFind(nodes)

    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda x: x[2])

    mst_edges = set()
    total_weight = 0

    # Initial state
    yield {
        'action': 'start',
        'nodes': nodes,
        'edges': edges,
        'visited': [],
        'current_node': None,
        'highlighted_edges': [],
        'path_edges': [],
        'description': f'Starting Kruskal. Sorted {len(sorted_edges)} edges by weight',
        'line': 0
    }

    # Process edges in order of weight
    for u, v, weight in sorted_edges:
        # Show edge being considered
        yield {
            'action': 'consider',
            'nodes': nodes,
            'edges': edges,
            'visited': [],
            'current_node': None,
            'highlighted_edges': [(u, v)],
            'path_edges': list(mst_edges),
            'description': f'Considering edge ({u}, {v}) with weight {weight}',
            'line': 1
        }

        # Check if adding edge creates cycle
        if uf.find(u) != uf.find(v):
            # Add edge to MST
            uf.union(u, v)
            mst_edges.add((u, v))
            total_weight += weight

            yield {
                'action': 'add_edge',
                'nodes': nodes,
                'edges': edges,
                'visited': [],
                'current_node': None,
                'highlighted_edges': [(u, v)],
                'path_edges': list(mst_edges),
                'description': f'Added edge ({u}, {v}) to MST. Total weight: {total_weight}',
                'line': 2
            }
        else:
            # Edge creates cycle, skip it
            yield {
                'action': 'skip',
                'nodes': nodes,
                'edges': edges,
                'visited': [],
                'current_node': None,
                'highlighted_edges': [(u, v)],
                'path_edges': list(mst_edges),
                'description': f'Skipped edge ({u}, {v}) - would create cycle',
                'line': 3
            }

        # Stop when MST is complete
        if len(mst_edges) == len(nodes) - 1:
            break

    # Done
    yield {
        'action': 'done',
        'nodes': nodes,
        'edges': edges,
        'visited': [],
        'current_node': None,
        'highlighted_edges': [],
        'path_edges': list(mst_edges),
        'description': f'Kruskal complete. MST weight: {total_weight}, Edges: {len(mst_edges)}',
        'line': 5
    }


def _generate_graph(arr):
    """
    Generate a tree from an array

    Args:
        arr: Input array

    Returns:
        Tuple of (nodes, edges, adjacency_list)
    """
    # Get unique nodes (limit to 10 for visualization)
    nodes = sorted(list(set(arr)))[:10]

    if len(nodes) < 2:
        return nodes, [], {}

    # Generate tree structure
    edges = []
    adj_list = {node: [] for node in nodes}

    # Create a balanced tree structure
    # First node is root, others are added as children in a breadth-first manner
    root = nodes[0]

    # For each node (except root), connect it to a parent
    for i in range(1, len(nodes)):
        # Parent is at index (i-1)//2 (binary tree structure)
        parent_idx = (i - 1) // 2
        parent = nodes[parent_idx]
        child = nodes[i]

        weight = abs(parent - child) % 10 + 1

        # Add edge (undirected for visualization)
        edges.append((parent, child, weight))
        adj_list[parent].append((child, weight))
        adj_list[child].append((parent, weight))

    return nodes, edges, adj_list


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': "Kruskal's Algorithm",
        'category': 'Graph Algorithms',
        'time_complexity': 'O(E log E)',
        'space_complexity': 'O(V)',
        'description': 'Finds the Minimum Spanning Tree by sorting edges and using Union-Find to detect cycles.',
        'code': '''def kruskal(edges, n):
    edges.sort(key=lambda x: x[2])  # Sort by weight
    uf = UnionFind(n)
    mst = []

    for u, v, weight in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.append((u, v, weight))

    return mst'''
    }
