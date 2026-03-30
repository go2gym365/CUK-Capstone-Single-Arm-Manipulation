# Task Specification

## 1. 목적
본 문서는 프로젝트에서 다루는 manipulation task의 정의와 목표를 명확히 하기 위해 작성되었습니다.

---

## 2. Task 목록

### 2.1 Push
- 목표: 로봇팔 end-effector를 이용해 물체를 목표 위치까지 밀기
- 입력: 현재 로봇 상태, 물체 위치, 목표 위치
- 출력: 연속 action
- 성공 조건: 물체가 목표 영역 안으로 이동

### 2.2 Grasp
- 목표: 로봇팔이 물체를 안정적으로 잡는 것
- 입력: 현재 로봇 상태, 물체 위치
- 출력: 연속 action 및 gripper control
- 성공 조건: 일정 시간 이상 물체를 안정적으로 grasp 유지

### 2.3 Pick-and-Place
- 목표: 물체를 집어서 목표 위치에 놓기
- 입력: 현재 로봇 상태, 물체 위치, 목표 위치
- 출력: 연속 action 및 gripper control
- 성공 조건: 물체를 목표 위치 근처에 안정적으로 배치

---

## 3. 공통 요소
- Observation space:
- Action space:
- Episode length:
- Reset 조건:
- Failure 조건:

---

## 4. 추후 확장 가능성
- Reach
- Staged curriculum learning
- Multi-object setting