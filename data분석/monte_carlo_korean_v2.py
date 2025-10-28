#!/usr/bin/env python3
"""
복수예가 몬테카를로 시뮬레이션 - 한글 고품질 시각화 v2

목적: 예정가격과 낙찰하한가의 확률분포를 10,000회 시뮬레이션으로 분석
모든 텍스트를 한글로 표기, 소수점 3자리 정밀도
Noto Sans KR 폰트 직접 로드 방식
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import ticker
from pathlib import Path

# Noto Sans KR 폰트 직접 로드
font_path = '/mnt/a/25/NotoSansKR.otf'
if Path(font_path).exists():
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
    print(f"한글 폰트 로드 성공: {font_prop.get_name()}")
else:
    print("폰트 파일을 찾을 수 없습니다. 기본 폰트 사용")
    font_prop = fm.FontProperties()

# 현재 공고 정보
BASE_AMOUNT = 39_000_000
AGENCY_RATE = 87.745
VARIANCE_RANGE = 0.03

# 시뮬레이션 설정
N_SIMULATIONS = 10_000
N_PRELIMINARY_PRICES = 15
N_SELECTED = 4

print("="*80)
print("복수예가 몬테카를로 시뮬레이션 - 한글 고품질 시각화 v2")
print("="*80)

# 1. 15개 예비가격 생성
min_price = BASE_AMOUNT * (1 - VARIANCE_RANGE)
max_price = BASE_AMOUNT * (1 + VARIANCE_RANGE)
preliminary_prices = np.linspace(min_price, max_price, N_PRELIMINARY_PRICES)

# 2. 몬테카를로 시뮬레이션
np.random.seed(42)

reserve_prices = []
min_winning_prices = []
base_to_min_winning_rates = []

for i in range(N_SIMULATIONS):
    selected = np.random.choice(preliminary_prices, N_SELECTED, replace=False)
    reserve_price = np.mean(selected)
    min_winning_price = reserve_price * (AGENCY_RATE / 100)
    base_to_min_winning_rate = (min_winning_price / BASE_AMOUNT) * 100

    reserve_prices.append(reserve_price)
    min_winning_prices.append(min_winning_price)
    base_to_min_winning_rates.append(base_to_min_winning_rate)

reserve_prices = np.array(reserve_prices)
min_winning_prices = np.array(min_winning_prices)
base_to_min_winning_rates = np.array(base_to_min_winning_rates)

# 3. 과거 데이터 로드
data_file = Path("/mnt/a/25/data전처리완료/투찰률_87_745%_데이터.xlsx")
if data_file.exists():
    df = pd.read_excel(data_file)
    df_first = df[df['순위'] == 1].copy()
    print(f"과거 1위 업체 데이터: {len(df_first)}개")
else:
    df_first = None
    print("과거 데이터 없음")

# 4. 한글 고품질 시각화
fig, axes = plt.subplots(2, 2, figsize=(20, 16))
fig.suptitle('복수예가 몬테카를로 시뮬레이션 (10,000회)',
             fontsize=24, fontweight='bold', fontproperties=font_prop, y=0.995)

# 4-1. 예정가격 분포
ax1 = axes[0, 0]
counts1, bins1, patches1 = ax1.hist(reserve_prices, bins=50, alpha=0.75,
                                      color='#5B9BD5', edgecolor='#2C5F8D', linewidth=0.8)
mean_reserve = reserve_prices.mean()
ax1.axvline(mean_reserve, color='#C00000', linestyle='--', linewidth=3,
            label=f'평균: {mean_reserve:,.0f}원', zorder=10)
ax1.axvline(BASE_AMOUNT, color='#70AD47', linestyle='--', linewidth=3,
            label=f'기초금액: {BASE_AMOUNT:,}원', zorder=10)

# 주석
ax1.annotate(f'평균\n{mean_reserve:,.0f}원',
            xy=(mean_reserve, max(counts1)*0.88),
            xytext=(mean_reserve + 250000, max(counts1)*0.95),
            fontsize=12, color='#C00000', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#C00000', lw=2),
            fontproperties=font_prop,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#C00000', alpha=0.9))

ax1.set_xlabel('예정가격 (원)', fontsize=15, fontweight='bold', fontproperties=font_prop)
ax1.set_ylabel('빈도', fontsize=15, fontweight='bold', fontproperties=font_prop)
ax1.set_title('예정가격 분포 (15개 중 4개 평균)', fontsize=17, fontweight='bold',
             fontproperties=font_prop, pad=15)
ax1.legend(prop=font_prop, fontsize=13, framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
ax1.ticklabel_format(style='plain', axis='x')
ax1.tick_params(labelsize=11)

# 4-2. 낙찰하한가 분포
ax2 = axes[0, 1]
counts2, bins2, patches2 = ax2.hist(min_winning_prices, bins=50, alpha=0.75,
                                      color='#ED7D31', edgecolor='#C65911', linewidth=0.8)
mean_min_winning = min_winning_prices.mean()
ax2.axvline(mean_min_winning, color='#C00000', linestyle='--', linewidth=3,
            label=f'평균: {mean_min_winning:,.0f}원', zorder=10)

# 주석
variance_amount = min_winning_prices.max() - min_winning_prices.min()
ax2.annotate(f'평균: {mean_min_winning:,.0f}원\n변동폭: {variance_amount:,.0f}원',
            xy=(mean_min_winning, max(counts2)*0.82),
            xytext=(mean_min_winning + 200000, max(counts2)*0.92),
            fontsize=12, color='#C00000', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#C00000', lw=2),
            fontproperties=font_prop,
            bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor='#C00000', alpha=0.9))

ax2.set_xlabel('낙찰하한가 (원)', fontsize=15, fontweight='bold', fontproperties=font_prop)
ax2.set_ylabel('빈도', fontsize=15, fontweight='bold', fontproperties=font_prop)
ax2.set_title(f'낙찰하한가 분포 (발주처투찰률: {AGENCY_RATE}%)', fontsize=17, fontweight='bold',
             fontproperties=font_prop, pad=15)
ax2.legend(prop=font_prop, fontsize=13, framealpha=0.95)
ax2.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
ax2.ticklabel_format(style='plain', axis='x')
ax2.tick_params(labelsize=11)

# 4-3. 기초대비 낙찰하한율 분포
ax3 = axes[1, 0]
counts3, bins3, patches3 = ax3.hist(base_to_min_winning_rates, bins=60, alpha=0.75,
                                      color='#A47AB5', edgecolor='#7A5495', linewidth=0.8)
mean_rate = base_to_min_winning_rates.mean()
median_rate = np.median(base_to_min_winning_rates)
min_rate = base_to_min_winning_rates.min()
max_rate = base_to_min_winning_rates.max()

ax3.axvline(mean_rate, color='#C00000', linestyle='--', linewidth=3,
            label=f'평균: {mean_rate:.3f}%', zorder=10)
ax3.axvline(AGENCY_RATE, color='#70AD47', linestyle='--', linewidth=3,
            label=f'발주처투찰률: {AGENCY_RATE}%', zorder=10)

# 주석 (범위 표시)
ax3.annotate(f'최소: {min_rate:.3f}%\n평균: {mean_rate:.3f}%\n최대: {max_rate:.3f}%\n\n변동폭: {max_rate-min_rate:.3f}%',
            xy=(mean_rate, max(counts3)*0.65),
            xytext=(mean_rate + 0.6, max(counts3)*0.82),
            fontsize=12, color='#C00000', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='white', alpha=0.95, edgecolor='#C00000', linewidth=2),
            arrowprops=dict(arrowstyle='->', color='#C00000', lw=2),
            fontproperties=font_prop)

ax3.set_xlabel('기초대비 낙찰하한율 (%)', fontsize=15, fontweight='bold', fontproperties=font_prop)
ax3.set_ylabel('빈도', fontsize=15, fontweight='bold', fontproperties=font_prop)
ax3.set_title('기초대비 낙찰하한율 분포 (AI 오류 증명)', fontsize=17, fontweight='bold',
             fontproperties=font_prop, pad=15)
ax3.legend(prop=font_prop, fontsize=13, framealpha=0.95)
ax3.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
ax3.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
ax3.tick_params(labelsize=11)

# 4-4. 시뮬레이션 vs 실제 데이터 비교
ax4 = axes[1, 1]
if df_first is not None:
    # 시뮬레이션 (보라색)
    ax4.hist(base_to_min_winning_rates, bins=60, alpha=0.6, color='#A47AB5',
             edgecolor='#7A5495', linewidth=0.7, label='시뮬레이션 낙찰하한율', density=True)

    # 과거 1위 (녹색)
    ax4.hist(df_first['기초대비투찰률'], bins=60, alpha=0.6, color='#70AD47',
             edgecolor='#507E32', linewidth=0.7, label='과거 1위 입찰률', density=True)

    sim_mean = base_to_min_winning_rates.mean()
    hist_mean = df_first['기초대비투찰률'].mean()
    hist_median = df_first['기초대비투찰률'].median()

    ax4.axvline(sim_mean, color='#A47AB5', linestyle='--', linewidth=3,
                label=f'시뮬 평균: {sim_mean:.3f}%', zorder=10)
    ax4.axvline(hist_mean, color='#70AD47', linestyle='--', linewidth=3,
                label=f'실제 평균: {hist_mean:.3f}%', zorder=10)
    ax4.axvline(hist_median, color='#FFC000', linestyle=':', linewidth=3,
                label=f'실제 중앙값: {hist_median:.3f}%', zorder=10)

    # 안전 마진 주석
    safety_margin = hist_mean - sim_mean
    ax4.annotate(f'안전 마진\n{safety_margin:.3f}%\n(실제 - 시뮬)',
                xy=(hist_mean, 0.55),
                xytext=(hist_mean + 0.35, 0.7),
                fontsize=12, color='#70AD47', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='white', alpha=0.95,
                         edgecolor='#70AD47', linewidth=2),
                arrowprops=dict(arrowstyle='->', color='#70AD47', lw=2),
                fontproperties=font_prop)

    # 추천 전략 주석
    recommended_amount = BASE_AMOUNT * hist_median / 100
    ax4.annotate(f'추천 입찰률\n{hist_median:.3f}%\n\n추천 입찰금액\n{recommended_amount:,.0f}원',
                xy=(hist_median, 0.25),
                xytext=(hist_median - 0.6, 0.45),
                fontsize=12, color='#FFC000', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.7', facecolor='#FFFACD', alpha=0.95,
                         edgecolor='#FFC000', linewidth=2.5),
                arrowprops=dict(arrowstyle='->', color='#FFC000', lw=2.5),
                fontproperties=font_prop)

    ax4.set_xlabel('투찰률 (%)', fontsize=15, fontweight='bold', fontproperties=font_prop)
    ax4.set_ylabel('확률밀도', fontsize=15, fontweight='bold', fontproperties=font_prop)
    ax4.set_title(f'시뮬레이션 vs 실제 낙찰자 비교 ({len(df_first)}개 사례)',
                 fontsize=17, fontweight='bold', fontproperties=font_prop, pad=15)
    ax4.legend(prop=font_prop, fontsize=12, loc='upper left', framealpha=0.95)
    ax4.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
    ax4.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
    ax4.tick_params(labelsize=11)
else:
    ax4.text(0.5, 0.5, '과거 데이터 없음', ha='center', va='center',
            fontsize=18, fontproperties=font_prop)
    ax4.set_title('과거 데이터 비교', fontsize=17, fontweight='bold',
                 fontproperties=font_prop, pad=15)

plt.tight_layout(rect=[0, 0, 1, 0.99])
output_file = Path('/mnt/a/25/data분석/monte_carlo_final.png')
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"\n✓ 한글 고해상도 시각화 저장: {output_file}")
print(f"  - 해상도: 300 DPI")
print(f"  - 폰트: {font_prop.get_name()}")
print(f"  - 소수점 3자리 표시")

# 5. 통계 요약 출력
print(f"\n{'='*80}")
print(f"시뮬레이션 결과 요약")
print(f"{'='*80}")
print(f"\n[예정가격]")
print(f"  평균: {reserve_prices.mean():,.0f}원")
print(f"  변동폭: {reserve_prices.max() - reserve_prices.min():,.0f}원")
print(f"\n[낙찰하한가]")
print(f"  평균: {min_winning_prices.mean():,.0f}원")
print(f"  변동폭: {min_winning_prices.max() - min_winning_prices.min():,.0f}원")
print(f"\n[기초대비 낙찰하한율]")
print(f"  평균: {base_to_min_winning_rates.mean():.3f}%")
print(f"  범위: {base_to_min_winning_rates.min():.3f}% ~ {base_to_min_winning_rates.max():.3f}%")
print(f"  변동폭: {base_to_min_winning_rates.max() - base_to_min_winning_rates.min():.3f}%")

if df_first is not None:
    print(f"\n[과거 1위 업체 ({len(df_first)}개)]")
    print(f"  평균: {df_first['기초대비투찰률'].mean():.3f}%")
    print(f"  중앙값: {df_first['기초대비투찰률'].median():.3f}%")
    print(f"\n[추천 전략]")
    print(f"  입찰률: {df_first['기초대비투찰률'].median():.3f}%")
    print(f"  입찰금액: {BASE_AMOUNT * df_first['기초대비투찰률'].median() / 100:,.0f}원")
    print(f"  안전 마진: {df_first['기초대비투찰률'].mean() - base_to_min_winning_rates.mean():.3f}%")

print(f"\n{'='*80}")
print(f"✓ 완료!")
print(f"{'='*80}")
