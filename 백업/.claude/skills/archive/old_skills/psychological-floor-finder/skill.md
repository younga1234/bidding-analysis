---
name: psychological-floor-finder
description: |
  하한가 미달 데이터를 통한 시장 심리적 바닥선 분석. 업체들이 "여기까지는 안전"하다고
  생각하는 심리적 안전선을 파악하고, 실제 하한가와의 격차를 통해 시장 심리 해석.
  Use when analyzing market psychology through below-minimum bid data. (project)
allowed-tools:
  - Read
  - Grep
  - Bash
  - mcp__smithery-ai-server-sequential-thinking__sequentialthinking
---

# 심리적 바닥선 탐색기

## 핵심 통찰

"하한가 미달은 실패가 아니라 시장 심리의 지도"

하한가 미달 데이터가 보여주는 것:
- 업체들이 느끼는 "안전선"
- 대다수가 회피하는 "위험 구간"
- 시장의 집단 심리

## 분석 방법

### 1. 심리적 안전선 도출
```python
def find_psychological_floor(bidding_data):
    """심리적 바닥선 찾기"""

    # 하한가 미달 업체들의 투찰률
    below_minimum = bidding_data[bidding_data['순위'] == -1]

    if len(below_minimum) == 0:
        return "미달 데이터 없음 - 매우 보수적 시장"

    # 미달 투찰률 분포
    rates = below_minimum['예가대비투찰률'].values

    # 미달 중 최고 투찰률 = 심리적 바닥
    psychological_floor = max(rates)

    # 실제 하한가와 격차
    actual_minimum = bidding_data['낙찰하한율'].iloc[0]
    gap = actual_minimum - psychological_floor

    return {
        "심리적_바닥": f"{psychological_floor:.3f}%",
        "실제_하한가": f"{actual_minimum:.3f}%",
        "안전_마진": f"{gap:.3f}%",
        "해석": f"업체들은 하한가보다 {gap:.3f}% 아래를 심리적 한계로 인식"
    }
```

### 2. 미달 밀집 구간 분석
```python
def analyze_below_minimum_concentration(below_data):
    """미달 업체 밀집 구간"""

    rates = below_data['예가대비투찰률'].values

    # 0.1% 단위 구간별 분포
    distribution = {}
    for rate in rates:
        key = round(rate * 10) / 10
        distribution[key] = distribution.get(key, 0) + 1

    # 가장 밀집된 구간
    densest_zone = max(distribution, key=distribution.get)
    density = distribution[densest_zone] / len(rates)

    return {
        "최밀집_구간": f"{densest_zone:.1f}%",
        "밀집도": f"{density:.1%}",
        "의미": "다수가 '여기는 위험하지만 도전해볼만' 생각하는 구간"
    }
```

### 3. 반복 미달 업체 추적
```python
def track_repeat_failures(company_history):
    """반복적으로 미달하는 업체"""

    failure_counts = {}
    for company, result in company_history:
        if result == "미달":
            failure_counts[company] = failure_counts.get(company, 0) + 1

    # 3회 이상 미달 업체
    repeat_failures = {k: v for k, v in failure_counts.items() if v >= 3}

    if repeat_failures:
        return {
            "반복_미달_업체": repeat_failures,
            "특징": "학습 없는 고정 전략 or 의도적 저가 전략",
            "활용": "이들의 투찰률은 심리적 바닥 지표"
        }
```

### 4. 심리적 압력 지수
```python
def calculate_psychological_pressure(bidding_data):
    """하한가 근처 심리적 압력"""

    # 하한가 ±1% 구간 데이터
    near_minimum = bidding_data[
        (bidding_data['예가대비투찰률'] >= bidding_data['낙찰하한율'] - 1) &
        (bidding_data['예가대비투찰률'] <= bidding_data['낙찰하한율'] + 1)
    ]

    # 구간별 분포
    above_count = len(near_minimum[near_minimum['순위'] > 0])
    below_count = len(near_minimum[near_minimum['순위'] == -1])

    pressure_index = above_count / (above_count + below_count) if (above_count + below_count) > 0 else 0

    return {
        "압력_지수": f"{pressure_index:.2f}",
        "해석": {
            "0.9 이상": "극도로 보수적 - 대부분 안전 추구",
            "0.7-0.9": "보수적 - 리스크 회피 성향",
            "0.5-0.7": "균형 - 적절한 리스크 감수",
            "0.5 미만": "공격적 - 하한가 도전 많음"
        }
    }
```

### 5. 시장 심리 변화 추적
```python
def track_market_sentiment_change(historical_data):
    """시간에 따른 시장 심리 변화"""

    monthly_sentiment = {}

    for month_data in historical_data:
        below_ratio = len(month_data[month_data['순위'] == -1]) / len(month_data)
        avg_gap = month_data['낙찰하한율'].mean() - month_data[month_data['순위'] == -1]['예가대비투찰률'].mean()

        monthly_sentiment[month_data['월']] = {
            "미달률": below_ratio,
            "안전마진": avg_gap
        }

    # 추세 분석
    if monthly_sentiment[-1]["미달률"] > monthly_sentiment[-6]["미달률"]:
        trend = "공격적으로 변화 중"
    else:
        trend = "보수적으로 변화 중"

    return {
        "6개월_추세": trend,
        "최근_미달률": f"{monthly_sentiment[-1]['미달률']:.1%}",
        "시장_온도": "뜨거움" if monthly_sentiment[-1]['미달률'] > 0.2 else "차가움"
    }
```

## 실전 활용 예시

```
[심리적 바닥선 분석]

현재 입찰: 국가유산청 발굴조사 용역

1. 심리적 바닥선: 86.234%
   - 실제 하한가: 86.745%
   - 안전 마진: 0.511%

2. 미달 밀집 구간: 86.2~86.3%
   - 23개 업체 중 15개 집중
   - "도전할만한 한계선"으로 인식

3. 반복 미달 업체: 5개사
   - A사: 7회 연속 미달
   - B사: 5회 연속 미달
   → 이들의 평균 투찰률 86.18% = 시장 심리적 바닥

4. 심리적 압력 지수: 0.73
   - 해석: 보수적 시장
   - 대부분 안전 추구

💡 전략 제안:
- 보수적 접근: 87.2% (안전)
- 균형 접근: 86.8% (경쟁력)
- 공격적 접근: 86.75% (하한가 +0.005%)
```

## 핵심 인사이트

1. **미달은 정보**: 실패가 아닌 시장 심리 지표
2. **심리적 벽**: 실제 하한가보다 약간 아래 형성
3. **집단 심리**: 다수가 회피 = 기회 구간
4. **학습 기회**: 반복 미달 업체에서 배우기

## 주의사항

- 하한가 미달 데이터 절대 제거 금지
- 시장별로 다른 심리선 형성
- 계절/경기에 따라 변동