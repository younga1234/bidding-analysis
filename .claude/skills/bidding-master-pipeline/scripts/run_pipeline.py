#!/usr/bin/env python3
"""
Bidding Master Pipeline v2.1
자동 순차 실행 스크립트
"""

import subprocess
import json
import sys
from datetime import datetime
from pathlib import Path

# 기본 경로 설정
BASE_DIR = Path("/mnt/a/25")
DATA_DIR = BASE_DIR / "data분석"
LOG_FILE = DATA_DIR / "pipeline_log.txt"

def log(message):
    """로그 메시지 출력 및 파일 기록"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

def run_command(cmd, stage_name):
    """명령 실행"""
    log(f"{stage_name} 시작")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            executable='/bin/bash'  # bash 사용
        )
        log(f"{stage_name} 완료")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        log(f"{stage_name} 실패: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    """메인 파이프라인 실행"""

    # 로그 초기화
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 파이프라인 시작 (v2.1)\n")

    # bidding_context.json 읽기
    context_file = DATA_DIR / "bidding_context.json"
    if not context_file.exists():
        log("❌ bidding_context.json 파일이 없습니다!")
        sys.exit(1)

    with open(context_file, "r", encoding="utf-8") as f:
        context = json.load(f)

    agency_rate = context["발주처투찰률"]
    base_amount = context["기초금액"]
    agency = context["발주처"]
    announcement_no = context["공고번호"]

    log(f"공고번호: {announcement_no}")
    log(f"발주처투찰률: {agency_rate}%")
    log(f"기초금액: {base_amount:,}원")
    log(f"발주처: {agency}")

    # 파일명용 발주처투찰률 (87.745 → 87_745)
    agency_rate_file = str(agency_rate).replace(".", "_")

    # 전처리 파일 확인
    preprocess_file = BASE_DIR / f"data전처리완료/투찰률_{agency_rate_file}%_데이터.xlsx"
    if not preprocess_file.exists():
        log(f"❌ 전처리 파일이 없습니다: {preprocess_file}")
        sys.exit(1)
    log(f"✅ 전처리 파일 확인: 투찰률_{agency_rate_file}%_데이터.xlsx")

    # venv 활성화 명령
    venv_activate = "source venv/bin/activate"

    # Stage 5-1: 기본 분석
    cmd_5_1 = f"""{venv_activate} && python .claude/skills/logic/analyze.py \
        --base-amount {base_amount} \
        --agency-rate {agency_rate} \
        --data-file "data전처리완료/투찰률_{agency_rate_file}%_데이터.xlsx"
    """
    if not run_command(cmd_5_1, "Stage 5-1: 기본 분석"):
        log("❌ Stage 5-1 실패로 중단")
        sys.exit(1)

    # Stage 5-2: 고급 분석
    cmd_5_2 = f"""{venv_activate} && python .claude/skills/bidding-advanced-analyzer/advanced_analyze.py \
        --agency-rate {agency_rate} \
        --data-file "data전처리완료/투찰률_{agency_rate_file}%_데이터.xlsx"
    """
    if not run_command(cmd_5_2, "Stage 5-2: 고급 분석"):
        log("❌ Stage 5-2 실패로 중단")
        sys.exit(1)

    # Stage 5-3: 메타 인지 분석
    month = datetime.now().month
    context_json = json.dumps({
        "기초금액": base_amount,
        "발주처": agency,
        "월": month
    }, ensure_ascii=False)

    cmd_5_3 = f"""{venv_activate} && python .claude/skills/bidding-meta-cognition/meta_analyze.py \
        --data-file "data전처리완료/투찰률_{agency_rate_file}%_데이터.xlsx" \
        --basic-result "data분석/bidding_analysis_{agency_rate_file}.json" \
        --advanced-result "data분석/bidding_analysis_advanced_{agency_rate_file}.json" \
        --context '{context_json}'
    """
    if not run_command(cmd_5_3, "Stage 5-3: 메타 인지 분석"):
        log("⚠️ Stage 5-3 실패, 계속 진행")

    # Stage 5-4: 통합 보고서 생성
    cmd_5_4 = f"{venv_activate} && python generate_reports.py {agency_rate_file}"
    if not run_command(cmd_5_4, "Stage 5-4: 통합 보고서 생성"):
        log("❌ Stage 5-4 실패로 중단")
        sys.exit(1)

    # 완료
    log("=" * 60)
    log("✅ 파이프라인 완료!")
    log(f"📊 보고서 위치: data분석/분석결과/입찰_분석_보고서_{agency_rate_file}.md")
    log("=" * 60)

    return 0

if __name__ == "__main__":
    sys.exit(main())
