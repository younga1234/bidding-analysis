---
name: decimal-pattern-analyzer
description: |
  Analyzes decimal point patterns in bid rates (.000, .500 preferences). Classifies bidders by precision
  strategy (conservative .000, half-step .500, strategic random), identifies collision zones at common
  decimals, and recommends unique decimal positions. Use when analyzing bidding precision patterns,
  avoiding decimal clustering, or implementing precision differentiation strategies.
---

# Decimal Pattern Analyzer - 소수점 패턴 분석

## Overview

This skill analyzes how bidders use decimal precision, revealing strategic types through their decimal point preferences.

## Pattern Classification

```python
def classify_decimal_patterns(bid_history):
    """
    소수점 사용 패턴으로 전략 유형 분류
    분석.md: "대부분의 업체는 일정한 투찰습관을 반복합니다"
    """
    decimal_patterns = {
        '.000': 'Conservative - 정수 선호형',
        '.500': 'Half-step - 중간값 선호형',
        '.123': 'Sequential - 연속숫자형',
        '.111': 'Repetitive - 반복숫자형',
        '.random': 'Strategic - 의도적 랜덤형'
    }

    company_types = {}
    for company, bids in bid_history.items():
        decimals = [str(bid).split('.')[-1] for bid in bids]
        most_common = max(set(decimals), key=decimals.count)

        if decimals.count(most_common) > len(decimals) * 0.3:
            company_types[company] = {
                'pattern': most_common,
                'type': decimal_patterns.get(f'.{most_common}', 'Custom'),
                'predictability': 'HIGH',
                'counter_strategy': f'Avoid .{most_common}, use nearby values'
            }

    return company_types
```

## Precision Differentiation

```python
def generate_unique_decimal():
    """
    충돌 회피를 위한 독특한 소수점 생성
    """
    unique_decimals = [
        '.017', '.023', '.037', '.043',  # Prime-based
        '.067', '.073', '.083', '.097'   # Irregular
    ]

    return random.choice(unique_decimals)
```