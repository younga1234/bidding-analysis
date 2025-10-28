#!/usr/bin/env python3
"""
실제 1위 업체들의 기초대비투찰률 분포 분석
어느 구간에 가장 많이 몰려있는가?
"""

import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter

# 데이터 로드
data_file = Path("/mnt/a/25/data전처리완료/투찰률_87_745%_데이터.xlsx")
df = pd.read_excel(data_file)

# 1위만 필터링
df_first = df[df['순위'] == 1].copy()

print("="*80)
print(f"실제 1위 업체 기초대비투찰률 분포 분석 (총 {len(df_first)}개)")
print("="*80)

# 기본 통계
rates = df_first['기초대비투찰률'].values
print(f"\n[기본 통계]")
print(f"  평균: {rates.mean():.3f}%")
print(f"  중앙값: {np.median(rates):.3f}%")
print(f"  표준편차: {rates.std():.3f}%")
print(f"  최소: {rates.min():.3f}%")
print(f"  최대: {rates.max():.3f}%")
print(f"  범위: {rates.max() - rates.min():.3f}%")

# 0.1% 단위 구간별 분포
print(f"\n[0.1% 단위 구간별 분포]")
bins_01 = np.arange(rates.min() // 0.1 * 0.1, rates.max() + 0.1, 0.1)
hist_01, edges_01 = np.histogram(rates, bins=bins_01)

# 상위 10개 구간
top_10_indices = np.argsort(hist_01)[-10:][::-1]
for idx in top_10_indices:
    if hist_01[idx] > 0:
        start = edges_01[idx]
        end = edges_01[idx + 1]
        count = hist_01[idx]
        pct = count / len(df_first) * 100
        print(f"  {start:.1f}% ~ {end:.1f}%: {count:3d}개 ({pct:5.1f}%)")

# 0.05% 단위 구간별 분포 (더 세밀하게)
print(f"\n[0.05% 단위 구간별 분포 - 상위 15개]")
bins_005 = np.arange(rates.min() // 0.05 * 0.05, rates.max() + 0.05, 0.05)
hist_005, edges_005 = np.histogram(rates, bins=bins_005)

top_15_indices = np.argsort(hist_005)[-15:][::-1]
for idx in top_15_indices:
    if hist_005[idx] > 0:
        start = edges_005[idx]
        end = edges_005[idx + 1]
        count = hist_005[idx]
        pct = count / len(df_first) * 100
        print(f"  {start:.2f}% ~ {end:.2f}%: {count:3d}개 ({pct:5.1f}%)")

# 소수점 첫째 자리 분석
print(f"\n[소수점 첫째 자리 분포]")
first_decimal = ((rates * 10) % 10).astype(int)
decimal_counts = Counter(first_decimal)
for digit in sorted(decimal_counts.keys()):
    count = decimal_counts[digit]
    pct = count / len(df_first) * 100
    print(f"  87.{digit}XX%: {count:3d}개 ({pct:5.1f}%)")

# 소수점 둘째 자리 분석
print(f"\n[소수점 둘째 자리 분포]")
second_decimal = ((rates * 100) % 10).astype(int)
decimal2_counts = Counter(second_decimal)
for digit in sorted(decimal2_counts.keys()):
    count = decimal2_counts[digit]
    pct = count / len(df_first) * 100
    print(f"  87.X{digit}X%: {count:3d}개 ({pct:5.1f}%)")

# 소수점 셋째 자리 분석
print(f"\n[소수점 셋째 자리 분포]")
third_decimal = ((rates * 1000) % 10).astype(int)
decimal3_counts = Counter(third_decimal)
for digit in sorted(decimal3_counts.keys()):
    count = decimal3_counts[digit]
    pct = count / len(df_first) * 100
    print(f"  87.XX{digit}%: {count:3d}개 ({pct:5.1f}%)")

# 정확한 값 빈도 분석 (소수점 셋째 자리까지)
print(f"\n[정확한 값 빈도 Top 20 (충돌 위험 구간)]")
rate_rounded = np.round(rates, 3)
rate_counts = Counter(rate_rounded)
for rate, count in rate_counts.most_common(20):
    pct = count / len(df_first) * 100
    if count > 1:
        print(f"  {rate:.3f}%: {count:3d}개 ({pct:5.1f}%) ⚠️ 충돌!")
    else:
        print(f"  {rate:.3f}%: {count:3d}개 ({pct:5.1f}%)")

# 집중 구간 식별 (±0.5% 범위에 몇 개?)
print(f"\n[집중 구간 분석 (±0.5% 범위)]")
for center in np.arange(87.0, 90.0, 0.1):
    lower = center - 0.5
    upper = center + 0.5
    in_range = np.sum((rates >= lower) & (rates < upper))
    if in_range > 5:
        pct = in_range / len(df_first) * 100
        print(f"  {center:.1f}% ± 0.5%: {in_range:3d}개 ({pct:5.1f}%)")

# 가장 안전한 구간 (경쟁 적은 곳)
print(f"\n[가장 안전한 구간 Top 10 (0.05% 단위, 경쟁 적음)]")
safe_indices = np.argsort(hist_005)[:10]
for idx in safe_indices:
    if hist_005[idx] >= 0:
        start = edges_005[idx]
        end = edges_005[idx + 1]
        count = hist_005[idx]
        # 미달 위험 체크 (87.5% 이상만)
        if start >= 87.0:
            print(f"  {start:.2f}% ~ {end:.2f}%: {count}개 (안전!)")

# ±2% 범위 분석 (사용자 질문)
print(f"\n[±2% 범위 내 분포]")
print(f"기초금액 대비 ±2% 범위: 98% ~ 102%")
print(f"하지만 기초대비투찰률 기준으로는:")
base_center = rates.mean()
for delta in [0.5, 1.0, 1.5, 2.0]:
    lower = base_center - delta
    upper = base_center + delta
    in_range = np.sum((rates >= lower) & (rates <= upper))
    pct = in_range / len(df_first) * 100
    print(f"  평균({base_center:.3f}%) ± {delta}%: {in_range:3d}개 ({pct:5.1f}%)")

print(f"\n{'='*80}")
print(f"결론: 가장 많이 몰린 구간과 회피해야 할 구간 확인!")
print(f"{'='*80}")
