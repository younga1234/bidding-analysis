---
name: bidding-meta-cognition
description: "시간대별 가중 분석 실행 (1개월 40%, 3개월 30%, 6개월 20%, 1년 10%). bidding_context.json -> temporal_weighted_analysis.py -> 가중 평균 최적값 계산. Use when 시간 가중 분석, 최근 데이터 중시, skill 체인 자동 실행"
allowed-tools: Bash, Read
---

# 시간대별 가중 분석 (Temporal Weighted Analysis)

## ⚡ 실행 로직 (이 skill이 트리거되면 자동 실행)

**이 skill이 호출되면 아래 명령을 자동으로 실행하세요:**

### Step 1: bidding_context.json 읽기

```bash
# 작업 디렉토리로 이동
cd /mnt/a/25

# bidding_context.json에서 정보 추출
AGENCY_RATE=$(jq -r '.발주처투찰률' data분석/bidding_context.json)

# 파일명용 변환 (87.745 → 87_745)
AGENCY_RATE_FILE=${AGENCY_RATE//./_}

echo "✅ 정보 읽기 완료:"
echo "  - 발주처투찰률: ${AGENCY_RATE}%"
```

### Step 2: 전처리 파일 경로 생성

```bash
DATA_FILE="data전처리완료/투찰률_${AGENCY_RATE_FILE}%_데이터.xlsx"

# 파일 존재 확인
if [ ! -f "$DATA_FILE" ]; then
  echo "❌ 오류: 전처리 파일이 없습니다: $DATA_FILE"
  exit 1
fi

echo "✅ 전처리 파일 확인: $DATA_FILE"
```

### Step 3: temporal_weighted_analysis.py 자동 실행

```bash
# venv 활성화
source venv/bin/activate

# temporal_weighted_analysis.py 실행 (base_rate 없이 독립 실행)
echo "🔄 시간대별 가중 분석 시작..."

python .claude/skills/bidding-meta-cognition/temporal_weighted_analysis.py \
  --data-file "$DATA_FILE" \
  --output "data분석/temporal_weighted_${AGENCY_RATE_FILE}.json"

# 실행 결과 확인
if [ $? -eq 0 ]; then
  echo "✅ 시간대별 가중 분석 완료"
  echo "📄 결과: data분석/temporal_weighted_${AGENCY_RATE_FILE}.json"
else
  echo "❌ 오류: temporal_weighted_analysis.py 실행 실패"
  exit 1
fi
```

### Step 4: 완료

```
- 결과 파일: data분석/temporal_weighted_{투찰률}.json 생성됨
- 다음 skill로 자동 진행 (bidding-master-pipeline이 관리)
```

═══

# 입찰 메타 인지 분석 스킬

## 개요

기본 분석(logic)과 고급 분석(advanced)의 결과를 받아서:
1. **의심하기**: 이 결과가 현재 상황에 맞나?
2. **검증하기**: 실제 데이터로 통계 검정
3. **발견하기**: 놓친 패턴 찾기
4. **제안하기**: 여러 전략 제시

## 사용법

### 자동 실행 (파이프라인)
```bash
# 낙찰가분석 실행 시 자동으로 Stage 4-4에서 실행됨
낙찰가분석
```

### 수동 실행
```bash
python meta_analyze.py \
  --data-file /mnt/a/25/data전처리완료/투찰률_{공고의_투찰률}%_데이터.xlsx \
  --basic-result /mnt/a/25/data분석/bidding_analysis_{투찰률}.json \
  --advanced-result /mnt/a/25/data분석/bidding_analysis_advanced_{투찰률}.json \
  --context '{"기초금액": {공고값}, "발주처": "{공고값}", "월": {공고값}}'
```

## 분석 프로세스

### 1단계: 요인 검증 (Factor Validation)
```python
# 실제 데이터로 통계 검증
발주처별 차이: ANOVA (p-value)
월별 차이: Kruskal-Wallis (p-value)
금액별 상관: Pearson Correlation (r, p-value)
지역별 차이: Chi-square (p-value)

→ p < 0.05이면 "유의미"
→ 효과 크기(effect size) 계산
```

