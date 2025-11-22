"""
Tree Visualization Canvas for DFS/BFS algorithms
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
import math


class TreeCanvas(QWidget):
    """Canvas for visualizing tree-based algorithms (DFS, BFS)"""

    def __init__(self):
        super().__init__()
        self.array = []
        self.current_state = None
        self.visited_indices = []
        self.current_index = None
        self.path = []

        # Color scheme
        self.default_color = QColor(100, 149, 237)  # Cornflower blue
        self.visiting_color = QColor(255, 215, 0)   # Gold
        self.visited_color = QColor(50, 205, 50)    # Lime green
        self.current_color = QColor(220, 20, 60)    # Crimson

        self.setMinimumHeight(500)

    def set_array(self, array):
        """Set the array to visualize as a tree"""
        self.array = array.copy()
        self.visited_indices = []
        self.current_index = None
        self.path = []
        self.update()

    def set_state(self, state):
        """Update visualization based on tree traversal state"""
        self.current_state = state
        self.array = state['array'].copy()

        action = state['action']

        if action == 'visit':
            self.current_index = state['indices'][0] if state['indices'] else None
            if self.current_index is not None and self.current_index not in self.visited_indices:
                self.visited_indices.append(self.current_index)
        elif action == 'done':
            self.current_index = None

        self.update()

    def reset(self):
        """Reset the visualization"""
        self.array = []
        self.current_state = None
        self.visited_indices = []
        self.current_index = None
        self.path = []
        self.update()

    def paintEvent(self, event):
        """Draw the tree visualization"""
        if not self.array:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        n = len(self.array)

        # Draw title
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        title = "Tree Traversal"
        if self.current_state:
            title += f" - {self.current_state.get('action', '').upper()}"
        painter.drawText(QRectF(20, 10, width - 40, 30), Qt.AlignmentFlag.AlignLeft, title)

        # Calculate tree layout
        levels = math.ceil(math.log2(n + 1)) if n > 0 else 1
        level_height = (height - 100) / (levels + 1)
        node_radius = min(25, level_height / 3)

        # Draw tree nodes and edges
        self.draw_tree(painter, 0, width // 2, 60, width // 2, level_height, node_radius)

        # Draw legend
        self.draw_legend(painter, width, height)

        # Draw traversal order
        if self.visited_indices:
            self.draw_traversal_order(painter, width, height)

    def draw_tree(self, painter, index, x, y, x_offset, level_height, node_radius):
        """Recursively draw tree nodes and edges"""
        if index >= len(self.array):
            return

        # Draw edges to children first (so they appear behind nodes)
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        if left_child < len(self.array):
            child_x = x - x_offset / 2
            child_y = y + level_height
            painter.setPen(QPen(Qt.GlobalColor.gray, 2))
            painter.drawLine(QPointF(x, y + node_radius), QPointF(child_x, child_y - node_radius))
            self.draw_tree(painter, left_child, child_x, child_y, x_offset / 2, level_height, node_radius)

        if right_child < len(self.array):
            child_x = x + x_offset / 2
            child_y = y + level_height
            painter.setPen(QPen(Qt.GlobalColor.gray, 2))
            painter.drawLine(QPointF(x, y + node_radius), QPointF(child_x, child_y - node_radius))
            self.draw_tree(painter, right_child, child_x, child_y, x_offset / 2, level_height, node_radius)

        # Draw current node
        if index == self.current_index:
            color = self.current_color
        elif index in self.visited_indices:
            color = self.visited_color
        else:
            color = self.default_color

        # Draw circle
        painter.setBrush(color)
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawEllipse(QPointF(x, y), node_radius, node_radius)

        # Draw value
        painter.setPen(QPen(Qt.GlobalColor.white if index in self.visited_indices or index == self.current_index else Qt.GlobalColor.black, 1))
        painter.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        painter.drawText(
            QRectF(x - node_radius, y - node_radius, node_radius * 2, node_radius * 2),
            Qt.AlignmentFlag.AlignCenter,
            str(self.array[index])
        )

        # Draw index label below node
        painter.setPen(QPen(Qt.GlobalColor.gray, 1))
        painter.setFont(QFont('Arial', 8))
        painter.drawText(
            QRectF(x - node_radius, y + node_radius + 5, node_radius * 2, 15),
            Qt.AlignmentFlag.AlignCenter,
            f"[{index}]"
        )

    def draw_legend(self, painter, width, height):
        """Draw legend explaining colors"""
        legend_y = height - 35
        legend_items = [
            (self.default_color, 'Not Visited'),
            (self.current_color, 'Current'),
            (self.visited_color, 'Visited')
        ]

        x_offset = 40
        for color, label in legend_items:
            # Draw color box
            painter.fillRect(QRectF(x_offset, legend_y, 20, 15), color)
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            painter.drawRect(QRectF(x_offset, legend_y, 20, 15))

            # Draw label
            painter.setFont(QFont('Arial', 9))
            painter.drawText(
                QRectF(x_offset + 25, legend_y, 100, 15),
                Qt.AlignmentFlag.AlignVCenter,
                label
            )

            x_offset += 125

    def draw_traversal_order(self, painter, width, height):
        """Draw the order of traversal"""
        painter.setFont(QFont('Arial', 10))
        painter.setPen(QPen(Qt.GlobalColor.black, 1))

        order_text = "Traversal Order: " + " → ".join(str(self.array[i]) for i in self.visited_indices[:15])
        if len(self.visited_indices) > 15:
            order_text += "..."

        painter.drawText(
            QRectF(40, height - 60, width - 80, 25),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            order_text
        )
