# System Architecture

## 1. 전체 구조
본 프로젝트의 전체 구조는 크게 두 부분으로 나뉩니다.

1. `src/`
   - 역할별 실험 및 개발 공간
   - 환경, 보상, BC, PPO, SAC를 개별적으로 개발 및 검증

2. `demo/`
   - 최종 통합 데모 파이프라인
   - 발표 및 시연용 코드만 관리

---

## 2. 주요 모듈
### Environment Module
- task별 환경 정의
- robot / object / goal 세팅
- reset / termination 로직 담당

### Reward Module
- task별 reward 설계
- success / failure metric 정의
- reward shaping 실험 담당

### BC Module
- trajectory 기반 imitation learning
- BC baseline 학습 및 평가

### PPO Module
- on-policy 방식의 강화학습
- task별 PPO 성능 측정 및 튜닝

### SAC Module
- off-policy 방식의 강화학습
- replay buffer 기반 학습 및 평가

### Demo Module
- 최종 선택된 환경, reward, policy를 하나로 묶어 실행
- 최종 성능 검증 및 시연 담당

---

## 3. 데이터 흐름
1. Environment 정의
2. Reward 및 success metric 정의
3. 알고리즘별 policy 학습
4. 결과 저장 및 비교
5. 최종 우수 정책 선정
6. demo 파이프라인으로 통합

---

## 4. 결과물 흐름
- 코드: `src/`, `demo/`
- 설정 파일: `configs/`
- 데이터: `data/`
- 결과: `results/`
- 문서: `docs/`# System Architecture

## 1. 전체 구조
본 프로젝트의 전체 구조는 크게 두 부분으로 나뉩니다.

1. `src/`
   - 역할별 실험 및 개발 공간
   - 환경, 보상, BC, PPO, SAC를 개별적으로 개발 및 검증

2. `demo/`
   - 최종 통합 데모 파이프라인
   - 발표 및 시연용 코드만 관리

---

## 2. 주요 모듈
### Environment Module
- task별 환경 정의
- robot / object / goal 세팅
- reset / termination 로직 담당

### Reward Module
- task별 reward 설계
- success / failure metric 정의
- reward shaping 실험 담당

### BC Module
- trajectory 기반 imitation learning
- BC baseline 학습 및 평가

### PPO Module
- on-policy 방식의 강화학습
- task별 PPO 성능 측정 및 튜닝

### SAC Module
- off-policy 방식의 강화학습
- replay buffer 기반 학습 및 평가

### Demo Module
- 최종 선택된 환경, reward, policy를 하나로 묶어 실행
- 최종 성능 검증 및 시연 담당

---

## 3. 데이터 흐름
1. Environment 정의
2. Reward 및 success metric 정의
3. 알고리즘별 policy 학습
4. 결과 저장 및 비교
5. 최종 우수 정책 선정
6. demo 파이프라인으로 통합

---

## 4. 결과물 흐름
- 코드: `src/`, `demo/`
- 설정 파일: `configs/`
- 데이터: `data/`
- 결과: `results/`
- 문서: `docs/`