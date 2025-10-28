---
name: number-selection-psychology
description: |
  Analyzes psychological biases in selecting 4 numbers from 15 preliminary prices in Korean government
  bidding. Identifies overselected numbers (10, 12, 15) and underselected options (2, 5, 9), calculates
  예정가 편향 (reserve price bias), and recommends contrarian selections to reduce collision probability.
  Use when selecting preliminary price numbers, avoiding crowd behavior, or exploiting human selection
  patterns. This skill leverages the fact that humans show predictable preferences even in supposedly
  random number selection.
---

# Number Selection Psychology - 예비번호 선택 심리 분석

## Overview

This skill analyzes the psychological patterns in how bidders select 4 numbers from 15 preliminary prices (복수예비가격), revealing that human selection is far from random and creates exploitable biases.

## The Fundamental Bias

### Numbers Are Random, Humans Are Not

**Core Insight from 분석.md**: "특정 번호(10, 12, 15 등)의 선택 빈도 분석 → 이탈 번호(2, 5, 9) 선택"
(Analyze selection frequency of certain numbers (10, 12, 15) → Choose outlier numbers (2, 5, 9))

Even when selecting from 15 equally probable options, humans show strong preferences:
- **Overselected**: 10, 12, 13, 15 (psychological comfort zones)
- **Underselected**: 2, 5, 9 (psychological avoidance zones)
- **Result**: 예정가격 becomes slightly biased toward popular selections

## Core Analysis Framework

### Phase 1: Map Selection Frequency Distribution

Analyze which numbers are most frequently selected:

```python
def analyze_number_selection_bias(historical_selections):
    """
    예비번호 선택 빈도 분석 - 인간의 선호 패턴 추출
    """
    selection_frequency = {i: 0 for i in range(1, 16)}

    for selection_set in historical_selections:
        for number in selection_set:
            selection_frequency[number] += 1

    # Categorize by popularity
    total_selections = sum(selection_frequency.values())
    bias_categories = {
        'overselected': [],   # >8% selection rate (expected: 6.67%)
        'popular': [],        # 6-8% selection rate
        'neutral': [],        # 5-6% selection rate
        'unpopular': [],      # 4-5% selection rate
        'underselected': []   # <4% selection rate
    }

    for number, count in selection_frequency.items():
        rate = (count / total_selections) * 100

        if rate > 8:
            bias_categories['overselected'].append({
                'number': number,
                'rate': rate,
                'bias_factor': rate / 6.67,  # Expected is 6.67%
                'risk': 'HIGH - Many competitors will select'
            })
        # ... categorize other ranges

    return bias_categories
```

### Phase 2: Identify Psychological Patterns

Common selection behaviors that create bias:

```python
def identify_selection_patterns():
    """
    인간의 번호 선택 심리 패턴 식별
    """
    patterns = {
        'middle_preference': {
            'numbers': [6, 7, 8, 9, 10],
            'reason': '중간값 선호 - 극단 회피 성향',
            'frequency': 'HIGH'
        },
        'round_number_bias': {
            'numbers': [5, 10, 15],
            'reason': '5의 배수 선호 - 단순성 편향',
            'frequency': 'MODERATE-HIGH'
        },
        'lucky_number_effect': {
            'numbers': [7, 13],
            'reason': '행운/불운 숫자 인식',
            'frequency': 'VARIABLE'
        },
        'edge_avoidance': {
            'numbers': [1, 2, 14, 15],
            'reason': '극단값 회피 심리',
            'frequency': 'LOW',
            'opportunity': 'HIGH - Use for differentiation'
        },
        'sequential_selection': {
            'pattern': '연속 번호 선택 (예: 6,7,8,9)',
            'reason': '인지적 편의성',
            'frequency': 'MODERATE'
        }
    }

    return patterns
```

### Phase 3: Calculate Reserve Price Bias Impact

How selection bias affects the final 예정가격:

