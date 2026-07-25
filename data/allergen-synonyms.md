# 동의어표 (EU 향료 알레르겐 26종 — INCI = 한글표준 = 이명/표기변형)

※ 각 쌍은 대한화장품협회 성분사전 기준 검증 필요 (지원 확정 대상)

※ **자동 조회 시도 결과**: kcia.or.kr/cid 성분검색은 JS 폼 기반이라 GET 파라미터로
직접 조회가 안 됨(두 가지 파라미터 추정 시도 모두 실패, 필터 안 된 전체
21,961건만 반환). 아래 표는 프로젝트 내 기존 검증 자료
([data/allergen_reference.tsv](allergen_reference.tsv), 대한화장품협회 성분사전 대조
완료분)와 실제 데이터셋([data/unique_ingredients.txt](unique_ingredients.txt))만으로
교차 확인한 것이며, 그 외 항목은 KCIA 원문 대조가 안 된 상태다. "검증"
표시가 없는 항목은 직접 KCIA에서 확인 필요.

## ⚠ 발견된 문제: Citronellol 표준/이명 순서 오류

초안에 `Citronellol = 시트로넬롤 = 시트로넬올`로 되어 있었는데, 아래 두 소스가
모두 반대로 확인된다:
- `data/allergen_reference.tsv` (5행, 기 검증본): `Citronellol	시트로넬올`
- `data/unique_ingredients.txt` (148행, 실제 제품 라벨): `시트로넬올 (11)`

즉 **표준은 "시트로넬올", "시트로넬롤"이 이명(표기변형)**이다. 아래 표는 이 순서로
정정해서 반영했다. (초안 그대로 넣었으면 위음성이 아니라 표준/변형이 뒤바뀐 채로
고정될 뻔한 케이스라 먼저 짚어둠.)

## 표기 규칙 메모 (검증됨)

- **알코올 vs 알콜**: 데이터셋(`unique_ingredients.txt`) 전체에서 "알코올"만
  6회 등장(t-부틸알코올, 베헤닐알코올, 변성알코올, 세테아릴알코올, 세틸알코올,
  폴리비닐알코올) — "알콜" 표기는 0회. `allergen_reference.tsv`의
  `Benzyl Alcohol → 벤질알코올`도 동일하게 "알코올". **표준 = 알코올, "알콜"은
  변형 표기(이 데이터셋에는 미출현하지만 다른 라벨에서 나올 수 있어 이명으로 유지)**.
- **-알(알데하이드 축약형) vs 알데하이드(완전형)**: `allergen_reference.tsv`의
  `Benzaldehyde → 벤즈알데하이드`는 완전형을 쓰는 반면, 신남알 계열(Cinnamal,
  Amyl Cinnamal, Hexyl Cinnamal, Hydroxycitronellal)은 관행상 "-알" 축약형으로
  표기된다. 이는 오탈자가 아니라 INCI 국문 표기 관행 자체가 성분군마다 다른
  것으로 확인됨 — 매칭 시 두 형태 다 열어둘 것.
- **추출물(Extract) 계열 매칭 원칙**: Evernia Prunastri/Furfuracea Extract(오크모스/
  트리모스)는 라벨에 그 이름 자체가 성분명으로 적히므로 매칭 대상이 맞다. 단,
  "이 추출물 안에 알레르겐 성분이 들어있을 것"이라고 확장 추론하는 것은 금지
  (환경 분석 모듈 규칙 2, 유래 추정 금지와 동일 원칙). 표기된 이름 문자열
  자체만 매칭한다.

---

# ── 데이터셋에서 실제 검출된 5종 (우선 검증) ──

| INCI | 한글표준 | 이명/표기변형 | 검증 |
|---|---|---|---|
| Linalool | 리날룰 | 리나룰, 리나롤 | 데이터셋 대조(59행 "리날룰") ✓ / KCIA 미대조 |
| Limonene | 리모넨 | 디-리모넨, d-리모넨 | `allergen_reference.tsv` 대조 ✓ + 데이터셋(60행) ✓ |
| Citronellol | 시트로넬올 | 시트로넬롤 | `allergen_reference.tsv` 대조 ✓ + 데이터셋(148행) ✓ — **순서 정정됨(위 참고)** |
| Geraniol | 제라니올 | 게라니올 | 데이터셋 대조(191행 "제라니올") ✓ / KCIA 미대조 |
| Citral | 시트랄 | (표기 변형 없음) | `allergen_reference.tsv` 대조 ✓ + 데이터셋(147행) ✓ |

# ── 나머지 EU 26종 (골격, KCIA 원문 대조 필요) ──

| INCI | 한글표준(초안) | 이명/표기변형 | 검증 |
|---|---|---|---|
| Eugenol | 유제놀 | 오이게놀 | 미검증 |
| Isoeugenol | 아이소유제놀 | 이소유제놀 | `allergen_reference.tsv` 대조 ✓ (4행) |
| Coumarin | 쿠마린 | — | 미검증 |
| Benzyl Alcohol | 벤질알코올 | 벤질알콜 | `allergen_reference.tsv` 대조 ✓ (2행) — "알코올" 표기 재확인 |
| Benzyl Benzoate | 벤질벤조에이트 | — | 미검증 |
| Benzyl Salicylate | 벤질살리실레이트 | — | 미검증 |
| Benzyl Cinnamate | 벤질신나메이트 | — | 미검증 |
| Cinnamal | 신남알 | 신나말, 시나몬알데하이드 | 미검증 (축약형 "-알" 표기, 위 메모 참고) |
| Cinnamyl Alcohol | 신나밀알코올 | 신나밀알콜 | 미검증 |
| Hydroxycitronellal | 하이드록시시트로넬알 | 히드록시시트로넬알 | 미검증 (축약형 "-알" 표기) |
| Anise Alcohol | 아니스알코올 | 아니스알콜 | 미검증 |
| Amyl Cinnamal | 아밀신남알 | 아밀신나말 | 미검증 (축약형 "-알" 표기) |
| Amylcinnamyl Alcohol | 아밀신나밀알코올 | — | 미검증 |
| Farnesol | 파네솔 | 파르네솔 | 미검증 |
| Hexyl Cinnamal | 헥실신남알 | 헥실신나말 | 미검증 (축약형 "-알" 표기) |
| Butylphenyl Methylpropional | 부틸페닐메틸프로피오날 | 릴리알, Lilial | 미검증 |
| Alpha-Isomethyl Ionone | 알파-아이소메틸이오논 | — | 미검증 |
| Evernia Prunastri Extract | 참나무이끼추출물 | 오크모스, Oakmoss | 미검증 (매칭 원칙은 위 메모 참고) |
| Evernia Furfuracea Extract | 나무이끼추출물 | 트리모스, Treemoss | 미검증 (매칭 원칙은 위 메모 참고) |
| Methyl 2-Octynoate | 메틸2-옥티노에이트 | — | 미검증 |

## 남은 작업
"미검증" 15종(Coumarin, Benzyl Benzoate/Salicylate/Cinnamate, Cinnamal 계열,
Farnesol, Butylphenyl Methylpropional, Alpha-Isomethyl Ionone, Evernia 2종,
Methyl 2-Octynoate 등)은 KCIA 성분사전(kcia.or.kr/cid)에서 직접 검색해 국문
표준명을 대조해야 한다. 자동 조회가 안 되니 직접 확인 후 알려주면 표에 반영.
