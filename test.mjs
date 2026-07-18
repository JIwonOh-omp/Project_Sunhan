// Sunhan 프롬프트 테스트 스크립트
// 사용법: node --env-file=.env test.mjs data/01.md
// (첫 번째 인자로 테스트할 전성분 데이터 파일을 지정)

import fs from "fs";

const PROMPT_FILE = "./prompts/v1.md"; // v2, v3 테스트 시 여기만 변경

const systemPrompt = fs.readFileSync(PROMPT_FILE, "utf-8");
const dataFile = process.argv[2];
if (!dataFile) {
  console.error("사용법: node --env-file=.env test.mjs data/01.md");
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
console.log(data.choices[0].message.content);