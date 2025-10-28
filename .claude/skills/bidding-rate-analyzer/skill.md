---
name: bidding-rate-analyzer
description: |
  투찰률 분포 정밀 분석. 낙찰하한율별 그룹 분리, 0.1% 단위 구간별 밀도 계산,
  핫존(과열구간)과 기회구간 식별, 1등 투찰률 패턴 분석. 0.001% 정밀도로 경쟁 지도 생성.
  Use when analyzing bidding rate distributions or competition density. (project)
allowed-tools:
  - Read
  - Bash
  - mcp__smithery-ai-server-sequential-thinking__sequentialthinking
---

# 투찰률 분포 정밀 분석기

## 핵심 기능

### 1. 낙찰하한율별 그룹 분리
```python
def separate_by_minimum_rate(df):
    """발주처별 다른 낙찰하한율 그룹화"""

    # 낙찰하한율 계산
    df['낙찰하한율'] = (df['낙찰하한가'] / df['예정가격'] * 100).round(3)

    # 그룹별 분리
    groups = {}
    for rate in df['낙찰하한율'].unique():
        groups[f'{rate:.3f}%'] = df[df['낙찰하한율'] == rate]

    return groups
```

### 2. 구간별 밀도 계산 (0.1% 단위)
```python
def calculate_density_map(df, precision=0.1):
    """0.1% 단위로 경쟁 밀도 계산"""

    min_rate = df['낙찰하한율'].iloc[0]
    rates = df['예가대비투찰률(%)'].values

    # 구간 설정: 하한가 -1% ~ +3%
    bins = np.arange(min_rate - 1, min_rate + 3, precision)
    density = np.histogram(rates, bins=bins)[0]

    # 밀도맵 생성
    density_map = {}
    for i, count in enumerate(density):
        range_start = bins[i]
        range_key = f'{range_start:.1f}%'
        density_map[range_key] = {
            'count': count,
            'percentage': count / len(df) * 100,
            'risk_level': classify_risk(count, len(df))
        }

    return density_map
```

### 3. 핫존(과열구간) 식별
```python
def identify_hot_zones(density_map, threshold_pct=15):
    """경쟁 과열 구간 찾기"""

    hot_zones = []
    for range_key, data in density_map.items():
        if data['percentage'] > threshold_pct:
            hot_zones.append({
                'range': range_key,
                'density': f"{data['percentage']:.1f}%",
                'count': data['count'],
                'recommendation': '회피 권장',
                'alternative': suggest_alternative(range_key, density_map)
            })

    return sorted(hot_zones, key=lambda x: x['count'], reverse=True)
```

### 4. 기회구간 탐색
```python
def find_opportunity_zones(density_map, max_density=5):
    """경쟁 희박 구간 찾기"""

    opportunities = []
    for range_key, data in density_map.items():
        if data['count'] <= max_density:
            rate_value = float(range_key.rstrip('%'))

            # 너무 낮거나 높은 구간 제외
            if -1 < rate_value - min_rate < 2:
                opportunities.append({
                    'range': range_key,
                    'current_count': data['count'],
                    'advantage': '낮은 경쟁',
                    'caution': check_zone_validity(rate_value)
                })

    return opportunities[:5]  # 상위 5개
```

### 5. 초정밀 분석 (0.001% 단위)
```python
def ultra_precision_analysis(df, target_rate, window=0.1):
    """특정 구간 0.001% 단위 분석"""

    # 타겟 구간 데이터
    in_window = df[
        (df['예가대비투찰률(%)'] >= target_rate - window) &
        (df['예가대비투찰률(%)'] <= target_rate + window)
    ]

    # 0.001% 단위 분포
    ultra_map = {}
    for rate in in_window['예가대비투찰률(%)']:
        key = f'{rate:.3f}%'
        ultra_map[key] = ultra_map.get(key, 0) + 1

    # 충돌 위험 분석
    collisions = {k: v for k, v in ultra_map.items() if v > 1}

    return {
        'total_in_window': len(in_window),
        'unique_rates': len(ultra_map),
        'collision_points': collisions,
        'safe_spots': find_safe_spots(ultra_map, target_rate)
    }
```

### 6. 1등 투찰률 패턴
```python
def analyze_winning_patterns(df):
    """1등 낙찰자 투찰률 패턴 분석"""

    winners = df[df['순위'] == 1]

    patterns = {
        '평균_1등_투찰률': winners['예가대비투찰률(%)'].mean(),
        '표준편차': winners['예가대비투찰률(%)'].std(),
        '최소_1등': winners['예가대비투찰률(%)'].min(),
        '최대_1등': winners['예가대비투찰률(%)'].max(),
        '중앙값': winners['예가대비투찰률(%)'].median(),
        '최빈_구간': find_mode_range(winners['예가대비투찰률(%)'])
    }

    # 하한가 대비 분포
    winners['하한가대비'] = winners['예가대비투찰률(%)'] - winners['낙찰하한율']
    patterns['평균_하한가_초과율'] = winners['하한가대비'].mean()

    return patterns
```

