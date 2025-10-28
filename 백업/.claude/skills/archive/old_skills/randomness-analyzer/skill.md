---
name: randomness-analyzer
description: |
  복수예가입찰 시스템의 구조적 무작위성 분석. 15개 예비가격 중 4개를 무작위 선택하여
  평균내는 시스템(15C4 = 1,365 경우의 수)의 본질적 예측 불가능성을 검증하고,
  분석 방향을 경쟁업체 행동 패턴으로 올바르게 설정.
  Use when analyzing bidding system randomness or validating analysis approaches. (project)
allowed-tools:
  - Read
  - Grep
  - mcp__smithery-ai-server-sequential-thinking__sequentialthinking
---

# 복수예가입찰 무작위성 분석기

## 핵심 원리

복수예가입찰 시스템의 **구조적 무작위성**을 이해하고 검증:
- 15개 예비가격 중 4개 무작위 선택
- 1,365가지 조합 = 완전 무작위
- 예정가격 예측 = 불가능
- 유일한 분석 대상 = 경쟁업체 행동

## 분석 방법

### 1. 무작위성 검증
```python
def validate_randomness(data):
    """예정가격의 무작위성 검증"""
    # 15C4 = 1,365 경우의 수
    combinations = 1365

    # 각 조합의 확률
    probability = 1 / combinations  # 0.0732%

    return {
        "randomness": "구조적 무작위",
        "predictability": "불가능",
        "probability_per_case": f"{probability:.4%}",
        "analysis_focus": "경쟁업체 행동 패턴만 분석 가능"
    }
```

### 2. 잘못된 접근 감지
```python
def detect_wrong_approach(analysis_plan):
    """예정가격 예측 시도 감지"""
    wrong_keywords = [
        "예정가격 예측",
        "가격 분포 학습",
        "금액 패턴 분석",
        "예정가격 추정"
    ]

    for keyword in wrong_keywords:
        if keyword in analysis_plan:
            return {
                "error": "잘못된 접근",
                "reason": "예정가격은 1/1365 무작위",
                "correction": "경쟁업체 행동 패턴 분석으로 전환"
            }
```

### 3. 올바른 분석 방향 설정
```python
def set_correct_direction():
    """올바른 분석 방향 제시"""
    return {
        "분석 가능": [
            "경쟁업체 투찰 습관",
            "투찰률 분포 패턴",
            "동가입찰 빈도",
            "하한가 근처 밀집도"
        ],
        "분석 불가능": [
            "예정가격 예측",
            "정확한 낙찰가 계산",
            "다음 입찰 가격"
        ]
    }
```

## 실행 시나리오

사용자: "이 입찰의 예정가격을 예측해줘"
응답:
```
⚠️ 잘못된 접근 감지

복수예가입찰 시스템 특성:
- 15개 중 4개 무작위 선택 = 1,365 경우의 수
- 각 경우의 확률 = 0.0732%
- 예정가격 예측 = 구조적으로 불가능

✅ 대신 분석 가능한 것:
1. 경쟁업체들의 투찰 패턴
2. 과거 낙찰률 분포
3. 동가입찰 위험 구간
4. 하한가 미달 패턴

분석 방향을 경쟁업체 행동으로 전환하시겠습니까?
```

## 주의사항

1. **절대 금지**: 예정가격 예측 시도
2. **항상 강조**: 1/1365 무작위성
3. **분석 초점**: 경쟁업체 행동만
4. **교육 필요**: 시스템 본질 이해