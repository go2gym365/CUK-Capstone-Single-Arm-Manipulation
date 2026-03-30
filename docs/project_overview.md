# Project Overview

## 1. 프로젝트 제목
CUK Capstone | Single-Arm Manipulation

## 2. 프로젝트 배경
로봇 manipulation task는 로봇이 환경 내 물체를 인식하고 조작하는 핵심 문제 중 하나입니다.  
그중 single-arm manipulation은 비교적 단순한 구조를 가지면서도, 실제로는 grasp, move, place와 같은 복합적인 행동이 필요하므로 연구 및 구현 가치가 높습니다.

본 프로젝트는 시뮬레이션 기반으로 single-arm manipulation task를 정의하고,  
여러 policy learning 방법을 적용하여 task 수행 성능을 비교·개선하는 것을 목표로 합니다.

## 3. 프로젝트 목표
- manipulation task 정의
- MuJoCo 기반 시뮬레이션 환경 구축
- reward 및 success metric 설계
- BC / PPO / SAC 기반 정책 학습
- task별 성능 비교
- 최종적으로 데모 가능한 통합 파이프라인 구성

## 4. 주요 task
- Push
- Grasp
- Pick-and-Place

## 5. 기대 결과
- task별 안정적인 policy 확보
- 알고리즘 간 비교 결과 도출
- 최종 시연 가능한 manipulation demo 구성