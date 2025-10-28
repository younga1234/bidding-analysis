---
name: below-minimum-analyzer
description: |
  하한가 미달 데이터 심층 분석. 시장 심리적 바닥선 도출, 미달 밀집 구간 파악,
  반복 미달 업체 추적, 심리적 압력 지수 계산. 미달 데이터를 '실패'가 아닌 '시장 심리 지표'로 해석.
  Use when analyzing below-minimum bid data or market psychology. (project)
allowed-tools:
  - Read
  - Bash
  - mcp__smithery-ai-server-sequential-thinking__sequentialthinking
---

# 하한가 미달 심층 분석기

## 핵심 통찰

> "하한가 미달은 실패가 아니라 시장 심리의 나침반"

미달 데이터가 보여주는 것:
- 업체들의 **심리적 안전선**
- 대다수가 회피하는 **위험 인식 구간**
- 시장의 **집단 공포 수준**

## 분석 기능

### 1. 심리적 바닥선 도출
```python
def find_psychological_floor(df):
    """시장이 느끼는 심리적 바닥"""

    # 하한가 미달 데이터 (순위 < 0)
    below_minimum = df[df['순위'] < 0]

    if len(below_minimum) == 0:
        return {
            'status': '미달 없음',
            'interpretation': '매우 보수적 시장 - 모두가 안전 추구'
        }

    # 미달 중 가장 높은 투찰률 = 심리적 바닥
    psychological_floor = below_minimum['예가대비투찰률(%)'].max()

    # 실제 하한가와 격차
    actual_minimum = df['낙찰하한율'].iloc[0]
    safety_margin = actual_minimum - psychological_floor

    # 미달 분포 분석
    below_stats = {
        '심리적_바닥': psychological_floor,
        '실제_하한가': actual_minimum,
        '안전_마진': safety_margin,
        '미달_업체수': len(below_minimum),
        '미달률': len(below_minimum) / len(df) * 100,
        '평균_미달_거리': below_minimum['낙찰하한가차이(원)'].mean(),
        '해석': interpret_psychology(safety_margin)
    }

    return below_stats
```

### 2. 미달 밀집 구간 분석
```python
def analyze_below_concentration(df):
    """미달 업체들의 밀집 구간"""

    below_data = df[df['순위'] < 0]
    if len(below_data) == 0:
        return None

    # 0.1% 단위 구간별 분포
    rates = below_data['예가대비투찰률(%)'].values
    min_rate = df['낙찰하한율'].iloc[0]

    concentration = {}
    for rate in rates:
        bucket = round((rate - min_rate) * 10) / 10  # 0.1% 단위
        key = f'하한가 {bucket:+.1f}%'
        concentration[key] = concentration.get(key, 0) + 1

    # 최밀집 구간
    densest = max(concentration, key=concentration.get)
    density = concentration[densest]

    return {
        '최밀집_구간': densest,
        '밀집_업체수': density,
        '밀집도': density / len(below_data) * 100,
        '의미': '다수가 "여기까지는 도전해볼만" 생각하는 경계',
        '전체_분포': concentration
    }
```

### 3. 반복 미달 업체 추적
```python
def track_repeat_failures(all_data):
    """여러 입찰에서 반복적으로 미달하는 업체"""

    # 전체 데이터에서 미달 기록
    failures = all_data[all_data['순위'] < 0]

    # 업체별 미달 횟수
    failure_counts = failures.groupby('업체명').size()

    # 3회 이상 미달 업체
    repeat_failures = failure_counts[failure_counts >= 3]

    if len(repeat_failures) == 0:
        return None

    # 상세 분석
    chronic_failures = {}
    for company in repeat_failures.index:
        company_data = failures[failures['업체명'] == company]
        chronic_failures[company] = {
            '미달_횟수': len(company_data),
            '평균_투찰률': company_data['예가대비투찰률(%)'].mean(),
            '표준편차': company_data['예가대비투찰률(%)'].std(),
            '패턴': classify_failure_pattern(company_data)
        }

    return {
        '반복_미달_업체수': len(repeat_failures),
        '상세': chronic_failures,
        '활용': '이들의 투찰률이 시장 심리적 바닥 지표'
    }
```

### 4. 심리적 압력 지수
```python
def calculate_psychological_pressure(df):
    """하한가 근처 심리적 압력 측정"""

    min_rate = df['낙찰하한율'].iloc[0]

    # 하한가 ±1% 구간
    near_minimum = df[
        abs(df['예가대비투찰률(%)'] - min_rate) <= 1.0
    ]

    # 성공 vs 실패 비율
    success_count = len(near_minimum[near_minimum['순위'] > 0])
    fail_count = len(near_minimum[near_minimum['순위'] < 0])
    total_near = success_count + fail_count

    if total_near == 0:
        return {'압력_지수': 0, '해석': '데이터 부족'}

    pressure_index = success_count / total_near

    # 구간별 세부 분석
    zones = {}
    for i in range(-10, 11):  # -1.0% ~ +1.0%를 0.1% 단위로
        zone_rate = min_rate + i * 0.1
        zone_data = df[
            abs(df['예가대비투찰률(%)'] - zone_rate) < 0.05
        ]
        if len(zone_data) > 0:
            zone_success = len(zone_data[zone_data['순위'] > 0])
            zones[f'{i*0.1:+.1f}%'] = {
                'total': len(zone_data),
                'success': zone_success,
                'fail': len(zone_data) - zone_success
            }

    return {
        '압력_지수': pressure_index,
        '해석': interpret_pressure(pressure_index),
        '구간별_상세': zones,
        '권장_전략': suggest_strategy(pressure_index)
    }
```

