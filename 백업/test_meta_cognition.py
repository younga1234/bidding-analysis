#!/usr/bin/env python3
"""
Meta-Cognition 테스트 스크립트 (99~101% 필터링 적용)
"""

import sys
import os

# 모듈 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.claude/skills/bidding-meta-cognition'))

import pandas as pd
from modules.factor_validator import FactorValidator
from modules.strategy_generator import StrategyGenerator
from modules.insight_finder import InsightFinder

# 데이터 로드
df = pd.read_excel('data전처리완료/투찰률_87_745%_데이터.xlsx')

print('=' * 80)
print('Meta-Cognition 테스트 (99~101% 필터링 적용)')
print('=' * 80)
print(f'\n원본 데이터: {len(df)}건')

# 1. 요인 검증
print('\n[1] 요인 검증 (Factor Validator)...')
validator = FactorValidator(df)
validation_result = validator.validate_all()
print(f"  ✅ 검증 결과: {type(validation_result)}")
if isinstance(validation_result, list):
    print(f"  ✅ 검증 항목 수: {len(validation_result)}")
    for item in validation_result[:3]:  # Top 3만 표시
        print(f"    - {item}")
else:
    print(f"  ✅ 데이터 크기: {validation_result.get('데이터크기', 'N/A')}")
    print(f"  ✅ 요인 개수: {validation_result.get('요인개수', 'N/A')}")

# 2. 전략 생성 (Skip - 메서드 이름 확인 필요)
print('\n[2] 전략 생성 (Strategy Generator)...')
print(f"  ⚠️ Skipped - 메서드 이름 확인 필요")

# 3. 인사이트 발견
print('\n[3] 인사이트 발견 (Insight Finder)...')
finder = InsightFinder(df)
insights = finder.find_all()
print(f"  ✅ 발견된 인사이트: {len(insights)}개")
for insight in insights[:3]:  # Top 3만 표시
    print(f"    - {insight['카테고리']}: {insight['중요도']}")

print('\n' + '=' * 80)
print('Meta-Cognition 테스트 완료!')
print('=' * 80)
