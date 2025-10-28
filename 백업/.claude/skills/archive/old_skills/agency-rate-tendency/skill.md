---
name: agency-rate-tendency
description: |
  Analyzes reserve price rate tendencies by contracting agency (발주처별 사정률). Calculates statistical
  expected values based on historical patterns, identifies agency-specific biases, and provides strategic
  positioning recommendations. Use when analyzing specific agency bidding patterns, calculating expected
  reserve prices, or identifying favorable contracting authorities.
---

# Agency Rate Tendency - 발주처별 사정률 경향

## Overview

This skill analyzes how different contracting agencies tend to set reserve prices within the ±2% range, providing statistical insights for strategic positioning.

## Core Analysis Framework

```python
def analyze_agency_tendency(agency_name, historical_data):
    """
    발주처별 사정률 경향 학습
    분석.md: "동일 발주처의 과거 개찰결과에서 사정률의 평균과 분산 학습"
    """
    agency_data = filter_by_agency(agency_name, historical_data)

    statistics = {
        'mean_rate': calculate_mean(agency_data['reserve_rates']),
        'std_dev': calculate_std(agency_data['reserve_rates']),
        'tendency': None,
        'recommendation': None
    }

    # Classify tendency
    if statistics['mean_rate'] > 1.005:  # Above base price
        statistics['tendency'] = 'HIGH - 기초금액 상향 경향'
        statistics['recommendation'] = '높은 투찰률 고려'
    elif statistics['mean_rate'] < 0.995:  # Below base price
        statistics['tendency'] = 'LOW - 기초금액 하향 경향'
        statistics['recommendation'] = '보수적 투찰률 권장'
    else:
        statistics['tendency'] = 'NEUTRAL - 중립적'
        statistics['recommendation'] = '표준 전략 적용'

    return statistics
```

## Agency-Specific Patterns

```python
def identify_agency_patterns():
    """
    발주처별 특성 패턴
    """
    patterns = {
        '조달청': {
            'minimum_rate': 80.495,
            'tendency': 'Conservative',
            'note': '예정가격 하향 경향'
        },
        '지자체': {
            'minimum_rate': 86.745,
            'tendency': 'Variable',
            'note': '부서별 편차 존재'
        },
        '공공기관': {
            'minimum_rate': 87.745,
            'tendency': 'Stable',
            'note': '일정한 패턴 유지'
        }
    }

    return patterns
```