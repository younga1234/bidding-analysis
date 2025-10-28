---
name: logic
description: |
  복수예가입찰 AI 분석 실행 로직 (3층 구조 알고리즘).

  analyze.py 실행:
  python3 /mnt/a/25/.claude/skills/logic/analyze.py \
    --base-amount <금액> \
    --agency-rate <발주처투찰률> \
    --output-dir /mnt/a/25/data분석

  3층 확률 게임 구현:
  1층 (Phase 1-2): 몬테카를로 시뮬레이션
  2층 (Phase 3-5): 경쟁 밀도 히트맵
  3층 (Phase 6-9): 조건부 확률 최적화

  핵심 변경사항 (2025-10-26):
  - Phase 9 완전 재작성 (CDF → 조건부 확률)
  - 1위 확률 = 경쟁 밀도 역수
  - 미달 확률 무시
  - 200명 이하 필터링

  Use when: 입찰 분석 실행, 알고리즘 확인, 파라미터 조정
---

# 복수예가입찰 AI 분석 실행 로직

## ⚠️ 이 문서는 분석 알고리즘의 구현 상세입니다

> **3층 확률 게임을 코드로 구현**
>
> 1층: 예정가 분포 (몬테카를로)
> 2층: 경쟁 밀도 (히트맵)
> 3층: 조건부 확률 (베이지안 최적화)

---

## 0. 실행 방법

### 기본 실행

```bash
python3 /mnt/a/25/.claude/skills/logic/analyze.py \
  --base-amount 39000000 \
  --agency-rate 87.745 \
  --output-dir /mnt/a/25/data분석
```

### 파라미터

```
필수:
  --base-amount: 기초금액 (원)
  --agency-rate: 발주처투찰률 (%)

선택:
  --data-file: 전처리된 데이터 경로 (기본: 자동 탐지)
  --output-dir: 출력 디렉토리 (기본: /mnt/a/25/data분석)
  --monte-carlo-n: 시뮬레이션 횟수 (기본: 10000)
  --bin-size: 히트맵 구간 크기 (기본: 0.0005 = 0.05%)
  --max-competitors: 경쟁자 필터 (기본: 200)
```

### 출력 파일

```
/mnt/a/25/data분석/
├── analysis_87_745.json      # 전체 분석 결과
├── report_87_745.md           # 한글 리포트
└── competition_heatmap.png    # 경쟁 밀도 시각화
```

---

## 1. 전체 구조: 9 Phase → 3층 매핑

### 9개 Phase 개요

```
1층: 예정가 분포 파악
├── Phase 1: 몬테카를로 시뮬레이션
└── Phase 2: 과거 1위 분석

2층: 경쟁 밀도 분석
├── Phase 3: 경쟁 밀도 히트맵
├── Phase 4: 소수점 패턴
└── Phase 5: 끝자리 선호도

3층: 조건부 확률 최적화
├── Phase 6: 하한가 미달 분석
├── Phase 7: 사정율-투찰율 상관관계
├── Phase 8: IQR 범위 계산
└── Phase 9: 베이지안 최적화 (핵심!)
```

### Phase별 입출력

| Phase | 입력 | 출력 | 목적 |
|-------|------|------|------|
| 1 | 기초금액, 발주처투찰률 | 예정가 분포, 낙찰하한가 분포 | 예정가 형성 확률 |
| 2 | 과거 1위 데이터 | 통계 (중앙값, 표준편차, 백분위) | 1위 분포 참고 |
| 3 | 전체 데이터 | 0.05% 구간별 경쟁자 수 | 경쟁 밀도 히트맵 |
| 4 | 전체 데이터 | 소수점 3자리 빈도 | 차별화 포인트 |
| 5 | 전체 데이터 | 끝자리 (10원 단위) 빈도 | 회피할 끝자리 |
| 6 | 전체 데이터 | 미달률, 미달 분포 | 미달 무시 확인 |
| 7 | 전체 데이터 | 사정율-투찰율 상관계수 | 업체 심리 패턴 |
| 8 | 과거 1위 데이터 | IQR, Q1, Q3 | 현실적 범위 |
| 9 | 1+2+3층 통합 | 최적 입찰률 3개 | 조건부 확률 최적화 |

---

## 2. 핵심 알고리즘: Phase 9 상세

