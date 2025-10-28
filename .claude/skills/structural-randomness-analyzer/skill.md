---
name: structural-randomness-analyzer
description: |
  Analyzes the structural randomness (15C4=1,365) of Korean government multiple reserve price bidding system.
  Demonstrates why price prediction is mathematically impossible and redirects analysis to competitor behavior patterns.
  Use when users ask about predicting bid prices, calculating winning amounts, or attempting statistical price analysis
  in 나라장터 복수예가입찰 system. This skill explains the fundamental unpredictability and guides toward analyzable elements.
---

# Structural Randomness Analyzer for 복수예가입찰

## Overview

This skill provides comprehensive analysis of the structural randomness inherent in Korea's multiple reserve price bidding system (나라장터 복수예가입찰), demonstrating why mathematical price prediction is impossible and guiding analysis toward the only predictable element: human behavioral patterns.

## Core Mathematical Reality: 1/1365 Complete Randomness

### The Unbreakable Structure

The multiple reserve price system creates **structural randomness** through:
```
15 preliminary prices (예비가격) generated within ±2% of base amount
↓
4 prices randomly selected from these 15
↓
Average of these 4 = Final reserve price (예정가격)
↓
Total combinations: 15C4 = 1,365
↓
Each combination probability: 1/1365 = 0.0732%
```

This is not probabilistic randomness that can be learned or predicted through patterns.
This is **structural randomness** - hardcoded into the system architecture.

## Workflow Decision Tree

```
User Query Analysis
├── Is it about price prediction? → Phase 1: Demonstrate Impossibility
├── Is it about probability calculation? → Phase 2: Show Random Structure
├── Is it about historical patterns? → Phase 3: Redirect to Behaviors
└── Is it about strategy? → Phase 4: Focus on Distribution Control
```

## Phase 1: Demonstrate Mathematical Impossibility

When users attempt price prediction, provide this fundamental truth:

```python
# The impossible calculation
def predict_reserve_price(historical_data):
    """
    This function demonstrates why prediction is impossible
    """
    combinations = 1365
    probability_per_case = 1 / combinations  # 0.0732%

    # Even with 1000 historical cases
    # Each new case is still 1/1365 random
    # No learning possible from random selection

    return {
        "prediction_accuracy": "0.0732%",
        "method": "Pure guessing",
        "conclusion": "Mathematically equivalent to lottery"
    }
```

### Key Message
"금액 분석은 '운의 영역'이고, 이 구조 안에서 분석을 시도할수록 오히려 계산오차가 증가합니다."
(Price analysis is the 'domain of luck', and attempting analysis within this structure only increases calculation errors.)

## Phase 2: Explain the Structural Lock

### The Three Layers of Randomness

1. **예정가격 자체를 예측할 수 없다**
   - 1365가지 경우의 수 중 하나가 선택
   - No patterns, no preferences, pure random

2. **낙찰하한가도 예정가격이 결정되기 전까지는 불명확**
   - Minimum threshold rate is fixed
   - But actual threshold amount varies with reserve price
   - Cannot calculate target until after randomness resolves

3. **분석적 접근의 함정**
   - More data ≠ better prediction
   - Historical averages = meaningless
   - Statistical models = 0.0732% accuracy ceiling

## Phase 3: Redirect to Analyzable Territory

### The Fundamental Shift Required

```
무작위 요소 (Unanalyzable)          |  인간 요소 (Analyzable)
-----------------------------------|----------------------------------
예정가격 산정: Complete random      |  투찰금액 결정: Human judgment patterns
낙찰하한가: Varies with random     |  번호 선택: Human selection bias
수학적 확률: Fixed at 1/1365       |  투찰시간: Habitual behaviors
```

### Provide This Strategic Framework

**"분석 불가능한 싸움"에서의 실력 = 분포 제어력**

In an unpredictable price structure, skill equals distribution control:
1. Identify where competitors cluster (e.g., 80.50-80.55%)
2. Find gaps in the distribution
3. Position in uncrowded zones
4. Avoid tie-bid scenarios

## Phase 4: Guide Toward Behavior Analysis

### The Only Meaningful Analysis

Direct analysis toward:

```python
def analyze_competitors(bidding_history):
    """
    The only analysis that matters: human patterns
    """
    patterns = {
        "ending_digit_preference": analyze_last_digits(),  # 0, 5 bias
        "decimal_patterns": find_decimal_habits(),         # .500, .000
        "range_clustering": identify_preferred_ranges(),   # +0.1-0.2%
        "time_patterns": analyze_submission_timing(),      # Last 5 min
        "number_selection": track_number_choices()         # 10,12,15 bias
    }

    return patterns
```

### Key Insight to Emphasize

"복수예비가격 입찰은 예측의 싸움이 아니라, 사람의 습관을 파악해 겹치지 않는 자리를 선점하는 싸움이다."
(Multiple reserve price bidding is not a battle of prediction, but of understanding human habits to secure non-overlapping positions.)

## Critical Warnings and Redirections

### When Users Insist on Price Analysis

Provide clear, firm guidance:
```
⚠️ STRUCTURAL IMPOSSIBILITY ALERT

What you're attempting:
- Predicting reserve price from historical data
- Calculating probability of specific amounts
- Finding patterns in random selections

Why it cannot work:
- Each selection is independent 1/1365 random
- No correlation between past and future
- Mathematical ceiling: 0.0732% accuracy

What CAN be analyzed:
✓ Competitor clustering patterns
✓ Behavioral habits and biases
✓ Distribution gaps and opportunities
✓ Collision (tie-bid) frequencies
```

## The Professional's Approach

### Three Pillars of Actual Analysis

1. **경쟁사 투찰패턴 분석 (Competitor Pattern Analysis)**
   - Track repeated bid rates by company
   - Identify habitual ranges
   - Map submission timing patterns

2. **비선호 구간 집중투찰 (Unpopular Zone Targeting)**
   - Find gaps where few compete
   - Position between common increments
   - Exploit human preference biases

3. **예비번호 선택심리 분석 (Number Selection Psychology)**
   - Identify overselected numbers (10, 12, 15)
   - Target underselected options (2, 5, 9)
   - Reduce random collision probability

## Implementation Scripts

### scripts/demonstrate_randomness.py
```python
# Calculates and visualizes the 1,365 combinations
# Shows equal probability distribution
# Proves independence of each draw
```

### scripts/analyze_behavior_patterns.py
```python
# Extracts human behavioral patterns from bid data
# Identifies habits, preferences, and biases
# Outputs actionable positioning strategies
```

### scripts/redirect_impossible_analysis.py
```python
# Detects when user attempts impossible analysis
# Provides clear explanation of why it won't work
# Suggests correct analytical approach
```

## References for Deep Understanding

- `references/mathematical_proof.md` - Rigorous proof of 1/1365 randomness
- `references/behavioral_patterns.md` - Catalog of human bidding habits
- `references/case_studies.md` - Real examples of failed predictions vs successful positioning

## Final Essential Truth

Deliver this message consistently:

**"수학적 분석으로는 이길 수 없지만, 경쟁자 분석으로는 충분히 확률을 바꿀 수 있다."**
(You cannot win through mathematical analysis, but you can definitely change the odds through competitor analysis.)

The skill is not in predicting the unpredictable, but in finding space where others don't compete.