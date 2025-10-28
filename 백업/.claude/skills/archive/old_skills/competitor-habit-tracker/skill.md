---
name: competitor-habit-tracker
description: |
  Tracks and analyzes repetitive behavioral patterns of competing companies in Korean government bidding.
  Identifies habitual bid rates, ending digit preferences, decimal patterns, time-of-submission habits,
  and number selection biases. Use when analyzing specific competitors, predicting company behaviors,
  identifying collision risks, or developing counter-strategies. This skill reveals that while prices
  are random, human behaviors are predictable patterns that can be exploited for strategic advantage.
---

# Competitor Habit Tracker - 경쟁업체 습관 추적기

## Overview

This skill analyzes the only predictable element in the structurally random Korean government bidding system: human behavioral patterns. It tracks and predicts competitor habits to find non-overlapping bidding positions and avoid tie-bid collisions.

## The Fundamental Truth

### Numbers are Random, Humans are Not

**"숫자는 무작위지만, 사람은 무작위로 움직이지 않기 때문입니다"**
(Numbers are random, but humans don't move randomly)

In the 복수예가 system where price prediction is impossible (1/1365), the ONLY analyzable variable is:
**업체행동패턴 (Company Behavioral Patterns)**

## Core Tracking Framework

### What Can and Cannot Be Analyzed

```
불가능한 분석 (Random)              |  가능한 분석 (Human Patterns)
-----------------------------------|----------------------------------
예정가격 산정: 완전 무작위          |  투찰금액 결정: 인간의 판단 반복
낙찰하한가: 값은 무작위            |  번호 선택 패턴: 인간의 선택 기억 경향
수학적 확률: 고정 1/1365           |  투찰시점, 시간대: 습관적 행위
```

## Phase 1: Identify Repetitive Bidding Patterns

### The Habit Detection Algorithm

```python
def detect_bidding_habits(company_history):
    """
    동일 업체의 반복 투찰패턴 추출
    대부분의 업체는 일정한 투찰습관을 반복합니다
    """
    patterns = {
        'bid_rate_habit': None,      # 항상 낙찰하한가 + 0.1 ~ 0.2%
        'number_preference': None,    # 같은 구간 번호 반복 선택 (6,8 / 12,13)
        'time_pattern': None,         # 마감직전 5분 이내 투찰 반복
        'decimal_habit': None         # 특정 소수점 선호 (.000, .500)
    }

    # Analyze bid rate consistency
    bid_rates = company_history['bid_rates']
    if std(bid_rates) < 0.1:  # Low variance = habit
        patterns['bid_rate_habit'] = {
            'type': '고정 투찰률형',
            'range': f'{mean(bid_rates):.3f} ± 0.1%',
            'predictability': 'HIGH',
            'example': '동일 발주처에서 항상 80.6% 수준으로 투찰'
        }

    return patterns
```

### Critical Insight
"그 업체는 예정가격이 바뀌어도 동일 비율에 가깝게 움직입니다"
(That company moves close to the same rate even when the reserve price changes)

## Phase 2: Track Ending Digit Preferences

### The Human Bias in Number Selection

```python
def analyze_ending_digit_bias(company_bids):
    """
    끝자리 선호도 분석 - 인간의 심리적 편향
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

## Phase 3: Map Decimal Pattern Habits

### Precision Patterns Reveal Strategy Types

```python
def classify_decimal_patterns(bid_history):
    """
    소수점 사용 패턴으로 전략 유형 분류
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

## Phase 4: Time Submission Analysis

### When They Bid Reveals How They Think

```python
def analyze_submission_timing(company_submissions):
    """
    투찰 시간대 분석 - 습관적 행위 패턴
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

## Phase 5: Number Selection Psychology

### The Numbers They Choose Reveal Their Thinking

```python
def analyze_number_selection_bias(company_selections):
    """
    예비번호 선택심리 분석
    """
    popular_numbers = [10, 12, 13, 15]  # 다수가 선호
    unpopular_numbers = [2, 5, 9]        # 소수가 선택

    selection_pattern = {
        'follows_crowd': [],
        'contrarian': [],
        'mixed': []
    }

    for company, numbers in company_selections.items():
        popular_rate = sum(1 for n in numbers if n in popular_numbers) / len(numbers)

        if popular_rate > 0.7:
            selection_pattern['follows_crowd'].append({
                'company': company,
                'pattern': '특정 번호(10, 12, 15) 선택 빈도 높음',
                'risk': '예정가 편향 발생 가능',
                'strategy': '이탈 번호(2, 5, 9) 선택으로 차별화'
            })
```

## Phase 6: Build Competitor Profiles

### Complete Behavioral Fingerprint

```python
def build_competitor_profile(company_name, all_data):
    """
    경쟁업체 완전 행동 프로파일 구축
    """
    profile = {
        'company': company_name,
        'total_bids': count_bids(company_name, all_data),
        'habits': {
            'bid_rate': detect_bidding_habits(company_name, all_data),
            'ending_digits': analyze_ending_digit_bias(company_name, all_data),
            'decimals': classify_decimal_patterns(company_name, all_data),
            'timing': analyze_submission_timing(company_name, all_data),
            'numbers': analyze_number_selection_bias(company_name, all_data)
        },
        'predictability_score': calculate_predictability(habits),
        'collision_risk': assess_collision_risk(habits),
        'counter_strategy': generate_counter_strategy(habits)
    }

    return profile
```

## Strategic Implementation

### The Distribution Control Principle

**"분석 불가능한 싸움 구조에서는, 실력 = 분포제어력"**
(In an unanalyzable fight structure, skill = distribution control capability)

To win through behavior analysis:
1. **Identify clustering zones**: 경쟁자들이 가장 많이 몰리는 투찰률 (e.g., 80.50~80.55%)
2. **Find behavioral gaps**: 낙찰하한가 대비 "+0.08~0.12%" 구간 확보
3. **Exploit biases**: 다수가 뽑는 복수예가번호 조합을 피함

### Collision Avoidance Through Habit Analysis

```python
def avoid_tie_bid_collision(target_company_profile, my_planned_bid):
    """
    동가입찰 회피 전략 - 습관 분석을 통한 충돌 방지
    """
    # If target company has strong habits
    if target_company_profile['predictability_score'] > 0.7:
        predicted_bid = target_company_profile['habits']['bid_rate']['range']

        if abs(my_planned_bid - predicted_bid) < 0.01:  # Within 0.01%
            return {
                'warning': 'HIGH COLLISION RISK',
                'reason': '경쟁사 투찰패턴과 겹침',
                'recommendation': 'Adjust by +0.005% or -0.005%',
                'explanation': '분석적으로 완벽히 같은 위치로 투찰하면 50% 추첨'
            }
```

## Implementation Scripts

### scripts/track_competitor_habits.py
```python
# Tracks all behavioral patterns for specified competitors
# Builds comprehensive habit profiles
# Updates patterns with each new bid
```

### scripts/predict_next_bid.py
```python
# Predicts likely bid ranges based on historical habits
# Calculates collision probabilities
# Suggests optimal positioning
```

### scripts/find_behavioral_gaps.py
```python
# Identifies zones where few competitors operate
# Maps habit-based clustering
# Finds strategic positioning opportunities
```

## References

- `references/habit_catalog.md` - Comprehensive catalog of observed habits
- `references/collision_cases.md` - Historical tie-bid collision analysis
- `references/profile_templates.md` - Standard competitor profiling formats

## Critical Warnings

### The Habit Trap

```
⚠️ BEWARE OF YOUR OWN HABITS ⚠️

While tracking others, remember:
- Your patterns are also being tracked
- Predictability = Vulnerability
- Occasionally break your own patterns
- Mix strategic randomness with analysis
```

## The Ultimate Strategic Truth

Always remember and apply:

**"무작위 가격이 아니라 습관화된 사람의 확률을 계산해야 합니다"**
(You must calculate not random prices, but the probability of habituated humans)

**"고수 낙찰자들은 경쟁사 투찰패턴을 분석해 겹치지 않는 위치를 찾아내는 것에 집중합니다"**
(Expert winners focus on analyzing competitor patterns to find non-overlapping positions)

In a system where the price is unknowable, knowing your competitors' habits is the only real edge.