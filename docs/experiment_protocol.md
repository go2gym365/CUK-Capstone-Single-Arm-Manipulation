# Experiment Protocol

## 1. 목적
본 문서는 모든 실험이 공통된 기준 아래에서 비교 가능하도록 하기 위해 작성되었습니다.

---

## 2. 공통 실험 원칙
- 동일 task에 대해 동일한 success metric 사용
- 동일 task에 대해 가능한 동일한 evaluation procedure 사용
- 알고리즘 비교 시 seed, episode 수, 평가 횟수를 명시
- 실험 결과는 반드시 로그와 함께 저장

---

## 3. 공통 기록 항목
각 실험은 아래 항목을 기록해야 합니다.

- Task 이름
- 알고리즘 이름
- 사용 config 파일
- 학습 시작 날짜
- 학습 종료 날짜
- random seed
- best checkpoint 경로
- 최종 success rate
- 평균 return
- 주요 failure case

---

## 4. 결과 저장 위치
- BC 결과: `results/bc/[task]/`
- PPO 결과: `results/ppo/[task]/`
- SAC 결과: `results/sac/[task]/`
- Demo 결과: `results/demo/`

---

## 5. 미디어 관리
- 실험용 비디오는 GitHub에 직접 올리지 않음
- 대표 gif / 스크린샷만 저장소에 포함 가능
- 고화질 원본 데모 영상은 외부 저장소 링크로 관리

---

## 6. 비교 실험 시 주의점
- reward 버전이 다른 실험은 직접 비교 시 명시 필요
- env 버전이 바뀐 경우 결과 비교 시 별도 표시
- config 변경 사항은 notes.md 또는 실험 로그에 반영