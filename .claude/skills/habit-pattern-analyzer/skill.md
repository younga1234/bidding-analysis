---
name: habit-pattern-analyzer
description: |
  업체별 투찰 습관 패턴 분석. 끝자리 0, 5 선호도, 특정 소수점 반복 사용,
  고정 투찰률 패턴 등 인간의 심리적 습관을 추적하여 예측 가능한 행동 패턴 도출.
  Use when analyzing company bidding habits or repetitive patterns. (project)
allowed-tools:
  - Read
  - Grep
  - Bash
  - mcp__smithery-ai-server-sequential-thinking__sequentialthinking
---

# 투찰 습관 패턴 분석기

## 핵심 개념

"인간은 습관의 동물" - 무작위로 보이는 투찰에도 반복되는 패턴 존재

## 추적 대상 습관

### 1. 끝자리 선호도
```python
def analyze_last_digit_preference(company_bids):
    """끝자리 0, 5 선호 패턴"""
    last_digits = [str(bid)[-1] for bid in company_bids]

    preferences = {
        "0_ending": last_digits.count("0") / len(last_digits),
        "5_ending": last_digits.count("5") / len(last_digits),
        "random_ending": 1 - (last_digits.count("0") + last_digits.count("5")) / len(last_digits)
    }

    if preferences["0_ending"] + preferences["5_ending"] > 0.4:
        return "강한 끝자리 습관 보유"
```

### 2. 소수점 패턴
```python
def analyze_decimal_pattern(company_bids):
    """소수점 이하 반복 패턴"""
    decimals = [str(bid).split(".")[-1] if "." in str(bid) else "000" for bid in company_bids]

    # 자주 사용하는 소수점
    common_decimals = [
        "000",  # 정수
        "500",  # 0.5
        "123",  # 연속숫자
        "111",  # 같은 숫자
        "777",  # 행운숫자
    ]

    pattern_score = sum(1 for d in decimals if d in common_decimals) / len(decimals)

    if pattern_score > 0.3:
        return "예측 가능한 소수점 습관"
```

### 3. 구간 집중도
```python
def analyze_range_concentration(company_bids, lower_limit):
    """특정 구간 반복 투찰"""
    # 하한가 대비 투찰률 계산
    rates = [(bid - lower_limit) / lower_limit * 100 for bid in company_bids]

    # 0.5% 단위로 구간 분할
    ranges = {}
    for rate in rates:
        range_key = round(rate * 2) / 2  # 0.5% 단위
        ranges[range_key] = ranges.get(range_key, 0) + 1

    # 가장 많이 사용한 구간
    favorite_range = max(ranges, key=ranges.get)
    concentration = ranges[favorite_range] / len(rates)

    if concentration > 0.4:
        return f"하한가 +{favorite_range}% 구간 집중 ({concentration:.1%})"
```

### 4. 고정 전략 탐지
```python
def detect_fixed_strategy(company_bids):
    """동일 투찰률 반복 사용"""
    rates = []
    for i in range(len(company_bids) - 1):
        if company_bids[i] > 0 and company_bids[i+1] > 0:
            rate_diff = abs(company_bids[i+1] - company_bids[i]) / company_bids[i]
            rates.append(rate_diff)

    # 변동률이 0.1% 미만인 경우
    fixed_count = sum(1 for r in rates if r < 0.001)

    if fixed_count / len(rates) > 0.5:
        return "고정 투찰률 전략 사용"
```

### 5. 시간대별 패턴
```python
def analyze_time_pattern(bid_times):
    """특정 시간대 선호"""
    hours = [bid_time.hour for bid_time in bid_times]

    morning = sum(1 for h in hours if 9 <= h < 12)
    afternoon = sum(1 for h in hours if 14 <= h < 17)

    if morning / len(hours) > 0.6:
        return "오전 집중 투찰 습관"
    elif afternoon / len(hours) > 0.6:
        return "오후 집중 투찰 습관"
```

## 실행 예시

```
[습관 패턴 분석 결과]

업체: (주)한국건설

1. 끝자리 습관: 0 또는 5로 끝나는 금액 65% 사용
2. 소수점 패턴: .500 사용률 45%
3. 구간 집중: 하한가 +0.5~1.0% 구간 70% 집중
4. 고정 전략: 최근 10회 중 8회 동일 투찰률
5. 시간 패턴: 오전 10-11시 집중 (80%)

⚠️ 예측 가능성: 높음
→ 추천: 이 업체와 경쟁 시 습관 구간 회피
```

## 활용 전략

1. **습관 역이용**: 상대가 선호하는 구간 회피
2. **차별화**: 비선호 소수점 사용으로 차별화
3. **교란**: 가끔 습관 구간 침입으로 교란
4. **학습**: 성공 업체의 습관 벤치마킹

## 주의사항

- 습관은 변할 수 있음 (최근 데이터 중시)
- 너무 많은 업체의 습관이 겹치면 오히려 경쟁 심화
- 자신의 습관도 노출될 수 있음에 유의