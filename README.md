# Project_Sunhan
AI Reboot 대회 제출용
# Sunhan (순한) — Your K-Beauty Ingredient Guide

> **Sunhan** means *"mild & gentle"* in Korean — and yes, it starts with **sun**(screen). 🌞

한국어 화장품 라벨을 읽지 못하는 외국인을 위한 K-뷰티 성분 번역·해설 서비스입니다.
A K-beauty ingredient translator for international users who can't read Korean cosmetic labels.

## 🎯 What it does (MVP)

한국어 전성분 리스트를 입력하면:

1. **영어 번역** — 성분명을 영어(INCI)로 번역
2. **쉬운 해설** — 각 성분의 기능을 비전공자 눈높이의 한 줄 설명으로
3. **피부타입 주의 표시** — 민감성/지성 등 피부 타입별 주의 성분 하이라이트 (알레르기 유발 향료 26종 포함)
4. **환경 플래그** — 산호초 유해 성분(자외선차단제 등)과 미세플라스틱(합성 고분자) 등 환경 우려 성분 표시

**범위:** 기초화장품(토너, 세럼, 크림) 및 선케어 중심의 기능성화장품
**하지 않는 것:** 제품 추천, 효능 보장, 의학적 조언

## 💡 Why I built this

**1. 화장품 회사 품질 연구원의 발견**
자외선 차단제, 여드름용 스킨케어 제품 등 일부 기능성 화장품은 한국에서는 화장품이지만 북미에서는 일반의약품(OTC) 등 별도 규제 대상으로 분류된다는 사실을 아시나요? 저는 화장품 제조 회사의 품질 부서에서 근무하며 이러한 제품들의 북미 수출을 위한 일반의약품 검증을 수행하는 역할을 맡았습니다. 이때 같은 제품이라도 국가에 따라 분류가 달라지고, 성분 정보가 소비자 안전의 핵심이라는 사실을 체감했습니다.

**2. 캐나다에서 마주친 실제 문제**
이후 캐나다 워킹홀리데이 중 카페에서 근무하며, 외국인 동료들이 <한국 여행 중 사고 싶은 화장품 리스트>를 보여주며 추천을 부탁할 때마다 난감함을 느꼈습니다. 캐나다 매장에서 파는 한국 화장품에는 보통 영문 라벨이 붙어 있지만, 한국 여행 중에 사는 제품들에는 영문 전성분 표기가 없습니다. 외국인 관광객이 한국에서 화장품을 고를 때 겪을 어려움이 눈에 보였습니다.

**3. K-뷰티 관광 시대의 서비스**
K-뷰티의 위상이 높아지면서 외국인 관광객에게 화장품 쇼핑은 한국 여행의 필수 코스가 되었습니다. 품질 검증 경력과 캐나다에서의 경험을 연결해, 외국인 관광객의 화장품 쇼핑을 도와줄 수 있는 서비스를 직접 만들어보기로 했습니다.

## 🛠 Tech Stack

- **Solar LLM (Upstage)** — 한국어 원문(성분명, 표기 관행) 처리가 핵심이므로 한국어에 강한 국내 LLM을 메인으로 선택
- **프롬프트 엔지니어링** — 도메인 지식(화장품 성분, 규제 기준)을 시스템 프롬프트에 층층이 주입해 환각을 통제

## 프로젝트 구조

