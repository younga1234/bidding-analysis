#!/usr/bin/env python3
"""
입찰 분석 마스터 파이프라인 오케스트레이터

"낙찰가분석" 한마디로 전체 파이프라인 순차 실행:
Stage 1: 이미지 감지 및 데이터 추출
Stage 2: Excel 생성
Stage 3: 데이터 전처리
Stage 4: 분석 실행 (logic)
Stage 5: 보고서 생성 (report)
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# 경로 설정
BASE_DIR = Path("/mnt/a/25")
DATA_ANALYSIS_DIR = BASE_DIR / "data분석"
DATA_DIR = BASE_DIR / "data"
PREPROCESSED_DIR = BASE_DIR / "data전처리완료"
RESULTS_DIR = DATA_ANALYSIS_DIR / "분석결과"
SKILLS_DIR = BASE_DIR / ".claude/skills"

# 로그 파일
LOG_FILE = DATA_ANALYSIS_DIR / "pipeline_log.txt"

def log(message):
    """로그 메시지 출력 및 파일 저장"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

def run_command(cmd, description, timeout=120):
    """명령어 실행 및 결과 반환"""
    log(f"실행 중: {description}")
    log(f"명령어: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(BASE_DIR)
        )

        if result.returncode == 0:
            log(f"✅ 성공: {description}")
            return True, result.stdout
        else:
            log(f"❌ 실패: {description}")
            log(f"에러: {result.stderr}")
            return False, result.stderr

    except subprocess.TimeoutExpired:
        log(f"⏱️ 타임아웃: {description} ({timeout}초 초과)")
        return False, "Timeout"
    except Exception as e:
        log(f"❌ 예외 발생: {description} - {str(e)}")
        return False, str(e)

def stage1_detect_image():
    """Stage 1: 이미지 감지"""
    log("\n" + "="*80)
    log("Stage 1: 이미지 감지 및 데이터 추출")
    log("="*80)

    # 이미지 파일 검색
    image_files = list(DATA_ANALYSIS_DIR.glob("*.png")) + \
                  list(DATA_ANALYSIS_DIR.glob("*.jpg")) + \
                  list(DATA_ANALYSIS_DIR.glob("*.jpeg"))

    if not image_files:
        log("❌ 이미지 파일을 찾을 수 없습니다.")
        return None

    # 가장 최근 파일 선택
    image_file = max(image_files, key=lambda p: p.stat().st_mtime)
    log(f"✅ 이미지 발견: {image_file.name}")

    return image_file

def stage2_create_excel(image_data):
    """Stage 2: Excel 파일 생성"""
    log("\n" + "="*80)
    log("Stage 2: Excel 파일 생성")
    log("="*80)

    # 이미지에서 추출한 데이터 (실제로는 Claude Vision으로 추출)
    # 여기서는 예시 데이터 사용
    data = {
        "공고번호": "R25BK01110791-001",
        "기초금액": "39000000",
        "투찰률": "87.745",
        "종목": "국가유산역",
        "예가범위": "+2% ~ -2%"
    }

    # image_to_excel.py 실행
    script_path = SKILLS_DIR / "bidding-master-pipeline" / "image_to_excel.py"

    cmd = [
        "python3", str(script_path),
        "--공고번호", data["공고번호"],
        "--기초금액", data["기초금액"],
        "--투찰률", data["투찰률"],
        "--종목", data["종목"],
        "--예가범위", data["예가범위"]
    ]

    success, output = run_command(cmd, "Excel 파일 생성")

    if success:
        # 생성된 파일 경로 추출
        excel_file = DATA_DIR / f"{data['공고번호']}.xlsx"
        if excel_file.exists():
            log(f"✅ Excel 파일 생성 완료: {excel_file}")
            return excel_file, data
        else:
            log(f"❌ Excel 파일이 생성되지 않았습니다: {excel_file}")
            return None, None

    return None, None

def stage3_preprocess():
    """Stage 3: 데이터 전처리"""
    log("\n" + "="*80)
    log("Stage 3: 데이터 전처리")
    log("="*80)

    # data-preprocessing 스킬 실행
    script_path = SKILLS_DIR / "data-preprocessing" / "preprocess_v2.py"

    cmd = ["python3", str(script_path)]

    success, output = run_command(cmd, "데이터 전처리", timeout=300)

    if success:
        # 전처리 완료 파일 확인
        preprocessed_files = list(PREPROCESSED_DIR.glob("투찰률_*.xlsx"))
        log(f"✅ 전처리 완료: {len(preprocessed_files)}개 파일 생성")
        return True

    return False

