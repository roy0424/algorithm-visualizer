# Algorithm Visualizer

알고리즘 학습을 위한 인터랙티브 시각화 도구입니다. 다양한 알고리즘의 동작 과정을 단계별로 확인하고 이해할 수 있습니다.

## 주요 기능

- **단계별 실행**: 알고리즘을 한 단계씩 실행하며 동작 과정 관찰
- **속도 조절**: 애니메이션 속도를 자유롭게 조절
- **코드 하이라이팅**: 현재 실행 중인 코드 라인 표시
- **사용자 입력**: 직접 데이터를 입력하여 테스트
- **복잡도 정보**: 시간/공간 복잡도 표시

## 지원 알고리즘

### 정렬 알고리즘 (6개 구현 완료)
- ✅ **Bubble Sort** - O(n²) - 인접한 요소를 비교하며 정렬
- ✅ **Selection Sort** - O(n²) - 최솟값을 찾아 앞으로 이동
- ✅ **Insertion Sort** - O(n²) - 요소를 올바른 위치에 삽입
- ✅ **Merge Sort** - O(n log n) - 분할 정복 방식의 정렬 (전용 시각화)
- ✅ **Quick Sort** - O(n log n) - 피벗 기반 분할 정렬
- ✅ **Heap Sort** - O(n log n) - 힙 자료구조를 이용한 정렬

### 탐색 알고리즘 (4개 구현 완료)
- ✅ **Linear Search** - O(n) - 순차 탐색
  - 사용자가 찾을 값을 직접 입력
  - 배열에 없는 값도 검색 가능 (not found 시나리오)
- ✅ **Binary Search** - O(log n) - 이진 탐색
  - 자동으로 배열 정렬 후 탐색
  - 원본 배열에서 target 선택하여 정렬 후에도 의미 있는 탐색
- ✅ **DFS** - O(n) - 깊이 우선 탐색 (트리 시각화)
  - 배열을 이진 트리로 표현하여 탐색
  - 스택 기반 LIFO 방식
- ✅ **BFS** - O(n) - 너비 우선 탐색 (트리 시각화)
  - 레벨 순서대로 탐색
  - 큐 기반 FIFO 방식

### 동적 프로그래밍 (4개 구현 완료)
- ✅ **Fibonacci** - O(n) - 피보나치 수열 (테이블 시각화)
  - Bottom-up DP 방식
  - n번째 피보나치 수 계산 (n: 2-20)
- ✅ **Knapsack Problem** - O(n×W) - 0/1 배낭 문제
  - 2D DP 테이블 시각화
  - 최대 가치 부분집합 찾기
- ✅ **Longest Common Subsequence** - O(m×n) - 최장 공통 부분수열
  - 두 수열 간 LCS 길이 계산
  - DP 테이블로 과정 표시
- ✅ **Coin Change** - O(n×amount) - 동전 교환 문제
  - 최소 동전 개수 찾기
  - 다양한 액면가 처리

## 설치 방법

1. 가상환경 활성화:
```bash
# Windows
.venv\Scripts\activate

# Unix/MacOS
source .venv/bin/activate
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
python src/main.py
```

## 사용 방법

1. **데이터 준비**
   - `Random Data`: 랜덤 배열 생성 (크기 5-50)
   - `Custom Input`: 직접 배열 입력 (쉼표로 구분, 예: 5,3,8,1,9)

2. **알고리즘 선택**
   - Category: 알고리즘 카테고리 선택
   - Algorithm: 구체적인 알고리즘 선택
   - 탐색 알고리즘 선택 시: Run/Step 실행 시 찾을 값(target) 입력 요청

3. **실행 제어**
   - `Run`: 자동 애니메이션 실행
   - `Step`: 한 단계씩 실행
   - `Pause`: 일시 정지
   - `Reset`: 초기 상태로 리셋
   - Speed 슬라이더: 애니메이션 속도 조절 (1-100%)

