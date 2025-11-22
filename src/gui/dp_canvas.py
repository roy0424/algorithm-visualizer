"""
Dynamic Programming Table Visualization Canvas
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont


class DPCanvas(QWidget):
    """Canvas for visualizing DP table-based algorithms"""

    def __init__(self):
        super().__init__()
        self.dp_table = []
        self.current_state = None
        self.current_cell = None
        self.problem_name = ""

        # Color scheme
        self.default_color = QColor(240, 240, 240)  # Light gray
        self.current_color = QColor(255, 215, 0)    # Gold
        self.computed_color = QColor(144, 238, 144) # Light green
        self.result_color = QColor(100, 149, 237)   # Cornflower blue

        self.setMinimumHeight(400)

    def set_array(self, array):
        """Initialize for DP problem"""
        self.dp_table = []
        self.current_cell = None
        self.update()

    def set_state(self, state):
        """Update visualization based on DP state"""
        self.current_state = state

        if 'dp_table' in state:
            self.dp_table = [row[:] for row in state['dp_table']]  # Deep copy

        if 'current_cell' in state:
            self.current_cell = state['current_cell']

        if 'problem' in state:
            self.problem_name = state['problem']

        self.update()

    def reset(self):
        """Reset the visualization"""
        self.dp_table = []
        self.current_state = None
        self.current_cell = None
        self.problem_name = ""
        self.update()

    def paintEvent(self, event):
        """Draw the DP table"""
        if not self.dp_table:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        # Draw title
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        title = f"Dynamic Programming - {self.problem_name}"
        painter.drawText(QRectF(20, 10, width - 40, 30), Qt.AlignmentFlag.AlignLeft, title)

        # Calculate table dimensions
        rows = len(self.dp_table)
        cols = len(self.dp_table[0]) if rows > 0 else 0

        if rows == 0 or cols == 0:
            return

        # Calculate cell size
        table_width = width - 100
        table_height = height - 120
        cell_width = min(table_width / cols, 80)
        cell_height = min(table_height / rows, 60)

        start_x = 50
        start_y = 60

        # Draw table
        for i in range(rows):
            for j in range(cols):
                x = start_x + j * cell_width
                y = start_y + i * cell_height

                # Determine cell color
                if self.current_cell and self.current_cell == (i, j):
                    color = self.current_color
                elif self.current_state and self.current_state.get('action') == 'done' and i == rows - 1 and j == cols - 1:
                    color = self.result_color
                elif self.dp_table[i][j] is not None and self.dp_table[i][j] != 0:
                    color = self.computed_color
                else:
                    color = self.default_color

                # Draw cell
                painter.fillRect(QRectF(x, y, cell_width, cell_height), color)
                painter.setPen(QPen(Qt.GlobalColor.black, 1))
                painter.drawRect(QRectF(x, y, cell_width, cell_height))

                # Draw value
                value = self.dp_table[i][j]
                if value is not None:
                    painter.setFont(QFont('Arial', 10, QFont.Weight.Bold))
                    painter.drawText(
                        QRectF(x, y, cell_width, cell_height),
                        Qt.AlignmentFlag.AlignCenter,
                        str(value)
                    )

                # Draw indices
                if i == 0 or j == 0:
                    painter.setFont(QFont('Arial', 7))
                    painter.setPen(QPen(Qt.GlobalColor.gray, 1))
                    painter.drawText(
                        QRectF(x + 2, y + 2, 20, 15),
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                        f"[{i},{j}]"
                    )
                    painter.setPen(QPen(Qt.GlobalColor.black, 1))

        # Draw description
        if self.current_state and 'description' in self.current_state:
            painter.setFont(QFont('Arial', 10))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            painter.drawText(
                QRectF(50, height - 50, width - 100, 40),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                self.current_state['description']
            )

        # Draw legend
        self.draw_legend(painter, width, height)

    def draw_legend(self, painter, width, height):
        """Draw legend"""
        legend_y = height - 35
        legend_items = [
            (self.default_color, 'Empty'),
            (self.current_color, 'Computing'),
            (self.computed_color, 'Computed'),
            (self.result_color, 'Result')
        ]

        x_offset = 50
        for color, label in legend_items:
            painter.fillRect(QRectF(x_offset, legend_y, 20, 15), color)
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            painter.drawRect(QRectF(x_offset, legend_y, 20, 15))

            painter.setFont(QFont('Arial', 9))
            painter.drawText(
                QRectF(x_offset + 25, legend_y, 80, 15),
                Qt.AlignmentFlag.AlignVCenter,
                label
            )

            x_offset += 105