```python
def calculate_price_bias_impact(popular_numbers, price_distribution):
    """
    인기 번호 편중이 예정가격에 미치는 영향 계산
    """
    # If many select the same 4 numbers, those prices have higher
    # probability of forming the reserve price

    bias_scenarios = {}

    # Scenario 1: Crowd follows popular numbers
    crowd_selection = [10, 12, 13, 15]  # Most popular
    crowd_avg = calculate_average(crowd_selection, price_distribution)

    # Scenario 2: Contrarian selects unpopular
    contrarian_selection = [2, 5, 9, 14]  # Least popular
    contrarian_avg = calculate_average(contrarian_selection, price_distribution)

    # Scenario 3: Random selection (theoretical)
    random_avg = sum(price_distribution) / 15  # True average

    return {
        'crowd_bias': crowd_avg - random_avg,
        'contrarian_bias': contrarian_avg - random_avg,
        'spread': abs(crowd_avg - contrarian_avg),
        'strategic_advantage': 'Select contrarian to avoid crowded price zones'
    }
```

## Strategic Selection Methodologies

### The Contrarian Approach

Exploit crowd bias by selecting underutilized numbers:

```python
def generate_contrarian_selection(crowd_preferences):
    """
    군중 심리와 반대로 움직이는 전략적 선택
    """
    # Identify least selected numbers
    all_numbers = set(range(1, 16))
    popular_numbers = set(crowd_preferences['overselected'])

    # Target underselected numbers
    contrarian_pool = all_numbers - popular_numbers

    # Strategic selection rules
    selection_strategy = {
        'primary': [],     # Least selected numbers
        'secondary': [],   # Edge numbers (1, 2, 14, 15)
        'tactical': []     # Numbers that break patterns
    }

    # Rule 1: Include at least 2 edge numbers
    edge_numbers = [1, 2, 14, 15]
    selection_strategy['secondary'] = random.sample(edge_numbers, 2)

    # Rule 2: Include underselected middle numbers
    underselected_middle = [n for n in [5, 9] if n in contrarian_pool]
    selection_strategy['primary'] = underselected_middle

    # Rule 3: Avoid any sequential patterns
    final_selection = avoid_sequential(selection_strategy)

    return {
        'numbers': final_selection,
        'rationale': '군중과 겹치지 않는 예정가격 형성 유도',
        'collision_reduction': 'Estimated 60-70% lower collision rate'
    }
```

### Pattern-Breaking Selection

Deliberately violate human tendencies:

```python
def pattern_breaking_selection():
    """
    인간의 자연스러운 선택 패턴을 의도적으로 깨트리기
    """
    strategies = {
        'prime_number_focus': {
            'numbers': [2, 3, 5, 7, 11, 13],
            'select': 4,
            'reason': 'Humans rarely think in primes'
        },
        'fibonacci_sequence': {
            'numbers': [1, 2, 3, 5, 8, 13],
            'select': 4,
            'reason': 'Mathematical pattern most don't recognize'
        },
        'extreme_edges': {
            'numbers': [1, 2, 14, 15],
            'select': 4,
            'reason': 'Maximum psychological discomfort = minimum competition'
        },
        'skip_pattern': {
            'numbers': [2, 5, 8, 11, 14],
            'select': 4,
            'reason': 'Every third number - unnatural for humans'
        }
    }

    # Select strategy based on competition analysis
    if high_competition:
        return strategies['extreme_edges']
    else:
        return strategies['skip_pattern']
```

## Psychological Exploitation Techniques

### The Comfort Zone Map

Understanding where competitors feel "safe":

```python
def map_psychological_comfort_zones():
    """
    경쟁자들이 심리적으로 편안하게 느끼는 번호 구간
    """
    comfort_zones = {
        'high_comfort': {
            'range': [8, 9, 10, 11, 12],
            'selection_rate': '45%',
            'reason': '중간값 + 안정감',
            'strategy': 'AVOID - Highest competition'
        },
        'moderate_comfort': {
            'range': [5, 6, 7, 13, 14],
            'selection_rate': '35%',
            'reason': '준중간값',
            'strategy': 'USE SPARINGLY'
        },
        'discomfort': {
            'range': [1, 2, 3, 4, 15],
            'selection_rate': '20%',
            'reason': '극단값 불안감',
            'strategy': 'TARGET - Lowest competition'
        }
    }

    return comfort_zones
```

