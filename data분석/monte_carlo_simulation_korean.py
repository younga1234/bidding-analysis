#!/usr/bin/env python3
"""
복수예가 몬테카를로 시뮬레이션 - 한글 고품질 시각화

목적: 예정가격과 낙찰하한가의 확률분포를 10,000회 시뮬레이션으로 분석
모든 텍스트를 한글로 표기, 소수점 3자리 정밀도
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import ticker
from pathlib import Path

# 한글 폰트 설정 (시스템에 설치된 한글 폰트 찾기)
def get_korean_font():
    """시스템에서 사용 가능한 한글 폰트 찾기"""
    font_list = [f.name for f in fm.fontManager.ttflist]

    # 우선순위: 맑은고딕 > 나눔고딕 > AppleGothic > 그 외
    preferred_fonts = ['Malgun Gothic', 'NanumGothic', 'NanumBarunGothic',
                      'Apple SD Gothic Neo', 'AppleGothic']

    for font in preferred_fonts:
        if font in font_list:
            print(f"한글 폰트 사용: {font}")
            return font

    # 한글 폰트가 없으면 기본 폰트
    print("한글 폰트를 찾을 수 없습니다. 기본 폰트 사용")
    return 'DejaVu Sans'

korean_font = get_korean_font()
plt.rcParams['font.family'] = korean_font
plt.rcParams['axes.unicode_minus'] = False

# 현재 공고 정보
BASE_AMOUNT = 39_000_000  # 기초금액
AGENCY_RATE = 87.745  # 발주처투찰률 (%)
VARIANCE_RANGE = 0.03  # ±3%

# 시뮬레이션 설정
N_SIMULATIONS = 10_000
N_PRELIMINARY_PRICES = 15
N_SELECTED = 4

print("="*80)
print("복수예가 몬테카를로 시뮬레이션 - 한글 고품질 시각화")
print("="*80)
print(f"기초금액: {BASE_AMOUNT:,}원")
print(f"발주처투찰률: {AGENCY_RATE}%")
print(f"예가범위: ±{VARIANCE_RANGE*100}%")
print(f"시뮬레이션 횟수: {N_SIMULATIONS:,}회")
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
    print(f"\n과거 1위 업체 데이터: {len(df_first)}개")
else:
    df_first = None
    print(f"\n과거 데이터 없음")

# 4. 한글 고품질 시각화
fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle('복수예가 몬테카를로 시뮬레이션 (10,000회)',
             fontsize=20, fontweight='bold', fontproperties=fm.FontProperties(family=korean_font))

# 4-1. 예정가격 분포
ax1 = axes[0, 0]
counts1, bins1, patches1 = ax1.hist(reserve_prices, bins=50, alpha=0.7,
                                      color='#5B9BD5', edgecolor='black', linewidth=0.5)
mean_reserve = reserve_prices.mean()
ax1.axvline(mean_reserve, color='#C00000', linestyle='--', linewidth=2.5,
            label=f'평균: {mean_reserve:,.0f}원')
ax1.axvline(BASE_AMOUNT, color='#70AD47', linestyle='--', linewidth=2.5,
            label=f'기초금액: {BASE_AMOUNT:,}원')

# 주석 추가
ax1.annotate(f'평균: {mean_reserve:,.0f}원',
            xy=(mean_reserve, max(counts1)*0.9),
            xytext=(mean_reserve + 200000, max(counts1)*0.95),
            fontsize=11, color='#C00000', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#C00000', lw=1.5),
            fontproperties=fm.FontProperties(family=korean_font))

ax1.set_xlabel('예정가격 (원)', fontsize=13, fontweight='bold',
              fontproperties=fm.FontProperties(family=korean_font))
ax1.set_ylabel('빈도', fontsize=13, fontweight='bold',
              fontproperties=fm.FontProperties(family=korean_font))
ax1.set_title('예정가격 분포 (15개 중 4개 평균)', fontsize=15, fontweight='bold',
             fontproperties=fm.FontProperties(family=korean_font))
ax1.legend(prop=fm.FontProperties(family=korean_font, size=11))
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.ticklabel_format(style='plain', axis='x')

# 4-2. 낙찰하한가 분포
ax2 = axes[0, 1]
counts2, bins2, patches2 = ax2.hist(min_winning_prices, bins=50, alpha=0.7,
                                      color='#ED7D31', edgecolor='black', linewidth=0.5)
mean_min_winning = min_winning_prices.mean()
ax2.axvline(mean_min_winning, color='#C00000', linestyle='--', linewidth=2.5,
            label=f'평균: {mean_min_winning:,.0f}원')

# 주석 추가
ax2.annotate(f'평균: {mean_min_winning:,.0f}원\n변동폭: {min_winning_prices.max()-min_winning_prices.min():,.0f}원',
            xy=(mean_min_winning, max(counts2)*0.85),
            xytext=(mean_min_winning + 150000, max(counts2)*0.9),
            fontsize=11, color='#C00000', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#C00000', lw=1.5),
            fontproperties=fm.FontProperties(family=korean_font))

ax2.set_xlabel('낙찰하한가 (원)', fontsize=13, fontweight='bold',
              fontproperties=fm.FontProperties(family=korean_font))
ax2.set_ylabel('빈도', fontsize=13, fontweight='bold',
              fontproperties=fm.FontProperties(family=korean_font))
ax2.set_title(f'낙찰하한가 분포 (발주처투찰률: {AGENCY_RATE}%)', fontsize=15, fontweight='bold',
             fontproperties=fm.FontProperties(family=korean_font))
ax2.legend(prop=fm.FontProperties(family=korean_font, size=11))
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.ticklabel_format(style='plain', axis='x')

# 4-3. 기초대비 낙찰하한율 분포
ax3 = axes[1, 0]
counts3, bins3, patches3 = ax3.hist(base_to_min_winning_rates, bins=60, alpha=0.7,
                                      color='#A47AB5', edgecolor='black', linewidth=0.5)
mean_rate = base_to_min_winning_rates.mean()
median_rate = np.median(base_to_min_winning_rates)
ax3.axvline(mean_rate, color='#C00000', linestyle='--', linewidth=2.5,
            label=f'평균: {mean_rate:.3f}%')
ax3.axvline(AGENCY_RATE, color='#70AD47', linestyle='--', linewidth=2.5,
            label=f'발주처투찰률: {AGENCY_RATE}%')

# 주석 추가 (범위 표시)
min_rate = base_to_min_winning_rates.min()
max_rate = base_to_min_winning_rates.max()
ax3.annotate(f'최소: {min_rate:.3f}%\n평균: {mean_rate:.3f}%\n최대: {max_rate:.3f}%\n변동폭: {max_rate-min_rate:.3f}%',
            xy=(mean_rate, max(counts3)*0.7),
            xytext=(mean_rate + 0.5, max(counts3)*0.8),
            fontsize=10, color='#C00000', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='#C00000'),
            arrowprops=dict(arrowstyle='->', color='#C00000', lw=1.5),
            fontproperties=fm.FontProperties(family=korean_font))

ax3.set_xlabel('기초대비 낙찰하한율 (%)', fontsize=13, fontweight='bold',
              fontproperties=fm.FontProperties(family=korean_font))
ax3.set_ylabel('빈도', fontsize=13, fontweight='bold',
              fontproperties=fm.FontProperties(family=korean_font))
ax3.set_title('기초대비 낙찰하한율 분포 (AI 오류 증명)', fontsize=15, fontweight='bold',
             fontproperties=fm.FontProperties(family=korean_font))
ax3.legend(prop=fm.FontProperties(family=korean_font, size=11))
ax3.grid(True, alpha=0.3, linestyle='--')
ax3.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))

# 4-4. 시뮬레이션 vs 실제 데이터 비교
ax4 = axes[1, 1]
if df_first is not None:
    # 시뮬레이션 (보라색)
    ax4.hist(base_to_min_winning_rates, bins=60, alpha=0.6, color='#A47AB5',
             edgecolor='black', linewidth=0.5, label='시뮬레이션 낙찰하한율', density=True)

    # 과거 1위 (녹색)
    ax4.hist(df_first['기초대비투찰률'], bins=60, alpha=0.6, color='#70AD47',
             edgecolor='black', linewidth=0.5, label='과거 1위 입찰률', density=True)

    sim_mean = base_to_min_winning_rates.mean()
    hist_mean = df_first['기초대비투찰률'].mean()
    hist_median = df_first['기초대비투찰률'].median()

    ax4.axvline(sim_mean, color='#A47AB5', linestyle='--', linewidth=2.5,
                label=f'시뮬 평균: {sim_mean:.3f}%')
    ax4.axvline(hist_mean, color='#70AD47', linestyle='--', linewidth=2.5,
                label=f'실제 평균: {hist_mean:.3f}%')
    ax4.axvline(hist_median, color='#FFC000', linestyle=':', linewidth=2.5,
                label=f'실제 중앙값: {hist_median:.3f}%')

    # 주석 추가 (안전 마진 표시)
    safety_margin = hist_mean - sim_mean
    ax4.annotate(f'안전 마진: {safety_margin:.3f}%\n(실제 - 시뮬)',
                xy=(hist_mean, 0.6),
                xytext=(hist_mean + 0.3, 0.7),
                fontsize=11, color='#70AD47', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='#70AD47'),
                arrowprops=dict(arrowstyle='->', color='#70AD47', lw=1.5),
                fontproperties=fm.FontProperties(family=korean_font))

    # 추천 전략 표시
    ax4.annotate(f'추천 입찰률\n{hist_median:.3f}%\n({BASE_AMOUNT * hist_median / 100:,.0f}원)',
                xy=(hist_median, 0.3),
                xytext=(hist_median - 0.5, 0.4),
                fontsize=11, color='#FFC000', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFFACD', alpha=0.9, edgecolor='#FFC000', linewidth=2),
                arrowprops=dict(arrowstyle='->', color='#FFC000', lw=2),
                fontproperties=fm.FontProperties(family=korean_font))

    ax4.set_xlabel('투찰률 (%)', fontsize=13, fontweight='bold',
                  fontproperties=fm.FontProperties(family=korean_font))
    ax4.set_ylabel('확률밀도', fontsize=13, fontweight='bold',
                  fontproperties=fm.FontProperties(family=korean_font))
    ax4.set_title(f'시뮬레이션 vs 실제 낙찰자 비교 ({len(df_first)}개)', fontsize=15, fontweight='bold',
                 fontproperties=fm.FontProperties(family=korean_font))
    ax4.legend(prop=fm.FontProperties(family=korean_font, size=10), loc='upper left')
    ax4.grid(True, alpha=0.3, linestyle='--')
    ax4.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
else:
    ax4.text(0.5, 0.5, '과거 데이터 없음',
             ha='center', va='center', fontsize=16,
             fontproperties=fm.FontProperties(family=korean_font))
    ax4.set_title('과거 데이터 비교', fontsize=15, fontweight='bold',
                 fontproperties=fm.FontProperties(family=korean_font))

plt.tight_layout()
output_file = Path('/mnt/a/25/data분석/monte_carlo_korean_highres.png')
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\n한글 고해상도 시각화 저장: {output_file}")

# 5. 통계 요약 저장 (JSON)
summary = {
    "기초금액": BASE_AMOUNT,
    "발주처투찰률": AGENCY_RATE,
    "시뮬레이션_횟수": N_SIMULATIONS,
    "예정가격": {
        "평균": float(reserve_prices.mean()),
        "중앙값": float(np.median(reserve_prices)),
        "표준편차": float(reserve_prices.std()),
        "최소": float(reserve_prices.min()),
        "최대": float(reserve_prices.max()),
        "변동폭": float(reserve_prices.max() - reserve_prices.min())
    },
    "낙찰하한가": {
        "평균": float(min_winning_prices.mean()),
        "중앙값": float(np.median(min_winning_prices)),
        "표준편차": float(min_winning_prices.std()),
        "최소": float(min_winning_prices.min()),
        "최대": float(min_winning_prices.max()),
        "변동폭": float(min_winning_prices.max() - min_winning_prices.min())
    },
    "기초대비_낙찰하한율": {
        "평균": round(base_to_min_winning_rates.mean(), 3),
        "중앙값": round(np.median(base_to_min_winning_rates), 3),
        "표준편차": round(base_to_min_winning_rates.std(), 3),
        "최소": round(base_to_min_winning_rates.min(), 3),
        "최대": round(base_to_min_winning_rates.max(), 3),
        "변동폭": round(base_to_min_winning_rates.max() - base_to_min_winning_rates.min(), 3),
        "백분위수": {
            "5%": round(np.percentile(base_to_min_winning_rates, 5), 3),
            "25%": round(np.percentile(base_to_min_winning_rates, 25), 3),
            "50%": round(np.percentile(base_to_min_winning_rates, 50), 3),
            "75%": round(np.percentile(base_to_min_winning_rates, 75), 3),
            "95%": round(np.percentile(base_to_min_winning_rates, 95), 3)
        }
    }
}

if df_first is not None:
    summary["과거_1위_데이터"] = {
        "데이터_개수": len(df_first),
        "평균": round(df_first['기초대비투찰률'].mean(), 3),
        "중앙값": round(df_first['기초대비투찰률'].median(), 3),
        "표준편차": round(df_first['기초대비투찰률'].std(), 3),
        "최소": round(df_first['기초대비투찰률'].min(), 3),
        "최대": round(df_first['기초대비투찰률'].max(), 3)
    }
    summary["비교분석"] = {
        "안전_마진": round(df_first['기초대비투찰률'].mean() - base_to_min_winning_rates.mean(), 3),
        "추천_입찰률": round(df_first['기초대비투찰률'].median(), 3),
        "추천_입찰금액": int(BASE_AMOUNT * df_first['기초대비투찰률'].median() / 100)
    }

import json
summary_file = Path('/mnt/a/25/data분석/monte_carlo_summary.json')
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print(f"통계 요약 저장: {summary_file}")

# 6. CSV 저장
summary_df = pd.DataFrame({
    "구분": ["예정가격", "낙찰하한가", "기초대비_낙찰하한율"],
    "평균": [
        f"{reserve_prices.mean():,.0f}원",
        f"{min_winning_prices.mean():,.0f}원",
        f"{base_to_min_winning_rates.mean():.3f}%"
    ],
    "중앙값": [
        f"{np.median(reserve_prices):,.0f}원",
        f"{np.median(min_winning_prices):,.0f}원",
        f"{np.median(base_to_min_winning_rates):.3f}%"
    ],
    "표준편차": [
        f"{reserve_prices.std():,.0f}원",
        f"{min_winning_prices.std():,.0f}원",
        f"{base_to_min_winning_rates.std():.3f}%"
    ],
    "최소": [
        f"{reserve_prices.min():,.0f}원",
        f"{min_winning_prices.min():,.0f}원",
        f"{base_to_min_winning_rates.min():.3f}%"
    ],
    "최대": [
        f"{reserve_prices.max():,.0f}원",
        f"{min_winning_prices.max():,.0f}원",
        f"{base_to_min_winning_rates.max():.3f}%"
    ]
})

csv_file = Path('/mnt/a/25/data분석/monte_carlo_summary.csv')
summary_df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"CSV 요약 저장: {csv_file}")

print("\n" + "="*80)
print("한글 고품질 시각화 완료!")
print("="*80)
