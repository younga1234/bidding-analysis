#!/usr/bin/env python3
"""
이미지에서 추출한 입찰 데이터를 Excel 파일로 변환

사용법:
    python image_to_excel.py <공고번호> <기초금액> <투찰률> [기타정보...]
"""

import sys
import json
from pathlib import Path
import pandas as pd
from datetime import datetime

def create_bidding_excel(data_dict, output_dir="/mnt/a/25/data"):
    """
    추출된 입찰 데이터를 Excel 파일로 생성

    Args:
        data_dict (dict): 입찰 정보 딕셔너리
        output_dir (str): 출력 디렉토리

    Returns:
        str: 생성된 파일 경로
    """
    # 필수 필드 검증
    required_fields = ['공고번호', '기초금액', '투찰률']
    for field in required_fields:
        if field not in data_dict:
            raise ValueError(f"필수 필드 누락: {field}")

    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 공고번호로 파일명 생성
    announcement_no = data_dict['공고번호']
    filename = f"{announcement_no}.xlsx"
    filepath = output_path / filename

    # 기초금액 파싱 (숫자만 추출)
    base_amount_str = str(data_dict['기초금액']).replace(',', '').replace('원', '').replace('원', '').strip()
    base_amount = int(base_amount_str) if base_amount_str.isdigit() else 0

    # 투찰률 파싱 (% 제거)
    bid_rate_str = str(data_dict['투찰률']).replace('%', '').strip()
    bid_rate = float(bid_rate_str) if bid_rate_str.replace('.', '').isdigit() else 0.0

    # 예가범위 파싱
    price_range = data_dict.get('예가범위', '+2% ~ -2%')

    # DataFrame 생성 (나라장터 형식)
    df = pd.DataFrame([{
        '공고번호': announcement_no,
        '종목': data_dict.get('종목', '국가유산역'),
        '지역제한': data_dict.get('지역제한', '전국'),
        '기초금액': base_amount,
        '추정가격': base_amount,  # 일반적으로 기초금액과 동일
        '투찰률': bid_rate,
        '낙찰방법': data_dict.get('낙찰방법', ''),
        '예가범위': price_range,
        '도급자한금액': data_dict.get('도급자한금액', ''),
        '관급자재금액': data_dict.get('관급자재금액', ''),
        '예정(추정)금액': data_dict.get('예정금액', base_amount),
        '담당자': data_dict.get('담당자', ''),
        '연락처': data_dict.get('연락처', ''),
        '발주기관': data_dict.get('발주기관', data_dict.get('종목', '')),
        '추출일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }])

    # Excel 저장
    df.to_excel(filepath, index=False, engine='openpyxl')

    return str(filepath)

def main():
    """CLI 인터페이스"""
    if len(sys.argv) < 2:
        print("사용법: python image_to_excel.py <JSON_DATA>")
        print("또는: python image_to_excel.py --공고번호 <번호> --기초금액 <금액> --투찰률 <률>")
        sys.exit(1)

    # JSON 문자열로 데이터 받기
    if sys.argv[1].startswith('{'):
        data_dict = json.loads(sys.argv[1])
    else:
        # 키-값 쌍으로 데이터 받기
        data_dict = {}
        i = 1
        while i < len(sys.argv):
            if sys.argv[i].startswith('--'):
                key = sys.argv[i][2:]
                value = sys.argv[i+1] if i+1 < len(sys.argv) else ''
                data_dict[key] = value
                i += 2
            else:
                i += 1

    try:
        filepath = create_bidding_excel(data_dict)
        print(f"SUCCESS: {filepath}")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
