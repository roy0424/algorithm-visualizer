"""
A* Pathfinding Algorithm on Weighted Graph
"""
import heapq
from algorithms.graph.dijkstra_weighted import _generate_weighted_graph


def astar_weighted(arr, target=None):
    """
    A* algorithm for finding shortest path in a weighted graph

    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)
    """
    if not arr:
        return

    nodes, edges, adj_list, start, goal, node_scale = _generate_weighted_graph(arr)
    if not nodes:
        return

    g_score = {node: float('inf') for node in nodes}
    g_score[start] = 0

    f_score = {node: float('inf') for node in nodes}
    f_score[start] = _heuristic(start, goal, nodes)

    pq = [(f_score[start], start)]
    visited = set()
    parent = {}

    # Initial state
    yield {
        'action': 'start',
        'nodes': nodes,
        'edges': edges,
        'start': start,
        'end': goal,
        'visited': [],
        'current': None,
        'highlighted_edges': [],
        'path': [],
        'description': f"A*: Starting from node {start} to {goal} (with heuristic)",
        'stats': {'nodes_visited': 0, 'path_length': 0, 'steps': 0, 'total_cost': 0},
        'node_scale': node_scale,
        'step': 0,
        'line': 0  # def astar...
    }

    step = 0

    while pq:
        yield {
            'action': 'loop',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': None,
            'highlighted_edges': [],
            'path': [],
            'description': "A*: Next iteration",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': 0
            },
            'node_scale': node_scale,
            'step': step,
            'line': 8  # while pq:
        }

        current_f, current = heapq.heappop(pq)

        yield {
            'action': 'pop',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': current,
            'highlighted_edges': [],
            'path': [],
            'description': f"A*: Pop {current} with f={current_f:.1f}",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': 0
            },
            'node_scale': node_scale,
            'step': step,
            'line': 9  # heapq.heappop(pq)
        }

        yield {
            'action': 'check_visit',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': current,
            'highlighted_edges': [],
            'path': [],
            'description': f"A*: Checking if {current} already visited",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': 0
            },
            'node_scale': node_scale,
            'step': step,
            'line': 10  # if node in visited
        }

        if current in visited:
            yield {
                'action': 'skip_visited',
                'nodes': nodes,
                'edges': edges,
                'start': start,
                'end': goal,
                'visited': list(visited),
                'current': current,
                'highlighted_edges': [],
                'path': [],
                'description': f"A*: {current} already visited, skipping",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': 0,
                    'steps': step,
                    'total_cost': 0
                },
                'node_scale': node_scale,
                'step': step,
                'line': 11  # continue
            }
            continue

        yield {
            'action': 'check_goal',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': current,
            'highlighted_edges': [],
            'path': [],
            'description': f"A*: Is {current} the goal?",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': 0
            },
            'node_scale': node_scale,
            'step': step,
            'line': 12  # if node == goal
        }

        if current == goal:
            path = []
            node = goal
            while node in parent:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()

            path_edges = []
            for i in range(len(path) - 1):
                path_edges.append((path[i], path[i+1]))

            yield {
                'action': 'done',
                'nodes': nodes,
                'edges': edges,
                'start': start,
                'end': goal,
                'visited': list(visited),
                'current': goal,
                'highlighted_edges': path_edges,
                'path': path,
                'description': f"A*: Goal reached! Cost: {int(g_score[goal])}, Nodes visited: {len(visited)} ⭐",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': int(g_score[goal]),
                    'steps': step,
                    'total_cost': int(g_score[goal])
                },
                'node_scale': node_scale,
                'step': step,
                'line': 12
            }
            return

        visited.add(current)
        step += 1

        h_value = _heuristic(current, goal, nodes)
        g_value = g_score[current]

        yield {
            'action': 'visit',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': current,
            'highlighted_edges': [],
            'path': [],
            'description': f"A*: Visiting node {current} (g={g_value:.0f}, h={h_value:.0f}, f={current_f:.0f})",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': int(g_value)
            },
            'node_scale': node_scale,
            'step': step,
            'line': 14  # visited.add(node)
        }

        yield {
            'action': 'neighbors',
            'nodes': nodes,
            'edges': edges,
            'start': start,
            'end': goal,
            'visited': list(visited),
            'current': current,
            'highlighted_edges': [],
            'path': [],
            'description': f"A*: Exploring neighbors of {current}",
            'stats': {
                'nodes_visited': len(visited),
                'path_length': 0,
                'steps': step,
                'total_cost': 0
            },
            'node_scale': node_scale,
            'step': step,
            'line': 16  # for neighbor
        }

        for neighbor, weight in adj_list.get(current, []):
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + weight

            h_temp = _heuristic(neighbor, goal, nodes)
            yield {
                'action': 'compute',
                'nodes': nodes,
                'edges': edges,
                'start': start,
                'end': goal,
                'visited': list(visited),
                'current': current,
                'highlighted_edges': [(current, neighbor)],
                'path': [],
                'description': f"A*: Compute g for {neighbor}: {g_score[current]:.0f} + {weight} = {tentative_g:.0f}, h={h_temp:.0f}",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': 0,
                    'steps': step,
                    'total_cost': 0
                },
                'node_scale': node_scale,
                'step': step,
                'line': 17  # tentative_g calculation
            }

            h = _heuristic(neighbor, goal, nodes)
            yield {
                'action': 'relax',
                'nodes': nodes,
                'edges': edges,
                'start': start,
                'end': goal,
                'visited': list(visited),
                'current': current,
                'highlighted_edges': [(current, neighbor)],
                'path': [],
                'description': f"A*: Checking ({current}, {neighbor}): g={tentative_g:.0f}, h={h:.0f}, f={tentative_g+h:.0f}",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': 0,
                    'steps': step,
                    'total_cost': 0
                },
                'node_scale': node_scale,
                'step': step,
                'line': 16  # for neighbor, weight in graph[node]
            }

            yield {
                'action': 'check_better',
                'nodes': nodes,
                'edges': edges,
                'start': start,
                'end': goal,
                'visited': list(visited),
                'current': current,
                'highlighted_edges': [(current, neighbor)],
                'path': [],
                'description': f"A*: Is {tentative_g:.0f} < g({neighbor})?",
                'stats': {
                    'nodes_visited': len(visited),
                    'path_length': 0,
                    'steps': step,
                    'total_cost': 0
                },
                'node_scale': node_scale,
                'step': step,
                'line': 18  # if tentative_g < g_score[neighbor]
            }

            if tentative_g < g_score[neighbor]:
                yield {
                    'action': 'compare_update',
                    'nodes': nodes,
                    'edges': edges,
                    'start': start,
                    'end': goal,
                    'visited': list(visited),
                    'current': current,
                    'highlighted_edges': [(current, neighbor)],
                    'path': [],
                    'description': f"A*: Updating {neighbor} with g={tentative_g:.0f}, f={tentative_g + h:.0f}",
                    'stats': {
                        'nodes_visited': len(visited),
                        'path_length': 0,
                        'steps': step,
                        'total_cost': 0
                    },
                    'node_scale': node_scale,
                    'step': step,
                    'line': 19  # g_score update block
                }

                g_score[neighbor] = tentative_g
                h = _heuristic(neighbor, goal, nodes)
                f_score[neighbor] = tentative_g + h
                parent[neighbor] = current

                yield {
                    'action': 'update_scores',
                    'nodes': nodes,
                    'edges': edges,
                    'start': start,
                    'end': goal,
                    'visited': list(visited),
                    'current': current,
                    'highlighted_edges': [(current, neighbor)],
                    'path': [],
                    'description': f"A*: Set g({neighbor})={tentative_g:.0f}, f={f_score[neighbor]:.0f}",
                    'stats': {
                        'nodes_visited': len(visited),
                        'path_length': 0,
                        'steps': step,
                        'total_cost': 0
                    },
                    'node_scale': node_scale,
                    'step': step,
                    'line': 20  # f_score update
                }

                heapq.heappush(pq, (f_score[neighbor], neighbor))

                yield {
                    'action': 'push_queue',
                    'nodes': nodes,
                    'edges': edges,
                    'start': start,
                    'end': goal,
                    'visited': list(visited),
                    'current': current,
                    'highlighted_edges': [(current, neighbor)],
                    'path': [],
                    'description': f"A*: Push {neighbor} with f={f_score[neighbor]:.0f} to queue",
                    'stats': {
                        'nodes_visited': len(visited),
                        'path_length': 0,
                        'steps': step,
                        'total_cost': 0
                    },
                    'node_scale': node_scale,
                    'step': step,
                    'line': 21  # heapq.heappush
                }

    # No path found
    yield {
        'action': 'done',
        'nodes': nodes,
        'edges': edges,
        'start': start,
        'end': goal,
        'visited': list(visited),
        'current': None,
        'highlighted_edges': [],
        'path': [],
        'description': f"A*: No path found. Nodes visited: {len(visited)}",
        'stats': {
            'nodes_visited': len(visited),
            'path_length': 0,
            'steps': step,
            'total_cost': 0
        },
        'node_scale': node_scale,
        'step': step,
        'line': 20  # return float('inf')
    }