### 목적 함수 (NEW)

```python
max Σ P(예정가=y) × [1/N(y,x)] × R(x)

여기서:
- P(예정가=y): 몬테카를로 분포 (예정가 y 형성 확률)
- N(y,x): y~x 구간의 경쟁자 수
- R(x): 이익률 = (100-x)/100
```

### 의사 코드

```python
def phase9_bayesian_optimization():
    candidates = []

    # 탐색 범위: IQR ± 0.3%
    for bid_rate in range(87.133, 88.506, 0.001):
        expected_utility = 0.0

        # 모든 예정가 경우의 수
        for reserve_rate in monte_carlo_result:
            # 낙찰하한가
            min_win = reserve_rate * 0.87745

            # 내 입찰이 하한가 이상?
            if bid_rate >= min_win:
                # 이 구간의 경쟁자 수
                competitors = count_in_range(min_win, bid_rate)

                # 1위 확률
                p_win = 1 / (competitors + 1)

                # 예정가 확률
                p_reserve = pdf(reserve_rate)

                # 이익률
                profit = (100 - bid_rate) / 100

                # 누적
                expected_utility += p_reserve * p_win * profit

        # 경쟁 밀도 필터: 200명 이하만
        if count_in_my_bin(bid_rate) <= 200:
            candidates.append({
                'rate': bid_rate,
                'expected_utility': expected_utility
            })

    # Top 3 추출
    optimal_1 = max(candidates, key='expected_utility')
    optimal_2 = min(candidates[:3], key='competitors')
    optimal_3 = min(candidates[:3], key='rate')

    return [optimal_1, optimal_2, optimal_3]
```

### OLD vs NEW 비교

**OLD (WRONG - CDF 기반)**:
```python
p_compete = np.sum(past_rates <= x) / len(past_rates)
p_win = p_floor * p_compete * (1 - p_collision)

# 문제:
# 88.503%: p_compete = 0.858 (85.8%의 1위가 이하)
# → "90%가 이하" ≠ "90% 확률"
# → 논리 반대!
```

**NEW (CORRECT - 조건부 확률)**:
```python
for reserve_rate in reserve_dist:
    min_win = reserve_rate * agency_rate
    if bid_rate >= min_win:
        p_win = 1 / (competitors + 1)
        expected += p_reserve * p_win * profit

# 올바른 접근:
# 예정가별로
# → 그 예정가 확률
# × 그 구간 1위 확률 (1/경쟁자)
# × 이익률
```

---

## 3. 실행 예시

### 입력

```bash
기초금액: 39,000,000원
발주처투찰률: 87.745%
```

### 출력 (87.745% 그룹)

```
[Phase 1/9] 몬테카를로 시뮬레이션... ✓
예정가 범위: 86.2~89.3% (기초대비)

[Phase 2/9] 과거 1위 분석... ✓
1위 112개, 중앙값: 87.843%

[Phase 3/9] 경쟁 밀도 히트맵... ✓
최고 밀집: 87.95~88.00% (358명)
최저 밀집: 87.05~87.10% (44명)

[Phase 6/9] 하한가 미달 분석... ✓
미달: 46.2% (무시)

[Phase 9/9] 베이지안 최적화... ✓

최적 입찰률 3개:

1. 기대값 최적
   - 입찰률: 87.523%
   - 입찰금액: 34,134,000원
   - 경쟁자: 196명
   - 1위 확률: 0.51%

2. 경쟁 회피
   - 입찰률: 87.089%
   - 입찰금액: 33,965,000원
   - 경쟁자: 44명
   - 1위 확률: 2.27% (4.5배!)

3. 이익 최대
   - 입찰률: 87.089%
   - 입찰금액: 33,965,000원
   - 경쟁자: 44명
   - 1위 확률: 2.27%

→ 경쟁 회피 = 이익 최대
→ 44명 vs 196명 (4.5배 차이)
```

---

## 4. 참고 문서

**필수 참조 순서:**
1. `/mnt/a/25/.claude/skills/core/SKILL.md` - 철학
2. `/mnt/a/25/CLAUDE.md` - 프로젝트 가이드
3. `/mnt/a/25/.claude/skills/report/SKILL.md` - 리포트

**Last Updated:** 2025-10-26
**Algorithm:** 3층 확률 게임
