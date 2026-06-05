"""
WooaPC(PCTools) KO 페이지 메타 디스크립션 CTR 최적화
- 최우선: "pc 포맷"(77)+"pc포맷"(22)+"pc 포멧"(10) = 109 노출, 0% → index.html
- 중요: "포맷 후 필수 프로그램"(25+변형들) = 51+ 노출, 0%
- 특별: ubisoft-connect (ubi소프트 런처 녹화 3노출), v3-lite (v3 lite vs 알집 2노출)
- 공통: "WooaPC 엄선 PC 포맷 후 필수 프로그램." → "PC 포맷 후 필수 프로그램, 공식 다운로드 안내."
         "[AppName] 공식 다운로드." → "[AppName] 무료 공식 다운로드 —"
"""
import re, os, glob

BASE = 'C:/개인/wooahouse/PCTools'

# ── 개별 완전 교체 ──────────────────────────────────────────────────────
INDIVIDUAL = {
    'index.html': (
        'PC 포맷 후 꼭 설치해야 할 필수 프로그램 58개 모음.',
        'PC 포맷 후 필수 프로그램 58개 모음 — 브라우저·백신·압축·미디어·게임·생산성·개발 도구까지 공식 다운로드 링크 한 곳에서 무료 확인. pc포맷 후 꼭 설치해야 할 pc 필수 프로그램만 엄선.'
    ),
    'apps/ubisoft-connect.html': (
        'Ubisoft Connect 공식 다운로드.',
        'Ubisoft Connect 무료 공식 다운로드 — 유비소프트 공식 런처, 어쌔신크리드·레인보우식스·파크라이. 게임 녹화·스크린샷 기능 포함, PC 포맷 후 필수 게임 런처 설치 안내.'
    ),
    'apps/v3-lite.html': (
        'V3 Lite 공식 다운로드.',
        'V3 Lite 무료 공식 다운로드 — 안랩(AhnLab) 무료 백신, 가벼운 리소스로 국내 위협 대응 특화. 알약·알집 대신 V3 선택 이유, PC 포맷 후 필수 백신 설치 가이드.'
    ),
    'apps/alzip.html': (
        '알집 공식 다운로드.',
        '알집 무료 공식 다운로드 — 이스트소프트 국내 대표 압축 프로그램, ALZ·EGG 전용 포맷 지원. PC 포맷 후 필수 압축 프로그램, 설치 가이드.'
    ),
}


def sync_og_twitter(content, new_val):
    content = re.sub(
        r'(<meta property="og:description" content=")[^"]*(")',
        lambda x: x.group(1) + new_val + x.group(2), content
    )
    content = re.sub(
        r'(<meta name="twitter:description" content=")[^"]*(")',
        lambda x: x.group(1) + new_val + x.group(2), content
    )
    return content


ok = 0
miss = 0

# ── 1) 개별 처리 ──────────────────────────────────────────────────────
for rel_path, (match_prefix, new_desc) in INDIVIDUAL.items():
    fpath = os.path.join(BASE, rel_path)
    if not os.path.exists(fpath):
        print(f'  SKIP: {rel_path}')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    pattern = r'(<meta name="description" content=")[^"]*(")'
    def replacer(m, mp=match_prefix, nd=new_desc):
        if mp in m.group(0):
            return m.group(1) + nd + m.group(2)
        return m.group(0)
    c2 = re.sub(pattern, replacer, c)
    if c2 == c:
        print(f'  MISS: {rel_path}')
        miss += 1
        continue
    c2 = sync_og_twitter(c2, new_desc)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c2)
    print(f'  OK (개별): {rel_path}')
    ok += 1

# ── 2) apps/*.html 공통 처리 ──────────────────────────────────────────
app_files = sorted(glob.glob(os.path.join(BASE, 'apps', '*.html')))
individually_done = {
    os.path.normpath(os.path.join(BASE, p)) for p in INDIVIDUAL
}

for fpath in app_files:
    if os.path.normpath(fpath) in individually_done:
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    m = re.search(r'<meta name="description" content="([^"]+)"', c)
    if not m:
        print(f'  SKIP (desc 없음): apps/{os.path.basename(fpath)}')
        continue
    old_desc = m.group(1)

    # Step1: "[AppName] 공식 다운로드." → "[AppName] 무료 공식 다운로드 —"
    new_desc = re.sub(
        r'^(.+?) 공식 다운로드\.',
        r'\1 무료 공식 다운로드 —',
        old_desc,
        count=1
    )

    # Step2: suffix 교체
    new_desc = re.sub(
        r'\s*WooaPC 엄선 PC 포맷 후 필수 프로그램\.',
        ' PC 포맷 후 필수 프로그램, 공식 다운로드 안내.',
        new_desc
    )

    if new_desc == old_desc:
        print(f'  MISS: apps/{os.path.basename(fpath)}')
        miss += 1
        continue

    c2 = c.replace(
        f'<meta name="description" content="{old_desc}"',
        f'<meta name="description" content="{new_desc}"',
        1
    )
    c2 = sync_og_twitter(c2, new_desc)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c2)
    print(f'  OK: apps/{os.path.basename(fpath)}')
    ok += 1

print(f'\n완료: {ok}개 교체, {miss}개 실패')
