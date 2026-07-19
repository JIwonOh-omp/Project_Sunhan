"""
v2 프롬프트 테스트 실행 스크립트 (Solar API)
---------------------------------------------
목적: v2 시스템 프롬프트를 대표 테스트 파일 4개에 돌려 v1 실패가 잡히는지 확인.

사용 전 준비:
  1) pip install openai
  2) 환경변수에 Solar API 키 설정
       Windows(PowerShell):  $env:UPSTAGE_API_KEY="발급받은_키"
       (또는 아래 코드에서 os.getenv 부분을 직접 키로 바꿔도 되지만 비권장)
  3) 아래 CONFIG의 경로/모델명이 실제 프로젝트와 맞는지 확인.

주의: MODEL 이름과 BASE_URL은 Upstage 콘솔/문서에서 현재 값을 확인할 것.
      (모델명은 시기에 따라 달라질 수 있음)
"""

import os
import glob
from pathlib import Path
from openai import OpenAI

# ========================= CONFIG =========================
# --- Solar API 설정 (Upstage 문서에서 현재 값 확인) ---
BASE_URL = "https://api.upstage.ai/v1"     # Solar는 OpenAI 호환 엔드포인트
MODEL    = "solar-pro3"
API_KEY  = os.getenv("UPSTAGE_API_KEY")     # 환경변수에서 읽음 (권장)

# --- 파일 경로 (프로젝트 구조에 맞게 조정) ---
PROMPT_DIR   = Path("prompts/v2")
DATA_DIR     = Path("data")
INPUTS_DIR   = DATA_DIR / "inputs"
RESULTS_DIR  = Path("results/v2")

MAIN_PROMPT  = PROMPT_DIR / "v2_prompt.md"
INGREDIENT_MAP = PROMPT_DIR / "v2_ingredient_map.md"
CORAL        = PROMPT_DIR / "v2_coral.md"
ALLERGEN     = DATA_DIR / "allergen_reference.tsv"

# --- 테스트 대상: 파일명에 이 번호가 포함된 입력 파일을 찾음 ---
# (실제 파일명이 다르면 TARGETS를 실제 이름으로 바꾸세요)
TARGET_NUMBERS = ["01", "04", "08", "11"]
# =========================================================


def read(path: Path) -> str:
    """파일을 UTF-8로 읽음. 없으면 에러 메시지와 함께 중단."""
    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없음: {path}")
    return path.read_text(encoding="utf-8")


def build_system_prompt() -> str:
    """
    v2_prompt.md의 '별첨 파일 ... 참조' 마커를 실제 파일 내용으로 치환해
    하나의 완성된 시스템 프롬프트를 조립한다.
    """
    prompt = read(MAIN_PROMPT)

    # §4 성분명 대응표 결합
    prompt = prompt.replace(
        "→ 별첨 파일 `v2_ingredient_map.md` 참조. (런타임에 본 위치에 결합)",
        read(INGREDIENT_MAP),
    )
    # §5 알레르겐 결합 (TSV를 그대로 텍스트로 삽입)
    prompt = prompt.replace(
        "→ 별첨 파일 `allergen_reference.tsv` 참조. (런타임에 본 위치에 결합)",
        "```\n" + read(ALLERGEN) + "\n```",
    )
    # §6 산호초 결합
    prompt = prompt.replace(
        "→ 별첨 파일 `v2_coral.md` 참조. (런타임에 본 위치에 결합)",
        read(CORAL),
    )
    return prompt


def find_input_files() -> dict:
    """TARGET_NUMBERS에 해당하는 입력 파일을 data/inputs/에서 찾는다."""
    found = {}
    all_files = sorted(glob.glob(str(INPUTS_DIR / "*")))
    for num in TARGET_NUMBERS:
        match = [f for f in all_files if num in Path(f).stem]
        if match:
            found[num] = Path(match[0])
        else:
            print(f"  ⚠️  {num}번 입력 파일을 찾지 못함 (INPUTS_DIR 확인 필요)")
    return found


def call_solar(client: OpenAI, system_prompt: str, ingredient_list: str) -> str:
    """Solar API 호출: 시스템 프롬프트 + 성분 리스트 → 응답 텍스트."""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": ingredient_list},
        ],
        temperature=0,   # 재현성을 위해 0 (테스트에 적합)
    )
    return resp.choices[0].message.content


def main():
    if not API_KEY:
        raise SystemExit("환경변수 UPSTAGE_API_KEY가 설정되지 않았습니다.")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    print("1) 시스템 프롬프트 조립 중...")
    system_prompt = build_system_prompt()
    print(f"   조립 완료 (길이: {len(system_prompt):,}자)")

    print("2) 입력 파일 탐색 중...")
    inputs = find_input_files()
    print(f"   찾은 파일: {list(inputs.keys())}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("3) Solar 호출 시작...")
    for num, path in inputs.items():
        print(f"   - {num}번 실행 중 ({path.name})...")
        ingredient_list = read(path)
        try:
            answer = call_solar(client, system_prompt, ingredient_list)
        except Exception as e:
            answer = f"[호출 실패] {e}"
            print(f"     ❌ 실패: {e}")
        out_path = RESULTS_DIR / f"v2_result_{num}.md"
        out_path.write_text(answer, encoding="utf-8")
        print(f"     저장: {out_path}")

    print("\n완료. results/v2/ 폴더의 결과 파일을 확인하세요.")


if __name__ == "__main__":
    main()
