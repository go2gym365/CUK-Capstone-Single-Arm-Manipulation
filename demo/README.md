---
# Demo Pipeline

## 1. 목적
이 폴더는 캡스톤 프로젝트의 **최종 통합 데모 파이프라인**을 관리하기 위한 공간입니다.

이곳에는 실험 중간 코드가 아니라,  
**검증이 완료되어 실제 발표 및 시연에 사용할 수 있는 코드만** 포함하는 것을 원칙으로 합니다.

---

## 2. 포함되는 내용
- 최종 환경(env)
- 최종 reward 로직
- 최종 policy checkpoint 로더
- 최종 평가 코드
- 최종 데모 실행 스크립트
- 데모 출력 결과

---

## 3. 폴더 구성
- `run_demo.py`: 최종 데모 실행 진입점
- `pipeline/env.py`: 데모용 환경
- `pipeline/reward.py`: 데모용 reward
- `pipeline/policy_loader.py`: 선택된 정책 불러오기
- `pipeline/evaluator.py`: 최종 정책 평가
- `checkpoints/`: 최종 선택된 모델
- `outputs/`: 데모 결과물 저장

---

## 4. 운영 원칙
- 불안정한 실험 코드는 이 폴더에 넣지 않습니다.
- `src/`에서 충분히 검증된 코드만 이 폴더로 반영합니다.
- 이 폴더는 언제든지 시연 가능 상태를 유지해야 합니다.

---

## 5. 실행 방법
```bash
python demo/run_demo.py