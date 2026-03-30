# Behavior Cloning Module

## 1. 목적
이 폴더는 Behavior Cloning 기반 imitation learning 실험을 관리하기 위한 공간입니다.

---

## 2. 주요 책임
- trajectory dataset 준비
- BC 모델 학습
- BC policy 평가
- BC baseline 결과 정리

---

## 3. 폴더 구조
- `model.py`: BC 모델 정의
- `trainer.py`: 학습 루프
- `dataset.py`: 데이터셋 처리
- `tasks/`: task별 BC 실험

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
- BC checkpoint
- evaluation 결과
- 학습 로그
- rollout 영상
- task별 실험 노트

---

## 6. 참고
BC는 baseline 및 imitation initialization 성격을 가지므로,  
trajectory 품질과 데이터셋 구성에 특히 주의합니다.