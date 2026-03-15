# PCTools 프로젝트 지침

## 프로젝트 개요
- **사이트명:** PCTools
- **URL:** https://pctools.wooahouse.com
- **GitHub:** https://github.com/ingmaster83-code/PCTools
- **배포:** GitHub Pages (main 브랜치 → root)
- **도메인 관리:** 호스팅케이알
- **DNS:** pctools CNAME → ingmaster83-code.github.io
- **수익 모델:** Google AdSense

## 기술 스택
- 순수 HTML / CSS / JS (프레임워크 없음)

## 서비스 목적
PC 포맷 후 사람들이 일일이 검색해서 설치해야 하는 기본 프로그램들의
공식 다운로드 링크를 한 곳에 모아서 제공하는 사이트.
한국 프로그램 포함, 한국 사용자 타겟.

## 파일 구조
```
PCTools/
├── index.html        # 메인 (프로그램 목록)
├── about.html        # 서비스 소개
├── privacy.html      # 개인정보처리방침
├── robots.txt
├── sitemap.xml
├── CNAME             # pctools.wooahouse.com
├── PROJECT_LOG.md    # 프로젝트 개발 로그
└── css/
    └── style.css
```

## 작업 규칙
- 프로그램 링크는 반드시 공식 사이트 또는 공식 배포 페이지만 사용 (서드파티 다운로드 사이트 금지)
- 한국 필수 프로그램(카카오톡, 알약, 한글 뷰어 등) 포함 필수
- SEO 키워드: PC 포맷 후 설치 프로그램, 윈도우 필수 프로그램, PC 초기화 후 설치
