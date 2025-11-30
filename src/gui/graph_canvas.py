"""
Graph Canvas - Visualization for graph algorithms
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
import math


class GraphCanvas(QWidget):
    """Canvas for visualizing graph algorithms (DFS, BFS, Dijkstra, MST, etc.)"""

    def __init__(self):
        super().__init__()
        # Grid mode (for DFS/BFS)
        self.grid = []

        # Node-edge mode (for Dijkstra/A*)
        self.nodes = []
        self.edges = []
        self.node_positions = {}
        self.node_scale = 1.0

        # Common attributes
        self.start = None
        self.end = None
        self.visited = set()
        self.current = None
        self.path = []
        self.description = ""
        self.stack_queue_state = None  # For DFS/BFS visualization
        self.stats = None  # For Dijkstra/A* statistics
        self.highlighted_edges = []  # For edge highlighting

        # Colors
        self.CELL_EMPTY = QColor(255, 255, 255)    # White
        self.CELL_WALL = QColor(40, 40, 40)        # Dark gray
        self.CELL_START = QColor(70, 130, 180)     # Steel blue
        self.CELL_END = QColor(220, 20, 60)        # Crimson
        self.CELL_VISITED = QColor(144, 238, 144)  # Light green
        self.CELL_CURRENT = QColor(255, 165, 0)    # Orange
        self.CELL_PATH = QColor(255, 215, 0)       # Gold
        self.GRID_LINE = QColor(200, 200, 200)     # Light gray
        self.TEXT_COLOR = QColor(0, 0, 0)          # Black

    def reset(self):
        """Reset the canvas to empty state"""
        self.grid = []
        self.nodes = []
        self.edges = []
        self.node_positions = {}
        self.node_scale = 1.0
        self.start = None
        self.end = None
        self.visited = set()
        self.current = None
        self.path = []
        self.description = ""
        self.stack_queue_state = None
        self.stats = None
        self.highlighted_edges = []
        self.update()

    def set_array(self, arr):
        """Set array (not used for graph canvas, but needed for interface compatibility)"""
        # Graph algorithms generate their own graph structure from the array
        # So we just reset here
        self.reset()

    def set_state(self, state):
        """Update visualization state from algorithm generator (main interface)"""
        self.update_state(state)

    def update_state(self, state):
        """Update visualization state from algorithm generator"""
        if state is None:
            return

        # Extract grid structure (for DFS/BFS)
        self.grid = state.get('grid', [])

        # Extract node-edge structure (for Dijkstra/A*)
        self.nodes = state.get('nodes', [])
        self.edges = state.get('edges', [])
        self.node_scale = state.get('node_scale', 1.0)

        # Calculate node positions if nodes are present
        if self.nodes:
            self._calculate_node_positions()

        # Extract common attributes
        self.start = state.get('start', None)
        self.end = state.get('end', None)

        # Extract visualization state
        self.visited = set(state.get('visited', []))
        self.current = state.get('current', None)
        self.path = state.get('path', [])
        self.description = state.get('description', '')
        self.highlighted_edges = state.get('highlighted_edges', [])

        # Extract stack/queue state if available
        self.stack_queue_state = state.get('stack_queue', None)

        # Extract statistics if available (for Dijkstra/A*)
        self.stats = state.get('stats', None)

        self.update()

    def resizeEvent(self, event):
        """Handle window resize - recalculate node positions"""
        super().resizeEvent(event)
        # Recalculate node positions if we have nodes
        if self.nodes:
            self._calculate_node_positions()
        self.update()

    def paintEvent(self, event):
        """Draw the visualization (grid or node-edge graph)"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.grid and not self.nodes:
            self._draw_empty_state(painter)
            return

        # Draw either grid or node-edge graph
        if self.grid:
            self._draw_grid(painter)
        elif self.nodes:
            self._draw_node_edge_graph(painter)

        # Draw stack/queue state (for DFS/BFS) or statistics (for Dijkstra/A*)
        if self.stack_queue_state:
            self._draw_stack_queue(painter)
        elif self.stats:
            self._draw_statistics(painter)

        # Draw description
        self._draw_description(painter)

    def _draw_grid(self, painter):
        """Draw the 2D grid"""
        if not self.grid:
            return

        rows = len(self.grid)
        cols = len(self.grid[0]) if rows > 0 else 0

        # Calculate cell size
        width = self.width()
        height = self.height() - 80  # Leave space for description

        cell_size = min(width // cols, height // rows)

        # Center the grid
        grid_width = cols * cell_size
        grid_height = rows * cell_size
        offset_x = (width - grid_width) // 2
        offset_y = (height - grid_height) // 2 + 20

        # Draw cells
        for i in range(rows):
            for j in range(cols):
                x = offset_x + j * cell_size
                y = offset_y + i * cell_size

                # Determine cell color
                cell_pos = (i, j)
                if cell_pos == self.start:
                    color = self.CELL_START
                elif cell_pos == self.end:
                    color = self.CELL_END
                elif cell_pos == self.current:
                    color = self.CELL_CURRENT
                elif cell_pos in self.path:
                    color = self.CELL_PATH
                elif cell_pos in self.visited:
                    color = self.CELL_VISITED
                elif self.grid[i][j] == 1:  # Wall
                    color = self.CELL_WALL
                else:  # Empty
                    color = self.CELL_EMPTY

                # Draw cell
                painter.fillRect(x, y, cell_size, cell_size, color)

                # Draw grid lines
                painter.setPen(QPen(self.GRID_LINE, 1))
                painter.drawRect(x, y, cell_size, cell_size)

    def _draw_stack_queue(self, painter):
        """Draw stack/queue state visualization"""
        if not self.stack_queue_state:
            return

        data_structure_type = self.stack_queue_state.get('type', 'stack')
        items = self.stack_queue_state.get('items', [])

        # Position in top-right corner
        box_width = 150
        box_x = self.width() - box_width - 20
        box_y = 20
        item_height = 35
        padding = 10
        max_display_items = 6  # Maximum items to show

        # Draw title
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        painter.setPen(QPen(self.TEXT_COLOR))
        title = "Stack:" if data_structure_type == 'stack' else "Queue:"
        painter.drawText(box_x, box_y, title)

        # Draw container box
        box_y += 25
        # Calculate height based on visible items + overflow indicator
        visible_count = min(len(items), max_display_items)
        extra_height = 30 if len(items) > max_display_items else 0
        container_height = max(100, visible_count * item_height + padding * 2 + extra_height)

        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.setBrush(QColor(245, 245, 245, 200))
        painter.drawRect(box_x, box_y, box_width, container_height)

        # Draw items
        painter.setFont(QFont('Arial', 11))

        if not items:
            # Empty message
            painter.setPen(QPen(QColor(150, 150, 150)))
            painter.drawText(
                box_x + padding,
                box_y + container_height // 2,
                "Empty"
            )
        else:
            # For stack, display in reverse order (top at the top)
            # For queue, display in normal order (front at the top)
            display_items = list(reversed(items)) if data_structure_type == 'stack' else items

            # Limit items to display
            items_to_show = display_items[:max_display_items]
            remaining_count = len(display_items) - max_display_items

            # Draw each visible item
            for i, item in enumerate(items_to_show):
                item_y = box_y + padding + i * item_height

                # Item box
                painter.setPen(QPen(QColor(70, 130, 180), 2))
                painter.setBrush(QColor(173, 216, 230))
                painter.drawRect(
                    box_x + padding,
                    item_y,
                    box_width - padding * 2,
                    item_height - 5
                )

                # Item text
                painter.setPen(QPen(QColor(0, 0, 0)))
                text = str(item)
                metrics = painter.fontMetrics()
                text_width = metrics.horizontalAdvance(text)
                text_height = metrics.height()

                painter.drawText(
                    box_x + padding + (box_width - padding * 2 - text_width) // 2,
                    item_y + (item_height - 5 + text_height) // 2,
                    text
                )

                # Arrow indicator for stack top or queue front
                # First item in display is always top/front
                if i == 0:
                    painter.setPen(QPen(QColor(255, 69, 0), 2))
                    arrow_text = "Top ->" if data_structure_type == 'stack' else "Front ->"
                    painter.drawText(
                        box_x - 50,
                        item_y + item_height // 2 + 5,
                        arrow_text
                    )

            # Draw overflow indicator if there are more items
            if remaining_count > 0:
                overflow_y = box_y + padding + len(items_to_show) * item_height + 5

                painter.setFont(QFont('Arial', 10))
                painter.setPen(QPen(QColor(100, 100, 100)))

                overflow_text = f"... +{remaining_count} more"
                metrics = painter.fontMetrics()
                text_width = metrics.horizontalAdvance(overflow_text)

                painter.drawText(
                    box_x + (box_width - text_width) // 2,
                    overflow_y + 15,
                    overflow_text
                )

    def _calculate_node_positions(self):
        """Calculate positions for nodes in a layered (neural network style) layout"""
        if not self.nodes:
            return

        # Determine which nodes are in which layer based on node metadata
        # Assume nodes are structured as: layer_id, node_in_layer_id
        # Or use simple grouping if that's not available

        # Group nodes by layer (assume layer info is in node structure)
        layers = {}
        for node in self.nodes:
            # If node is tuple/list, first element is layer
            if isinstance(node, (tuple, list)):
                layer_id = node[0]
                if layer_id not in layers:
                    layers[layer_id] = []
                layers[layer_id].append(node)
            else:
                # Fallback: distribute nodes evenly across layers
                # For now, use simple numeric grouping
                layer_id = node // 3  # Group every 3 nodes
                if layer_id not in layers:
                    layers[layer_id] = []
                layers[layer_id].append(node)

        # Calculate layout area (leave room for stats panel/description)
        width = self.width() - 250
        top_margin = 60
        bottom_margin = 120
        available_height = max(200, self.height() - top_margin - bottom_margin)

        num_layers = len(layers)
        if num_layers == 0:
            return

        # X spacing for layers (left to right) - wider spacing
        x_spacing = int(width * 1.2 // (num_layers + 1))

        # Position each layer
        for layer_idx, (layer_id, nodes_in_layer) in enumerate(sorted(layers.items())):
            x = 80 + layer_idx * x_spacing

            # Y spacing for nodes in this layer (top to bottom)
            num_nodes = len(nodes_in_layer)
            if num_nodes == 1:
                y_positions = [top_margin + available_height // 2]
            else:
                y_positions = [
                    top_margin + int((idx + 1) * available_height / (num_nodes + 1))
                    for idx in range(num_nodes)
                ]

            # Sort nodes for consistent positioning
            nodes_in_layer.sort()

            for node_idx, node in enumerate(nodes_in_layer):
                y = y_positions[node_idx]
                self.node_positions[node] = (x, y)

    def _draw_node_edge_graph(self, painter):
        """Draw node-edge graph with weights"""
        if not self.nodes:
            return

        # Draw edges first (so they appear behind nodes)
        self._draw_edges(painter)

        # Draw nodes
        self._draw_nodes(painter)

    def _draw_edges(self, painter):
        """Draw edges with weights using curves to avoid overlap"""
        from PyQt6.QtGui import QPainterPath

        # Group edges by source-target pair to calculate curve offset
        edge_counts = {}
        for edge in self.edges:
            if len(edge) >= 2:
                node1, node2 = edge[0], edge[1]
                key = tuple(sorted([node1, node2]))
                edge_counts[key] = edge_counts.get(key, 0) + 1

        edge_index = {}

        for edge in self.edges:
            if len(edge) == 3:
                node1, node2, weight = edge
            else:
                node1, node2 = edge
                weight = 1

            if node1 not in self.node_positions or node2 not in self.node_positions:
                continue

            x1, y1 = self.node_positions[node1]
            x2, y2 = self.node_positions[node2]

            # Calculate curve offset for parallel edges
            key = tuple(sorted([node1, node2]))
            if key not in edge_index:
                edge_index[key] = 0
            idx = edge_index[key]
            edge_index[key] += 1

            # Curve control point offset
            curve_offset = 0
            if edge_counts[key] > 1:
                # Multiple edges between same nodes - add curve
                curve_offset = (idx - edge_counts[key] / 2) * 30

            # Check if this edge is highlighted or in path
            is_highlighted = (node1, node2) in self.highlighted_edges or (node2, node1) in self.highlighted_edges
            is_in_path = False

            # Check if edge is in path
            if self.path:
                for i in range(len(self.path) - 1):
                    if ((self.path[i] == node1 and self.path[i+1] == node2) or
                        (self.path[i] == node2 and self.path[i+1] == node1)):
                        is_in_path = True
                        break

            # Set pen based on edge state
            if is_in_path:
                painter.setPen(QPen(QColor(255, 215, 0), 5))  # Gold for path
            elif is_highlighted:
                painter.setPen(QPen(QColor(255, 165, 0), 4))  # Orange for highlighted
            else:
                painter.setPen(QPen(QColor(150, 150, 150), 2))  # Light gray for normal

            # Draw curved edge
            path = QPainterPath()
            path.moveTo(x1, y1)

            # Calculate control point for quadratic curve
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            # Perpendicular offset for curve
            dx = x2 - x1
            dy = y2 - y1
            length = (dx**2 + dy**2)**0.5
            if length > 0:
                # Perpendicular direction
                perp_x = -dy / length
                perp_y = dx / length

                # Control point
                ctrl_x = mid_x + perp_x * curve_offset
                ctrl_y = mid_y + perp_y * curve_offset

                path.quadTo(ctrl_x, ctrl_y, x2, y2)
            else:
                path.lineTo(x2, y2)

            painter.drawPath(path)

            # Draw weight label near the midpoint; spread labels if edges are parallel
            if length > 0:
                label_offset = 0
                if edge_counts[key] > 1:
                    label_offset = (idx - (edge_counts[key] - 1) / 2) * 0.08
                t = min(0.75, max(0.25, 0.5 + label_offset))
                label_x = (1-t)**2 * x1 + 2*(1-t)*t * ctrl_x + t**2 * x2
                label_y = (1-t)**2 * y1 + 2*(1-t)*t * ctrl_y + t**2 * y2

                # Nudge label perpendicular to the edge to avoid overlap
                if edge_counts[key] > 1:
                    label_perp_offset = (idx - (edge_counts[key] - 1) / 2) * 12
                    label_x += perp_x * label_perp_offset
                    label_y += perp_y * label_perp_offset
            else:
                label_x = mid_x
                label_y = mid_y

            # Background for weight
            font_size = max(8, int(11 * self.node_scale))
            painter.setFont(QFont('Arial', font_size, QFont.Weight.Bold))
            if is_in_path:
                painter.setPen(QPen(QColor(200, 100, 0)))
            else:
                painter.setPen(QPen(QColor(0, 0, 0)))

            text = str(int(weight))
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(text)
            text_height = metrics.height()

            # Background sized to text
            pad_x = max(8, int(10 * self.node_scale))
            pad_y = max(6, int(8 * self.node_scale))
            bg_width = text_width + pad_x
            bg_height = text_height + pad_y

            painter.setBrush(QColor(255, 255, 255, 240))
            painter.setPen(QPen(QColor(100, 100, 100), 1))
            painter.drawRoundedRect(
                int(label_x - bg_width / 2),
                int(label_y - bg_height / 2),
                int(bg_width),
                int(bg_height),
                6, 6
            )

            painter.drawText(int(label_x - text_width // 2), int(label_y + text_height // 3), text)

    def _draw_nodes(self, painter):
        """Draw nodes"""
        for node in self.nodes:
            if node not in self.node_positions:
                continue

            x, y = self.node_positions[node]
            radius = max(12, int(25 * self.node_scale))

            # Determine node color
            if node == self.start:
                color = QColor(34, 139, 34)  # Green for start
            elif node == self.end:
                color = QColor(220, 20, 60)  # Red for end
            elif node == self.current:
                color = QColor(255, 165, 0)  # Orange for current
            elif node in self.visited:
                color = QColor(135, 206, 250)  # Light blue for visited
            else:
                color = QColor(200, 200, 200)  # Gray for unvisited

            # Draw node circle
            painter.setBrush(color)
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

            # Draw node label
            font_size = max(8, int(10 * self.node_scale))
            painter.setFont(QFont('Arial', font_size, QFont.Weight.Bold))
            painter.setPen(QPen(QColor(0, 0, 0) if node not in [self.start, self.end] else QColor(255, 255, 255)))

            # Format node text
            if isinstance(node, (tuple, list)):
                # For layered nodes (layer, id), just show the id within layer
                if node == self.start:
                    text = "S"
                elif node == self.end:
                    text = "G"
                else:
                    text = str(node[1])
            else:
                text = str(node)

            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(text)
            text_height = metrics.height()
            painter.drawText(x - text_width // 2, y + text_height // 3, text)

    def _draw_statistics(self, painter):
        """Draw statistics panel for Dijkstra/A*"""
        if not self.stats:
            return

        # Position in top-right corner
        panel_x = self.width() - 230
        panel_y = 20
        panel_width = 210

        # Background
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.setBrush(QColor(245, 245, 245, 230))
        painter.drawRect(panel_x, panel_y, panel_width, 150)

        # Title
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.drawText(panel_x + 10, panel_y + 25, "Statistics")

        # Stats
        painter.setFont(QFont('Arial', 10))
        y_offset = panel_y + 55
        line_height = 30

        nodes_visited = self.stats.get('nodes_visited', 0)
        total_weight = self.stats.get('path_length', 0)

        stats_text = [
            f"Nodes Visited: {nodes_visited}",
            f"Total Weight: {total_weight}",
        ]

        for i, text in enumerate(stats_text):
            painter.drawText(panel_x + 15, y_offset + i * line_height, text)


    def _draw_description(self, painter):
        """Draw description text"""
        if self.description:
            painter.setFont(QFont('Arial', 10))
            painter.setPen(QPen(self.TEXT_COLOR))
            painter.drawText(10, self.height() - 10, self.description)

    def _draw_empty_state(self, painter):
        """Draw message when no grid is loaded"""
        painter.setPen(QPen(QColor(128, 128, 128)))
        painter.setFont(QFont('Arial', 12))
        text = "No grid loaded. Generate data to visualize pathfinding algorithms."
        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(text)
        painter.drawText(
            int(self.width()/2 - text_width/2),
            int(self.height()/2),
            text
        )