### 5. 미달 패턴 분류
```python
def classify_failure_patterns(below_data):
    """미달 패턴 유형 분류"""

    patterns = {
        '공격적_도전형': [],  # 하한가 -0.5% 이내
        '계산된_모험형': [],  # 하한가 -1% 이내
        '무모한_도박형': [],  # 하한가 -2% 이내
        '전략_부재형': []    # 하한가 -2% 초과
    }

    min_rate = below_data['낙찰하한율'].iloc[0]

    for _, row in below_data.iterrows():
        gap = row['예가대비투찰률(%)'] - min_rate

        if gap > -0.5:
            patterns['공격적_도전형'].append(row['업체명'])
        elif gap > -1.0:
            patterns['계산된_모험형'].append(row['업체명'])
        elif gap > -2.0:
            patterns['무모한_도박형'].append(row['업체명'])
        else:
            patterns['전략_부재형'].append(row['업체명'])

    return {
        type_name: {
            'count': len(companies),
            'percentage': len(companies) / len(below_data) * 100,
            'companies': companies[:5]  # 상위 5개만
        }
        for type_name, companies in patterns.items()
        if companies
    }
```

## 실행 스크립트

```python
import pandas as pd
import numpy as np

def full_below_minimum_analysis(file_path):
    """하한가 미달 완전 분석"""

    df = pd.read_excel(file_path)

    # 데이터 전처리
    for col in ['낙찰하한가', '예정가격']:
        df[col] = df[col].str.replace('원', '').str.replace(',', '').astype(float)

    df['낙찰하한율'] = (df['낙찰하한가'] / df['예정가격'] * 100).round(3)

    print(f"\n{'='*60}")
    print(f"하한가 미달 분석: {df['공고번호'].iloc[0]}")
    print(f"{'='*60}\n")

    # 1. 심리적 바닥선
    floor = find_psychological_floor(df)
    print(f"📍 심리적 바닥선: {floor['심리적_바닥']:.3f}%")
    print(f"   실제 하한가: {floor['실제_하한가']:.3f}%")
    print(f"   안전 마진: {floor['안전_마진']:.3f}%")
    print(f"   미달률: {floor['미달률']:.1f}%")

    # 2. 밀집 구간
    concentration = analyze_below_concentration(df)
    if concentration:
        print(f"\n🎯 미달 밀집 구간")
        print(f"   {concentration['최밀집_구간']}: {concentration['밀집_업체수']}개 업체")
        print(f"   의미: {concentration['의미']}")

    # 3. 심리적 압력
    pressure = calculate_psychological_pressure(df)
    print(f"\n🌡️ 심리적 압력 지수: {pressure['압력_지수']:.2f}")
    print(f"   해석: {pressure['해석']}")
    print(f"   전략: {pressure['권장_전략']}")

    # 4. 미달 패턴
    patterns = classify_failure_patterns(df[df['순위'] < 0])
    if patterns:
        print(f"\n📊 미달 패턴 분류")
        for pattern_type, data in patterns.items():
            if data['count'] > 0:
                print(f"   {pattern_type}: {data['count']}개 ({data['percentage']:.1f}%)")

    return {
        'floor': floor,
        'concentration': concentration,
        'pressure': pressure,
        'patterns': patterns
    }
```

## 실전 해석 예시

```
============================================================
하한가 미달 분석: 20230905571-00
============================================================

📍 심리적 바닥선: 80.349%
   실제 하한가: 80.495%
   안전 마진: 0.146%
   미달률: 66.7%

🎯 미달 밀집 구간
   하한가 -0.1%: 8개 업체
   의미: 다수가 "여기까지는 도전해볼만" 생각하는 경계

🌡️ 심리적 압력 지수: 0.33
   해석: 공격적 시장 - 많은 업체가 리스크 감수
   전략: 보수적 접근 권장 (하한가 +0.2% 이상)

📊 미달 패턴 분류
   공격적_도전형: 8개 (80.0%)
   계산된_모험형: 2개 (20.0%)
```

## 전략적 활용

### 시장 상태별 대응

| 압력 지수 | 시장 상태 | 권장 전략 |
|----------|----------|----------|
| 0.9 이상 | 극도로 보수적 | 하한가 +0.05% 공격적 접근 |
| 0.7-0.9 | 보수적 | 하한가 +0.1% 균형 접근 |
| 0.5-0.7 | 균형 | 하한가 +0.15% 안정 추구 |
| 0.5 미만 | 공격적 | 하한가 +0.2% 이상 보수적 |

## 핵심 인사이트

1. **미달은 정보다**: 실패가 아닌 시장 심리 지표
2. **심리적 벽 존재**: 실제 하한가보다 약간 아래
3. **집단 심리 활용**: 다수 회피 구간이 기회
4. **반복 미달 주목**: 시장 바닥 예측 지표

## 주의사항

- 하한가 미달 데이터 **절대 제거 금지**
- 발주처별 다른 심리선 형성
- 참여업체수에 따라 해석 조정