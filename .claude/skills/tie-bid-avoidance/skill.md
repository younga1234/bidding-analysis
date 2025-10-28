---
name: tie-bid-avoidance
description: |
  Analyzes and prevents tie-bid collisions (동가입찰) in Korean government bidding where identical
  bids result in 50% random selection. Calculates collision probabilities, identifies safe bidding
  zones, and recommends precise bid adjustments to 0.001% accuracy. Use when positioning bids to
  avoid exact matches with competitors, calculating collision risk, or optimizing bid placement in
  crowded competitive zones. This skill is essential because winning shifts from 100% to 50%
  probability when tie-bids occur.
---

# Tie-Bid Avoidance Strategy - 동가입찰 회피 전략

## Overview

This skill prevents the most critical failure mode in Korean government bidding: tie-bid collisions (동가입찰) where identical bid amounts trigger random 50/50 selection, destroying analytical advantage.

## The Fundamental Problem

### Why Tie-Bids Are Fatal

In 나라장터 bidding rules:
1. **낙찰하한가 이상, 가장 근접한 금액** → Winner
2. **동점(동일금액) 발생 시 자동추첨** → 50% random chance
3. **하한가 미달 시 자동탈락** → Disqualified

**Critical Truth**: "분석적으로 완벽히 같은 위치로 투찰하면, 이길 가능성은 동전 던지기 확률(50%)로 떨어집니다"
(If you bid at analytically the same position, winning probability drops to coin-flip 50%)

## Core Collision Detection Framework

### Phase 1: Map Competition Clustering Zones

Identify where competitors concentrate their bids:

```python
def identify_collision_zones(historical_bids):
    """
    경쟁자들이 가장 많이 몰리는 투찰률 구간 식별
    """
    collision_zones = {
        'extreme_danger': [],  # 3+ companies expected
        'high_risk': [],      # 2 companies expected
        'moderate': [],       # 1 company expected
        'safe': []           # 0-1 companies expected
    }

    # Common clustering patterns from 분석.md
    danger_zones = [
        {'range': (80.50, 80.55), 'reason': '대부분 하한가 근처 집중'},
        {'range': (80.495, 80.505), 'reason': '심리적 반올림 효과'},
        {'range': (80.60, 80.61), 'reason': '안전마진 표준값'}
    ]

    return analyze_density(historical_bids, danger_zones)
```

### Phase 2: Calculate Exact Collision Probability

For any given bid rate, calculate tie-bid risk:

```python
def calculate_collision_probability(bid_rate, competitor_patterns):
    """
    특정 투찰률에서 동가입찰 발생 확률 계산
    0.001% 단위까지 정밀 분석
    """
    # Key insight: Most companies round to 0.01% or 0.005%
    # Precision bidders use 0.001% to avoid collisions

    collision_risk = 0
    precision = 0.001  # 0.001% accuracy

    for company in competitor_patterns:
        if abs(company['expected_rate'] - bid_rate) < precision:
            collision_risk += company['probability']

    return {
        'rate': bid_rate,
        'collision_probability': collision_risk,
        'expected_competitors': collision_risk * len(competitor_patterns),
        'recommendation': generate_avoidance_strategy(collision_risk)
    }
```

### Phase 3: Find Non-Overlapping Positions

The core strategy from expert bidders:

```python
def find_safe_bidding_position(target_range, competitor_data):
    """
    경쟁사와 겹치지 않는 위치 찾기
    고수 낙찰자들의 핵심 전략
    """
    # Start from 낙찰하한가 and scan upward
    min_rate = target_range['minimum_threshold']
    max_rate = min_rate + 0.5  # Typically within 0.5%

    safe_positions = []
    step = 0.001  # 0.001% increments

    current = min_rate
    while current <= max_rate:
        collision_prob = calculate_collision_probability(current, competitor_data)

        if collision_prob['collision_probability'] < 0.1:  # Less than 10% risk
            safe_positions.append({
                'rate': current,
                'risk': collision_prob['collision_probability'],
                'safety_score': 1 - collision_prob['collision_probability']
            })

        current += step

    # Sort by safety score, return top positions
    return sorted(safe_positions, key=lambda x: x['safety_score'], reverse=True)[:5]
```

## Practical Implementation Patterns

### The Distribution Control Principle

From 분석.md: **"분석 불가능한 싸움 구조에서는, 실력 = 분포제어력"**
(In an unanalyzable fight structure, skill = distribution control capability)

To execute distribution control:

1. **Identify clustering zones** where 3+ competitors concentrate
2. **Find distribution gaps** between common bid increments
3. **Position precisely** using 0.001% adjustments
4. **Verify uniqueness** against known competitor patterns

### Precision Bidding Techniques

```python
def apply_precision_adjustment(base_rate):
    """
    0.001% 단위 정밀 조정으로 충돌 회피
    """
    # Avoid common endings that cause collisions
    dangerous_endings = ['.000', '.500', '.100']  # High collision
    safe_endings = ['.017', '.023', '.037', '.043']  # Low collision

    # Convert to precise decimal
    rate_str = f"{base_rate:.3f}"

    # Check if adjustment needed
    for danger in dangerous_endings:
        if rate_str.endswith(danger[1:]):  # Skip the dot
            # Apply safe adjustment
            adjustment = random.choice([0.003, 0.007, 0.013, 0.017])
            return base_rate + adjustment

    return base_rate
```

