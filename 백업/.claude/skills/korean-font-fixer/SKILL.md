---
name: korean-font-fixer
description: |
  matplotlib 한국어 폰트 문제 자동 해결 (Noto Sans KR 설치).

  실행:
  python3 /mnt/a/25/.claude/skills/korean-font-fixer/fix_korean_font.py

  주요 기능:
  1. 시스템 한국어 폰트 진단
  2. Noto Sans KR 자동 다운로드
  3. matplotlib 폰트 캐시 재생성
  4. 한국어 폰트 설정 자동 적용

  Use when: 한국어 깨짐, 폰트 오류, Malgun Gothic 없음, DejaVu Sans 경고
---

# matplotlib 한국어 폰트 자동 수정

## ⚠️ 문제 상황

matplotlib로 그래프 생성 시 한국어가 깨지는 현상:

```python
# 경고 메시지:
findfont: Font family 'Malgun Gothic' not found.
UserWarning: Glyph 44592 (\N{HANGUL SYLLABLE GI}) missing from font(s) DejaVu Sans.
```

**원인**: 시스템에 한국어 폰트가 설치되지 않음 (총 92개 폰트 중 한국어 폰트 0개)

---

## 🛠️ 자동 해결 방법

### 1. 스크립트 실행 (권장)

```bash
python3 /mnt/a/25/.claude/skills/korean-font-fixer/fix_korean_font.py
```

**실행 내용:**
1. 시스템 한국어 폰트 확인
2. Noto Sans KR 폰트 다운로드 (Google Fonts)
3. ~/.local/share/fonts/ 에 설치
4. matplotlib 폰트 캐시 재생성
5. 자동 설정 완료

### 2. 수동 설치 (선택)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install fonts-nanum fonts-noto-cjk
fc-cache -fv
```

**WSL/사용자 폴더:**
```bash
mkdir -p ~/.local/share/fonts
cd ~/.local/share/fonts
wget https://github.com/google/fonts/raw/main/ofl/notosanskr/NotoSansKR-Regular.ttf
fc-cache -fv
```

**matplotlib 캐시 재생성:**
```python
import matplotlib.font_manager as fm
fm._rebuild()
```

---

## 📊 사용 방법

### analyze.py에서 자동 적용

스크립트 실행 후 `analyze.py`가 자동으로 Noto Sans KR을 사용합니다:

```python
# analyze.py에서 폰트 설정 (이미 적용됨)
import matplotlib.pyplot as plt

# 한국어 폰트 자동 감지 및 설정
plt.rcParams['font.family'] = 'Noto Sans KR'  # 또는 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False
```

### 그래프 생성 시 확인

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 사용 가능한 한국어 폰트 확인
korean_fonts = [f.name for f in fm.fontManager.ttflist
                if 'Noto' in f.name or 'Nanum' in f.name]
print('한국어 폰트:', korean_fonts)

# 테스트 그래프
plt.figure(figsize=(8, 6))
plt.title('한국어 테스트: 복수예가입찰 분석')
plt.xlabel('기초대비투찰률 (%)')
plt.ylabel('경쟁자 밀도 (명)')
plt.savefig('test_korean.png', dpi=150)
```

---

## 🔍 진단 도구

### 현재 폰트 상태 확인

```bash
python3 /mnt/a/25/.claude/skills/korean-font-fixer/fix_korean_font.py --check-only
```

**출력 예시:**
```
📊 현재 matplotlib 폰트 설정:
============================================================
기본 폰트: ['sans-serif']
폰트 파일 개수: 92

🇰🇷 한국어 지원 폰트 검색:
------------------------------------------------------------
  ✓ Noto Sans KR
  ✓ NanumGothic
  ✓ NanumBarunGothic

총 3개의 한국어 폰트 발견
```

---

## 📁 파일 구조

```
~/.local/share/fonts/
├── NotoSansKR-Regular.ttf
├── NotoSansKR-Bold.ttf
└── NotoSansKR-Light.ttf

~/.cache/matplotlib/
└── fontlist-v*.json    # 재생성됨
```

---

## 🚨 트러블슈팅

### 1. 폰트 설치 후에도 여전히 깨짐

**해결:**
```python
import matplotlib.font_manager as fm
fm._rebuild()  # 강제 재빌드
```

### 2. 특정 폰트를 사용하고 싶음

**analyze.py 수정:**
```python
# create_balance_graph() 함수 내
plt.rcParams['font.family'] = 'NanumGothic'  # 원하는 폰트
```

### 3. WSL에서 폰트 경로 인식 안 됨

**해결:**
```bash
# matplotlib 설정 파일 생성
mkdir -p ~/.config/matplotlib
cat > ~/.config/matplotlib/matplotlibrc <<EOF
font.family: Noto Sans KR
axes.unicode_minus: False
EOF
```

### 4. venv 환경에서만 적용하려면

**venv 활성화 후:**
```bash
source /mnt/a/25/venv/bin/activate
python3 /mnt/a/25/.claude/skills/korean-font-fixer/fix_korean_font.py --venv-only
```

---

## 🎯 권장 폰트

### 1. **Noto Sans KR** (권장)
- Google Fonts 공식
- 깔끔한 산세리프
- 경량 파일 (Regular: ~2MB)
- matplotlib 호환성 우수

### 2. **Nanum Gothic**
- 네이버 나눔 폰트
- 한국에서 가장 보편적
- 무료 오픈소스

### 3. **Malgun Gothic**
- Windows 기본 폰트
- Linux/WSL에서는 수동 설치 필요
- 라이선스 제약 있음

---

## 📝 참고 문서

**matplotlib 한국어 설정 공식 가이드:**
- https://matplotlib.org/stable/tutorials/text/text_props.html

**Google Fonts - Noto Sans KR:**
- https://fonts.google.com/noto/specimen/Noto+Sans+KR

**fontconfig 캐시 관리:**
```bash
fc-list :lang=ko  # 한국어 폰트 목록
fc-cache -fv      # 폰트 캐시 재생성
```

---

## ✅ 실행 체크리스트

- [ ] `fix_korean_font.py` 실행
- [ ] 한국어 폰트 3개 이상 설치 확인
- [ ] matplotlib 폰트 캐시 재생성 완료
- [ ] `analyze.py` 재실행 (경고 없이 그래프 생성)
- [ ] `balance_graph_87745.png` 한국어 정상 표시 확인

---

**Last Updated:** 2025-10-26
**Status:** 한국어 폰트 0개 → Noto Sans KR 자동 설치
**테스트 완료:** WSL2 Ubuntu 환경
