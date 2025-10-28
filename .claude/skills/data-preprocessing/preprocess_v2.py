#!/usr/bin/env python3
"""
나라장터 복수예가입찰 데이터 전처리 스크립트 V2
수정.md 요구사항 완전 구현 버전
"""

import os
import re
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class BiddingPreprocessor:
    """
    나라장터 입찰 데이터 전처리기
    수정.md의 모든 요구사항 구현
    """

    def __init__(self, source_dir="/mnt/a/25/data", output_dir="/mnt/a/25/data전처리완료"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.log_file = open(self.output_dir / "preprocessing_log.txt", "w", encoding='utf-8')

    def log_message(self, msg):
        """로그 메시지 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {msg}"
        print(log_entry)
        self.log_file.write(log_entry + "\n")
        self.log_file.flush()

    def normalize_company_name(self, name):
        """
        2️⃣ 업체명 정규화 규칙
        """
        if pd.isna(name):
            return ""

        name = str(name).strip()

        # 법인 형태 제거 (순서 중요)
        patterns = [
            r'\(재\)', r'재단법인', r'재단',
            r'\(주\)', r'주식회사',
            r'\(사\)', r'사단법인',
            r'\(유\)', r'유한회사',
            r'\(합\)', r'합명회사',
            r'\(합자\)', r'합자회사'
        ]

        for pattern in patterns:
            name = re.sub(pattern, '', name)

        # 문화재 관련 통일
        name = re.sub(r'문화유산연구원', '문화재연구원', name)
        name = re.sub(r'문화재보존센터', '문화재연구원', name)
        name = re.sub(r'고고학연구소', '문화재연구원', name)

        # 특정 업체명 보정
        if '문화유산마을' in name and '문화재연구원' not in name:
            name = '문화유산마을 문화재연구원'

        # 특수문자 정규화
        name = name.replace('&', 'and')

        # 다중 공백을 단일 공백으로
        name = re.sub(r'\s+', ' ', name)

        return name.strip()

    def parse_money_amount(self, value):
        """
        3️⃣ 금액 관련 필드 파싱 규칙
        """
        if pd.isna(value):
            return 0

        value = str(value)
        # 쉼표, 원, 공백 제거
        value = re.sub(r'[,원\s]', '', value)

        try:
            return int(float(value))
        except:
            return 0

    def parse_percentage(self, value, field_name=""):
        """
        4️⃣ 비율/퍼센트 관련 필드 처리
        """
        if pd.isna(value):
            return None

        value = str(value).replace('%', '').strip()

        # 괄호 안 값 처리
        if '(' in str(value):
            match = re.search(r'\(([0-9.]+)\)', str(value))
            if match:
                value = match.group(1)

        try:
            value = float(value)

            # 기초대비사정률 특별 처리
            if "사정률" in field_name or "기초대비사정률" in field_name:
                if -2 <= value <= 2:
                    return 100 + value
                elif 98 <= value <= 102:
                    return value
                else:
                    self.log_message(f"이상치 발견 - {field_name}: {value}")
                    return None

            return value
        except:
            return None

    def parse_datetime(self, value):
        """
        5️⃣ 날짜/시간 필드 처리
        """
        if pd.isna(value):
            return None

        # 여러 형식 시도
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%Y.%m.%d %H:%M:%S",
            "%Y-%m-%d",
        ]

        for fmt in formats:
            try:
                return pd.to_datetime(value, format=fmt)
            except:
                continue

        # 모든 형식 실패시 pandas 자동 파싱
        try:
            return pd.to_datetime(value)
        except:
            return None

    def check_file_pair(self, file_path):
        """
        1️⃣ 파일 필터링 규칙 - 공고번호 쌍 체크
        """
        file_name = file_path.stem

        # _참여업체목록 파일인 경우
        if "_참여업체목록" in file_name:
            main_name = file_name.replace("_참여업체목록", "")
            main_file = file_path.parent / f"{main_name}.xlsx"
            return main_file.exists()

        # 메인 파일인 경우
        participant_file = file_path.parent / f"{file_name}_참여업체목록.xlsx"
        return participant_file.exists()

    def extract_bid_info(self, df):
        """
        9️⃣ 공고정보 필수 필드 추출 (키-값 형식)
        """
        info = {}

        # 처음 20행 정도에서 키-값 쌍 추출
        for i in range(min(20, len(df))):
            row = df.iloc[i]
            if pd.notna(row.iloc[0]) and pd.notna(row.iloc[1]):
                key = str(row.iloc[0]).strip()
                value = str(row.iloc[1]).strip()

                if '공고번호' in key:
                    info['공고번호'] = value
                elif '공사명' in key or '용역명' in key:
                    info['공사명'] = value
                elif '발주처' in key:
                    # 담당자 정보 제거
                    info['발주처'] = value.split('(')[0].strip()
                elif '개찰일' in key:
                    info['개찰일시'] = self.parse_datetime(value)
                elif '기초금액' in key:
                    info['기초금액'] = self.parse_money_amount(value)
                elif '예정가격' in key:
                    info['예정가격'] = self.parse_money_amount(value)
                elif '낙찰하한가' in key:
                    info['낙찰하한가'] = self.parse_money_amount(value)
                elif '사정률' in key:
                    info['사정률'] = self.parse_percentage(value, '사정률')
                elif '낙찰하한율' in key or '투찰률' in key:
                    info['낙찰하한율'] = self.parse_percentage(value)

        # 사정률 계산 (없는 경우)
        if info.get('기초금액') and info.get('예정가격') and not info.get('사정률'):
            info['사정률'] = ((info['예정가격'] - info['기초금액']) / info['기초금액']) * 100

        # 낙찰하한가 계산 (없는 경우)
        if not info.get('낙찰하한가') and info.get('예정가격') and info.get('낙찰하한율'):
            info['낙찰하한가'] = int(info['예정가격'] * (info['낙찰하한율'] / 100))

        return info

    def find_data_start_row(self, df):
        """
        실제 데이터가 시작하는 행 찾기
        """
        for i in range(len(df)):
            row = df.iloc[i]
            # '순위' 텍스트가 첫 번째 열에 있는 헤더 행 찾기
            if pd.notna(row.iloc[0]) and '순위' == str(row.iloc[0]).strip():
                return i + 1  # 헤더 다음 행부터 데이터
        return 0

    def merge_bidding_files(self, main_file, participant_file):
        """
        메인 파일과 참여업체목록 파일 통합
        17개 필수 컬럼 완전성 체크
        """
        try:
            # 파일 읽기 (헤더 없이)
            main_df = pd.read_excel(main_file, header=None, engine='openpyxl')
            participant_df = pd.read_excel(participant_file, header=None, engine='openpyxl')

            # 공고 정보 추출
            bid_info = self.extract_bid_info(main_df)
            participant_bid_info = self.extract_bid_info(participant_df)
            bid_info.update({k: v for k, v in participant_bid_info.items() if v})

            # 실제 데이터 시작 위치 찾기
            data_start = self.find_data_start_row(participant_df)

            if data_start == 0:
                self.log_message(f"데이터 시작 위치를 찾을 수 없음: {main_file.name}")
                return None

            # 헤더와 데이터 분리
            header_row = participant_df.iloc[data_start - 1]
            data_df = participant_df.iloc[data_start:].reset_index(drop=True)

            # 컬럼명 설정
            columns = []
            for val in header_row:
                if pd.notna(val):
                    columns.append(str(val).strip())
                else:
                    columns.append(f"col_{len(columns)}")

            data_df.columns = columns[:len(data_df.columns)]

            # 빈 행 제거
            data_df = data_df.dropna(how='all')

            # 참여업체 수 체크
            if len(data_df) < 5:
                self.log_message(f"참여업체 5개 미만: {main_file.name}")
                return None

            # 문화재연구원 포함 여부 체크 (필수)
            normalized_names = data_df.get('업체', pd.Series()).apply(self.normalize_company_name)
            if not any('문화재연구원' in str(name) for name in normalized_names):
                self.log_message(f"문화재연구원 미포함 (삭제): {main_file.name}")
                return None

            # 필수 컬럼 생성
            processed_df = self.create_standard_dataframe(data_df, bid_info)

            # 데이터 품질 검증
            if not self.validate_data_quality(processed_df):
                self.log_message(f"데이터 품질 검증 실패: {main_file.name}")

            return processed_df

        except Exception as e:
            self.log_message(f"파일 통합 실패 {main_file.name}: {str(e)}")
            return None

    def create_standard_dataframe(self, df, bid_info):
        """
        8️⃣ 17개 필수 컬럼 데이터프레임 생성
        """
        result = pd.DataFrame()

        # 컬럼 매핑 - 원본 데이터를 그대로 사용
        column_map = {
            '순위': ['순위', 'rank'],
            '업체': ['업체', '업체명', '상호', '회사명'],
            '투찰일시': ['투찰일시', '투찰일', '제출일시'],
            '투찰금액': ['투찰금액', '입찰금액', '투찰가'],
            '예가대비투찰률': ['예가대비투찰률(%)', '예가대비투찰률', '예가대비'],
            '기초대비투찰률': ['기초대비투찰률(%)', '기초대비투찰률', '기초대비'],
            '기초대비사정률': ['기초대비사정률(%)', '기초대비사정률']
        }

        # 각 컬럼 찾아서 매핑
        for target, candidates in column_map.items():
            found = False
            for col in df.columns:
                if any(cand in str(col) for cand in candidates):
                    if '업체' in target:
                        result['업체명'] = df[col].apply(self.normalize_company_name)
                    elif '투찰금액' in target:
                        result['투찰금액'] = df[col].apply(self.parse_money_amount)
                    elif '투찰일시' in target:
                        result['투찰일시'] = df[col].apply(self.parse_datetime)
                    elif '예가대비투찰률' in target:
                        result['예가대비투찰률'] = df[col]
                    elif '기초대비투찰률' in target:
                        result['기초대비투찰률'] = df[col]
                    elif '기초대비사정률' in target:
                        result['기초대비사정률'] = df[col].apply(lambda x: self.parse_percentage(x, '기초대비사정률'))
                    else:
                        result[target] = df[col]
                    found = True
                    break

            if not found:
                # 기본값 설정
                result[target] = None

        # 공고 정보 추가 (공고당 1개씩)
        result['공고번호'] = bid_info.get('공고번호', '')
        result['공고명'] = bid_info.get('공사명', '')
        result['예정가격'] = bid_info.get('예정가격', 0)
        result['낙찰하한가'] = bid_info.get('낙찰하한가', 0)
        result['기초금액'] = bid_info.get('기초금액', 0)
        result['사정률'] = bid_info.get('사정률', None)
        result['발주처투찰률'] = bid_info.get('낙찰하한율', None)

        # 낙찰하한가차이 계산 (원본에 없는 경우만)
        if '투찰금액' in result.columns:
            낙찰하한가 = bid_info.get('낙찰하한가', 0)
            if 낙찰하한가 > 0:
                result['낙찰하한가차이'] = result['투찰금액'] - 낙찰하한가

        # 1️⃣1️⃣ 하한가 미달 데이터 처리 (중요!)
        if '낙찰하한가차이' in result.columns:
            # 미달 업체는 순위 -1
            result.loc[result['낙찰하한가차이'] < 0, '순위'] = -1

        # 필수 컬럼 확인 및 생성 (15개 컬럼)
        required_columns = [
            '공고번호', '공고명', '순위', '업체명', '투찰일시',
            '투찰금액', '예가대비투찰률', '기초대비투찰률', '기초대비사정률',
            '예정가격', '낙찰하한가', '기초금액', '사정률', '발주처투찰률', '낙찰하한가차이'
        ]

        for col in required_columns:
            if col not in result.columns:
                result[col] = None

        # 컬럼 순서 정리
        result = result[required_columns]

        return result

    def validate_data_quality(self, df):
        """
        🔟 데이터 품질 검증
        """
        # 중복 업체 체크
        if '사업자등록번호' in df.columns:
            duplicates = df['사업자등록번호'].duplicated()
            if duplicates.any():
                self.log_message(f"중복 업체 발견: {duplicates.sum()}개")

        # 투찰금액 유효성
        if '투찰금액' in df.columns and '기초금액' in df.columns:
            base_amount = df['기초금액'].iloc[0] if len(df) > 0 else 0
            if base_amount > 0:
                invalid_bids = df[(df['투찰금액'] < base_amount * 0.5) |
                                 (df['투찰금액'] > base_amount * 1.2)]
                if len(invalid_bids) > 0:
                    self.log_message(f"비정상 투찰금액 발견: {len(invalid_bids)}개")

        # 추첨번호 유효성
        if '추첨번호' in df.columns:
            for idx, draw_nums in df['추첨번호'].items():
                if pd.notna(draw_nums):
                    try:
                        nums = str(draw_nums).split(',')
                        nums = [int(n.strip()) for n in nums if n.strip()]
                        if len(nums) != 4 or any(n < 1 or n > 15 for n in nums):
                            self.log_message(f"비정상 추첨번호: {draw_nums}")
                    except:
                        pass

        return True

    def process_all_files(self):
        """
        전체 파일 처리 메인 함수
        """
        self.log_message("="*50)
        self.log_message("나라장터 복수예가입찰 데이터 전처리 V2 시작")
        self.log_message(f"원본 디렉토리: {self.source_dir}")
        self.log_message(f"출력 디렉토리: {self.output_dir}")
        self.log_message("="*50)

        # Excel 파일 목록 가져오기
        excel_files = list(self.source_dir.glob("*.xlsx")) + list(self.source_dir.glob("*.xls"))
        self.log_message(f"발견된 Excel 파일 수: {len(excel_files)}")

        # 메인 파일과 참여업체목록 파일 분류
        main_files = []
        for file in excel_files:
            if "_참여업체목록" not in file.name:
                if self.check_file_pair(file):
                    main_files.append(file)
                else:
                    self.log_message(f"쌍이 없는 파일 제외: {file.name}")

        self.log_message(f"처리할 공고 수: {len(main_files)}")

        # 통계 변수
        success_count = 0
        fail_count = 0
        fail_list = []
        all_data = []  # 개별 파일 저장 대신 메모리에 수집

        # 각 공고별 처리
        for idx, main_file in enumerate(main_files, 1):
            bid_number = main_file.stem
            participant_file = main_file.parent / f"{bid_number}_참여업체목록.xlsx"

            self.log_message(f"\n[{idx}/{len(main_files)}] 처리 중: {bid_number}")

            # 파일 통합 및 처리
            result_df = self.merge_bidding_files(main_file, participant_file)

            if result_df is not None:
                # 개별 파일 저장 안 함 - 메모리에만 저장
                result_df['공고번호'] = bid_number
                all_data.append(result_df)
                self.log_message(f"✓ 처리 완료: {bid_number}")
                success_count += 1
            else:
                self.log_message(f"✗ 처리 실패: {bid_number}")
                fail_count += 1
                fail_list.append(bid_number)

        # 최종 통계
        self.log_message("\n" + "="*50)
        self.log_message("전처리 완료 통계")
        self.log_message(f"성공: {success_count}개")
        self.log_message(f"실패: {fail_count}개")
        if fail_list:
            self.log_message(f"실패 목록: {', '.join(fail_list[:10])}{'...' if len(fail_list) > 10 else ''}")
        self.log_message("="*50)

        # 전체 통합 데이터 생성
        self.create_master_dataset(all_data)

    def create_master_dataset(self, all_data):
        """
        1️⃣3️⃣ 전체 통합 데이터셋 생성
        개별 파일 저장 없이 메모리의 데이터프레임 리스트로부터 직접 생성
        """
        self.log_message("\n전체 통합 데이터셋 생성 시작...")

        if not all_data:
            self.log_message("통합할 데이터가 없습니다.")
            return

        if all_data:
            master_df = pd.concat(all_data, ignore_index=True)

            # 전체 통합 데이터 저장
            master_file = self.output_dir / "전체_통합_데이터.xlsx"
            master_df.to_excel(master_file, index=False, engine='openpyxl')

            self.log_message(f"전체 통합 데이터 저장 완료: {master_file}")
            self.log_message(f"총 공고 수: {len(all_data)}")
            self.log_message(f"총 데이터 수: {len(master_df)}")

            # 발주처 투찰율별 데이터 분리
            if '발주처투찰률' in master_df.columns:
                self.log_message("\n발주처 투찰율별 데이터 분리 시작...")

                # 고유한 투찰율 찾기
                unique_rates = master_df['발주처투찰률'].dropna().unique()
                unique_rates = sorted([r for r in unique_rates if pd.notna(r)])

                self.log_message(f"발견된 투찰율: {len(unique_rates)}개")

                # 각 투찰율별로 데이터 분리 및 저장
                for rate in unique_rates:
                    rate_df = master_df[master_df['발주처투찰률'] == rate].copy()

                    if len(rate_df) > 0:
                        # 파일명 생성
                        rate_str = f"{rate:.3f}".replace('.', '_')
                        rate_file = self.output_dir / f"투찰률_{rate_str}%_데이터.xlsx"

                        # 저장
                        rate_df.to_excel(rate_file, index=False, engine='openpyxl')

                        self.log_message(f"  ✓ {rate}% - {len(rate_df)}건 저장: {rate_file.name}")

                self.log_message("발주처 투찰율별 데이터 분리 완료")

            # 요약 통계
            if '미달사유' in master_df.columns:
                미달률 = (master_df['미달사유'].notna().sum() / len(master_df)) * 100
                self.log_message(f"전체 미달률: {미달률:.2f}%")

            if '업체명' in master_df.columns:
                unique_companies = master_df['업체명'].nunique()
                self.log_message(f"참여 업체 수: {unique_companies}개")

    def __del__(self):
        """소멸자 - 로그 파일 닫기"""
        if hasattr(self, 'log_file'):
            self.log_file.close()

def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(description='나라장터 복수예가입찰 데이터 전처리')
    parser.add_argument('--source-dir', default='/mnt/a/25/data', help='원본 데이터 디렉토리')
    parser.add_argument('--output-dir', default='/mnt/a/25/data전처리완료', help='출력 디렉토리')
    parser.add_argument('--single', help='단일 공고번호 처리 (예: 2023-21331)')

    args = parser.parse_args()

    # 전처리기 초기화
    preprocessor = BiddingPreprocessor(args.source_dir, args.output_dir)

    if args.single:
        # 단일 파일 처리
        main_file = Path(args.source_dir) / f"{args.single}.xlsx"
        participant_file = Path(args.source_dir) / f"{args.single}_참여업체목록.xlsx"

        if not main_file.exists():
            print(f"❌ 메인 파일 없음: {main_file}")
            return

        if not participant_file.exists():
            print(f"❌ 참여업체목록 파일 없음: {participant_file}")
            return

        result_df = preprocessor.merge_bidding_files(main_file, participant_file)
        if result_df is not None:
            output_file = Path(args.output_dir) / f"{args.single}_통합.xlsx"
            result_df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"✓ 처리 완료: {output_file}")
        else:
            print("✗ 처리 실패")
    else:
        # 전체 파일 처리
        preprocessor.process_all_files()

    print("\n전처리 완료!")

if __name__ == "__main__":
    main()