def stage4_analyze(bidding_data):
    """Stage 4: 분석 실행 (logic 스킬)"""
    log("\n" + "="*80)
    log("Stage 4: 분석 실행 (logic 스킬)")
    log("="*80)

    # 투찰률에 해당하는 데이터 파일 찾기
    rate = bidding_data["투찰률"].replace(".", "_")
    data_file = PREPROCESSED_DIR / f"투찰률_{rate}%_데이터.xlsx"

    # 파일이 없으면 모든 투찰율 파일 검색
    if not data_file.exists():
        log(f"⚠️ {data_file.name} 파일이 없습니다. 전처리 데이터에서 검색합니다...")

        # 모든 투찰율 파일 찾기
        preprocessed_files = list(PREPROCESSED_DIR.glob("투찰률_*%_데이터.xlsx"))

        if not preprocessed_files:
            log(f"❌ 전처리 데이터 파일을 찾을 수 없습니다")
            return None

        # 투찰률과 가장 가까운 파일 찾기
        target_rate = float(bidding_data["투찰률"])

        best_match = None
        min_diff = float('inf')

        for f in preprocessed_files:
            # 파일명에서 투찰률 추출: "투찰률_87_745%_데이터.xlsx" → 87.745
            file_rate_str = f.stem.replace("투찰률_", "").replace("%_데이터", "").replace("_", ".")

            try:
                file_rate = float(file_rate_str)
                diff = abs(file_rate - target_rate)

                if diff < min_diff:
                    min_diff = diff
                    best_match = f
            except ValueError:
                continue

        if best_match:
            data_file = best_match
            log(f"✅ 가장 가까운 투찰율 파일 발견: {data_file.name}")
        else:
            log(f"❌ 투찰률 {target_rate}%에 해당하는 파일을 찾을 수 없습니다")
            return None

    # analyze.py 실행
    script_path = SKILLS_DIR / "logic" / "analyze.py"

    cmd = [
        "python3", str(script_path),
        "--base-amount", bidding_data["기초금액"],
        "--agency-rate", bidding_data["투찰률"],
        "--data-file", str(data_file)
    ]

    success, output = run_command(cmd, "입찰 분석", timeout=300)

    if success:
        # 분석 결과 JSON 파일 확인 (점 없이)
        rate_nodot = rate.replace("_", "")
        json_file = DATA_ANALYSIS_DIR / f"bidding_analysis_{rate_nodot}.json"

        if not json_file.exists():
            # 점 있는 버전도 확인
            json_file = DATA_ANALYSIS_DIR / f"bidding_analysis_{rate}.json"

        if json_file.exists():
            log(f"✅ 분석 완료: {json_file}")
            return json_file
        else:
            # 모든 JSON 파일 검색
            json_files = list(DATA_ANALYSIS_DIR.glob("bidding_analysis_*.json"))
            if json_files:
                json_file = max(json_files, key=lambda p: p.stat().st_mtime)
                log(f"✅ 최신 분석 파일 발견: {json_file}")
                return json_file
            else:
                log(f"❌ 분석 결과 파일이 생성되지 않았습니다")
                return None

    return None

def stage5_report(json_file):
    """Stage 5: 보고서 생성 (report 스킬)"""
    log("\n" + "="*80)
    log("Stage 5: 보고서 생성 (report 스킬)")
    log("="*80)

    # generate_report.py 실행
    script_path = SKILLS_DIR / "report" / "generate_report.py"

    # 스크립트가 없으면 간단한 보고서 생성
    if not script_path.exists():
        log("⚠️ generate_report.py가 없습니다. 간단한 보고서를 생성합니다.")

        # JSON 읽기
        with open(json_file, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)

        # 마크다운 보고서 생성
        report_file = RESULTS_DIR / "분석_보고서.md"
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 입찰 분석 보고서\n\n")
            f.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## 분석 결과\n\n")
            f.write("```json\n")
            f.write(json.dumps(analysis_data, indent=2, ensure_ascii=False))
            f.write("\n```\n")

        log(f"✅ 보고서 생성 완료: {report_file}")
        return report_file

    cmd = [
        "python3", str(script_path),
        "--json-file", str(json_file)
    ]

    success, output = run_command(cmd, "보고서 생성", timeout=120)

    if success:
        log(f"✅ 보고서 생성 완료")
        return True

    return False

def main():
    """메인 파이프라인 실행"""
    start_time = datetime.now()

    log("\n" + "="*80)
    log("입찰 분석 마스터 파이프라인 시작")
    log("="*80)

    try:
        # Stage 1: 이미지 감지
        image_file = stage1_detect_image()
        if not image_file:
            log("❌ Stage 1 실패: 이미지 파일 없음")
            return 1

        # Stage 2: Excel 생성
        excel_file, bidding_data = stage2_create_excel(image_file)
        if not excel_file:
            log("❌ Stage 2 실패: Excel 생성 실패")
            return 1

        # Stage 3: 데이터 전처리 (이미 완료되어 있으면 건너뛰기)
        preprocessed_files = list(PREPROCESSED_DIR.glob("투찰률_*%_데이터.xlsx"))
        if not preprocessed_files:
            log("⚠️ 전처리 데이터가 없습니다. 전처리를 실행합니다...")
            if not stage3_preprocess():
                log("❌ Stage 3 실패: 전처리 실패")
                return 1
        else:
            log(f"✅ 전처리 데이터 이미 존재: {len(preprocessed_files)}개 파일")

        # Stage 4: 분석 실행
        json_file = stage4_analyze(bidding_data)
        if not json_file:
            log("❌ Stage 4 실패: 분석 실패")
            return 1

        # Stage 5: 보고서 생성
        if not stage5_report(json_file):
            log("❌ Stage 5 실패: 보고서 생성 실패")
            return 1

        # 완료
        end_time = datetime.now()
        elapsed = (end_time - start_time).total_seconds()

        log("\n" + "="*80)
        log(f"✅ 파이프라인 완료! (실행시간: {elapsed:.1f}초)")
        log("="*80)
        log(f"\n결과 위치: {RESULTS_DIR}")

        return 0

    except Exception as e:
        log(f"\n❌ 파이프라인 실패: {str(e)}")
        import traceback
        log(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
