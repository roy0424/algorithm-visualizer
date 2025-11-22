"""
Visualization Canvas for displaying algorithm execution
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont


class VisualizationCanvas(QWidget):
    """Canvas for visualizing sorting algorithms with bar charts"""

    def __init__(self):
        super().__init__()
        self.array = []
        self.highlighted_indices = []  # Indices being compared
        self.swapped_indices = []      # Indices that were swapped
        self.sorted_indices = []        # Indices that are sorted
        self.action = None
        self.target_value = None        # For search algorithms

        # Color scheme
        self.default_color = QColor(100, 149, 237)  # Cornflower blue
        self.compare_color = QColor(255, 215, 0)    # Gold
        self.swap_color = QColor(220, 20, 60)       # Crimson
        self.sorted_color = QColor(50, 205, 50)     # Lime green
        self.found_color = QColor(147, 112, 219)    # Medium purple
        self.pivot_color = QColor(255, 140, 0)      # Dark orange

        self.setMinimumHeight(400)

    def set_array(self, array):
        """Set the array to visualize"""
        self.array = array.copy()
        self.update()

    def set_state(self, state):
        """
        Update visualization based on algorithm state

        Args:
            state: Dictionary from algorithm generator containing:
                - action: Type of action
                - indices: Indices involved
                - array: Current array state
                - target: (optional) Target value for search algorithms
        """
        self.array = state['array'].copy()
        self.action = state['action']
        self.target_value = state.get('target', None)

        # Reset highlights
        self.highlighted_indices = []
        self.swapped_indices = []

        # Handle different actions
        action = state['action']

        if action in ['compare', 'mark_key', 'mark_position', 'range', 'search_left', 'search_right']:
            self.highlighted_indices = state['indices']
        elif action in ['swap', 'shift']:
            self.swapped_indices = state['indices']
        elif action in ['sorted', 'insert', 'pivot_placed', 'found']:
            self.sorted_indices.extend(state['indices'])
        elif action in ['done', 'not_found']:
            if action == 'done' and state['indices']:
                self.sorted_indices = state['indices']
        elif action in ['divide', 'merge', 'pivot', 'partition_start']:
            self.highlighted_indices = state['indices']

        self.update()

    def reset(self):
        """Reset the visualization"""
        self.array = []
        self.highlighted_indices = []
        self.swapped_indices = []
        self.sorted_indices = []
        self.action = None
        self.target_value = None
        self.update()

    def paintEvent(self, event):
        """Draw the visualization"""
        if not self.array:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate dimensions
        width = self.width()
        height = self.height()
        n = len(self.array)
        max_value = max(self.array) if self.array else 1

        # Bar dimensions
        bar_width = (width - 40) / n  # Padding of 20 on each side
        max_bar_height = height - 100  # Leave space for labels

        # Draw target indicator if searching
        if self.target_value is not None:
            self.draw_target_indicator(painter, width, height, self.target_value)

        # Draw bars
        for i, value in enumerate(self.array):
            # Calculate bar position and size
            x = 20 + i * bar_width
            bar_height = (value / max_value) * max_bar_height
            y = height - 60 - bar_height  # 60 pixels from bottom for labels

            # Determine bar color based on action
            if self.action == 'pivot' and i in self.highlighted_indices:
                color = self.pivot_color
            elif self.action == 'found' and i in self.sorted_indices:
                color = self.found_color
            elif i in self.sorted_indices:
                color = self.sorted_color
            elif i in self.swapped_indices:
                color = self.swap_color
            elif i in self.highlighted_indices:
                color = self.compare_color
            else:
                color = self.default_color

            # Draw bar
            painter.fillRect(QRectF(x + 2, y, bar_width - 4, bar_height), color)

            # Draw border (thicker for target match)
            if self.target_value is not None and value == self.target_value:
                painter.setPen(QPen(Qt.GlobalColor.red, 3))
            else:
                painter.setPen(QPen(Qt.GlobalColor.black, 1))
            painter.drawRect(QRectF(x + 2, y, bar_width - 4, bar_height))

            # Draw value label
            if n <= 30:  # Only show labels if not too many bars
                painter.setFont(QFont('Arial', 8 if n > 20 else 10))
                painter.setPen(QPen(Qt.GlobalColor.black, 1))
                painter.drawText(
                    QRectF(x, height - 50, bar_width, 20),
                    Qt.AlignmentFlag.AlignCenter,
                    str(value)
                )

                # Draw index label
                painter.setFont(QFont('Arial', 7 if n > 20 else 9))
                painter.setPen(QPen(Qt.GlobalColor.gray, 1))
                painter.drawText(
                    QRectF(x, height - 30, bar_width, 20),
                    Qt.AlignmentFlag.AlignCenter,
                    str(i)
                )

        # Draw legend
        self.draw_legend(painter, width, height)

    def draw_target_indicator(self, painter, width, height, target):
        """Draw an indicator showing the target value being searched"""
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        painter.setPen(QPen(Qt.GlobalColor.red, 2))
        text = f"Searching for: {target}"
        painter.drawText(QRectF(width - 200, 10, 180, 30), Qt.AlignmentFlag.AlignCenter, text)

    def draw_legend(self, painter, width, height):
        """Draw legend explaining colors"""
        legend_y = 10
        legend_items = [
            (self.default_color, 'Unsorted'),
            (self.compare_color, 'Comparing'),
            (self.swap_color, 'Swapping'),
            (self.sorted_color, 'Sorted')
        ]

        x_offset = 20
        for color, label in legend_items:
            # Draw color box
            painter.fillRect(QRectF(x_offset, legend_y, 20, 15), color)
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            painter.drawRect(QRectF(x_offset, legend_y, 20, 15))

            # Draw label
            painter.setFont(QFont('Arial', 9))
            painter.drawText(
                QRectF(x_offset + 25, legend_y, 80, 15),
                Qt.AlignmentFlag.AlignVCenter,
                label
            )

            x_offset += 105