### 2단계: 전략 생성 (Strategy Generation)
```python
# 여러 전략 생성
전략 A (보수): 경쟁 밀도 최소화
전략 B (공격): 1위 확률 최대화
전략 C (균형): 기대값 최적화
전략 D (맞춤): 검증된 요인 반영

→ 각 전략마다 입찰률, 근거, 리스크 제시
```

### 3단계: 패턴 발견 (Insight Discovery)
```python
# 능동적으로 탐색
이상 패턴: 최근 3개월 추세 변화
숨은 상관: 예상 못한 변수 간 관계
위험 구간: 갑자기 경쟁 밀도 증가한 구간
기회 영역: 비어있는 저경쟁 구간

→ 사용자가 요청 안 해도 발견 제시
```

### 4단계: 신뢰도 평가 (Confidence Assessment)
```python
# 현재 상황 vs 과거 데이터
데이터 충분성: 샘플 수 > 30?
컨텍스트 매칭: 금액/발주처/월 유사도
시간적 유효성: 최근 데이터 비중
이상치 탐지: 현재 상황이 극단값?

→ 신뢰도 점수 (0~1)
→ 0.5 미만이면 "불확실" 경고
```

## 출력 형식 (실제 값은 분석 후 계산됨)

```json
{
  "메타분석_결과": {
    "검증된_영향요인": [
      {
        "요인": "{분석_요인}",
        "통계_검정": "{검정_방법}",
        "p_value": {계산값},
        "유의미": {true/false},
        "효과크기": "{계산값}",
        "인사이트": "{데이터_기반_발견}"
      }
    ],
    "생성된_전략": [
      {
        "전략명": "{전략_유형}",
        "입찰률": {계산값},
        "입찰금액": {계산값},
        "예상_경쟁자": {데이터_기반},
        "예상_1위확률": "{계산값}",
        "리스크": "{평가_결과}",
        "근거": "{데이터_기반_근거}"
      }
    ],
    "능동적_발견": [
      {
        "카테고리": "{패턴_유형}",
        "내용": "{실제_발견_내용}",
        "중요도": "{평가_결과}"
      }
    ],
    "신뢰도_평가": {
      "전체_신뢰도": {계산값},
      "평가": "{평가_결과}",
      "근거": {
        "데이터_충분성": {계산값},
        "컨텍스트_매칭": {계산값},
        "시간적_유효성": {계산값},
        "이상치_여부": {true/false}
      },
      "권장사항": "{상황별_권장사항}"
    },
    "최종_추천": {
      "전략": "{선택된_전략}",
      "입찰률": {계산값},
      "신뢰도": {계산값},
      "이유": "{선택_근거}"
    }
  }
}
```

## 기본 분석과의 차이

| 항목 | 기본 분석 (logic) | 메타 분석 (meta-cognition) |
|------|-------------------|----------------------------|
| 목적 | 최적 입찰률 계산 | 결과 검증 및 대안 제시 |
| 출력 | 1개 답 | 여러 전략 + 신뢰도 |
| 접근 | 데이터 → 공식 | 데이터 → 검증 → 의심 → 대안 |
| 상황 고려 | 없음 (항상 같은 답) | 있음 (상황에 따라 다른 답) |
| 불확실성 | 표시 안 함 | 명시적으로 표시 |

## 설계 원칙

1. **실제 데이터만 사용**: 가정이나 임의값 금지, 모든 수치는 통계 검정 결과
2. **여러 관점 제시**: 하나의 정답이 아닌 여러 전략 제시
3. **능동적 탐색**: 사용자가 묻기 전에 패턴 발견
4. **솔직한 평가**: 데이터 부족/맞지 않으면 "불확실" 명시

## 참고

- 기본 분석: `.claude/skills/logic/`
- 고급 분석: `.claude/skills/bidding-advanced-analyzer/`
- 파이프라인: `.claude/skills/bidding-master-pipeline/`
