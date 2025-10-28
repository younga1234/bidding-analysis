---
name: competition-intensity-analyzer
description: |
  투찰률 구간별 경쟁 밀도 분석. 0.1% 단위로 구간을 나누어 각 구간의 업체 수를 계산하고,
  경쟁이 집중되는 핫존과 상대적으로 비어있는 기회 구간을 식별.
  Use when analyzing competition density across bidding rate ranges. (project)
allowed-tools:
  - Read
  - Grep
  - Bash
  - mcp__smithery-ai-server-sequential-thinking__sequentialthinking
---

# 경쟁 밀도 분석기

## 핵심 개념

"0.1% 차이가 순위를 결정하는 초정밀 경쟁"

- 1% 단위: 전체 지형 파악
- 0.1% 단위: 실전 경쟁 구간
- 0.01% 단위: 정밀 타격 지점

## 분석 방법

### 1. 구간별 밀도 계산
```python
def calculate_competition_density(bidding_data, precision=0.1):
    """구간별 경쟁 밀도 계산"""

    # 하한가 기준 상대 투찰률
    min_rate = bidding_data['낙찰하한율'].iloc[0]
    relative_rates = bidding_data['예가대비투찰률'] - min_rate

    # precision 단위로 구간 분할
    density_map = {}
    for rate in relative_rates:
        if rate >= 0:  # 하한가 이상만
            bucket = round(rate / precision) * precision
            density_map[bucket] = density_map.get(bucket, 0) + 1

    # 밀도 정규화 (전체 대비 %)
    total = sum(density_map.values())
    for key in density_map:
        density_map[key] = {
            "count": density_map[key],
            "percentage": density_map[key] / total * 100
        }

    return density_map
```

### 2. 핫존(과열 구간) 식별
```python
def identify_hot_zones(density_map, threshold=20):
    """경쟁 과열 구간 찾기"""

    hot_zones = []
    for bucket, data in density_map.items():
        if data["percentage"] > threshold:
            hot_zones.append({
                "range": f"하한가 +{bucket:.1f}%",
                "density": f"{data['percentage']:.1f}%",
                "count": data["count"],
                "risk": "동가입찰 위험 높음"
            })

    return sorted(hot_zones, key=lambda x: x["count"], reverse=True)
```

### 3. 기회 구간(빈 구간) 탐색
```python
def find_opportunity_zones(density_map, min_threshold=5):
    """경쟁 희박 구간 찾기"""

    # 모든 가능한 구간 생성 (하한가 ~ 하한가+2%)
    all_buckets = [round(x * 0.1, 1) for x in range(0, 21)]

    opportunity_zones = []
    for bucket in all_buckets:
        if bucket not in density_map or density_map[bucket]["count"] < min_threshold:
            current_count = density_map.get(bucket, {"count": 0})["count"]
            opportunity_zones.append({
                "range": f"하한가 +{bucket:.1f}%",
                "current_count": current_count,
                "opportunity": "낮은 경쟁"
            })

    return opportunity_zones[:5]  # 상위 5개
```

### 4. 정밀 경쟁 지도
```python
def create_precision_competition_map(bidding_data):
    """0.01% 단위 초정밀 경쟁 지도"""

    # 1등과 2등 격차가 0.01% 미만인 케이스
    ultra_competitive = []

    grouped = bidding_data.groupby('공고번호')
    for bid_no, group in grouped:
        sorted_group = group.sort_values('순위')
        if len(sorted_group) >= 2:
            gap = sorted_group.iloc[1]['예가대비투찰률'] - sorted_group.iloc[0]['예가대비투찰률']
            if gap < 0.01:
                ultra_competitive.append({
                    "공고번호": bid_no,
                    "1등_투찰률": sorted_group.iloc[0]['예가대비투찰률'],
                    "2등_투찰률": sorted_group.iloc[1]['예가대비투찰률'],
                    "격차": f"{gap:.3f}%"
                })

    return {
        "초정밀_경쟁_비율": f"{len(ultra_competitive) / len(grouped) * 100:.1f}%",
        "사례": ultra_competitive[:3]
    }
```

### 5. 시간대별 밀도 변화
```python
def analyze_density_evolution(historical_data):
    """시간 경과에 따른 밀도 변화"""

    monthly_patterns = {}

    for month in historical_data['월'].unique():
        month_data = historical_data[historical_data['월'] == month]
        density = calculate_competition_density(month_data)

        # 최고 밀도 구간
        hottest = max(density.items(), key=lambda x: x[1]["count"])
        monthly_patterns[month] = {
            "핫존": f"하한가 +{hottest[0]:.1f}%",
            "밀도": hottest[1]["percentage"]
        }

    # 추세 분석
    recent_hot = monthly_patterns[max(monthly_patterns.keys())]
    past_hot = monthly_patterns[min(monthly_patterns.keys())]

    return {
        "과거_핫존": past_hot["핫존"],
        "현재_핫존": recent_hot["핫존"],
        "변화": "이동 중" if past_hot["핫존"] != recent_hot["핫존"] else "고정"
    }
```

## 실전 밀도 지도 예시

```
[경쟁 밀도 분석 결과]

전체 참여: 87개 업체

=== 1% 단위 지형도 ===
하한가 +0%: ████████████ (35개, 40.2%)
하한가 +1%: ██████ (18개, 20.7%)
하한가 +2%: ███ (9개, 10.3%)

=== 0.1% 단위 정밀 분석 ===

🔥 핫존 (과열 구간):
1. 하한가 +0.3%: 15개 업체 (17.2%) ⚠️
2. 하한가 +0.5%: 12개 업체 (13.8%) ⚠️
3. 하한가 +0.8%: 10개 업체 (11.5%) ⚠️

💎 기회 구간 (빈 곳):
1. 하한가 +0.15%: 1개 업체 ✅
2. 하한가 +0.35%: 2개 업체 ✅
3. 하한가 +0.65%: 0개 업체 ✅

=== 0.01% 초정밀 경쟁 ===
- 전체의 23%가 0.01% 이내 격차
- 실제 사례:
  1등: 87.234%
  2등: 87.238% (격차: 0.004%)

💡 전략 제안:
- 회피 구간: +0.3%, +0.5%, +0.8%
- 공략 구간: +0.15%, +0.35%, +0.65%
- 정밀도: 소수점 3자리 필수
```

## 밀도별 전략

### 고밀도 구간 (>15%)
- **리스크**: 동가입찰 확률 높음
- **전략**: 회피 or 미세 조정 (+0.001%)

### 중밀도 구간 (5-15%)
- **특징**: 적당한 경쟁
- **전략**: 일반적 접근

### 저밀도 구간 (<5%)
- **기회**: 낮은 경쟁
- **주의**: 너무 높거나 낮을 수 있음

### 무인 구간 (0%)
- **판단**: 위험 or 기회
- **검토**: 과거 성공 사례 확인

## 핵심 인사이트

1. **0.1%가 운명을 가름**: 정밀도가 생존 열쇠
2. **핫존 회피**: 다수가 몰리는 곳 피하기
3. **빈틈 공략**: 아무도 없는 0.01% 찾기
4. **동적 대응**: 밀도는 계속 변화

## 주의사항

- 참여업체 수에 따라 전략 조정
- 너무 빈 구간은 이유 확인 필요
- 실시간 밀도는 예측일 뿐