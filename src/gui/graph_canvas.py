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
        self.nodes = []
        self.edges = []
        self.node_positions = {}
        self.visited_nodes = set()
        self.current_node = None
        self.highlighted_edges = set()
        self.path_edges = set()
        self.distances = {}
        self.description = ""

        # Colors
        self.NODE_DEFAULT = QColor(200, 200, 200)  # Light gray
        self.NODE_CURRENT = QColor(255, 69, 0)     # Red-orange
        self.NODE_VISITED = QColor(50, 205, 50)    # Green
        self.NODE_START = QColor(70, 130, 180)     # Steel blue
        self.NODE_TARGET = QColor(255, 140, 0)     # Dark orange
        self.EDGE_DEFAULT = QColor(150, 150, 150)  # Gray
        self.EDGE_HIGHLIGHT = QColor(255, 215, 0)  # Gold
        self.EDGE_PATH = QColor(255, 69, 0)        # Red
        self.TEXT_COLOR = QColor(0, 0, 0)          # Black

    def reset(self):
        """Reset the canvas to empty state"""
        self.nodes = []
        self.edges = []
        self.node_positions = {}
        self.visited_nodes = set()
        self.current_node = None
        self.highlighted_edges = set()
        self.path_edges = set()
        self.distances = {}
        self.description = ""
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

        # Extract graph structure
        self.nodes = state.get('nodes', [])
        self.edges = state.get('edges', [])

        # Extract visualization state
        self.visited_nodes = set(state.get('visited', []))
        self.current_node = state.get('current_node', None)
        self.highlighted_edges = set(state.get('highlighted_edges', []))
        self.path_edges = set(state.get('path_edges', []))
        self.distances = state.get('distances', {})
        self.description = state.get('description', '')

        # Calculate node positions (circular layout)
        self._calculate_positions()

        self.update()

    def _calculate_positions(self):
        """Calculate node positions in circular layout"""
        if not self.nodes:
            return

        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2

        # Calculate radius (leave margin)
        margin = 80
        radius = min(width, height) / 2 - margin

        n = len(self.nodes)
        for i, node in enumerate(self.nodes):
            angle = 2 * math.pi * i / n - math.pi / 2  # Start from top
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.node_positions[node] = (x, y)

    def paintEvent(self, event):
        """Draw the graph"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.nodes:
            self._draw_empty_state(painter)
            return

        # Draw edges first (so nodes appear on top)
        self._draw_edges(painter)

        # Draw nodes
        self._draw_nodes(painter)

        # Draw description
        self._draw_description(painter)

    def _draw_edges(self, painter):
        """Draw all edges"""
        for edge in self.edges:
            if len(edge) == 3:
                from_node, to_node, weight = edge
            else:
                from_node, to_node = edge
                weight = 1

            if from_node not in self.node_positions or to_node not in self.node_positions:
                continue

            x1, y1 = self.node_positions[from_node]
            x2, y2 = self.node_positions[to_node]

            # Determine edge color and width
            edge_tuple = (from_node, to_node)
            reverse_edge = (to_node, from_node)

            if edge_tuple in self.path_edges or reverse_edge in self.path_edges:
                color = self.EDGE_PATH
                width = 4
            elif edge_tuple in self.highlighted_edges or reverse_edge in self.highlighted_edges:
                color = self.EDGE_HIGHLIGHT
                width = 3
            else:
                color = self.EDGE_DEFAULT
                width = 2

            pen = QPen(color, width)
            painter.setPen(pen)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

            # Draw weight label
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            painter.setFont(QFont('Arial', 9))
            painter.setPen(QPen(self.TEXT_COLOR))

            # Background for weight text
            text = str(weight)
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(text)
            text_height = metrics.height()

            # Draw white background
            painter.fillRect(
                int(mid_x - text_width/2 - 2),
                int(mid_y - text_height/2),
                text_width + 4,
                text_height,
                QColor(255, 255, 255, 200)
            )

            painter.drawText(
                int(mid_x - text_width/2),
                int(mid_y + text_height/3),
                text
            )

    def _draw_nodes(self, painter):
        """Draw all nodes"""
        node_radius = 25

        for node in self.nodes:
            if node not in self.node_positions:
                continue

            x, y = self.node_positions[node]

            # Determine node color
            if node == self.current_node:
                color = self.NODE_CURRENT
            elif node in self.visited_nodes:
                color = self.NODE_VISITED
            elif node == self.nodes[0]:  # Start node
                color = self.NODE_START
            else:
                color = self.NODE_DEFAULT

            # Draw node circle
            painter.setBrush(color)
            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            painter.drawEllipse(
                int(x - node_radius),
                int(y - node_radius),
                node_radius * 2,
                node_radius * 2
            )

            # Draw node label
            painter.setFont(QFont('Arial', 11, QFont.Weight.Bold))
            painter.setPen(QPen(Qt.GlobalColor.white if node in self.visited_nodes or node == self.current_node else Qt.GlobalColor.black))

            text = str(node)
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(text)
            text_height = metrics.height()

            painter.drawText(
                int(x - text_width/2),
                int(y + text_height/3),
                text
            )

            # Draw distance label (for Dijkstra)
            if node in self.distances:
                dist = self.distances[node]
                dist_text = str(dist) if dist != float('inf') else '∞'

                painter.setFont(QFont('Arial', 9))
                painter.setPen(QPen(self.TEXT_COLOR))

                metrics = painter.fontMetrics()
                text_width = metrics.horizontalAdvance(dist_text)

                painter.drawText(
                    int(x - text_width/2),
                    int(y + node_radius + 15),
                    dist_text
                )

    def _draw_description(self, painter):
        """Draw description text"""
        if self.description:
            painter.setFont(QFont('Arial', 10))
            painter.setPen(QPen(self.TEXT_COLOR))
            painter.drawText(10, self.height() - 10, self.description)

    def _draw_empty_state(self, painter):
        """Draw message when no graph is loaded"""
        painter.setPen(QPen(QColor(128, 128, 128)))
        painter.setFont(QFont('Arial', 12))
        text = "No graph loaded. Generate data to visualize graph algorithms."
        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(text)
        painter.drawText(
            int(self.width()/2 - text_width/2),
            int(self.height()/2),
            text
        )

    def resizeEvent(self, event):
        """Recalculate positions on resize"""
        super().resizeEvent(event)
        self._calculate_positions()
