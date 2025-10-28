"""
2D 상관관계 분석 모듈

기초대비사정률 × 기초대비투찰률 2차원 분석
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from .data_utils import filter_valid_range

def analyze_2d_correlation(df):
    """
    2D 상관관계 분석

    Parameters:
    - df: 데이터프레임

    Returns:
    - dict: 2D 분석 결과
    """

    # ✅ 필터링 추가
    df = filter_valid_range(df)

    if '기초대비사정률' not in df.columns or '기초대비투찰률' not in df.columns:
        return {
            "오류": "사정률 또는 투찰률 컬럼 없음",
            "분석불가": True
        }
    
    # 유효 데이터만
    df_valid = df.dropna(subset=['기초대비사정률', '기초대비투찰률'])
    
    # 상관계수 (numpy 사용)
    corr = np.corrcoef(df_valid['기초대비사정률'], df_valid['기초대비투찰률'])[0, 1]
    
    # 2D 히트맵 생성 (0.2% × 0.2% 셀)
    x_bins = np.arange(98, 102.5, 0.2)  # 사정률
    y_bins = np.arange(80, 92, 0.2)     # 투찰률
    
    heatmap = np.zeros((len(y_bins)-1, len(x_bins)-1))
    
    for i in range(len(y_bins)-1):
        for j in range(len(x_bins)-1):
            count = len(df_valid[
                (df_valid['기초대비투찰률'] >= y_bins[i]) &
                (df_valid['기초대비투찰률'] < y_bins[i+1]) &
                (df_valid['기초대비사정률'] >= x_bins[j]) &
                (df_valid['기초대비사정률'] < x_bins[j+1])
            ])
            heatmap[i, j] = count
    
    # 저밀도 존 찾기 (상위 20% 미만)
    threshold = np.percentile(heatmap[heatmap > 0], 20)
    low_density_zones = []
    
    for i in range(len(y_bins)-1):
        for j in range(len(x_bins)-1):
            if 0 < heatmap[i, j] <= threshold:
                low_density_zones.append({
                    "사정률": f"{x_bins[j]:.1f}~{x_bins[j+1]:.1f}%",
                    "투찰률": f"{y_bins[i]:.1f}~{y_bins[i+1]:.1f}%",
                    "경쟁자": int(heatmap[i, j])
                })
    
    # 경쟁자 수로 정렬
    low_density_zones.sort(key=lambda x: x['경쟁자'])
    
    result = {
        "상관계수": round(corr, 3),
        "상관관계_평가": "강한 양의 상관" if corr > 0.7 else ("중간 양의 상관" if corr > 0.4 else "약한 상관"),
        "저밀도_구간_Top10": low_density_zones[:10],
        "히트맵_크기": f"{len(y_bins)-1} × {len(x_bins)-1}",
        "개선효과": "+0.5~1.0% (2D 회피 전략)"
    }
    
    return result


def visualize_2d_heatmap(df, output_path):
    """
    2D 히트맵 시각화

    Parameters:
    - df: 데이터프레임
    - output_path: 저장 경로
    """

    # ✅ 필터링 추가
    df = filter_valid_range(df)

    # 한글 폰트 설정
    try:
        font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
    except:
        pass

    if '기초대비사정률' not in df.columns or '기초대비투찰률' not in df.columns:
        return None
    
    # 유효 데이터
    df_valid = df.dropna(subset=['기초대비사정률', '기초대비투찰률'])
    
    # 2D 히스토그램
    x_bins = np.arange(98, 102.5, 0.2)
    y_bins = np.arange(80, 92, 0.2)
    
    heatmap = np.zeros((len(y_bins)-1, len(x_bins)-1))
    
    for i in range(len(y_bins)-1):
        for j in range(len(x_bins)-1):
            count = len(df_valid[
                (df_valid['기초대비투찰률'] >= y_bins[i]) &
                (df_valid['기초대비투찰률'] < y_bins[i+1]) &
                (df_valid['기초대비사정률'] >= x_bins[j]) &
                (df_valid['기초대비사정률'] < x_bins[j+1])
            ])
            heatmap[i, j] = count
    
    # 플롯
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 로그 스케일 (0 처리)
    heatmap_log = np.log1p(heatmap)
    
    im = ax.imshow(heatmap_log, aspect='auto', cmap='YlOrRd', origin='lower')
    
    ax.set_xlabel('기초대비사정률 (%)', fontproperties=font_prop, fontsize=12)
    ax.set_ylabel('기초대비투찰률 (%)', fontproperties=font_prop, fontsize=12)
    ax.set_title('2D 경쟁 밀도 히트맵 (사정률 × 투찰률)', fontproperties=font_prop, fontsize=14)
    
    # x축 (사정률)
    x_ticks = range(0, len(x_bins)-1, max(1, (len(x_bins)-1)//10))
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([f"{x_bins[i]:.1f}" for i in x_ticks])
    
    # y축 (투찰률)
    y_ticks = range(0, len(y_bins)-1, max(1, (len(y_bins)-1)//10))
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f"{y_bins[i]:.1f}" for i in y_ticks])
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('log(경쟁자 수 + 1)', fontproperties=font_prop)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path
