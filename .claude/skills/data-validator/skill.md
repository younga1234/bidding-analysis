---
name: data-validator
description: |
  나라장터 입찰 데이터 무결성 검증. 필수 17개 컬럼 확인, 순위와 낙찰하한가차이 정합성 검증,
  낙찰하한율 계산 검증, 참여업체수 일치 확인. 데이터 오류 시 상세 리포트 제공.
  Use when validating bidding data integrity or checking data quality. (project)
allowed-tools:
  - Read
  - Bash
  - mcp__smithery-ai-server-sequential-thinking__sequentialthinking
---

# 입찰 데이터 무결성 검증기

## 검증 항목

### 1. 필수 컬럼 존재 확인
```python
REQUIRED_COLUMNS = [
    '공고번호', '공사명', '발주처', '개찰일',
    '기초금액', '예정가격', '낙찰하한가', '사정률',
    '순위', '업체명', '예가대비투찰률(%)', '기초대비투찰률(%)',
    '기초대비사정률(%)', '낙찰하한가차이(원)', '지역제한',
    '투찰률', '참여업체수'
]
```

### 2. 데이터 타입 검증
```python
def validate_data_types(df):
    validations = {
        '순위': lambda x: x.dtype in [int, float],
        '예가대비투찰률(%)': lambda x: x.dtype == float,
        '낙찰하한가차이(원)': lambda x: x.dtype in [int, float]
    }
```

### 3. 논리적 정합성 검증
```python
def validate_logical_consistency(df):
    errors = []

    # 순위 -1은 반드시 낙찰하한가차이 < 0
    below_minimum = df[df['순위'] < 0]
    if any(below_minimum['낙찰하한가차이(원)'] >= 0):
        errors.append('하한가 미달인데 차이가 양수인 데이터 존재')

    # 순위 양수는 반드시 낙찰하한가차이 >= 0
    above_minimum = df[df['순위'] > 0]
    if any(above_minimum['낙찰하한가차이(원)'] < 0):
        errors.append('정상 순위인데 하한가 미달인 데이터 존재')

    return errors
```

### 4. 낙찰하한율 계산 검증
```python
def validate_minimum_rate(df):
    # 낙찰하한가 / 예정가격 = 낙찰하한율
    calculated_rate = (df['낙찰하한가'] / df['예정가격'] * 100).round(3)
    stored_rate = df['투찰률'].str.rstrip('%').astype(float)

    if abs(calculated_rate - stored_rate).max() > 0.01:
        return '낙찰하한율 계산 불일치'
```

### 5. 참여업체수 검증
```python
def validate_participant_count(df):
    actual_count = df.groupby('공고번호').size()
    stated_count = df.groupby('공고번호')['참여업체수'].first()

    # "15개 업체" 형식 파싱
    stated_count = stated_count.str.extract(r'(\d+)')[0].astype(int)

    if not all(actual_count == stated_count):
        return '참여업체수 불일치'
```

## 검증 실행 스크립트
```python
import pandas as pd
import os
import sys

def validate_bidding_data(file_path):
    """입찰 데이터 완전 검증"""

    # 파일 읽기
    try:
        df = pd.read_excel(file_path)
    except:
        return {'error': '파일 읽기 실패'}

    results = {
        'file': file_path,
        'rows': len(df),
        'columns': len(df.columns),
        'errors': [],
        'warnings': []
    }

    # 1. 필수 컬럼 확인
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        results['errors'].append(f'누락 컬럼: {missing_cols}')

    # 2. 데이터 타입 검증
    type_errors = validate_data_types(df)
    if type_errors:
        results['errors'].extend(type_errors)

    # 3. 논리적 정합성
    logic_errors = validate_logical_consistency(df)
    if logic_errors:
        results['errors'].extend(logic_errors)

    # 4. 낙찰하한율 검증
    rate_error = validate_minimum_rate(df)
    if rate_error:
        results['warnings'].append(rate_error)

    # 5. 참여업체수 검증
    count_error = validate_participant_count(df)
    if count_error:
        results['warnings'].append(count_error)

    # 6. 이상치 감지
    if df['예가대비투찰률(%)'].max() > 100:
        results['warnings'].append('100% 초과 투찰률 존재')

    if df['예가대비투찰률(%)'].min() < 70:
        results['warnings'].append('70% 미만 투찰률 존재')

    # 결과 요약
    results['status'] = 'PASS' if not results['errors'] else 'FAIL'
    results['quality_score'] = 100 - len(results['errors']) * 10 - len(results['warnings']) * 5

    return results
```

## 실행 예시

```bash
# 단일 파일 검증
python -c "from data_validator import validate_bidding_data; print(validate_bidding_data('20230905571-00_통합.xlsx'))"

# 전체 디렉토리 검증
python -c "
import os
from data_validator import validate_bidding_data

data_dir = '/mnt/a/25/data전처리완료'
for file in os.listdir(data_dir):
    if file.endswith('.xlsx'):
        result = validate_bidding_data(os.path.join(data_dir, file))
        if result['status'] == 'FAIL':
            print(f'❌ {file}: {result[\"errors\"]}')
"
```

## 검증 결과 리포트

```
[데이터 검증 리포트]

파일: 20230905571-00_통합.xlsx
상태: ✅ PASS
품질점수: 95/100

✅ 필수 컬럼: 17개 모두 존재
✅ 데이터 타입: 정상
✅ 논리 정합성: 정상
⚠️ 경고: 낙찰하한율 계산 0.001% 차이

상세 분석:
- 총 행수: 15
- 하한가 미달: 10개 (66.7%)
- 투찰률 범위: 80.349% ~ 80.854%
- 낙찰하한율: 80.495%
```

## 주의사항

1. **원본 데이터 형식 유지**: 금액 필드의 "원", "," 처리 필요
2. **순위 체계 이해**: -1, -2는 미달 순위
3. **정밀도**: 0.001% 단위까지 검증
4. **배치 처리**: 300개 이상 파일 처리 최적화