4. **시각화 (4가지 캔버스 타입)**
   - 알고리즘에 따라 자동으로 적절한 시각화 선택

   **StandardCanvas** - 일반 정렬 (Bubble, Selection, Insertion, Quick, Heap Sort):
   - 파란색: 정렬되지 않은 요소
   - 금색: 비교 중인 요소
   - 빨간색: 교환/이동 중인 요소
   - 초록색: 정렬 완료된 요소
   - 주황색: 피벗 (Quick Sort)

   **MergeSortCanvas** - Merge Sort 전용:
   - 분할(Divide)과 병합(Merge) 과정을 명확히 표시
   - 금색: 분할 중인 범위
   - 빨간색: 병합 중인 요소
   - 주황색: 비교 중인 요소

   **TreeCanvas** - DFS/BFS:
   - 배열을 이진 트리로 시각화
   - 빨간색: 현재 방문 중인 노드
   - 초록색: 방문 완료된 노드
   - 회색 선: 부모-자식 관계
   - 하단에 탐색 순서 표시

   **DPCanvas** - 동적 프로그래밍:
   - 2D DP 테이블 시각화
   - 연한 회색: 빈 셀
   - 금색: 현재 계산 중인 셀
   - 연한 초록색: 계산 완료된 셀
   - 파란색: 최종 결과

## 프로젝트 구조

```
pythonProject1/
├── src/
│   ├── main.py                          # 애플리케이션 진입점
│   ├── gui/
│   │   ├── main_window.py               # 메인 윈도우 및 컨트롤러
│   │   └── visualization_canvas.py      # 시각화 캔버스
│   ├── algorithms/
│   │   ├── algorithm_registry.py        # 알고리즘 등록 및 관리
│   │   ├── sorting/
│   │   │   ├── bubble_sort.py
│   │   │   ├── selection_sort.py
│   │   │   ├── insertion_sort.py
│   │   │   ├── merge_sort.py
│   │   │   └── quick_sort.py
│   │   └── searching/
│   │       ├── linear_search.py
│   │       └── binary_search.py
│   └── utils/
└── tests/
```

## 주요 기술적 특징

1. **알고리즘별 맞춤 시각화 (4가지 캔버스)**
   - **StandardCanvas**: 일반 정렬 (Bubble, Selection, Insertion, Quick, Heap)
   - **MergeSortCanvas**: 분할 정복 과정 강조
   - **TreeCanvas**: 트리 구조 탐색 (DFS, BFS)
   - **DPCanvas**: 2D 테이블 기반 DP 과정 표시

2. **제너레이터 패턴**
   - 각 알고리즘은 Python generator로 구현
   - `yield`를 통해 각 단계의 상태 반환
   - 메모리 효율적이고 단계별 제어 가능
   - 14개 알고리즘 모두 일관된 인터페이스

3. **동적 캔버스 전환**
   - QStackedWidget으로 알고리즘에 맞는 시각화 자동 전환
   - 확장 가능한 구조로 새로운 시각화 타입 추가 용이
   - 알고리즘 선택 시 자동으로 적절한 캔버스 로드

4. **인터랙티브 파라미터 입력**
   - 탐색 알고리즘: target 값 입력
   - Fibonacci: n번째 수 선택 (2-20)
   - Knapsack: 배낭 용량 지정
   - Coin Change: 목표 금액 설정

## 통계

- **총 14개 알고리즘** 구현 완료
  - 정렬: 6개
  - 탐색: 4개
  - 동적 프로그래밍: 4개
- **4가지 시각화 타입**
- **라인 수**: ~2,500줄 (Python)

## 기술 스택

- **Python 3.x**
- **PyQt6**: GUI 프레임워크
  - QScintilla: 코드 에디터 및 하이라이팅
  - QPainter: 커스텀 시각화 렌더링
  - QStackedWidget: 다중 캔버스 관리
  - QTimer: 애니메이션 제어
