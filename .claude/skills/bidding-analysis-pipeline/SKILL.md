---
name: bidding-analysis-pipeline
description: |
  입찰 이미지 포괄 분석 파이프라인. /mnt/a/25/data분석/ 이미지 읽고
  20개 분석 스킬을 6단계 순차 실행 (검증→기본분석→패턴→심리→경쟁→시간).
  각 단계 결과를 다음 단계 입력으로 사용. 최종 종합 리포트 생성.
  Use when analyzing bidding images comprehensively. (project)
allowed-tools:
  - Read
  - Write
  - Bash
  - Skill
  - mcp__smithery-ai-server-sequential-thinking__sequentialthinking
---

# 입찰 분석 파이프라인

## 목적

입찰 결과 이미지를 읽고 **20개 분석 스킬을 순차적으로 실행**하여 포괄적인 입찰 전략 인사이트를 도출합니다.

## 실행 조건

- 입력: `/mnt/a/25/data분석/` 디렉토리의 입찰 이미지
- 출력: `/mnt/a/25/data분석/분석결과/` 디렉토리에 단계별 결과 저장

## 6단계 순차 파이프라인 (17개 호환 스킬)

### Phase 1: 데이터 검증 & 보정 (2개)
```
1. data-validator → 데이터 무결성 검증
2. ai-data-correction → AI 기반 데이터 보정
```

### Phase 2: 기본 통계 분석 (2개)
```
3. bidding-rate-analyzer → 투찰률 분포 분석
4. below-minimum-analyzer → 하한가 미달 분석
```

### Phase 3: 패턴 발견 (5개)
```
5. decimal-pattern-analyzer → 소수점 패턴
6. ending-digit-preference → 끝자리 선호도
7. habit-pattern-analyzer → 습관 패턴
8. randomness-analyzer → 무작위성 분석 (교육용)
9. structural-randomness-analyzer → 구조적 무작위성 (교육용)
```

### Phase 4: 심리 분석 (2개)
```
10. psychological-floor-analyzer → 심리적 바닥
11. psychological-floor-finder → 심리적 바닥가 탐지
```

### Phase 5: 경쟁 분석 (4개)
```
12. competition-intensity-analyzer → 경쟁 강도
13. competition-density-heatmap → 경쟁 밀도 히트맵
14. competitor-habit-tracker → 경쟁사 습관 추적
15. tie-bid-avoidance → 동점 회피 전략
```

### Phase 6: 시간 분석 (2개)
```
16. submission-timing-analyzer → 제출 시간 패턴
17. rate-calculation-definitions → 계산 정의 참조
```

## ⚠️ 제외된 스킬 (2개)

**number-selection-psychology**: 예비번호 선택 데이터 미포함 (전처리 시 손실)
**agency-rate-tendency**: 발주처투찰률이 고정값이므로 경향 분석 불가

## 실행 흐름

1. **이미지 읽기**: `/mnt/a/25/data분석/image.png` 등 이미지 파일 읽기
2. **데이터 추출**: 이미지에서 입찰 데이터 추출 (OCR 또는 직접 분석)
3. **순차 실행**: Phase 1 → Phase 6까지 각 스킬을 Skill tool로 호출
4. **결과 저장**: 각 단계별 분석 결과를 분석결과/ 디렉토리에 저장
5. **최종 리포트**: 모든 인사이트를 종합한 리포트 생성

## 스킬 호출 방법

각 분석 스킬은 `Skill` tool을 사용하여 호출:

```
Skill tool → command: "data-validator"
Skill tool → command: "ai-data-correction"
Skill tool → command: "bidding-rate-analyzer"
...
```

## 출력 파일 형식

- `YYYYMMDD_phase1_검증결과.md`
- `YYYYMMDD_phase2_기본분석.md`
- `YYYYMMDD_phase3_패턴분석.md`
- `YYYYMMDD_phase4_심리분석.md`
- `YYYYMMDD_phase5_경쟁분석.md`
- `YYYYMMDD_phase6_시간분석.md`
- `YYYYMMDD_종합분석리포트.md` (최종)

## 에러 처리

- 스킬 실행 실패 시 로그 기록 후 다음 스킬 계속 진행
- 치명적 오류 (이미지 없음, 데이터 추출 실패) 시 중단

## 성공 기준

✅ 모든 20개 스킬이 순차적으로 실행됨
✅ 각 Phase별 결과 파일 생성
✅ 최종 종합 리포트에 실행 가능한 전략 포함
