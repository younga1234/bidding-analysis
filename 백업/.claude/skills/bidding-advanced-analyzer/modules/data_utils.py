#!/usr/bin/env python3
"""
데이터 유틸리티 - 공통 함수

모든 분석 스킬에서 사용하는 공통 필터링 함수
"""

import pandas as pd


def filter_valid_range(df):
    """
    기초대비사정률 유효 범위 필터링 (99~101%)

    Args:
        df: 원본 데이터프레임

    Returns:
        필터링된 데이터프레임
    """
    if '기초대비사정률' in df.columns:
        original_count = len(df)
        df = df[
            (df['기초대비사정률'] >= 99.0) &
            (df['기초대비사정률'] <= 101.0)
        ].copy()
        filtered_count = original_count - len(df)
        if filtered_count > 0:
            print(f"  ⚠️ 범위 외 데이터 제거: {filtered_count}건 (99~101% 범위 외)")
    return df
