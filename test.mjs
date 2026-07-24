// Sunhan 프롬프트 테스트 스크립트
// 사용법: node --env-file=.env test.mjs data/inputs/01-sunscreen-rejuran [outFile] [label]
// (첫 번째 인자로 테스트할 전성분 데이터 파일을 지정.
//  outFile을 주면 결과를 콘솔 대신 해당 파일에 저장하고, label을 주면
//  파일 맨 위에 <!-- ... --> 주석으로 어떤 입력·몇 회차인지 남긴다.)

import fs from "fs";
import path from "path";

const REFERENCE_DIR = "./prompts/v2"; // 성분명 대응표·산호초 리스트는 버전 공통으로 여기서 참조
const PROMPT_FILE = "./prompts/v3/v3.1_prompt.md"; // v3.1 테스트용. 다른 버전 테스트 시 여기만 변경
const INGREDIENT_MAP = path.join(REFERENCE_DIR, "v2_ingredient_map.md");
const CORAL = path.join(REFERENCE_DIR, "v2_coral.md");
const ALLERGEN = "./data/allergen_reference.tsv";

// v2/v2.1 프롬프트의 "별첨 파일 ... 참조" 마커를 실제 참조 파일 내용으로 치환한다.
function buildSystemPrompt() {
  let prompt = fs.readFileSync(PROMPT_FILE, "utf-8");
  prompt = prompt.replace(
    "→ 별첨 파일 `v2_ingredient_map.md` 참조. (런타임에 본 위치에 결합)",
    fs.readFileSync(INGREDIENT_MAP, "utf-8")
  );
  prompt = prompt.replace(
    "→ 별첨 파일 `allergen_reference.tsv` 참조. (런타임에 본 위치에 결합)",
    "```\n" + fs.readFileSync(ALLERGEN, "utf-8") + "\n```"
  );
  prompt = prompt.replace(
    "→ 별첨 파일 `v2_coral.md` 참조. (런타임에 본 위치에 결합)",
    fs.readFileSync(CORAL, "utf-8")
  );
  return prompt;
}

const systemPrompt = buildSystemPrompt();
const dataFile = process.argv[2];
const outFile = process.argv[3];
const label = process.argv[4];
if (!dataFile) {
  console.error(
    "사용법: node --env-file=.env test.mjs data/inputs/01-sunscreen-rejuran [outFile] [label]"
  );
  process.exit(1);
}
const ingredients = fs.readFileSync(dataFile, "utf-8");

const res = await fetch("https://api.upstage.ai/v1/chat/completions", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.UPSTAGE_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "solar-pro2",
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: ingredients },
    ],
  }),
});

if (!res.ok) {
  console.error(`Upstage API 오류 (status ${res.status}):`);
  console.error(await res.text());
  process.exit(1);
}

const data = await res.json();
const finishReason = data.choices[0].finish_reason ?? data.choices[0].stop_reason;
const outputTokens =
  data.usage?.completion_tokens ?? data.usage?.output_tokens ?? data.usage;
console.log(`finish_reason(stop_reason): ${finishReason}`);
console.log(`usage.output_tokens: ${outputTokens}`);
const answer = data.choices[0].message.content;

if (outFile) {
  const headerLines = [];
  if (label) headerLines.push(label);
  headerLines.push(`finish_reason: ${finishReason}`);
  headerLines.push(`usage.output_tokens: ${outputTokens}`);
  const header = headerLines.map((l) => `<!-- ${l} -->`).join("\n") + "\n\n";
  fs.mkdirSync(path.dirname(outFile), { recursive: true });
  fs.writeFileSync(outFile, header + answer, "utf-8");
  console.log(`저장: ${outFile}`);
} else {
  console.log(answer);
}