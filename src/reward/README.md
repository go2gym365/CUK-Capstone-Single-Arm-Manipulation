# Reward Module

## 1. 목적
이 폴더는 manipulation task에 필요한 reward 및 success metric을 관리하기 위한 공간입니다.

---

## 2. 주요 책임
- task별 reward 함수 설계
- success / failure 기준 정의
- reward shaping 실험
- 공통 reward utility 제공

---

## 3. 폴더 구조
- `reward_utils.py`: 공통 reward 계산 유틸
- `success_metrics.py`: 공통 success metric
- `tasks/`: task별 reward 정의

---

## 4. task 구성
- `tasks/push/`
- `tasks/grasp/`
- `tasks/pick_and_place/`

각 task 폴더에는 아래 내용을 포함합니다.
- `reward.py`
- `metrics.py`
- `notes.md`

---

## 5. 기대 산출물
- task별 reward 구현
- success metric 정의
- reward 버전별 비교
- reward 설계 노트

---

## 6. 참고
reward 변경 사항은 반드시 notes와 config에 반영합니다.