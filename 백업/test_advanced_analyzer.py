#!/usr/bin/env python3
"""
Advanced Analyzer 테스트 스크립트 (99~101% 필터링 적용)
"""

import sys
import os

# 모듈 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.claude/skills/bidding-advanced-analyzer'))

import pandas as pd
from modules.temporal_analysis import analyze_temporal_patterns
from modules.agency_analysis import analyze_agency_patterns
from modules.correlation_2d import analyze_2d_correlation

# 데이터 로드
df = pd.read_excel('data전처리완료/투찰률_87_745%_데이터.xlsx')

print('=' * 80)
print('Advanced Analyzer 테스트 (99~101% 필터링 적용)')
print('=' * 80)
print(f'\n원본 데이터: {len(df)}건')

# 1. 시간대별 패턴 분석
print('\n[1] 시간대별 패턴 분석...')
temporal_result = analyze_temporal_patterns(df)
if '오류' not in temporal_result:
    print(f"  ✅ 전체 데이터: {temporal_result['데이터개수']['전체']}건")
    print(f"  ✅ 최근 데이터: {temporal_result['데이터개수']['최근']}건")
    print(f"  ✅ 가중평균 최적구간: {temporal_result['가중평균_최적구간']}")
else:
    print(f"  ❌ 오류: {temporal_result['오류']}")

# 2. 발주처별 특성 분석
print('\n[2] 발주처별 특성 분석...')
agency_result = analyze_agency_patterns(df)
if '오류' not in agency_result:
    print(f"  ✅ 발주처 개수: {agency_result['발주처_개수']}")
    for agency, data in list(agency_result['발주처별_분석'].items())[:5]:  # Top 5만 표시
        print(f"    - {agency}: {data['데이터개수']}건, 1위={data['1위개수']}건")
else:
    print(f"  ❌ 오류: {agency_result['오류']}")

# 3. 2D 상관관계 분석
print('\n[3] 2D 상관관계 분석...')
corr_result = analyze_2d_correlation(df)
if '오류' not in corr_result:
    print(f"  ✅ 상관계수: {corr_result['상관계수']}")
    print(f"  ✅ 상관관계 평가: {corr_result['상관관계_평가']}")
    print(f"  ✅ 저밀도 구간 Top10: {len(corr_result['저밀도_구간_Top10'])}개")
else:
    print(f"  ❌ 오류: {corr_result['오류']}")

print('\n' + '=' * 80)
print('Advanced Analyzer 테스트 완료!')
print('=' * 80)
