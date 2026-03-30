# SAC Module

## 1. 목적
이 폴더는 SAC 기반 강화학습 실험을 관리하기 위한 공간입니다.

---

## 2. 주요 책임
- SAC policy 학습
- replay buffer 기반 실험 관리
- task별 성능 평가
- PPO 및 BC와의 결과 비교

---

## 3. 폴더 구조
- `agent.py`: SAC 에이전트 정의
- `trainer.py`: 학습 루프
- `replay_buffer.py`: replay buffer 구현
- `tasks/`: task별 SAC 실험

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
- SAC checkpoint
- evaluation 로그
- 학습 곡선
- task별 rollout 영상
- 실험 노트

---

## 6. 참고
SAC는 off-policy 특성상 replay buffer 구성, exploration 안정성, reward scale에 주의합니다.