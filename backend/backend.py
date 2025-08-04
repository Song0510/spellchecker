from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# CORS 설정 (프론트: localhost:3000 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GPT API 키 불러오기
with open(r"C:\Users\재훈\PyCharmMiscProject\Student12.txt", 'r') as f:
    API_KEY = f.read().strip()

client = OpenAI(api_key=API_KEY)

# 클라이언트로부터 받을 메시지 구조
class Message(BaseModel):
    message: str

# 맞춤법 검사 API
@app.post("/spellcheck")
def spell_check(msg: Message):
    try:
        print("입력값:", msg.message)
        # GPT에게 맞춤법 교정 요청
        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "당신은 국어 맞춤법 검사 도우미입니다. "
                        "사용자의 문장에서 맞춤법이 틀린 부분을 찾아 "
                        "그 단어의 시작 인덱스(start), 끝 인덱스(end), 그리고 수정 제안(suggestion)을 "
                        "JSON 형태로 출력하세요. 예: "
                        "{\"corrections\": [{\"start\": 3, \"end\": 7, \"suggestion\": \"반갑습니다\"}]}"
                    )
                },
                {
                    "role": "user",
                    "content": msg.message
                }
            ]
        )

        # GPT 응답의 텍스트(JSON 문자열)만 반환
        return completion.choices[0].message.content

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))