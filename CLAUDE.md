# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Algorithm Visualizer - 알고리즘 학습을 위한 인터랙티브 시각화 데스크톱 애플리케이션. PyQt6 기반으로 정렬, 탐색, 그래프, 동적 프로그래밍 알고리즘의 실행 과정을 시각적으로 표현합니다.

## Environment Setup

```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (Unix/MacOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
python src/main.py
```

## Architecture

### Core Components

1. **GUI Layer** (`src/gui/`)
   - `main_window.py`: 메인 애플리케이션 윈도우, 전체 레이아웃 관리
     - QStackedWidget으로 여러 시각화 캔버스 관리
     - 알고리즘 선택 시 적절한 캔버스로 자동 전환
   - `visualization_canvas.py`: 일반 정렬/탐색 알고리즘용 바 차트 시각화
   - `merge_sort_canvas.py`: Merge Sort 전용 분할/병합 과정 시각화
   - 왼쪽: 코드 에디터 (QScintilla 사용, 실행 라인 하이라이팅)
   - 오른쪽: 시각화 영역 (동적 캔버스)
   - 상단: 컨트롤 패널 (알고리즘 선택, 실행/일시정지/리셋, 속도 조절)
   - 하단: 복잡도 정보 표시

2. **Algorithm Layer** (`src/algorithms/`)
   - 각 알고리즘은 제너레이터 패턴으로 구현 예정
   - `yield` 문을 사용하여 각 단계의 상태를 반환
   - 각 카테고리별로 모듈 분리:
     - `sorting/`: 정렬 알고리즘
     - `searching/`: 탐색 알고리즘
     - `graph/`: 그래프 알고리즘
     - `dp/`: 동적 프로그래밍

3. **Utilities** (`src/utils/`)
   - 공통 유틸리티 함수
   - 애니메이션 헬퍼
   - 데이터 생성기

### Key Design Patterns

- **Generator Pattern**: 알고리즘의 각 단계를 yield로 반환하여 단계별 실행 구현
- **Strategy Pattern**: 알고리즘별로 다른 시각화 캔버스 사용 (QStackedWidget)
- **MVC Pattern**: GUI(View), 알고리즘 로직(Model), 컨트롤러 분리

### PyQt6 Specific Notes

- PyQt6는 PyQt5와 다르게 Enum을 사용: `Qt.AlignmentFlag.AlignCenter` (PyQt5: `Qt.AlignCenter`)
- QScintilla는 코드 하이라이팅과 라인 번호 표시에 사용
- QTimer를 사용하여 애니메이션 속도 제어

## Algorithm Implementation Guidelines

알고리즘 구현 시:
1. 각 알고리즘은 제너레이터 함수로 작성
2. 중요한 단계마다 `yield` 문으로 현재 상태 반환
3. 반환값에는 시각화에 필요한 정보 포함 (예: 현재 비교 중인 인덱스, 변경된 값 등)
4. 시간/공간 복잡도 정보를 함수 docstring에 명시
5. **코드 하이라이팅**: `line` 값은 get_algorithm_info()의 'code' 문자열 기준 (0-based)
6. **특수 시각화 필요 시**: 새로운 Canvas 클래스 생성하고 main_window.py에서 분기 처리

### Adding New Visualization Types

1. `src/gui/` 에 새 캔버스 클래스 생성 (예: `graph_canvas.py`)
2. `main_window.py`의 `create_visualization_area()`에 캔버스 추가
3. `on_algorithm_changed()`에서 알고리즘 이름으로 캔버스 전환 로직 추가
4. 필요한 action 타입을 캔버스의 `set_state()`에서 처리

예시:
```python
def bubble_sort(arr):
    """
    Bubble Sort Algorithm
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            # Yield current comparison
            yield {
                'comparing': [j, j+1],
                'array': arr.copy(),
                'line': 10  # Current line number for code highlighting
            }
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                # Yield after swap
                yield {
                    'swapped': [j, j+1],
                    'array': arr.copy(),
                    'line': 12
                }
```

## Implemented Features

✅ **Sorting Algorithms**
- Bubble Sort, Selection Sort, Insertion Sort
- Merge Sort, Quick Sort

✅ **Searching Algorithms**
- Linear Search
- Binary Search (automatically sorts array first)

✅ **Visualization Canvas**
- Bar chart visualization with color coding
- Support for different algorithm actions (compare, swap, pivot, found, etc.)
- Target value indicator for search algorithms
- Legend for color meanings

✅ **User Interface**
- Algorithm category and selection
- Random data generation with configurable size
- Custom data input (comma-separated values)
- Run, Step, Pause, Reset controls
- Speed slider (1-100%)
- Time/Space complexity display
- Code highlighting in QScintilla editor with markers

✅ **Code Line Highlighting**
- Yellow background marker for current execution line
- Automatic marker clearing on reset/completion
- Note: Line numbers in yield statements must match the simplified code in get_algorithm_info()

✅ **Multi-Canvas Architecture**
- QStackedWidget manages multiple visualization types
- Automatic canvas switching based on selected algorithm
- Currently: StandardCanvas (바 차트) and MergeSortCanvas (분할/병합 시각화)

## Future Development Tasks

**High Priority:**
- DFS/BFS visualization with tree/graph structure
- Heap Sort algorithm
- Graph visualization canvas (nodes and edges)
- Performance metrics tracking (comparisons, swaps count)

**Medium Priority:**
- Graph algorithms (Dijkstra, Kruskal, Prim, Bellman-Ford)
- Dynamic Programming visualizations
- Export visualization as GIF/video
- Save/Load custom datasets

**Low Priority:**
- Dark mode theme
- Multiple visualization layouts
- Comparison mode (run two algorithms side-by-side)
- Educational tooltips and explanations
