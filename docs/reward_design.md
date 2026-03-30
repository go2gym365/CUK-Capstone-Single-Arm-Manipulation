# Reward Design

## 1. 목적
본 문서는 manipulation task별 reward 설계 원칙과 구성 요소를 정리하기 위해 작성되었습니다.

---

## 2. Reward 설계 원칙
- 가능한 한 task 목적과 직접 연결된 보상 사용
- dense reward와 sparse reward를 상황에 따라 비교
- success condition은 명확한 수치 기준으로 정의
- shaping reward는 학습 안정성을 위해 최소한으로 사용하되, 필요 시 단계별 추가

---

## 3. Task별 reward 예시

### 3.1 Push
- 물체와 목표 위치 간 거리 감소 보상
- end-effector와 물체 정렬 보상
- 목표 영역 도달 시 성공 보상

### 3.2 Grasp
- end-effector와 물체 간 거리 감소 보상
- grasp 성공 시 추가 보상
- 일정 시간 grasp 유지 시 성공 보상

### 3.3 Pick-and-Place
- 물체 접근 보상
- grasp 보상
- 물체 들어올리기 보상
- 목표 위치 접근 보상
- 정확한 placement 성공 보상

---

## 4. Success Metric
- task별 success rate
- 평균 episode return
- 평균 completion time
- 실패 유형별 빈도

---

## 5. 버전 관리
- reward v0.1:
- reward v0.2:
- reward v1.0:

---

## 6. 비고
최종 reward는 task별 notes 및 실험 결과를 바탕으로 업데이트합니다.