def _heuristic(node, goal, nodes):
    """
    Heuristic function for A* - estimate distance to goal
    For layered graph, use layer distance as heuristic

    Args:
        node: Current node (layer_id, node_id)
        goal: Goal node (layer_id, node_id)
        nodes: List of all nodes

    Returns:
        Estimated cost from node to goal
    """
    if isinstance(node, (tuple, list)) and isinstance(goal, (tuple, list)):
        current_layer = node[0]
        goal_layer = goal[0]
        layer_distance = abs(goal_layer - current_layer)
        return layer_distance * 3
    else:
        return 0


def get_algorithm_info():
    """Return algorithm metadata"""
    return {
        'name': "A* Algorithm",
        'category': 'Graph Algorithms',
        'time_complexity': 'O((V + E) log V)',
        'space_complexity': 'O(V)',
        'description': 'Finds shortest weighted path using heuristic (f=g+h). More efficient than Dijkstra!',
        'code': '''def astar(graph, start, goal, heuristic):
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)
    pq = [(f_score[start], start)]
    visited = set()

    while pq:
        _, node = heapq.heappop(pq)
        if node in visited:
            continue
        if node == goal:
            return g_score[goal]
        visited.add(node)

        for neighbor, weight in graph[node]:
            tentative_g = g_score[node] + weight
            if tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_score[neighbor], neighbor))

    return float('inf')'''
    }
