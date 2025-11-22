"""
Specialized Visualization Canvas for Merge Sort
Shows the divide and conquer process with multiple levels
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
import math


class MergeSortCanvas(QWidget):
    """Canvas for visualizing merge sort with divide-and-conquer visualization"""

    def __init__(self):
        super().__init__()
        self.array = []
        self.current_state = None
        self.merge_levels = []  # Store different levels of division
        self.current_level = 0
        self.highlighted_range = []

        # Color scheme
        self.default_color = QColor(100, 149, 237)  # Cornflower blue
        self.divide_color = QColor(255, 215, 0)     # Gold
        self.merge_color = QColor(220, 20, 60)      # Crimson
        self.sorted_color = QColor(50, 205, 50)     # Lime green
        self.compare_color = QColor(255, 140, 0)    # Dark orange

        self.setMinimumHeight(500)

    def set_array(self, array):
        """Set the array to visualize"""
        self.array = array.copy()
        self.merge_levels = []
        self.current_level = 0
        self.highlighted_range = []
        self.update()

    def set_state(self, state):
        """Update visualization based on merge sort state"""
        self.current_state = state
        self.array = state['array'].copy()

        action = state['action']

        if action == 'divide':
            # Show the range being divided
            self.highlighted_range = state['indices']
        elif action in ['merge', 'compare']:
            self.highlighted_range = state['indices']
        elif action == 'done':
            self.highlighted_range = []

        self.update()

    def reset(self):
        """Reset the visualization"""
        self.array = []
        self.current_state = None
        self.merge_levels = []
        self.current_level = 0
        self.highlighted_range = []
        self.update()

    def paintEvent(self, event):
        """Draw the merge sort visualization"""
        if not self.array:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        n = len(self.array)
        max_value = max(self.array) if self.array else 1

        # Draw title
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawText(QRectF(20, 10, width - 40, 30), Qt.AlignmentFlag.AlignLeft, "Merge Sort - Divide and Conquer")

        # Calculate dimensions for main array
        bar_width = (width - 80) / n
        max_bar_height = (height - 100) / 2  # Use half height for main array
        y_start = 60

        # Draw main array with highlights
        for i, value in enumerate(self.array):
            x = 40 + i * bar_width
            bar_height = (value / max_value) * max_bar_height
            y = y_start + max_bar_height - bar_height

            # Determine color
            if self.current_state:
                action = self.current_state.get('action', '')
                if action == 'divide' and i in self.highlighted_range:
                    color = self.divide_color
                elif action == 'merge' and i in self.highlighted_range:
                    color = self.merge_color
                elif action == 'compare' and i in self.highlighted_range:
                    color = self.compare_color
                elif action == 'done':
                    color = self.sorted_color
                else:
                    color = self.default_color
            else:
                color = self.default_color

            # Draw bar
            painter.fillRect(QRectF(x + 1, y, bar_width - 2, bar_height), color)
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            painter.drawRect(QRectF(x + 1, y, bar_width - 2, bar_height))

            # Draw value
            if n <= 25:
                painter.setFont(QFont('Arial', 8 if n > 15 else 10))
                painter.setPen(QPen(Qt.GlobalColor.black, 1))
                painter.drawText(
                    QRectF(x, y + bar_height + 5, bar_width, 20),
                    Qt.AlignmentFlag.AlignCenter,
                    str(value)
                )

        # Draw level indicator and action description
        y_info = y_start + max_bar_height + 40
        if self.current_state:
            action = self.current_state.get('action', '')
            painter.setFont(QFont('Arial', 10))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))

            if action == 'divide':
                desc = f"Dividing: Processing range {self.highlighted_range[0]}-{self.highlighted_range[-1]}"
            elif action == 'merge':
                desc = f"Merging: Combining sorted subarrays"
            elif action == 'compare':
                desc = f"Comparing: Selecting smaller element"
            elif action == 'done':
                desc = "Merge Sort Complete!"
            else:
                desc = f"Action: {action}"

            painter.drawText(QRectF(40, y_info, width - 80, 30), Qt.AlignmentFlag.AlignLeft, desc)

        # Draw legend
        self.draw_legend(painter, width, height)

    def draw_legend(self, painter, width, height):
        """Draw legend explaining colors"""
        legend_y = height - 35
        legend_items = [
            (self.default_color, 'Unsorted'),
            (self.divide_color, 'Dividing'),
            (self.compare_color, 'Comparing'),
            (self.merge_color, 'Merging'),
            (self.sorted_color, 'Completed')
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
                QRectF(x_offset + 25, legend_y, 80, 15),
                Qt.AlignmentFlag.AlignVCenter,
                label
            )

            x_offset += 105