## 실전 분석 스크립트

```python
import pandas as pd
import numpy as np
import os

def full_rate_analysis(file_path):
    """완전 투찰률 분석"""

    df = pd.read_excel(file_path)

    # 금액 필드 정리
    for col in ['기초금액', '예정가격', '낙찰하한가']:
        df[col] = df[col].str.replace('원', '').str.replace(',', '').astype(float)

    # 낙찰하한율 계산
    df['낙찰하한율'] = (df['낙찰하한가'] / df['예정가격'] * 100).round(3)

    print(f"\n{'='*60}")
    print(f"입찰 분석: {df['공고번호'].iloc[0]}")
    print(f"발주처: {df['발주처'].iloc[0]}")
    print(f"낙찰하한율: {df['낙찰하한율'].iloc[0]:.3f}%")
    print(f"참여업체: {len(df)}개")
    print(f"{'='*60}\n")

    # 1. 밀도 분석
    density = calculate_density_map(df)
    print("📊 구간별 밀도 (0.1% 단위)")
    for key, data in sorted(density.items(), key=lambda x: x[1]['count'], reverse=True)[:5]:
        print(f"  {key}: {'█' * data['count']} ({data['count']}개, {data['percentage']:.1f}%)")

    # 2. 핫존 분석
    hot_zones = identify_hot_zones(density)
    if hot_zones:
        print("\n🔥 과열 구간")
        for zone in hot_zones[:3]:
            print(f"  {zone['range']}: {zone['count']}개 업체 ({zone['density']})")

    # 3. 기회 구간
    opportunities = find_opportunity_zones(density)
    if opportunities:
        print("\n💎 기회 구간")
        for opp in opportunities[:3]:
            print(f"  {opp['range']}: {opp['current_count']}개 업체만")

    # 4. 1등 패턴
    winner_patterns = analyze_winning_patterns(df)
    print(f"\n🏆 1등 투찰률: {winner_patterns['평균_1등_투찰률']:.3f}%")
    print(f"   하한가 +{winner_patterns['평균_하한가_초과율']:.3f}%")

    # 5. 초정밀 분석 (1등 근처)
    if len(df[df['순위'] == 1]) > 0:
        winner_rate = df[df['순위'] == 1]['예가대비투찰률(%)'].iloc[0]
        ultra = ultra_precision_analysis(df, winner_rate, 0.1)
        print(f"\n🔬 1등 근처 초정밀 분석 (±0.1%)")
        print(f"   경쟁자: {ultra['total_in_window']}개")
        print(f"   충돌점: {len(ultra['collision_points'])}개")

    return {
        'density': density,
        'hot_zones': hot_zones,
        'opportunities': opportunities,
        'winner_patterns': winner_patterns
    }
```

## 실행 예시

```bash
# 단일 파일 분석
python -c "
from bidding_rate_analyzer import full_rate_analysis
result = full_rate_analysis('/mnt/a/25/data전처리완료/20230920668-00_통합.xlsx')
"
```

## 출력 예시

```
============================================================
입찰 분석: 20230920668-00
발주처: 국가유산진흥원
낙찰하한율: 86.745%
참여업체: 75개
============================================================

📊 구간별 밀도 (0.1% 단위)
  86.7%: ███████████████ (15개, 20.0%)
  86.8%: ████████████ (12개, 16.0%)
  86.9%: ██████████ (10개, 13.3%)
  87.0%: ████████ (8개, 10.7%)
  86.6%: ██████ (6개, 8.0%)

🔥 과열 구간
  86.7%: 15개 업체 (20.0%)
  86.8%: 12개 업체 (16.0%)

💎 기회 구간
  86.55%: 2개 업체만
  86.65%: 3개 업체만
  87.15%: 1개 업체만

🏆 1등 투찰률: 86.834%
   하한가 +0.089%

🔬 1등 근처 초정밀 분석 (±0.1%)
   경쟁자: 27개
   충돌점: 3개
```

## 전략적 활용

1. **핫존 회피**: 15% 이상 밀집 구간 피하기
2. **기회 활용**: 5개 이하 구간 공략
3. **정밀 조정**: 0.001% 단위로 차별화
4. **패턴 학습**: 1등 평균 초과율 참고

## 주의사항

- 낙찰하한율별로 반드시 분리 분석
- 참여업체수에 따라 기준 조정
- 발주처 특성 고려