## Advanced Collision Patterns

### Temporal Collision Analysis

Bids submitted at the same time often cluster:

```python
def analyze_temporal_collisions(submission_times):
    """
    마감 5분전 제출 → 높은 충돌 위험
    """
    deadline_rush = []  # Last 5 minutes
    early_birds = []    # First 30% of time

    for bid in submission_times:
        if bid['minutes_before_deadline'] <= 5:
            deadline_rush.append(bid)

    # Companies submitting in last 5 min often collide
    collision_multiplier = len(deadline_rush) / total_bids

    return {
        'deadline_collision_risk': collision_multiplier,
        'safe_submission_window': 'T-30 to T-10 minutes',
        'danger_window': 'T-5 to T-0 minutes'
    }
```

### Psychological Number Avoidance

Humans prefer certain numbers, creating collision patterns:

```python
def avoid_psychological_clustering():
    """
    인간의 숫자 선호 패턴을 피하는 전략
    """
    # High collision zones (psychological preferences)
    avoid_these = {
        'round_numbers': [80.50, 80.55, 80.60],  # .00 and .05 endings
        'halfway_points': [80.525, 80.575],       # .025 and .075
        'common_safety': [80.51, 80.52, 80.53]    # +0.01 increments
    }

    # Low collision zones (psychological avoidance)
    target_these = {
        'prime_endings': [80.507, 80.513, 80.517, 80.523],
        'irregular': [80.511, 80.519, 80.527, 80.531],
        'precise': [80.5037, 80.5043, 80.5067, 80.5073]
    }

    return target_these
```

## Implementation Workflow

### Complete Collision Avoidance Pipeline

```python
def execute_collision_avoidance(bid_request):
    """
    Complete tie-bid avoidance strategy execution
    """
    # Step 1: Analyze competition
    competitors = analyze_competitor_patterns(bid_request['participants'])

    # Step 2: Map collision zones
    danger_zones = identify_collision_zones(bid_request['historical_data'])

    # Step 3: Calculate base position
    base_rate = bid_request['minimum_threshold'] + 0.1  # Starting point

    # Step 4: Check collision probability
    collision_risk = calculate_collision_probability(base_rate, competitors)

    # Step 5: Find safe alternatives if risky
    if collision_risk['collision_probability'] > 0.15:  # >15% risk
        safe_positions = find_safe_bidding_position(
            bid_request,
            competitors
        )
        recommended = safe_positions[0]['rate']
    else:
        recommended = base_rate

    # Step 6: Apply precision adjustment
    final_rate = apply_precision_adjustment(recommended)

    return {
        'recommended_rate': final_rate,
        'collision_probability': collision_risk['collision_probability'],
        'safety_analysis': generate_safety_report(final_rate, competitors),
        'precision': '0.001%',
        'confidence': calculate_confidence(collision_risk)
    }
```

## Critical Success Factors

### The 0.001% Advantage

**Key Insight**: "대부분 0.01% 단위로 입찰하지만, 전문가는 0.001% 단위로 미세조정한다"
(Most bid in 0.01% units, but experts fine-tune in 0.001% units)

This 10x precision advantage creates unique positions:
- 80.517% instead of 80.52%
- 80.5043% instead of 80.50%
- 80.5237% instead of 80.52%

### Collision Risk Thresholds

| Risk Level | Collision Probability | Action Required |
|------------|---------------------|-----------------|
| Extreme | >30% | Mandatory repositioning |
| High | 20-30% | Strong repositioning recommended |
| Moderate | 10-20% | Precision adjustment advised |
| Low | 5-10% | Optional fine-tuning |
| Safe | <5% | Maintain position |

## Scripts Usage

### scripts/calculate_collision_probability.py
```python
# Calculate exact tie-bid risk for any rate
# Input: bid_rate, competitor_data
# Output: collision probability and recommendations
```

### scripts/find_safe_zones.py
```python
# Scan full range to identify low-collision zones
# Input: minimum_threshold, competitor_patterns
# Output: ranked list of safe positions
```

### scripts/precision_optimizer.py
```python
# Apply 0.001% adjustments for collision avoidance
# Input: base_rate, collision_data
# Output: optimized rate with minimal collision risk
```

## References

- `references/collision_patterns.md` - Historical tie-bid collision analysis
- `references/precision_examples.md` - Real cases of 0.001% positioning success
- `references/clustering_psychology.md` - Human number preference patterns

## Strategic Warnings

### Never Ignore Collision Risk

```
⚠️ CRITICAL: 동가입찰 = 50% 확률 = 분석 무효화 ⚠️

A tie-bid immediately converts your analysis into a coin flip.
All analytical advantage disappears in random selection.
Even 0.001% separation maintains 100% analytical control.
```

### The Ultimate Truth

**"고수 낙찰자들은 경쟁사 투찰패턴을 분석해 겹치지 않는 위치를 찾아내는 것에 집중합니다"**
(Expert winners focus on analyzing competitor patterns to find non-overlapping positions)

In a system where the price is unknowable, avoiding collisions is the only controllable factor.