#!/usr/bin/env python3
"""
경쟁업체 분석 V2 - 발주처투찰률별 + AI 사용 여부 판단

1. 발주처투찰률별로 완전히 분리하여 분석
2. AI 분석 사용 가능성 판단
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path
from collections import Counter
from scipy import stats
import json
from datetime import datetime

def get_korean_font():
    """한국어 폰트 감지"""
    preferred_fonts = [
        'Noto Sans KR', 'NotoSansKR', 'Noto Sans CJK KR',
        'Noto Sans CJK JP', 'NanumGothic', 'NanumBarunGothic',
        'Malgun Gothic', 'DejaVu Sans'
    ]
    available_fonts = {f.name for f in fm.fontManager.ttflist}
    for font in preferred_fonts:
        if font in available_fonts:
            return font
    return 'DejaVu Sans'

class CompetitorAnalyzerV2:
    """경쟁업체 분석기 V2 - 발주처투찰률별 + AI 판단"""

    def __init__(self, data_file, company_name):
        self.data_file = data_file
        self.company_name = company_name
        self.df = None
        self.company_df = None
        self.results = {}
        self.ai_analysis = {}

        # 한글 폰트
        korean_font = get_korean_font()
        plt.rcParams['font.family'] = korean_font
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 10
        print(f"[폰트] {korean_font}")

    def load_data(self):
        """데이터 로드"""
        print(f"\n[데이터 로드] {self.data_file}")
        self.df = pd.read_excel(self.data_file)
        print(f"  전체 데이터: {len(self.df):,}건")

        # 업체명 필터링
        mask = self.df['업체명'].str.contains(self.company_name, case=False, na=False)
        self.company_df = self.df[mask].copy()

        print(f"  '{self.company_name}' 참여: {len(self.company_df):,}건")

        if len(self.company_df) == 0:
            print(f"\n⚠️ '{self.company_name}' 데이터가 없습니다.")
            return False

        return True

    def analyze_by_agency_rate(self):
        """발주처투찰률별 완전 분리 분석"""
        print(f"\n{'='*80}")
        print("발주처투찰률별 분리 분석")
        print(f"{'='*80}")

        agency_rates = sorted(self.company_df['발주처투찰률'].unique())
        self.results['발주처투찰률별_분석'] = {}

        for rate in agency_rates:
            print(f"\n{'─'*80}")
            print(f"[발주처투찰률 {rate}%]")
            print(f"{'─'*80}")

            subset = self.company_df[self.company_df['발주처투찰률'] == rate].copy()

            analysis = self._analyze_single_group(subset, rate)
            self.results['발주처투찰률별_분석'][str(rate)] = analysis

    def _analyze_single_group(self, df, rate):
        """단일 발주처투찰률 그룹 분석"""

        result = {}

        # 1. 기본 통계
        total = len(df)
        wins = (df['순위'] == 1).sum()
        below = (df['순위'] == -1).sum()

        result['참여'] = int(total)
        result['1위'] = int(wins)
        result['1위확률'] = round((wins / total * 100) if total > 0 else 0, 2)
        result['미달'] = int(below)
        result['미달확률'] = round((below / total * 100) if total > 0 else 0, 2)

        print(f"  참여: {total}건, 1위: {wins}건 ({result['1위확률']}%), 미달: {below}건 ({result['미달확률']}%)")

        # 2. 투찰률 통계
        rates = df['기초대비투찰률'].dropna()

        if len(rates) > 0:
            result['투찰률_통계'] = {
                '평균': round(rates.mean(), 3),
                '중앙값': round(rates.median(), 3),
                '표준편차': round(rates.std(), 3),
                '최소': round(rates.min(), 3),
                '최대': round(rates.max(), 3),
                '백분위수': {
                    '25%': round(rates.quantile(0.25), 3),
                    '50%': round(rates.quantile(0.50), 3),
                    '75%': round(rates.quantile(0.75), 3)
                }
            }
            print(f"  투찰률: 평균 {rates.mean():.3f}%, 중앙값 {rates.median():.3f}%, 표준편차 {rates.std():.3f}%")

        # 3. 1위 패턴
        wins_df = df[df['순위'] == 1]
        win_rates = wins_df['기초대비투찰률'].dropna()

        if len(win_rates) > 0:
            result['1위_패턴'] = {
                '평균': round(win_rates.mean(), 3),
                '중앙값': round(win_rates.median(), 3),
                '표준편차': round(win_rates.std(), 3),
                '최소': round(win_rates.min(), 3),
                '최대': round(win_rates.max(), 3)
            }
            print(f"  1위 시: 평균 {win_rates.mean():.3f}%, 중앙값 {win_rates.median():.3f}%")

        # 4. 소수점 패턴
        if len(rates) > 0:
            decimal_3rd = ((rates * 1000) % 10).astype(int)
            decimal_counts = Counter(decimal_3rd)

            result['소수점_3자리_분포'] = {str(k): int(v) for k, v in sorted(decimal_counts.items())}

            # 끝자리 패턴 (기초금액 50,000,000 가정)
            amounts = 50000000 * rates / 100
            endings = (amounts % 1000).astype(int)
            ending_counts = Counter(endings)

            result['끝자리_분포'] = {str(k): int(v) for k, v in sorted(ending_counts.most_common(10))}

        return result

    def detect_ai_usage(self):
        """AI 분석 사용 여부 판단"""
        print(f"\n{'='*80}")
        print("AI 분석 사용 여부 판단")
        print(f"{'='*80}")

        indicators = []
        scores = []

        # 1. 소수점 패턴의 전략성
        decimal_score, decimal_desc = self._check_decimal_strategy()
        indicators.append(("소수점 패턴 전략성", decimal_score, decimal_desc))
        scores.append(decimal_score)

        # 2. 경쟁 밀도 회피 패턴
        density_score, density_desc = self._check_density_avoidance()
        indicators.append(("경쟁 밀도 회피", density_score, density_desc))
        scores.append(density_score)

        # 3. 시간에 따른 학습 패턴
        learning_score, learning_desc = self._check_learning_pattern()
        indicators.append(("시간에 따른 학습", learning_score, learning_desc))
        scores.append(learning_score)

        # 4. 투찰률 정교함
        precision_score, precision_desc = self._check_precision()
        indicators.append(("투찰률 정교함", precision_score, precision_desc))
        scores.append(precision_score)

        # 5. 발주처별 차별화
        agency_score, agency_desc = self._check_agency_differentiation()
        indicators.append(("발주처별 차별화", agency_score, agency_desc))
        scores.append(agency_score)

        # 종합 점수
        total_score = sum(scores)
        max_score = len(scores) * 10

        self.ai_analysis = {
            '종합_점수': f"{total_score}/{max_score}",
            '백분율': round((total_score / max_score) * 100, 1),
            '판단': self._judge_ai_usage(total_score, max_score),
            '세부_지표': [
                {
                    '항목': name,
                    '점수': f"{score}/10",
                    '설명': desc
                }
                for name, score, desc in indicators
            ]
        }

        print(f"\n{'─'*80}")
        print(f"종합 판단: {self.ai_analysis['판단']}")
        print(f"종합 점수: {total_score}/{max_score} ({self.ai_analysis['백분율']}%)")
        print(f"{'─'*80}")

        for item in self.ai_analysis['세부_지표']:
            print(f"\n{item['항목']}: {item['점수']}")
            print(f"  {item['설명']}")

    def _check_decimal_strategy(self):
        """소수점 패턴 전략성 검사"""
        all_rates = self.company_df['기초대비투찰률'].dropna()

        if len(all_rates) < 10:
            return 0, "데이터 부족"

        # 소수점 3자리
        decimal_3rd = ((all_rates * 1000) % 10).astype(int)
        counts = Counter(decimal_3rd)

        # 균등 분포면 각 숫자가 10%씩
        expected = len(decimal_3rd) / 10

        # 카이제곱 검정
        observed = [counts.get(i, 0) for i in range(10)]
        chi2, p_value = stats.chisquare(observed, [expected] * 10)

        # p < 0.05면 전략적 (균등 분포 아님)
        if p_value < 0.05:
            # 가장 적게 사용된 숫자들
            least_used = sorted(counts.items(), key=lambda x: x[1])[:3]
            least_digits = [str(d) for d, _ in least_used]

            score = min(10, int((1 - p_value) * 10))
            desc = f"전략적 회피 감지 (p={p_value:.4f}). 숫자 {', '.join(least_digits)} 회피. AI 가능성 높음."
        else:
            score = 0
            desc = f"무작위 분포 (p={p_value:.4f}). AI 패턴 없음."

        return score, desc

    def _check_density_avoidance(self):
        """경쟁 밀도 회피 패턴 검사"""
        # 각 발주처투찰률별로 경쟁 밀도 분석
        avoid_count = 0
        total_groups = 0

        for rate in self.company_df['발주처투찰률'].unique():
            company_subset = self.company_df[self.company_df['발주처투찰률'] == rate]
            all_subset = self.df[self.df['발주처투찰률'] == rate]

            if len(company_subset) < 5 or len(all_subset) < 100:
                continue

            total_groups += 1

            # 전체 경쟁자의 투찰률 분포
            all_rates = all_subset['기초대비투찰률'].dropna()
            company_rates = company_subset['기초대비투찰률'].dropna()

            if len(all_rates) == 0 or len(company_rates) == 0:
                continue

            # 히스토그램 (0.1% 단위)
            bins = np.arange(all_rates.min(), all_rates.max() + 0.1, 0.1)
            all_hist, _ = np.histogram(all_rates, bins=bins)
            company_hist, _ = np.histogram(company_rates, bins=bins)

            # 고밀도 구간 (상위 20%)
            threshold = np.percentile(all_hist, 80)
            high_density = all_hist >= threshold

            # 해당 업체가 고밀도 구간을 회피하는가?
            if len(company_hist[high_density]) > 0:
                company_in_high = company_hist[high_density].sum()
                company_total = company_hist.sum()

                if company_in_high / company_total < 0.3:  # 30% 미만
                    avoid_count += 1

        if total_groups == 0:
            return 0, "데이터 부족"

        avoid_rate = avoid_count / total_groups

        if avoid_rate >= 0.7:
            score = 10
            desc = f"경쟁 밀도 회피 패턴 강함 ({avoid_count}/{total_groups} 그룹). AI 가능성 매우 높음."
        elif avoid_rate >= 0.5:
            score = 7
            desc = f"경쟁 밀도 회피 패턴 있음 ({avoid_count}/{total_groups} 그룹). AI 가능성 있음."
        elif avoid_rate >= 0.3:
            score = 4
            desc = f"부분적 회피 패턴 ({avoid_count}/{total_groups} 그룹). 약한 AI 패턴."
        else:
            score = 0
            desc = f"회피 패턴 없음 ({avoid_count}/{total_groups} 그룹). AI 패턴 없음."

        return score, desc

    def _check_learning_pattern(self):
        """시간에 따른 학습 패턴 검사"""
        if '투찰일시' not in self.company_df.columns:
            return 0, "투찰일시 데이터 없음"

        df = self.company_df.copy()
        df['투찰일시'] = pd.to_datetime(df['투찰일시'], errors='coerce')
        df = df.dropna(subset=['투찰일시', '기초대비투찰률'])
        df = df.sort_values('투찰일시')

        if len(df) < 30:
            return 0, "데이터 부족 (30건 미만)"

        # 전반부 vs 후반부
        mid = len(df) // 2
        first_half = df.iloc[:mid]
        second_half = df.iloc[mid:]

        # 1위 확률 비교
        first_win_rate = (first_half['순위'] == 1).sum() / len(first_half) * 100
        second_win_rate = (second_half['순위'] == 1).sum() / len(second_half) * 100

        # 표준편차 비교 (정교해지면 감소)
        first_std = first_half['기초대비투찰률'].std()
        second_std = second_half['기초대비투찰률'].std()

        improvement = second_win_rate - first_win_rate
        precision_gain = first_std - second_std

        if improvement > 1.5 and precision_gain > 0.3:
            score = 10
            desc = f"명확한 학습 패턴 (1위 확률 {improvement:.1f}%p 향상, 정교도 {precision_gain:.3f}% 개선). AI 학습 가능성 매우 높음."
        elif improvement > 0.5 or precision_gain > 0.1:
            score = 6
            desc = f"학습 징후 있음 (1위 확률 {improvement:.1f}%p, 정교도 {precision_gain:.3f}%). AI 가능성 있음."
        elif improvement > -0.5:
            score = 3
            desc = f"변화 미미 (1위 확률 {improvement:.1f}%p). 약한 학습 패턴."
        else:
            score = 0
            desc = f"학습 패턴 없음 (1위 확률 {improvement:.1f}%p 감소). AI 패턴 없음."

        return score, desc

    def _check_precision(self):
        """투찰률 정교함 검사"""
        all_rates = self.company_df['기초대비투찰률'].dropna()

        if len(all_rates) < 10:
            return 0, "데이터 부족"

        # 소수점 3자리 다양성
        decimal_3rd = ((all_rates * 1000) % 10).astype(int)
        unique_count = len(set(decimal_3rd))

        # 끝자리 다양성 (기초금액 50,000,000 가정)
        amounts = 50000000 * all_rates / 100
        endings = (amounts % 1000).astype(int)
        unique_endings = len(set(endings))

        # 정교함 점수
        if unique_count >= 8 and unique_endings >= 20:
            score = 10
            desc = f"매우 정교함 (소수점 {unique_count}/10 다양, 끝자리 {unique_endings}종). AI 최적화 가능성 높음."
        elif unique_count >= 6 and unique_endings >= 10:
            score = 7
            desc = f"정교함 (소수점 {unique_count}/10, 끝자리 {unique_endings}종). AI 가능성 있음."
        elif unique_count >= 4:
            score = 4
            desc = f"보통 (소수점 {unique_count}/10). 약한 정교함."
        else:
            score = 0
            desc = f"단순함 (소수점 {unique_count}/10). AI 패턴 없음."

        return score, desc

    def _check_agency_differentiation(self):
        """발주처별 차별화 전략 검사"""
        agency_rates = self.company_df['발주처투찰률'].unique()

        if len(agency_rates) < 2:
            return 0, "발주처투찰률 1개만 참여"

        # 각 발주처투찰률별 평균 투찰률
        agency_avgs = []
        for rate in agency_rates:
            subset = self.company_df[self.company_df['발주처투찰률'] == rate]
            avg = subset['기초대비투찰률'].mean()
            agency_avgs.append((rate, avg))

        # 발주처별 차이 계산
        diffs = []
        for i in range(len(agency_avgs)):
            for j in range(i+1, len(agency_avgs)):
                rate1, avg1 = agency_avgs[i]
                rate2, avg2 = agency_avgs[j]
                diff = abs(avg1 - avg2)
                diffs.append(diff)

        if not diffs:
            return 0, "비교 불가"

        avg_diff = np.mean(diffs)

        if avg_diff > 1.0:
            score = 10
            desc = f"발주처별 차별화 강함 (평균 차이 {avg_diff:.3f}%). AI 전략 가능성 매우 높음."
        elif avg_diff > 0.5:
            score = 7
            desc = f"발주처별 차별화 있음 (평균 차이 {avg_diff:.3f}%). AI 가능성 있음."
        elif avg_diff > 0.2:
            score = 4
            desc = f"약간의 차별화 (평균 차이 {avg_diff:.3f}%)."
        else:
            score = 0
            desc = f"차별화 없음 (평균 차이 {avg_diff:.3f}%). AI 패턴 없음."

        return score, desc

    def _judge_ai_usage(self, score, max_score):
        """AI 사용 종합 판단"""
        percentage = (score / max_score) * 100

        if percentage >= 70:
            return "AI 분석 사용 가능성 매우 높음 ⚠️"
        elif percentage >= 50:
            return "AI 분석 사용 가능성 높음"
        elif percentage >= 30:
            return "AI 분석 사용 가능성 있음"
        elif percentage >= 10:
            return "AI 분석 사용 가능성 낮음"
        else:
            return "AI 분석 사용 가능성 거의 없음"

    def visualize(self):
        """시각화"""
        print(f"\n[시각화 생성]")

        # 발주처투찰률별 그래프 생성
        agency_rates = sorted(self.company_df['발주처투찰률'].unique())

        # 주요 3개 그룹만 시각화
        top_agencies = self.company_df['발주처투찰률'].value_counts().head(3).index

        for rate in top_agencies:
            self._visualize_single_group(rate)

    def _visualize_single_group(self, rate):
        """단일 발주처투찰률 그룹 시각화"""
        subset = self.company_df[self.company_df['발주처투찰률'] == rate]

        if len(subset) < 5:
            return

        fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=150)
        fig.suptitle(f'{self.company_name} - 발주처투찰률 {rate}% 그룹 분석',
                     fontsize=16, weight='bold')

        # 1. 투찰률 분포
        ax1 = axes[0, 0]
        rates = subset['기초대비투찰률'].dropna()
        if len(rates) > 0:
            ax1.hist(rates, bins=20, color='#3498db', alpha=0.7, edgecolor='black')
            ax1.axvline(rates.mean(), color='red', linestyle='--', linewidth=2,
                       label=f'평균: {rates.mean():.3f}%')
            ax1.axvline(rates.median(), color='green', linestyle='--', linewidth=2,
                       label=f'중앙값: {rates.median():.3f}%')
            ax1.set_xlabel('기초대비투찰률 (%)', fontsize=11, weight='bold')
            ax1.set_ylabel('빈도', fontsize=11, weight='bold')
            ax1.set_title('투찰률 분포', fontsize=12, weight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)

        # 2. 순위 분포
        ax2 = axes[0, 1]
        rank_counts = subset['순위'].value_counts().sort_index()
        colors = ['#2ecc71' if r == 1 else '#e74c3c' if r == -1 else '#95a5a6'
                  for r in rank_counts.index]
        ax2.bar(rank_counts.index, rank_counts.values, color=colors, edgecolor='black')
        ax2.set_xlabel('순위', fontsize=11, weight='bold')
        ax2.set_ylabel('빈도', fontsize=11, weight='bold')
        ax2.set_title('순위 분포', fontsize=12, weight='bold')
        ax2.grid(True, alpha=0.3, axis='y')

        # 3. 소수점 3자리 분포
        ax3 = axes[1, 0]
        if len(rates) > 0:
            decimal_3rd = ((rates * 1000) % 10).astype(int)
            decimal_counts = Counter(decimal_3rd)
            ax3.bar(decimal_counts.keys(), decimal_counts.values(),
                   color='#9b59b6', edgecolor='black')
            ax3.set_xlabel('소수점 셋째자리', fontsize=11, weight='bold')
            ax3.set_ylabel('빈도', fontsize=11, weight='bold')
            ax3.set_title('소수점 패턴 (AI 전략 탐지)', fontsize=12, weight='bold')
            ax3.grid(True, alpha=0.3, axis='y')

        # 4. 시간에 따른 패턴
        ax4 = axes[1, 1]
        if '투찰일시' in subset.columns:
            time_df = subset.copy()
            time_df['투찰일시'] = pd.to_datetime(time_df['투찰일시'], errors='coerce')
            time_df = time_df.dropna(subset=['투찰일시', '기초대비투찰률'])
            time_df = time_df.sort_values('투찰일시')

            if len(time_df) > 0:
                ax4.plot(range(len(time_df)), time_df['기초대비투찰률'].values,
                        'o-', color='#e74c3c', alpha=0.6)
                ax4.set_xlabel('시간 순서', fontsize=11, weight='bold')
                ax4.set_ylabel('기초대비투찰률 (%)', fontsize=11, weight='bold')
                ax4.set_title('시간에 따른 투찰률 변화 (학습 패턴)', fontsize=12, weight='bold')
                ax4.grid(True, alpha=0.3)

        plt.tight_layout()

        output_file = f'/mnt/a/25/data분석/{self.company_name}_{int(rate*1000)}_분석.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"  ✅ {rate}% 그래프: {output_file}")

    def save_report(self):
        """분석 결과 저장"""
        print(f"\n[결과 저장]")

        # JSON 저장
        output = {
            '분석시각': datetime.now().isoformat(),
            '업체명': self.company_name,
            '발주처투찰률별_분석': self.results.get('발주처투찰률별_분석', {}),
            'AI_사용_판단': self.ai_analysis
        }

        json_file = f'/mnt/a/25/data분석/{self.company_name}_발주처별_분석.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"  ✅ JSON: {json_file}")

        # 마크다운 보고서
        report = self.generate_markdown_report()
        md_file = f'/mnt/a/25/data분석/{self.company_name}_발주처별_분석_보고서.md'
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"  ✅ 보고서: {md_file}")

    def generate_markdown_report(self):
        """마크다운 보고서 생성"""
        report = []

        report.append(f"# {self.company_name} 입찰 패턴 분석 (발주처투찰률별)")
        report.append("")
        report.append(f"**분석 시각:** {datetime.now().isoformat()}")
        report.append("")
        report.append("---")
        report.append("")

        # AI 사용 판단
        if self.ai_analysis:
            report.append("## 🤖 AI 분석 사용 여부 판단")
            report.append("")
            report.append(f"### 종합 판단: **{self.ai_analysis['판단']}**")
            report.append("")
            report.append(f"- **종합 점수:** {self.ai_analysis['종합_점수']} ({self.ai_analysis['백분율']}%)")
            report.append("")
            report.append("### 세부 지표")
            report.append("")

            for item in self.ai_analysis['세부_지표']:
                report.append(f"#### {item['항목']}: {item['점수']}")
                report.append(f"{item['설명']}")
                report.append("")

            report.append("---")
            report.append("")

        # 발주처투찰률별 분석
        report.append("## 📊 발주처투찰률별 상세 분석")
        report.append("")

        if '발주처투찰률별_분석' in self.results:
            for rate, data in sorted(self.results['발주처투찰률별_분석'].items(),
                                    key=lambda x: float(x[0])):
                report.append(f"### 발주처투찰률 {rate}%")
                report.append("")

                report.append(f"#### 참여 요약")
                report.append("")
                report.append(f"- **참여:** {data['참여']}건")
                report.append(f"- **1위:** {data['1위']}건 (**{data['1위확률']}%**)")
                report.append(f"- **미달:** {data['미달']}건 ({data['미달확률']}%)")
                report.append("")

                if '투찰률_통계' in data:
                    stats = data['투찰률_통계']
                    report.append(f"#### 투찰률 패턴")
                    report.append("")
                    report.append(f"- **평균:** {stats['평균']}%")
                    report.append(f"- **중앙값:** {stats['중앙값']}%")
                    report.append(f"- **표준편차:** {stats['표준편차']}%")
                    report.append(f"- **범위:** {stats['최소']}% ~ {stats['최대']}%")
                    report.append("")
                    report.append("**백분위수:**")
                    for pct, val in stats['백분위수'].items():
                        report.append(f"- {pct}: {val}%")
                    report.append("")

                if '1위_패턴' in data:
                    win = data['1위_패턴']
                    report.append(f"#### 1위 패턴")
                    report.append("")
                    report.append(f"- **평균:** {win['평균']}%")
                    report.append(f"- **중앙값:** {win['중앙값']}%")
                    report.append(f"- **표준편차:** {win['표준편차']}%")
                    report.append("")

                if '소수점_3자리_분포' in data:
                    report.append(f"#### 소수점 패턴")
                    report.append(f"분포: {data['소수점_3자리_분포']}")
                    report.append("")

                report.append("---")
                report.append("")

        # 경쟁 전략
        report.append("## 🎯 경쟁 전략")
        report.append("")
        report.append("### 발주처투찰률별 회피 전략")
        report.append("")

        if '발주처투찰률별_분석' in self.results:
            for rate, data in sorted(self.results['발주처투찰률별_분석'].items(),
                                    key=lambda x: float(x[0])):
                if '투찰률_통계' in data:
                    stats = data['투찰률_통계']
                    median = stats['중앙값']

                    report.append(f"**{rate}% 그룹:**")
                    report.append(f"- 중앙값: {median}%")
                    report.append(f"- 회피 전략 1: {median - 0.1:.3f}% (더 낮게)")
                    report.append(f"- 회피 전략 2: {median + 0.1:.3f}% (더 높게)")
                    report.append("")

        report.append("---")
        report.append("")
        report.append("**⚠️ 이 보고서는 과거 데이터 기반 분석이며, 최종 입찰 결정은 사용자의 판단과 책임입니다.**")

        return "\n".join(report)

    def run(self):
        """전체 분석 실행"""
        print("="*80)
        print(f"{self.company_name} 입찰 패턴 분석 V2")
        print("발주처투찰률별 분리 + AI 사용 판단")
        print("="*80)

        if not self.load_data():
            return

        self.analyze_by_agency_rate()
        self.detect_ai_usage()
        self.visualize()
        self.save_report()

        print("\n" + "="*80)
        print("분석 완료!")
        print("="*80)

def main():
    """메인 실행"""
    import sys

    # 커맨드라인 인자로 업체명 받기
    if len(sys.argv) < 2:
        print("사용법: python analyze.py [업체명]")
        print("예시: python analyze.py 해동문화재연구원")
        sys.exit(1)

    company_name = sys.argv[1]

    analyzer = CompetitorAnalyzerV2(
        data_file='/mnt/a/25/data전처리완료/전체_통합_데이터.xlsx',
        company_name=company_name
    )
    analyzer.run()

if __name__ == '__main__':
    main()
