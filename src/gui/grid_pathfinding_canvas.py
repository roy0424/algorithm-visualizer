"""
Grid Pathfinding Canvas - Enhanced visualization for comparing pathfinding algorithms
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush
import math


class GridPathfindingCanvas(QWidget):
    """Enhanced canvas for visualizing grid-based pathfinding algorithms with comparison features"""

    def __init__(self):
        super().__init__()
        self.grid = []
        self.start = None
        self.end = None
        self.visited = set()
        self.current = None
        self.path = []
        self.description = ""
        self.visit_order = {}  # Maps (row, col) -> visit order number
        self.stats = {
            'nodes_visited': 0,
            'path_length': 0,
            'steps': 0
        }

        # Colors
        self.CELL_EMPTY = QColor(255, 255, 255)    # White
        self.CELL_WALL = QColor(40, 40, 40)        # Dark gray
        self.CELL_START = QColor(34, 139, 34)      # Forest green
        self.CELL_END = QColor(220, 20, 60)        # Crimson
        self.CELL_VISITED = QColor(135, 206, 250)  # Light sky blue
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
        self.visit_order = {}
        self.stats = {
            'nodes_visited': 0,
            'path_length': 0,
            'steps': 0
        }
        self.update()

    def set_array(self, arr):
        """Set array (not used for grid canvas, but needed for interface compatibility)"""
        self.reset()

    def set_state(self, state):
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

        # Extract visit order
        self.visit_order = state.get('visit_order', {})

        # Extract statistics
        self.stats = state.get('stats', {
            'nodes_visited': len(self.visited),
            'path_length': len(self.path),
            'steps': state.get('step', 0)
        })

        self.update()

    def paintEvent(self, event):
        """Draw the 2D grid with enhanced visualization"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.grid:
            self._draw_empty_state(painter)
            return

        # Draw grid
        self._draw_grid(painter)

        # Draw statistics panel
        self._draw_statistics(painter)

        # Draw description
        self._draw_description(painter)

        # Draw legend
        self._draw_legend(painter)

    def _draw_grid(self, painter):
        """Draw the 2D grid with visit order numbers"""
        if not self.grid:
            return

        rows = len(self.grid)
        cols = len(self.grid[0]) if rows > 0 else 0

        # Calculate cell size (leave space for stats panel on the right)
        available_width = self.width() - 250  # Reserve 250px for stats
        height = self.height() - 120  # Leave space for description and legend

        # Calculate optimal cell size
        cell_size = min(available_width // cols, height // rows)

        # Dynamic clamping based on grid size
        if rows <= 20:
            cell_size = max(20, min(cell_size, 50))  # Larger cells for small grids
        elif rows <= 50:
            cell_size = max(10, min(cell_size, 30))  # Medium cells
        else:
            cell_size = max(5, min(cell_size, 15))   # Smaller cells for large grids

        # Center the grid
        grid_width = cols * cell_size
        grid_height = rows * cell_size
        offset_x = (available_width - grid_width) // 2
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
                    # Gradient based on visit order
                    if cell_pos in self.visit_order:
                        order = self.visit_order[cell_pos]
                        max_order = max(self.visit_order.values()) if self.visit_order else 1
                        # Gradient from light blue to darker blue
                        intensity = int(250 - (order / max_order) * 100)
                        color = QColor(135, 206, max(150, intensity))
                    else:
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

                # Draw visit order number for visited cells (if cell is large enough)
                if cell_size >= 15 and cell_pos in self.visit_order and cell_pos not in self.path:
                    order = self.visit_order[cell_pos]
                    # Dynamic font size based on cell size
                    font_size = max(6, min(cell_size // 3, 12))
                    painter.setFont(QFont('Arial', font_size))
                    painter.setPen(QPen(QColor(50, 50, 50)))

                    text = str(order)
                    metrics = painter.fontMetrics()
                    text_width = metrics.horizontalAdvance(text)
                    text_height = metrics.height()

                    painter.drawText(
                        x + (cell_size - text_width) // 2,
                        y + (cell_size + text_height) // 2 - 2,
                        text
                    )

        # Draw start/end markers (only if cell is large enough)
        if cell_size >= 15:
            marker_font_size = max(8, min(cell_size // 2, 14))
            painter.setFont(QFont('Arial', marker_font_size, QFont.Weight.Bold))

            if self.start:
                i, j = self.start
                x = offset_x + j * cell_size
                y = offset_y + i * cell_size
                painter.setPen(QPen(QColor(255, 255, 255)))

                text = "S"
                metrics = painter.fontMetrics()
                text_width = metrics.horizontalAdvance(text)
                text_height = metrics.height()

                painter.drawText(
                    x + (cell_size - text_width) // 2,
                    y + (cell_size + text_height) // 2 - 2,
                    text
                )

            if self.end:
                i, j = self.end
                x = offset_x + j * cell_size
                y = offset_y + i * cell_size
                painter.setPen(QPen(QColor(255, 255, 255)))

                text = "G"
                metrics = painter.fontMetrics()
                text_width = metrics.horizontalAdvance(text)
                text_height = metrics.height()

                painter.drawText(
                    x + (cell_size - text_width) // 2,
                    y + (cell_size + text_height) // 2 - 2,
                    text
                )

    def _draw_statistics(self, painter):
        """Draw statistics panel on the right side"""
        # Position
        panel_x = self.width() - 230
        panel_y = 40
        panel_width = 210

        # Background
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.setBrush(QColor(245, 245, 245, 230))
        painter.drawRect(panel_x, panel_y, panel_width, 180)

        # Title
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.drawText(panel_x + 10, panel_y + 25, "📊 Statistics")

        # Stats
        painter.setFont(QFont('Arial', 10))
        y_offset = panel_y + 55
        line_height = 30

        stats_text = [
            f"Nodes Visited: {self.stats['nodes_visited']}",
            f"Path Length: {self.stats['path_length']}",
            f"Steps: {self.stats['steps']}"
        ]

        for i, text in enumerate(stats_text):
            painter.drawText(panel_x + 15, y_offset + i * line_height, text)

        # Efficiency metric
        if self.stats['nodes_visited'] > 0 and self.stats['path_length'] > 0:
            efficiency = (self.stats['path_length'] / self.stats['nodes_visited']) * 100
            painter.setFont(QFont('Arial', 9))
            painter.setPen(QPen(QColor(0, 100, 0)))
            painter.drawText(panel_x + 15, y_offset + 3 * line_height + 10,
                           f"Efficiency: {efficiency:.1f}%")

    def _draw_legend(self, painter):
        """Draw color legend"""
        legend_x = 10
        legend_y = self.height() - 90
        box_size = 20
        spacing = 10

        # Background
        painter.setBrush(QColor(250, 250, 250, 200))
        painter.setPen(QPen(QColor(150, 150, 150), 1))
        painter.drawRect(legend_x - 5, legend_y - 5, 600, 70)

        painter.setFont(QFont('Arial', 9))

        legend_items = [
            (self.CELL_START, "Start (S)"),
            (self.CELL_END, "Goal (G)"),
            (self.CELL_WALL, "Wall"),
            (self.CELL_VISITED, "Visited"),
            (self.CELL_CURRENT, "Current"),
            (self.CELL_PATH, "Path"),
        ]

        for i, (color, label) in enumerate(legend_items):
            x = legend_x + (i % 3) * 180
            y = legend_y + (i // 3) * 30

            # Color box
            painter.fillRect(x, y, box_size, box_size, color)
            painter.setPen(QPen(self.GRID_LINE, 1))
            painter.drawRect(x, y, box_size, box_size)

            # Label
            painter.setPen(QPen(self.TEXT_COLOR))
            painter.drawText(x + box_size + spacing, y + 15, label)

    def _draw_description(self, painter):
        """Draw description text"""
        if self.description:
            painter.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            painter.setPen(QPen(QColor(0, 0, 139)))
            painter.drawText(10, 20, self.description)

    def _draw_empty_state(self, painter):
        """Draw message when no grid is loaded"""
        painter.setPen(QPen(QColor(128, 128, 128)))
        painter.setFont(QFont('Arial', 12))
        text = "Select algorithm and grid size to start pathfinding visualization"
        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(text)
        painter.drawText(
            int(self.width()/2 - text_width/2),
            int(self.height()/2),
            text
        )
