# PPO Module

## 1. 목적
이 폴더는 PPO 기반 강화학습 실험을 관리하기 위한 공간입니다.

---

## 2. 주요 책임
- PPO policy 학습
- task별 성능 평가
- 하이퍼파라미터 튜닝
- BC / SAC와의 결과 비교를 위한 실험 기록

---

## 3. 폴더 구조
- `agent.py`: PPO 에이전트 정의
- `trainer.py`: PPO 학습 루프
- `tasks/`: task별 PPO 실험

---

## 4. task 구성
- `tasks/push/`
- `tasks/grasp/`
- `tasks/pick_and_place/`

각 task 폴더에는 아래 내용을 포함합니다.
- `train.py`
- `eval.py`
- `config.yaml`
- `notes.md`

---

## 5. 기대 산출물
- PPO checkpoint
- success rate 곡선
- 학습 로그
- task별 영상
- 하이퍼파라미터 실험 기록

---

## 6. 참고
PPO 실험 시 reward scale, rollout length, batch size, gamma, gae lambda 등의 설정을 명확히 기록합니다.