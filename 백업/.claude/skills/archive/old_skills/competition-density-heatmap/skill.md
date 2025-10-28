---
name: competition-density-heatmap
description: |
  Creates visual heatmaps of bidding competition density across bid rate ranges. Identifies crowded zones
  (80.50-80.55%), safe gaps, and optimal positioning opportunities. Use when visualizing competition
  distribution, finding low-density bidding zones, or strategic positioning. This skill reveals where
  competitors cluster and where opportunities exist in the distribution gaps.
---

# Competition Density Heatmap - 경쟁밀도 히트맵

## Overview

This skill visualizes bidding competition density across different rate ranges, revealing clustering patterns and strategic gaps for optimal positioning.

## Core Visualization Framework

### Generate Competition Heatmap

```python
def generate_competition_heatmap(bidding_data):
    """
    투찰률 구간별 경쟁밀도 히트맵 생성
    From 분석.md: 경쟁 밀집구간(80.45~80.55%) 회피 → 80.57~80.60% 선택
    """
    density_map = {}

    # Segment bid rates into 0.05% intervals
    for rate in range(8000, 8100, 5):  # 80.00% to 81.00% in 0.05% steps
        zone = rate / 100
        density_map[zone] = {
            'count': 0,
            'companies': [],
            'risk_level': None
        }

    # Populate density
    for bid in bidding_data:
        zone_key = round(bid['rate'] * 20) / 20  # Round to 0.05%
        if zone_key in density_map:
            density_map[zone_key]['count'] += 1
            density_map[zone_key]['companies'].append(bid['company'])

    # Classify risk levels
    for zone, data in density_map.items():
        if data['count'] >= 5:
            data['risk_level'] = 'EXTREME - 과열구간'
        elif data['count'] >= 3:
            data['risk_level'] = 'HIGH - 경쟁밀집'
        elif data['count'] >= 2:
            data['risk_level'] = 'MODERATE - 일반경쟁'
        else:
            data['risk_level'] = 'SAFE - 틈새구간'

    return density_map
```

### Visual Output Format

```
투찰률 구간    업체밀도    하한미달률    추천여부
80.45~80.50%   ████████    45%          ❌ 위험
80.51~80.55%   ██████████  20%          ❌ 과열
80.56~80.60%   ███         5%           ✅ 추천
80.61~80.70%   ████        0%           △ 안전하나 고가
```

## Strategic Gap Identification

```python
def identify_strategic_gaps(heatmap_data):
    """
    경쟁이 약한 틈새 구간 식별
    분석.md: "경쟁자들이 가장 많이 몰리는 투찰률을 피한다"
    """
    opportunities = []

    for zone, data in heatmap_data.items():
        if data['risk_level'] == 'SAFE':
            opportunities.append({
                'zone': zone,
                'density': data['count'],
                'advantage': '낮은 경쟁으로 충돌 회피 가능',
                'strategy': f'{zone:.2f}% ± 0.02% 타겟'
            })

    return sorted(opportunities, key=lambda x: x['density'])
```