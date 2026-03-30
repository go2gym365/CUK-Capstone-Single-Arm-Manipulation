# Environment Module

## 1. 목적
이 폴더는 single-arm manipulation task를 위한 시뮬레이션 환경을 관리하는 공간입니다.

---

## 2. 주요 책임
- MuJoCo 기반 환경 구성
- task별 env 정의
- robot / object / goal 세팅
- reset, transition, termination 로직 구현
- 공통 env 인터페이스 제공

---

## 3. 폴더 구조
- `base_env.py`: 공통 환경 클래스
- `env_utils.py`: 환경 관련 유틸
- `robot_model/`: 로봇 모델 관련 파일
- `tasks/`: task별 환경 정의

---

## 4. task 구성
- `tasks/push/`
- `tasks/grasp/`
- `tasks/pick_and_place/`

각 task 폴더에는 아래 내용을 포함합니다.
- `env.py`
- `objects.py`
- `reset.py`
- `notes.md`

---

## 5. 기대 산출물
- 실행 가능한 env 코드
- task별 reset 테스트
- 환경 동작 영상
- 환경 설계 노트

---

## 6. 참고
이 폴더는 환경 자체를 정의하는 역할을 하며,  
알고리즘별 학습은 `src/bc`, `src/ppo`, `src/sac`에서 수행합니다.