### Cultural Number Preferences

Korean-specific number psychology:

```python
def analyze_cultural_preferences():
    """
    한국 특유의 숫자 선호도 분석
    """
    cultural_factors = {
        'lucky_numbers': {
            'numbers': [3, 7, 8],
            'reason': '문화적 길한 숫자',
            'impact': 'Slightly higher selection'
        },
        'unlucky_numbers': {
            'numbers': [4, 13],
            'reason': '죽음(4), 서양 불운(13)',
            'impact': 'Lower selection rate',
            'opportunity': 'Use 4 for differentiation'
        },
        'round_preference': {
            'numbers': [5, 10, 15],
            'reason': '단위 선호',
            'impact': 'Significant overselection'
        }
    }

    return cultural_factors
```

## Implementation Workflow

### Complete Number Selection Pipeline

```python
def execute_strategic_number_selection(bidding_context):
    """
    전략적 예비번호 선택 실행
    """
    # Step 1: Analyze historical patterns
    historical_bias = analyze_number_selection_bias(
        bidding_context['past_selections']
    )

    # Step 2: Identify current competition level
    competition_intensity = assess_competition(
        bidding_context['participant_count']
    )

    # Step 3: Map psychological patterns
    psych_patterns = identify_selection_patterns()
    comfort_zones = map_psychological_comfort_zones()

    # Step 4: Generate selection strategy
    if competition_intensity > 0.7:  # High competition
        strategy = 'extreme_contrarian'
        selection = generate_contrarian_selection(historical_bias)
    elif competition_intensity > 0.4:  # Moderate
        strategy = 'pattern_breaker'
        selection = pattern_breaking_selection()
    else:  # Low competition
        strategy = 'balanced'
        selection = balanced_selection()

    # Step 5: Validate and adjust
    final_selection = validate_selection(selection, constraints)

    return {
        'selected_numbers': final_selection,
        'strategy_used': strategy,
        'expected_collision_reduction': calculate_collision_reduction(final_selection),
        'psychological_distance': measure_distance_from_crowd(final_selection),
        'confidence': assess_selection_confidence(final_selection)
    }
```

## Critical Success Metrics

### Selection Differentiation Index

Measure how different your selection is from the crowd:

```python
def calculate_differentiation_index(your_selection, crowd_average):
    """
    군중과의 차별화 지수 계산
    """
    # Higher index = less collision probability

    overlap_count = len(set(your_selection) & set(crowd_average))
    differentiation = 1 - (overlap_count / 4)

    return {
        'index': differentiation,
        'interpretation': {
            '>0.75': 'Excellent - Minimal collision risk',
            '0.50-0.75': 'Good - Moderate differentiation',
            '0.25-0.50': 'Poor - High collision risk',
            '<0.25': 'Critical - Following the crowd'
        }
    }
```

## Scripts Usage

### scripts/analyze_selection_patterns.py
```python
# Analyze historical number selection patterns
# Input: past bidding data with number selections
# Output: bias distribution and recommendations
```

### scripts/generate_contrarian_selection.py
```python
# Generate strategic number selection
# Input: crowd preferences, competition level
# Output: optimized 4-number selection
```

## References

- `references/selection_psychology.md` - Detailed psychological patterns in number selection
- `references/cultural_factors.md` - Korean-specific number preferences
- `references/historical_bias.md` - Statistical analysis of selection frequencies

## Strategic Warnings

### The Selection Paradox

```
⚠️ CRITICAL: Popular Numbers Create Popular Prices ⚠️

When everyone selects 10, 12, 13, 15:
- These prices have higher weight in reserve price
- More competitors cluster around this price zone
- Collision probability increases dramatically

Solution: Be where others are not.
```

### The Ultimate Truth

**"다수가 뽑는 복수예가번호 조합(예: 10, 12 / 13, 15)을 분석하여 피한다"**
(Analyze and avoid the preliminary number combinations that many select)

In a random system, the only edge is being different from the crowd.
