# 프로젝트 작업 메모 (Codex 컨텍스트 요약)

이 파일은 앞으로 대화 없이도 최근 변경 맥락을 빠르게 복원하기 위한 요약입니다. 필요한 내용을 자유롭게 추가/수정하세요.

## 최근 변경 요약
- UI/테마: `src/gui/main_window.py`에 현대적인 라이트 테마 적용, 컨트롤/캔버스 카드화, 레벨·그리드 옵션 토글 추가.  
- 그래프 시각화: `src/gui/graph_canvas.py`에서 노드 레이아웃 중앙 정렬, 레벨별 노드 스케일 축소, 병렬 간선 가중치 라벨 분산, 그래프 DFS/BFS만 그리드 사이즈 노출. 통계에서 Efficiency 제거.
- 그래프 알고리즘:  
  - Dijkstra/A*: 레벨 선택으로 레이어 수 3~10, 시작→다음 레이어/직전→목표 강제 연결, 레벨별 노드 축소.  
  - 통계의 Total Weight는 총 가중치 합으로 표시.  
  - 실행 단계별 세밀한 하이라이트(while/pop/visit/goal/거리 계산/업데이트/큐 push 등) 추가.  
  - Dijkstra 루프 들여쓰기/return 오류 수정.
- DFS/BFS(그래프용 2D grid): 단계별 하이라이트 세밀화.  
  - DFS: loop/pop/visited 체크/visit/neighbor 탐색/stack push 라인 번호를 스니펫 기준으로 재정렬.  
  - BFS: loop/popleft/neighbor 방문/visited 추가/queue append를 각각 상태로 분리해 하이라이트.

## 주요 파일
- `src/algorithms/graph/astar_weighted.py`
- `src/algorithms/graph/dijkstra_weighted.py`
- `src/algorithms/graph/graph_dfs.py`
- `src/algorithms/graph/graph_bfs.py`
- `src/gui/main_window.py`
- `src/gui/graph_canvas.py`

## 앞으로 참고
- 코드 하이라이트 라인 번호는 `get_algorithm_info()['code']` 스니펫 기준(0-based)으로 맞춤.  
- 그래프 카테고리: DFS/BFS만 Grid Size 노출, Dijkstra/A*는 Level(3~10) 노출.  
- 빈 줄에 하이라이트되지 않도록 라인 매핑을 주기적으로 검토.
