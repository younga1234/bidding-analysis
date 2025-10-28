---
name: submission-timing-analyzer
description: |
  Analyzes bid submission timing patterns (마감 5분전 집중). Identifies deadline rush periods with high
  collision risk, maps temporal clustering patterns, and recommends optimal submission windows. Use when
  analyzing submission time patterns, avoiding temporal collisions, or strategically timing bid submissions
  to minimize competition overlap.
---

# Submission Timing Analyzer - 시간대별 투찰 패턴

## Overview

This skill analyzes when companies submit their bids, revealing temporal clustering that creates collision risks.

## Temporal Pattern Analysis

```python
def analyze_submission_timing(company_submissions):
    """
    투찰 시간대 분석 - 습관적 행위 패턴
    분석.md: "마감직전 5분 이내 투찰 반복"
    """
    time_patterns = {
        'last_5_minutes': 'Deadline pressure type - 마감 압박형',
        'early_morning': 'Early bird type - 조기 제출형',
        'business_hours': 'Regular worker - 업무시간형',
        'random_times': 'Strategic randomizer - 의도적 분산형'
    }

    submission_times = [parse_time(s['time']) for s in company_submissions]

    # Classify by predominant pattern
    if count_last_5_min(submission_times) > 0.6:
        return {
            'type': time_patterns['last_5_minutes'],
            'behavior': '마감직전 5분 이내 투찰 반복',
            'psychology': 'Risk-taker, last-minute decision maker',
            'collision_risk': 'HIGH - many compete in final minutes'
        }
```

## Collision Risk by Time

```python
def calculate_temporal_collision_risk():
    """
    시간대별 충돌 위험도
    """
    risk_zones = {
        'T-5 to T-0': {
            'risk': 'EXTREME',
            'density': '60% of submissions',
            'strategy': 'AVOID'
        },
        'T-30 to T-10': {
            'risk': 'LOW',
            'density': '20% of submissions',
            'strategy': 'RECOMMENDED'
        },
        'T-60 to T-30': {
            'risk': 'MINIMAL',
            'density': '10% of submissions',
            'strategy': 'OPTIMAL'
        }
    }

    return risk_zones
```

## Strategic Message

**"마감 5분전 제출 = 높은 충돌 위험"**
(Submission in last 5 minutes = High collision risk)