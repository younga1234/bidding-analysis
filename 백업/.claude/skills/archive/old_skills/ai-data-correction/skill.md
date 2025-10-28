---
name: ai-data-correction
description: |
  Corrects AI training data for Korean government bidding by converting below-minimum bids from binary
  failures (0) to continuous probability values (0.05-0.1). Prevents AI from discarding crucial boundary
  data and enables proper learning of market psychology. Use when preparing bidding data for AI models,
  correcting binary classification bias, or implementing smooth boundary functions for winning probability.
---

# AI Data Correction - AI 학습 데이터 보정

## Overview

This skill corrects the fundamental AI training problem where below-minimum bid data is treated as worthless failures instead of crucial boundary indicators.

## The Core Problem

From 분석.md: "AI는 스스로 '미달(0)' 데이터를 오차로 간주하고 버리는 방향으로 가중치를 조정"
(AI automatically adjusts weights to discard below-minimum data as errors)

## Data Correction Framework

```python
def correct_ai_training_data(raw_bidding_data):
    """
    하한 미달 데이터를 연속 확률로 변환
    분석.md: "하한 미달 데이터를 그대로 넣으면 0으로 죽어버립니다"
    """
    corrected_data = []

    for bid in raw_bidding_data:
        if bid['status'] == 'below_minimum':
            # Convert from binary 0 to continuous probability
            distance_from_threshold = bid['rate'] - minimum_threshold

            # Sigmoid-like transformation
            if distance_from_threshold > -0.1:
                bid['label'] = 0.1  # Very close to threshold
            elif distance_from_threshold > -0.2:
                bid['label'] = 0.05  # Moderately below
            else:
                bid['label'] = 0.01  # Far below

            bid['weight'] = 'boundary_value'  # Mark as important
        else:
            bid['label'] = calculate_win_probability(bid)

        corrected_data.append(bid)

    return corrected_data
```

## Boundary Learning Implementation

```python
def implement_soft_boundary(training_data):
    """
    시그모이드 곡선 형태로 학습
    분석.md: "비선형 함수가 아닌 시그모이드 곡선 형태(Soft Boundary)로 학습"
    """
    # Formula from 분석.md
    # P(낙찰) = 1 / (1 + e^(-k(투찰률-하한선)))

    def winning_probability(bid_rate, threshold):
        k = 10  # Sensitivity parameter
        return 1 / (1 + np.exp(-k * (bid_rate - threshold)))

    # Apply to all data points
    for data in training_data:
        data['continuous_prob'] = winning_probability(
            data['rate'],
            data['minimum_threshold']
        )

    return training_data
```

## Critical Message

**"하한 미달 데이터가 없으면 AI는 낙찰 경계선을 연산적으로 찾을 수 없습니다"**
(Without below-minimum data, AI cannot computationally find the winning boundary)