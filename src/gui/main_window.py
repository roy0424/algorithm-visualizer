"""
Main Window for Algorithm Visualizer
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QSlider, QLabel, QSplitter, QInputDialog, QMessageBox,
    QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from PyQt6.Qsci import QsciScintilla, QsciLexerPython
import random
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.algorithm_registry import get_algorithm, get_all_algorithms_in_category
from gui.visualization_canvas import VisualizationCanvas
from gui.merge_sort_canvas import MergeSortCanvas
from gui.tree_canvas import TreeCanvas
from gui.dp_canvas import DPCanvas
from gui.graph_canvas import GraphCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Algorithm Visualizer")
        self.setGeometry(100, 100, 1400, 900)

        # Algorithm execution state
        self.current_algorithm = None
        self.algorithm_generator = None
        self.algorithm_info = None
        self.is_running = False
        self.current_array = []

        # Animation control
        self.timer = QTimer()
        self.timer.timeout.connect(self.execute_step)
        self.animation_delay = 500  # milliseconds

        self.setup_ui()
        self.generate_random_array()

    def setup_ui(self):
        """Set up the main user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Top control panel
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)

        # Splitter for code editor and visualization
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Code editor (left side)
        self.code_editor = self.create_code_editor()
        splitter.addWidget(self.code_editor)

        # Visualization area (right side)
        self.visualization_widget = self.create_visualization_area()
        splitter.addWidget(self.visualization_widget)

        # Set initial splitter sizes (30% code, 70% visualization)
        splitter.setSizes([420, 980])

        main_layout.addWidget(splitter)

        # Bottom status bar
        self.statusBar().showMessage("Ready")

    def create_control_panel(self):
        """Create the top control panel with algorithm selection and controls"""
        panel = QWidget()
        layout = QHBoxLayout(panel)

        # Algorithm category selection
        layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "Sorting Algorithms",
            "Searching Algorithms",
            "Graph Algorithms",
            "Dynamic Programming"
        ])
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        layout.addWidget(self.category_combo)

        # Specific algorithm selection
        layout.addWidget(QLabel("Algorithm:"))
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.currentTextChanged.connect(self.on_algorithm_changed)
        layout.addWidget(self.algorithm_combo)

        layout.addSpacing(30)

        # Data generation button
        self.generate_button = QPushButton("Random Data")
        self.generate_button.clicked.connect(self.on_generate_data)
        layout.addWidget(self.generate_button)

        # Custom input button
        self.input_button = QPushButton("Custom Input")
        self.input_button.clicked.connect(self.on_custom_input)
        layout.addWidget(self.input_button)

        layout.addSpacing(20)

        # Control buttons
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.on_run)
        layout.addWidget(self.run_button)

        self.step_button = QPushButton("Step")
        self.step_button.clicked.connect(self.on_step)
        layout.addWidget(self.step_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.on_pause)
        self.pause_button.setEnabled(False)
        layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.on_reset)
        layout.addWidget(self.reset_button)

        layout.addSpacing(30)

        # Speed control
        layout.addWidget(QLabel("Speed:"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        self.speed_slider.setFixedWidth(150)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        layout.addWidget(self.speed_slider)

        self.speed_label = QLabel("50%")
        layout.addWidget(self.speed_label)

        layout.addStretch()

        return panel

    def create_code_editor(self):
        """Create the code editor with syntax highlighting"""
        editor = QsciScintilla()

        # Set Python lexer for syntax highlighting
        lexer = QsciLexerPython()
        editor.setLexer(lexer)

        # Editor settings
        editor.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        editor.setMarginWidth(0, "0000")
        editor.setTabWidth(4)
        editor.setIndentationsUseTabs(False)
        editor.setAutoIndent(True)
        editor.setReadOnly(True)

        # Set up marker for current line highlighting
        editor.markerDefine(QsciScintilla.MarkerSymbol.Background, 0)
        editor.setMarkerBackgroundColor(QColor(255, 255, 0, 80), 0)  # Yellow with transparency

        # Set initial sample code
        editor.setText("""# Algorithm will be displayed here
def example_algorithm(arr):
    # Your algorithm code
    pass
""")

        return editor

    def create_visualization_area(self):
        """Create the visualization area"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Info panel
        info_widget = QWidget()
        info_layout = QHBoxLayout(info_widget)

        self.complexity_label = QLabel("Time Complexity: O(?)")
        info_layout.addWidget(self.complexity_label)

        info_layout.addSpacing(20)

        self.space_label = QLabel("Space Complexity: O(?)")
        info_layout.addWidget(self.space_label)

        info_layout.addStretch()

        layout.addWidget(info_widget)

        # Visualization canvas - use stacked widget to switch between different canvas types
        self.canvas_stack = QStackedWidget()

        # Create different canvas types
        self.standard_canvas = VisualizationCanvas()
        self.standard_canvas.setStyleSheet("VisualizationCanvas { background-color: white; border: 2px solid #ccc; }")

        self.merge_sort_canvas = MergeSortCanvas()
        self.merge_sort_canvas.setStyleSheet("MergeSortCanvas { background-color: white; border: 2px solid #ccc; }")

        self.tree_canvas = TreeCanvas()
        self.tree_canvas.setStyleSheet("TreeCanvas { background-color: white; border: 2px solid #ccc; }")

        self.dp_canvas = DPCanvas()
        self.dp_canvas.setStyleSheet("DPCanvas { background-color: white; border: 2px solid #ccc; }")

        self.graph_canvas = GraphCanvas()
        self.graph_canvas.setStyleSheet("GraphCanvas { background-color: white; border: 2px solid #ccc; }")

        # Add canvases to stack
        self.canvas_stack.addWidget(self.standard_canvas)  # Index 0
        self.canvas_stack.addWidget(self.merge_sort_canvas)  # Index 1
        self.canvas_stack.addWidget(self.tree_canvas)  # Index 2
        self.canvas_stack.addWidget(self.dp_canvas)  # Index 3
        self.canvas_stack.addWidget(self.graph_canvas)  # Index 4

        # Default to standard canvas
        self.canvas = self.standard_canvas
        self.canvas_stack.setCurrentIndex(0)

        layout.addWidget(self.canvas_stack)

        return widget

    def on_category_changed(self, category):
        """Handle category selection change"""
        self.algorithm_combo.clear()
        algorithms = get_all_algorithms_in_category(category)
        self.algorithm_combo.addItems(algorithms)

    def on_algorithm_changed(self, algorithm_name):
        """Handle algorithm selection change"""
        if not algorithm_name:
            return

        category = self.category_combo.currentText()
        algo_func, algo_info = get_algorithm(category, algorithm_name)

        if algo_func and algo_info:
            self.current_algorithm = algo_func
            self.algorithm_info = algo_info

            # Switch canvas based on algorithm
            if algorithm_name == "Merge Sort":
                self.canvas_stack.setCurrentIndex(1)  # Merge Sort canvas
                self.canvas = self.merge_sort_canvas
            elif algorithm_name in ["DFS", "BFS"]:
                self.canvas_stack.setCurrentIndex(2)  # Tree canvas
                self.canvas = self.tree_canvas
            elif category == "Dynamic Programming":
                self.canvas_stack.setCurrentIndex(3)  # DP canvas
                self.canvas = self.dp_canvas
            elif category == "Graph Algorithms":
                self.canvas_stack.setCurrentIndex(4)  # Graph canvas
                self.canvas = self.graph_canvas
            else:
                self.canvas_stack.setCurrentIndex(0)  # Standard canvas
                self.canvas = self.standard_canvas

            # Reset current canvas
            self.canvas.reset()
            self.canvas.set_array(self.current_array)

            # Update code editor
            self.code_editor.setText(algo_info['code'])

            # Update complexity labels
            self.complexity_label.setText(f"Time Complexity: {algo_info['time_complexity']}")
            self.space_label.setText(f"Space Complexity: {algo_info['space_complexity']}")

            self.statusBar().showMessage(f"Selected: {algo_info['name']}")
        else:
            self.statusBar().showMessage(f"{algorithm_name} - Not yet implemented")
            self.code_editor.setText(f"# {algorithm_name}\n# Coming soon...")
            self.complexity_label.setText("Time Complexity: N/A")
            self.space_label.setText("Space Complexity: N/A")

    def generate_random_array(self, size=15):
        """Generate a random array for visualization"""
        self.current_array = [random.randint(5, 100) for _ in range(size)]
        # Update all canvases
        self.standard_canvas.set_array(self.current_array)
        self.merge_sort_canvas.set_array(self.current_array)
        self.tree_canvas.set_array(self.current_array)
        self.dp_canvas.set_array(self.current_array)
        self.graph_canvas.set_array(self.current_array)
        self.statusBar().showMessage(f"Generated random array of size {size}")

    def on_generate_data(self):
        """Handle generate data button click"""
        size, ok = QInputDialog.getInt(
            self,
            "Generate Random Data",
            "Enter array size:",
            15, 5, 50, 1
        )
        if ok:
            self.generate_random_array(size)
            self.on_reset()

    def on_custom_input(self):
        """Handle custom input button click"""
        text, ok = QInputDialog.getText(
            self,
            "Custom Input",
            "Enter comma-separated numbers (e.g., 5,3,8,1,9):"
        )

        if ok and text:
            try:
                # Parse the input
                numbers = [int(x.strip()) for x in text.split(',')]

                if not numbers:
                    raise ValueError("No numbers entered")

                if len(numbers) > 50:
                    QMessageBox.warning(
                        self,
                        "Too Many Elements",
                        "Please enter 50 or fewer numbers."
                    )
                    return

                # Validate range
                if any(n < 1 or n > 100 for n in numbers):
                    QMessageBox.warning(
                        self,
                        "Invalid Range",
                        "All numbers must be between 1 and 100."
                    )
                    return

                # Set the custom array
                self.current_array = numbers
                # Update all canvases
                self.standard_canvas.set_array(self.current_array)
                self.merge_sort_canvas.set_array(self.current_array)
                self.tree_canvas.set_array(self.current_array)
                self.dp_canvas.set_array(self.current_array)
                self.graph_canvas.set_array(self.current_array)
                self.statusBar().showMessage(f"Loaded custom array with {len(numbers)} elements")
                self.on_reset()

            except ValueError as e:
                QMessageBox.critical(
                    self,
                    "Invalid Input",
                    f"Error parsing input: {str(e)}\nPlease enter comma-separated integers."
                )

    def on_run(self):
        """Handle run button click"""
        if not self.current_algorithm:
            self.statusBar().showMessage("Please select an algorithm first")
            return

        # Initialize algorithm with parameters
        self._initialize_algorithm()

        if not self.algorithm_generator:
            # User cancelled
            return

        self.is_running = True

        # Update UI
        self.run_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.step_button.setEnabled(False)
        self.generate_button.setEnabled(False)
        self.input_button.setEnabled(False)

        # Start animation
        self.timer.start(self.animation_delay)
        self.statusBar().showMessage("Running algorithm...")

    def on_step(self):
        """Handle step button click"""
        if not self.current_algorithm:
            self.statusBar().showMessage("Please select an algorithm first")
            return

        # Initialize generator if needed (reuse on_run logic)
        if not self.algorithm_generator:
            # Temporarily call on_run logic but without starting timer
            self._initialize_algorithm()
            if not self.algorithm_generator:
                # User cancelled
                return

        # Execute one step
        self.execute_step()

    def _initialize_algorithm(self):
        """Helper to initialize algorithm with parameters"""
        category = self.category_combo.currentText()
        algorithm_name = self.algorithm_combo.currentText()
        target = None

        if category == "Searching Algorithms":
            target, ok = QInputDialog.getInt(
                self,
                "Search Target",
                f"Array: [{', '.join(str(x) for x in self.current_array[:10])}{'...' if len(self.current_array) > 10 else ''}]\n\nEnter the value to search for (1-100):",
                self.current_array[0] if self.current_array else 50,
                1, 100, 1
            )
            if not ok:
                return
        elif category == "Dynamic Programming":
            if algorithm_name == "Fibonacci":
                target, ok = QInputDialog.getInt(
                    self, "Fibonacci Number",
                    "Which Fibonacci number to compute? (2-20):",
                    10, 2, 20, 1
                )
                if not ok:
                    return
            elif algorithm_name == "Knapsack Problem":
                max_capacity = sum(self.current_array)
                target, ok = QInputDialog.getInt(
                    self, "Knapsack Capacity",
                    f"Enter knapsack capacity (1-{min(max_capacity, 50)}):",
                    max_capacity // 2, 1, min(max_capacity, 50), 1
                )
                if not ok:
                    return
            elif algorithm_name == "Coin Change":
                max_amount = sum(self.current_array)
                target, ok = QInputDialog.getInt(
                    self, "Target Amount",
                    f"Enter target amount (1-{min(max_amount, 50)}):",
                    max_amount // 2, 1, min(max_amount, 50), 1
                )
                if not ok:
                    return

        # Initialize generator
        if target is not None:
            self.algorithm_generator = self.current_algorithm(self.current_array.copy(), target)
        else:
            self.algorithm_generator = self.current_algorithm(self.current_array.copy())

    def execute_step(self):
        """Execute one step of the algorithm"""
        try:
            state = next(self.algorithm_generator)
            self.canvas.set_state(state)

            # Highlight current line in code editor
            if 'line' in state:
                self.highlight_code_line(state['line'])

            self.statusBar().showMessage(f"Action: {state['action']} | Pass: {state.get('current_pass', 0)}")
        except StopIteration:
            # Algorithm finished
            self.on_algorithm_complete()

    def highlight_code_line(self, line_number):
        """Highlight a specific line in the code editor"""
        # Clear previous markers
        self.code_editor.markerDeleteAll(0)

        # Add marker to the current line (line_number is 1-based, but we show relative to function start)
        # Since our code displays the whole function, we add an offset
        if line_number > 0:
            # Line numbers in the editor are 0-based
            actual_line = line_number  # Adjust based on your code structure
            self.code_editor.markerAdd(actual_line, 0)

    def on_algorithm_complete(self):
        """Handle algorithm completion"""
        self.is_running = False
        self.timer.stop()

        self.run_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.step_button.setEnabled(True)
        self.generate_button.setEnabled(True)
        self.input_button.setEnabled(True)

        # Clear code highlighting
        self.code_editor.markerDeleteAll(0)

        self.statusBar().showMessage("Algorithm completed!")

    def on_pause(self):
        """Handle pause button click"""
        self.is_running = False
        self.timer.stop()

        self.run_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.step_button.setEnabled(True)
        self.input_button.setEnabled(True)

        self.statusBar().showMessage("Paused")

    def on_reset(self):
        """Handle reset button click"""
        self.is_running = False
        self.timer.stop()
        self.algorithm_generator = None

        # Reset current canvas
        self.canvas.reset()
        self.canvas.set_array(self.current_array)

        # Clear code highlighting
        self.code_editor.markerDeleteAll(0)

        # Reset UI
        self.run_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.step_button.setEnabled(True)
        self.generate_button.setEnabled(True)
        self.input_button.setEnabled(True)

        self.statusBar().showMessage("Reset")

    def on_speed_changed(self, value):
        """Handle speed slider change"""
        self.speed_label.setText(f"{value}%")
        # Convert slider value to delay (inverse relationship)
        # 1% = 1000ms, 100% = 10ms
        self.animation_delay = int(1010 - (value * 10))
        if self.is_running:
            self.timer.setInterval(self.animation_delay)
