# 고급 입찰 분석 스킬 (Bidding Advanced Analyzer)

> 기존 분석을 넘어 **1위 확률 +1~2% 개선**을 목표로 하는 10가지 심층 분석

---

## 📊 개요

복수예가입찰 분석의 고급 기능을 제공하는 스킬입니다.

**기존 `logic` 스킬의 한계**:
- 전체 데이터의 평균적 패턴만 분석
- 시간 변화 무시 (2023년 = 2025년)
- 발주처별 차이 무시
- 단일 차원 분석 (투찰률만)

**고급 분석의 돌파구**:
- 시간 차원: 최근 트렌드 가중
- 발주처 차원: 발주처별 최적 전략
- 2D 공간: 사정률 × 투찰률 조합 분석
- 다차원 통합: 숨겨진 기회 발견

---

## 🚀 Quick Start

### 기본 실행

```bash
# 가상환경 활성화
source /mnt/a/25/venv/bin/activate

# 전체 고급 분석 실행
python3 /mnt/a/25/.claude/skills/bidding-advanced-analyzer/advanced_analyze.py \
  --data-file "/mnt/a/25/data전처리완료/투찰률_82_995%_데이터.xlsx" \
  --agency-rate 82.995
```

### 특정 모듈만 실행

```bash
# 시간대별 + 발주처별만
python3 advanced_analyze.py \
  --data-file "..." \
  --agency-rate 82.995 \
  --modules temporal,agency
```

---

## 📦 구조

```
bidding-advanced-analyzer/
├── SKILL.md                    # 스킬 정의
├── advanced_analyze.py         # 메인 실행 스크립트
├── modules/                    # 분석 모듈
│   ├── __init__.py
│   ├── temporal_analysis.py   # Phase 1 ✅
│   ├── agency_analysis.py     # Phase 1 ✅
│   ├── correlation_2d.py      # Phase 1 ✅
│   ├── company_patterns.py    # Phase 2 (추후)
│   ├── psychological.py       # Phase 2 (추후)
│   ├── seasonality.py         # Phase 2 (추후)
│   ├── rank_gap.py           # Phase 3 (추후)
│   ├── cluster_detect.py     # Phase 3 (추후)
│   ├── amount_range.py       # Phase 3 (추후)
│   └── monte_carlo_plus.py   # Phase 3 (추후)
└── README.md                   # 이 파일
```

---

## 🎯 Phase 1: 핵심 분석 (완료 ✅)

### 1. 시간대별 패턴 (`temporal_analysis.py`)

**문제**: 2023년과 2025년 데이터가 같은 가중치?

**해결**:
- 최근 3개월 데이터 70% 가중
- 과거 데이터 30% 가중
- 트렌드 변화 감지

**출력 예시**:
```json
{
  "트렌드_요약": "87.8-88.0% 구간 경쟁 증가 (+15% in 3개월)",
  "가중_조정_최적률": 99.156
}
```

**기대 효과**: +0.3~0.5%

---

### 2. 발주처별 특성 (`agency_analysis.py`)

**문제**: 국가유산진흥원 vs 문화재청 = 다른 경쟁 환경

**해결**:
- 발주처 자동 식별
- 발주처별 경쟁 밀도
- 발주처별 최적 전략

**출력 예시**:
```json
{
  "발주처별_통계": {
    "R 계열": {
      "평균_경쟁밀도": 18.5,
      "경쟁_강도": "낮음",
      "최적_입찰률": 99.123
    }
  }
}
```

**기대 효과**: +0.2~0.4%

---

### 3. 2D 상관관계 (`correlation_2d.py`)

**문제**: 사정률과 투찰률을 따로 보면 패턴을 놓침

**해결**:
- 2D 히트맵 생성
- 상관계수 계산
- 저밀도 2D 셀 추출

**출력 예시**:
```json
{
  "상관계수": {
    "Pearson": 0.67,
    "해석": "중간 상관관계"
  },
  "저밀도_셀": [
    {"사정률": 99.5, "투찰률": 87.3, "경쟁자수": 12}
  ]
}
```

**기대 효과**: +0.5~1.0%

---

## 📈 출력 파일

### JSON 결과
```
/mnt/a/25/data분석/bidding_analysis_advanced_82995.json
```

구조:
```json
{
  "메타정보": {...},
  "시간대별_패턴": {...},
  "발주처별_특성": {...},
  "2D_상관관계": {...}
}
```

### 시각화 파일
```
/mnt/a/25/data분석/2d_correlation_82995.png
```

---

## 🔧 개발 로드맵

### ✅ Phase 1: 핵심 분석 (완료)
- [x] temporal_analysis.py
- [x] agency_analysis.py
- [x] correlation_2d.py

### ⏳ Phase 2: 전략 고도화 (예정)
- [ ] company_patterns.py - 업체별 반복 패턴
- [ ] psychological.py - 심리적 앵커 회피
- [ ] seasonality.py - 계절성/월별 패턴

### 🔮 Phase 3: 고급 분석 (장기)
- [ ] rank_gap.py - 순위 간격 분석
- [ ] cluster_detect.py - 담합/클러스터 탐지
- [ ] amount_range.py - 기초금액 구간별
- [ ] monte_carlo_plus.py - 고급 몬테카를로

---

## 🧪 테스트

### 모듈별 테스트

```bash
# 시간대별 패턴
python3 modules/temporal_analysis.py

# 발주처별 특성
python3 modules/agency_analysis.py

# 2D 상관관계
python3 modules/correlation_2d.py
```

### 전체 통합 테스트

```bash
# 82.995% 그룹 테스트
python3 advanced_analyze.py \
  --data-file "/mnt/a/25/data전처리완료/투찰률_82_995%_데이터.xlsx" \
  --agency-rate 82.995

# 결과 확인
cat /mnt/a/25/data분석/bidding_analysis_advanced_82995.json
```

---

## ⚠️ 현실적 한계

**솔직한 평가**:
```
기본 분석: 2.04% (82.995% 그룹)
고급 분석 적용: 3~4%
실제 현실: 50명이 1.65%포인트에 몰림

→ 여전히 25번 입찰해야 1번 낙찰
→ 복수예가 = 50% 전략 + 50% 운
```

**고급 분석의 진짜 가치**:
- "최악의 선택" 회피
- "상대적으로 나은 선택" 제시
- 메타 게임 대응
- 발주처별 특화 전략

---

## 🔗 관련 스킬

- `logic`: 기본 분석 (경쟁 밀도, 몬테카를로)
- `data-preprocessing`: 데이터 전처리
- `report`: 보고서 생성

---

## 📝 변경 이력

- **2025-10-27**: 스킬 생성, Phase 1 완료
  - temporal_analysis.py ✅
  - agency_analysis.py ✅
  - correlation_2d.py ✅

---

## 👨‍💻 기여

Phase 2, Phase 3 모듈 구현 환영합니다!

각 모듈은 독립적으로 작동하므로 단계적 구현 가능합니다.

---

**Made with Claude Code**