```
prompts/            버전별 프롬프트
  v1.md, v4.md        단일 파일 버전(v1, v4 개인화 모듈)
  v2/, v3/            버전별 프롬프트 + 참조 파일
  modules/            서브 모듈 (환경 분석: 리프세이프 + 미세플라스틱)
data/               입력 성분 리스트 및 참조 자료
  01~12번 제품 문서    제품별 원본 자료(전성분·시험 포인트·체크리스트)
  inputs/             제품별 전성분만 추출한 원본
  showcase/           GitHub Pages 쇼케이스용 제품 JSON (product-11.json 등)
  allergen_reference.tsv, allergen-synonyms.md, unique_ingredients.txt
                      알레르겐/성분 참조표
docs/               GitHub Pages 소스 (저장소 루트가 Pages 소스)
  index.html          앱 랜딩(첫 화면) — 가치제안 1줄 + 3요약 + "Get Started" → profile.html.
                       한 번 진입하면 localStorage 플래그로 재방문 시 자동 스킵(search.html로).
                       ?show=1 또는 각 화면 로고 탭으로 다시 볼 수 있음
  profile.html        온보딩/프로필(FYP) 화면(구 index.html) — 선택값을 sessionStorage로 전달
  search.html         제품 검색(Home) — 로컬 12개 중 필터링, "스캔" 버튼은 샘플(11번) 연출
  analysis.html       분석 결과 + For You 카드 화면 — 11번 제품 전용, "Save to Skin Journey" 버튼
  skin-journey.html   저장한 제품 기록(Journey 탭) — localStorage, 여행사진 추가는 Coming soon
  community.html      Coming soon 화면(Community 탭) — 정적 비전 카드
  palette-preview.html 색 팔레트 후보 비교용
  Sunhan App Mockup.* UI 목업 원본(html/png, 참조용 — 수정 금지)
진입 흐름: 랜딩(index.html) → Get Started → 프로필(profile.html) → 이하 탭 4개(Home·Journey·Community·Profile)
프로젝트/대회 소개는 앱 UI에 없음 — 이 README가 "About this project" 역할
results/            버전별(v2, v2.1, v3, v3.1) 테스트 결과
outputs/            v1 테스트 원시 출력
log/                일일 개발 로그
```

## 🗓 Progress Log

### 프로젝트 시작 — 범위 확정
저장소 개설, MVP 범위 확정, 테스트용 제품 12종 전성분 수집 완료
(별칭 매핑·환경 플래그·알레르겐 등 시험 유형 설계).

### v1 — 베이스라인 프롬프트
Solar API 테스트 환경 구축(Node.js). 선크림 3종 테스트로 실패 유형 8건 수집 —
오역→가짜 안전정보 연쇄, 성분 누락 후 허위 자가보고, 커버리지 불안정 등.
상세: [prompts/v1.md](prompts/v1.md)

### v2 — 도메인 지식 주입
9섹션 골격(역할/입력·작업/출력규칙/대응표/알레르겐/산호초/피부기준/금지/자가검증)
조립 및 도메인 데이터를 대한화장품협회 성분사전과 전수 대조. 대표 4파일 테스트 —
한련초 오역 연쇄 차단·산호초 Tier 구분·지방알코올/살리실레이트 오탐 방지·
알레르겐 확대판 매칭 성공. 남은 과제(v3): 빈 알레르겐 리스트 환각, 대응표 밖 오역,
출력 형식 불안정. 상세: [log/daily-0720](log/daily-0720)

### v3 — 출력 형식 안정화
고정 스키마 + [n/N] 개수 + 빈집합 고정 블록 + 풀사이즈 few-shot.
→ 형식 일관성·빈집합 위양성 차단 성공. 긴 목록 절단은 미해결(v3.1로 이관).

### v3.1 — 긴 목록 절단 대응 (경계 규명)
번역·해설 병합 + 앵커 + CHECK last 필드로 시도.
→ 절단 미해결. finish_reason=stop, 분량 축소에도 조기 종료 → "성분 ~50개 벽"으로
   규명. solar-pro2의 프롬프트 제어 한계로 기록(청킹 등 아키텍처 대응 필요 영역).

### 환경 분석 모듈 (v2 계열 확장) — 리프세이프 + 미세플라스틱
Tier 구조(확정/회색지대) + look-alike 억제 + 유래 추정 금지로 통합.
검증: 282성분 중 미세플라스틱 확정 2종·회색지대 3종 검출, look-alike 8종 정확히 비검출.
KR/EU 규제 갭(한국 비대상 leave-on 고분자 = EU 규제 대상)을 외국 사용자용 정보로 노출.
동의어표(EU 향료 알레르겐 26종) 병행 작성 — KCIA 성분사전 자동조회는 불가 확인,
기존 검증 자료로 교차 확인하다 Citronellol 표준/이명 순서 오류 발견·정정.

### v4 — 개인화 분석 (목업 "For You" 카드 대응)
입력: 피부 타입 · 회피 성분 · 피부 고민 + 전성분. 출력: 개인화 알림 카드.
위양성→위음성 전환 축. 유래·교차반응 추정 금지 + 의학 판단 금지 +
빈집합 고정 출력(v3 학습) + 절단 경고. 결정론적 매칭이라 페이지에서 클라이언트
사이드 라이브 구현 가능. 성분 번호는 번역 모듈 결과를 단일 기준으로 상속(B 구조).

