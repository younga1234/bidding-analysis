---
name: psychological-floor-analyzer
description: |
  Analyzes below-minimum bid data as market psychological floor indicators in Korean government bidding.
  Interprets failed bids not as errors but as crucial market sentiment data showing where competitors
  draw their risk boundaries. Use when analyzing 하한가 미달 (below-minimum) data, calculating market
  temperature, identifying psychological safety zones, or understanding collective bidding psychology.
  This skill reveals the invisible market fear line and competition intensity through failure patterns.
---

# Psychological Floor Analyzer - 심리적 바닥선 분석기

## Overview

This skill analyzes below-minimum bid data (하한가 미달) in the Korean government bidding system, treating these "failures" as the most valuable market psychology indicators that reveal where the collective market draws its risk boundaries.

## Fundamental Paradigm Shift

### The Critical Insight

**"하한가 미달 데이터는 실패가 아니라 시장의 심리적 나침반이다"**
(Below-minimum data is not failure, but the market's psychological compass)

What below-minimum data truly reveals:
- **심리적 바닥선**: Where the market collectively believes is "too dangerous"
- **경쟁 강도**: How aggressively competitors are pushing boundaries
- **집단 공포선**: The collective fear threshold of the market
- **다음 회차 예측**: Where competition will cluster in future rounds

## Core Analysis Framework

### Phase 1: Extract the Psychological Floor

```python
def find_psychological_floor(bidding_data):
    """
    하한가 미달 데이터에서 시장 심리적 바닥 추출
    """
    below_minimum = bidding_data[bidding_data['status'] == 'below_minimum']

    if below_minimum.empty:
        return {
            'interpretation': '미달 없음 = 극도로 보수적 시장',
            'strategy': '공격적 접근 가능'
        }

    # 심리적 바닥 = 미달 중 가장 높은 투찰률
    psychological_floor = below_minimum['bid_rate'].max()
    actual_minimum = bidding_data['minimum_threshold'].iloc[0]

    return {
        'psychological_floor': psychological_floor,
        'actual_minimum': actual_minimum,
        'safety_margin': actual_minimum - psychological_floor,
        'interpretation': f'시장은 {actual_minimum - psychological_floor:.3f}% 를 위험선으로 인식'
    }
```

### Key Message
"어디까지 내려가면 죽는지를 보여주는 데이터가 하한 미달 데이터입니다"
(Below-minimum data shows exactly where the death line is)

## Phase 2: Calculate Competition Intensity

### The Temperature Gauge Formula

```
경쟁강도 = (하한미달업체수 / 전체참여업체수) × 100
```

Interpret the market temperature:

```python
def calculate_market_temperature(miss_rate):
    """
    하한 미달 비율로 시장 온도 측정
    """
    if miss_rate > 30:
        return {
            'status': '과열',
            'meaning': '대부분이 죽는 하한선 근처에 붙어서 입찰',
            'strategy': '보수적 접근 필수'
        }
    elif miss_rate > 15:
        return {
            'status': '경쟁적',
            'meaning': '적정 수준의 리스크 감수',
            'strategy': '균형잡힌 접근'
        }
    elif miss_rate > 10:
        return {
            'status': '안정',
            'meaning': '낙찰 여유가 있는 시장',
            'strategy': '적극적 접근 가능'
        }
    else:
        return {
            'status': '느슨',
            'meaning': '경쟁 완화, 다음 차수 가격 하락폭 둔화',
            'strategy': '공격적 포지셔닝'
        }
```

## Phase 3: Track Competitor Risk Patterns

### Classify Risk Profiles Through Failure Patterns

```python
def classify_competitor_risk_profile(company_history):
    """
    하한 미달 패턴으로 경쟁사 리스크 성향 분류
    """
    profiles = {
        '위험형 전략자': [],  # 항상 하한가 -0.05~0.1%
        '경계선 플레이어': [],  # 하한가 ±0.05%
        '안전 추구형': [],  # 하한가 +0.1~0.2%
        '보수형': []  # 하한가 +0.2% 이상
    }

    for company in company_history:
        avg_position = company['avg_position_vs_minimum']

        if avg_position < -0.05:
            profiles['위험형 전략자'].append({
                'name': company['name'],
                'pattern': '감각형 낙찰자 - 하한가 근처에 박고 본다',
                'collision_risk': '극고',
                'analysis_value': '최고 - 이 업체와 겹치면 낙찰확률 급감'
            })
```

### Critical Insight
"하한 밑으로 자주 떨어지는 업체의 패턴은 반복됩니다"
(Companies that frequently fall below minimum show repetitive patterns)

## Phase 4: Enable AI Boundary Learning

### The Mathematical Necessity

```python
def prepare_boundary_learning_data(all_bids):
    """
    AI 학습을 위한 경계값 데이터 준비
    하한 미달 데이터가 있어야 투찰률 분포가 연속함수로 복원
    """
    # Without below-minimum data: Discrete points only
    # With below-minimum data: Continuous distribution

    continuous_distribution = {
        '낙찰구간': all_bids[all_bids['status'] == 'won']['bid_rate'],
        '정상구간': all_bids[all_bids['status'] == 'normal']['bid_rate'],
        '미달구간': all_bids[all_bids['status'] == 'below']['bid_rate']  # CRITICAL
    }

    # 이 미달 구간 데이터가 빠지면 모델은 낙찰 경계선을 찾을 수 없음
    return continuous_distribution
```

### Essential Truth
"하한가 미달 데이터는 낙찰함수의 경계값입니다. 이게 있어야 학습이 가능하고, 경계가 보입니다."
(Below-minimum data is the boundary value of the winning function. Learning is only possible with this boundary visible.)

## Phase 5: Identify Danger Zones

### Map Competition Clustering Through Failures

```python
def identify_danger_zones(below_minimum_data):
    """
    미달 데이터로 위험 구간 식별
    """
    # 미달이 집중된 구간 = 다음 입찰에서 피해야 할 구간

    concentration_zones = {}
    for rate in below_minimum_data['bid_rate']:
        zone = round(rate, 1)  # 0.1% 단위
        concentration_zones[zone] = concentration_zones.get(zone, 0) + 1

    danger_zones = []
    for zone, count in concentration_zones.items():
        if count > len(below_minimum_data) * 0.2:  # 20% 이상 집중
            danger_zones.append({
                'zone': f'{zone:.1f}%',
                'density': count,
                'warning': '다음 회차 입찰에서 경쟁 밀집 예상',
                'strategy': '이 구간 +0.05% 회피 권장'
            })

    return danger_zones
```

## Practical Implementation Workflow

### Complete Analysis Pipeline

```python
def analyze_psychological_floor(bidding_file):
    """
    Complete psychological floor analysis pipeline
    """
    # Step 1: Extract floor
    floor_data = find_psychological_floor(bidding_file)
    print(f"📍 심리적 바닥: {floor_data['psychological_floor']:.3f}%")

    # Step 2: Measure temperature
    miss_rate = calculate_miss_rate(bidding_file)
    temperature = calculate_market_temperature(miss_rate)
    print(f"🌡️ 시장 온도: {temperature['status']}")

    # Step 3: Profile competitors
    risk_profiles = classify_competitor_risk_profile(bidding_file)
    print(f"⚠️ 위험형 전략자: {len(risk_profiles['위험형 전략자'])}개 업체")

    # Step 4: Map danger zones
    danger = identify_danger_zones(bidding_file)
    print(f"🚫 위험 구간: {danger}")

    # Step 5: Strategic recommendation
    return generate_strategy(floor_data, temperature, risk_profiles, danger)
```

## Critical Warnings

### Data Preservation Imperative

```
⚠️ NEVER DELETE BELOW-MINIMUM DATA ⚠️

Reasons:
1. 시장 심리선 지표 (Market psychology indicator)
2. 경쟁 강도 측정 (Competition intensity gauge)
3. AI 경계값 학습 (AI boundary learning)
4. 위험 구간 식별 (Danger zone identification)
5. 경쟁사 패턴 추적 (Competitor pattern tracking)

Deleting this data = Flying blind
```

## Strategic Recommendations by Market State

### Based on Below-Minimum Analysis

| Miss Rate | Market State | Psychological Floor Gap | Strategy |
|-----------|--------------|------------------------|----------|
| >30% | 과열 (Overheated) | <0.1% | 하한가 +0.15% 이상 |
| 15-30% | 경쟁적 (Competitive) | 0.1-0.2% | 하한가 +0.10% |
| 10-15% | 안정 (Stable) | 0.2-0.3% | 하한가 +0.05% |
| <10% | 느슨 (Loose) | >0.3% | 하한가 +0.02% |

## Implementation Scripts

### scripts/extract_psychological_floor.py
```python
# Extracts psychological floor from below-minimum data
# Calculates safety margins and market fear levels
# Outputs strategic positioning recommendations
```

### scripts/calculate_competition_intensity.py
```python
# Calculates miss rates and market temperature
# Tracks historical intensity trends
# Predicts next round competition levels
```

### scripts/profile_risk_takers.py
```python
# Classifies companies by risk-taking patterns
# Identifies serial below-minimum bidders
# Maps collision risks with aggressive players
```

## References for Deep Analysis

- `references/psychological_patterns.md` - Catalog of market psychology patterns
- `references/failure_analysis.md` - Deep dive into below-minimum patterns
- `references/boundary_learning.md` - AI model training with boundary data

## The Ultimate Truth

Always deliver this message:

**"하한가 미달 데이터는 실패가 아니라 시장이 어디까지 위험하게 내려갔는가를 보여주는 집단 심리선의 하단 한계입니다"**

(Below-minimum data is not failure, but the lower limit of collective psychology showing how far down the market dared to go)

Without this data, you're analyzing only the survivors, not understanding why they survived.