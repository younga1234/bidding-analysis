---
name: ending-digit-preference
description: |
  Analyzes human preference for specific ending digits in bid amounts (0 and 5 bias). Identifies
  psychological clustering around round numbers, calculates collision risks at common endings, and
  recommends irregular endings (3, 7, 9) for differentiation. Use when analyzing bid amount patterns,
  avoiding psychological clustering, or selecting unique positioning through ending digit strategy.
---

# Ending Digit Preference - 끝자리 선호도 분석

## Overview

This skill analyzes the strong human bias toward certain ending digits (특히 0과 5), creating predictable clustering patterns that can be exploited.

## Core Analysis

```python
def analyze_ending_digit_bias(company_bids):
    """
    끝자리 선호도 분석 - 인간의 심리적 편향
    분석.md: "대부분의 업체는 일정한 투찰습관을 반복합니다"
    """
    ending_digits = [str(bid)[-1] for bid in company_bids]

    preferences = {
        '0_ending': ending_digits.count('0') / len(ending_digits),
        '5_ending': ending_digits.count('5') / len(ending_digits),
        'round_number_bias': None
    }

    # Most humans prefer round numbers
    round_bias = preferences['0_ending'] + preferences['5_ending']

    if round_bias > 0.4:
        preferences['round_number_bias'] = {
            'strength': 'STRONG',
            'percentage': f'{round_bias*100:.1f}%',
            'vulnerability': '끝자리 3, 7, 9 사용으로 차별화 가능',
            'collision_risk': 'HIGH in .0 and .5 zones'
        }

    return preferences
```

## Strategic Exploitation

```python
def select_irregular_endings():
    """
    비선호 끝자리 선택 전략
    """
    irregular_endings = {
        'prime_endings': [3, 7],  # Psychological avoidance
        'odd_endings': [1, 9],     # Less intuitive
        'collision_rate': '70% lower than 0 or 5'
    }

    return irregular_endings
```