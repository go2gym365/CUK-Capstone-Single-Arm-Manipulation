# ENV 설정 변경 이력 및 GUI 데모 가이드

> Remark: 먼저 프로젝트 루트에서 아래 순서로 `.venv`를 준비하세요 (`requirements.txt` 기준).
>
> ```bash
> python3 -m venv .venv
> source .venv/bin/activate
> pip install -r requirements.txt
> ```

## 1. 문서 목적
이 문서는 `src/env` 하위에서 최근 진행한 ROBOTIS OMX 기반 환경 설정 변경사항을 한 번에 정리한 기록입니다.  
특히 "초기 환경 구성 추가 + 공통 씬 통합 정리"까지 포함해, Pick-and-Place 실험 기준을 현재 코드 상태로 정리합니다.

## 2. 변경 개요
- ROBOTIS OMX 모델 에셋 / XML / 실행 러너를 env에 초기 추가
- `requirements.txt` 기반 실행 환경(.venv) 준비 방식 반영
- ROBOTIS OMX 관련 코드/에셋 중심을 `src/env/robotis_model/`로 정리
- `scene_reach.xml` 제거, 공통 작업 씬 `scene_cube_bottle.xml` 도입
- 공통 씬에 로봇 + 테이블 + 큐브 + 병 + placeholder(목표 패드) 반영
- GUI 실행 스크립트에서 site group 0 마커 기본 OFF 적용
- 환경 기본 XML 및 설정 파일 경로를 `scene_cube_bottle.xml` 기준으로 변경

### 2.1 커밋 단위 요약
- `bc2d207` (`feat(env): add ROBOTIS OMX model env and runners`)
  - ROBOTIS OMX 모델/에셋 추가
  - env 실행 기본 구조(`robotis_env`, `factory`, `runners`) 추가
  - `configs/env/reach.yaml` 및 실행 의존성(requirements) 반영
- `c96eb11` (`feat(env): consolidate cube-bottle scene and docs`)
  - `scene_cube_bottle.xml` 도입 및 `scene_reach.xml` 제거
  - 파일 경로 재정리(`src/env` -> `src/env/robotis_model`)
  - GUI 마커 기본 OFF, 문서(`ENV_SETUP_NOTES.md`) 추가

## 3. 씬 구조 변경
### 3.1 유지/추가/삭제
- 유지: `src/env/robotis_model/scene.xml` (기본 베이스 씬)
- 추가: `src/env/robotis_model/scene_cube_bottle.xml` (공통 작업 씬)
- 삭제: `src/env/robotis_model/scene_reach.xml`

### 3.2 공통 작업 씬(`scene_cube_bottle.xml`) 구성
- 로봇: `omx.xml` include
- 테이블: 상판 + 4개 다리
- 물체:
  - 큐브: `object_main` (`freejoint`, `box`)
  - 물병: `object_bottle` (`freejoint`, 5-part geom: base/body/shoulder/neck/cap)
- 목표 placeholder:
  - `cube_placeholder_pad` (얇은 원판)
  - `bottle_placeholder_pad` (얇은 원판)
  - 두 패드 모두 `contype="0"`, `conaffinity="0"`로 비충돌 시각 마커
- 목표 site:
  - `cube_goal_site`
  - `bottle_goal_site`
  - `reach_target_site`

## 4. 오브젝트/목표 좌표 (현재 기준)
### 4.1 물체 초기 배치
- 큐브: `object_main pos="0.20 -0.08 0.132"`
- 병: `object_bottle pos="0.28 -0.08 0.162"`
- 두 물체는 `x`축 기준으로 나란히 배치됨 (`y=-0.08` 동일)

### 4.2 목표 placeholder 배치
- 큐브 패드: `cube_placeholder_pad pos="0.20 0.08 0.1215"` / `size="0.014 0.0015"`
- 병 패드: `bottle_placeholder_pad pos="0.28 0.08 0.1215"` / `size="0.020 0.0015"`
- 두 패드는 물체와 평행한 `x` 위치를 유지하고 로봇 오른쪽(`y>0`)에 배치됨

### 4.3 목표 site 배치
- `cube_goal_site pos="0.20 0.08 0.122"`
- `bottle_goal_site pos="0.28 0.08 0.122"`
- goal site는 각 placeholder 중심에 맞춰 배치됨

## 5. 실행 스크립트/기본값 변경
### 5.1 GUI 실행 스크립트
파일: `src/env/robotis_model/runners/view_robotis.py`
- `--scene` 선택지: `base`, `cube_bottle`
- 기본값: `cube_bottle`
- 기본 동작: site group 0 OFF
- 옵션: `--show-site-group0`를 주면 site group 0 ON
- `--dry-run` 지원 (모델 로드만 확인)

### 5.2 환경 기본 XML
파일: `src/env/robotis_model/robotis_env.py`
- `xml_path` 미지정 시 기본값:
  - `src/env/robotis_model/scene_cube_bottle.xml`

### 5.3 설정 파일 경로
파일: `configs/env/reach.yaml`
- `xml_path: src/env/robotis_model/scene_cube_bottle.xml`

## 6. GUI 데모 실행 방법
프로젝트 루트 기준:

```bash
# 1) 기본 GUI 실행 (site group 0 마커 OFF)
.venv/bin/python -m src.env.robotis_model.runners.view_robotis --scene cube_bottle
```

```bash
# 2) 마커 포함 GUI 실행 (site group 0 ON)
.venv/bin/python -m src.env.robotis_model.runners.view_robotis --scene cube_bottle --show-site-group0
```

```bash
# 3) 로드 확인만 수행 (GUI 미오픈)
.venv/bin/python -m src.env.robotis_model.runners.view_robotis --scene cube_bottle --dry-run
```

```bash
# 4) 환경 스모크 테스트
.venv/bin/python -m src.env.robotis_model.runners.smoke_test --steps 5
```

## 7. 현재 상태 체크리스트 (이 문서 기준 최신 기준 파일)
- [ ] `src/env/robotis_model/scene_cube_bottle.xml` 존재
- [ ] `src/env/robotis_model/scene.xml` 존재
- [ ] `src/env/robotis_model/scene_reach.xml` 제거됨
- [ ] `src/env/robotis_model/runners/view_robotis.py`에 `--scene cube_bottle` 기본값 적용
- [ ] `src/env/robotis_model/runners/view_robotis.py`에 site group 0 기본 OFF 적용
- [ ] `src/env/robotis_model/robotis_env.py` 기본 XML이 `scene_cube_bottle.xml`
- [ ] `configs/env/reach.yaml`의 `xml_path`가 `scene_cube_bottle.xml`
- [ ] `src/env/__init__.py`가 `robotis_model` 경로 기반 import 사용

## 8. 참고
- 이 문서는 "현재 워크트리 기준" 변경사항을 정리한 운영 메모입니다.
- task 확장(grasp, pick-and-place reward/종료 조건 분리)은 별도 task 로직 문서에서 관리 권장.