### 핵심 원칙 (전 버전 관통)
구조적 강제는 작동하고(빈집합 고정 블록), 모델 자율 의존은 샌다(개수검증·절단·자기수정).
→ 환경 분석·v4 개인화 매칭까지 자율 판단이 아닌 구조적 강제로 일관 설계.

### GitHub Pages 쇼케이스 1단계 — 제품11 분석 결과 화면
프롬프트 모듈을 실제 정적 웹 화면으로 처음 구현. 화면2(Analysis result)만 범위로
잡고, 데이터 스키마(`data/showcase/product-11.json`)부터 확정 — `analyzed` 플래그로
"미확인"과 "확인 후 안전"을 구분해 위음성 방지 원칙을 스키마 레벨까지 연장.
개인화 매칭은 LLM 없이 클라이언트 사이드 문자열 매칭, 성분 번호는 번역 결과를
단일 기준으로 상속(v4 설계 그대로 실구현). 번역 소스는 `results/v3/v3_result_11_run2.md`
REDO 최종본으로 확정 — 66성분·알레르겐 6종 caution·reef/microplastic tier 없음·
폴리비닐알코올 lookalike 억제까지 실데이터로 채워 검증 완료. Pages는 main/root를
소스로 활성화, 빌드·라이브 fetch 둘 다 확인.

### GitHub Pages 쇼케이스 2~6단계 — 온보딩부터 랜딩까지 전체 흐름 완성
화면1(온보딩) 구현 → 흐름을 온보딩→검색/선택→결과로 재배치 → 상시 리스트를
걷어내고 검색(로컬 필터)·스캔(샘플 연출, 정직성 라벨 명시) 두 진입로로 재구성 →
탭바를 Home·Skin Journey·Community·Profile 4개로 정리하고 Skin Journey를
`localStorage` 기반 실기능(저장·조회·삭제)으로 구현, Community는 순수 정적
Coming soon으로 분리 → 앱 랜딩 화면 신설(가치제안 "Understand what's really in
your Korean skincare.", Get Started→프로필 진입, 재방문 시 자동 스킵). 제품11의
실제 제품명(WHIPPED Mugtree Vegan Cookie Clay Pack Cleanser)도 원본 자료 확인 후
반영. 전 구간 헤드리스 브라우저로 실제 클릭 재현 검증. 상세: [log/daily-0727](log/daily-0727)

## 개발 현황
- [x] v1: 베이스라인 프롬프트 + 실패 유형 8가지 도출
- [x] v2: 도메인 지식 주입 (성분 대응표·EU 알레르겐 확대판·
      산호초 Tier·피부타입 기준·자가검증)
- [x] v3: 출력 형식 고정 스키마 + 빈집합 위양성 차단
- [x] v3.1: 긴 목록 절단 한계 규명 (프롬프트 레벨 한계로 기록, 아키텍처 대응은 별도 과제)
- [x] 환경 분석 모듈: 리프세이프 + 미세플라스틱 Tier 판정 통합, EU 알레르겐 동의어표 작성
- [x] v4: 개인화 분석("For You" 카드) 모듈 설계
- [x] GitHub Pages 쇼케이스 1단계: 제품11 분석 결과 화면 + 스키마 확정, 실데이터 반영
- [x] GitHub Pages 쇼케이스 2단계: 화면1(온보딩) 구현 + 개인화 배선(sessionStorage)
- [x] GitHub Pages 쇼케이스 3단계: 온보딩→검색/선택→결과 흐름 재배치, 탭바 네비, Coming soon 화면
- [x] GitHub Pages 쇼케이스 4단계: 상시 리스트 제거, 검색(로컬 필터)·스캔(샘플 연출) 두 진입로로 재구성 + 정직성 라벨
- [x] GitHub Pages 쇼케이스 5단계: 탭바 4개(Home·Journey·Community·Profile) 재구성,
      Skin Journey 실기능(localStorage 저장·조회·삭제) 구현, Community는 정적 Coming soon으로 분리
- [x] GitHub Pages 쇼케이스 6단계: 앱 랜딩 화면 신설(가치제안 "Understand what's really in
      your Korean skincare.") + Get Started→프로필 진입 흐름, 재방문 시 랜딩 자동 스킵(localStorage)
- [ ] 쇼케이스 확장: 나머지 11개 제품 실데이터 채우기 (예정)
