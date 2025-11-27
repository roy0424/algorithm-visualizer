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
        self.grid = []
        self.start = None
        self.end = None
        self.visited = set()
        self.current = None
        self.path = []
        self.description = ""
        self.stack_queue_state = None  # For DFS/BFS visualization

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
        self.start = None
        self.end = None
        self.visited = set()
        self.current = None
        self.path = []
        self.description = ""
        self.stack_queue_state = None
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

        # Extract grid structure
        self.grid = state.get('grid', [])
        self.start = state.get('start', None)
        self.end = state.get('end', None)

        # Extract visualization state
        self.visited = set(state.get('visited', []))
        self.current = state.get('current', None)
        self.path = state.get('path', [])
        self.description = state.get('description', '')

        # Extract stack/queue state if available
        self.stack_queue_state = state.get('stack_queue', None)

        self.update()

    def paintEvent(self, event):
        """Draw the 2D grid"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.grid:
            self._draw_empty_state(painter)
            return

        # Draw grid
        self._draw_grid(painter)

        # Draw stack/queue state (for DFS/BFS)
        if self.stack_queue_state:
            self._draw_stack_queue(painter)

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

        # Draw title
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        painter.setPen(QPen(self.TEXT_COLOR))
        title = "Stack:" if data_structure_type == 'stack' else "Queue:"
        painter.drawText(box_x, box_y, title)

        # Draw container box
        box_y += 25
        container_height = max(100, len(items) * item_height + padding * 2)

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
            # Draw each item
            for i, item in enumerate(items):
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
                if i == 0:
                    painter.setPen(QPen(QColor(255, 69, 0), 2))
                    arrow_text = "← Top" if data_structure_type == 'stack' else "← Front"
                    painter.drawText(
                        box_x - 50,
                        item_y + item_height // 2 + 5,
                        arrow_text
                    )

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
