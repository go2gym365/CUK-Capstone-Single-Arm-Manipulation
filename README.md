# CUK Capstone | Single-Arm Manipulation

## 1. 프로젝트 개요
이 저장소는 가톨릭대학교 캡스톤 프로젝트 **Single-Arm Manipulation**의 전체 개발 내용을 관리하기 위한 레포지토리입니다.

본 프로젝트는 MuJoCo 기반 시뮬레이션 환경에서 단일 로봇팔(single-arm)을 이용한 manipulation task를 정의하고,  
각 task에 대해 다양한 policy learning 방법을 적용하여 성능을 비교·개선하는 것을 목표로 합니다.

장기적으로는 시뮬레이션에서 학습한 정책을 기반으로 최종 통합 데모 파이프라인을 구성하는 것을 목표로 합니다.

---

## 2. 프로젝트 목표
- single-arm manipulation을 위한 시뮬레이션 환경 구축
- task별 reward 설계 및 success metric 정의
- BC, PPO, SAC 기반 정책 학습 및 성능 비교
- 최종적으로 데모 가능한 통합 파이프라인 구성

---

## 3. 주요 task
현재 프로젝트에서 다루는 주요 task는 다음과 같습니다.

- Push
- Grasp
- Pick-and-Place

필요 시 Reach 등 보조 task를 추가할 수 있습니다.

---

## 4. 사용 알고리즘
- Behavior Cloning (BC)
- Proximal Policy Optimization (PPO)
- Soft Actor-Critic (SAC)

---

## 5. 저장소 구조
- `demo/`: 최종 발표 및 시연용 통합 파이프라인
- `src/`: 역할별 실험 및 개발 코드
- `configs/`: 환경, 보상, 알고리즘 설정 파일
- `docs/`: 프로젝트 문서, 회의록, 주간 기록
- `results/`: 실험 결과, 로그, 그래프, 비디오
- `data/`: trajectory 및 전처리 데이터
- `notebooks/`: 분석 및 시각화용 노트북

---

## 6. 역할 분담
- Environment
- Reward Design
- Behavior Cloning
- PPO
- SAC
- Integration / Demo

각 역할별 상세 내용은 `src/` 하위 폴더 및 노션 페이지에서 관리합니다.

---

## 7. 실행 예시
예시 실행 명령은 아래와 같습니다.

```bash
python src/ppo/tasks/pick_and_place/train.py
python src/sac/tasks/push/train.py
python demo/run_demo.py