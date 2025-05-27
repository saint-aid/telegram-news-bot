# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# tokenizer = AutoTokenizer.from_pretrained("digit82/kobart-summarization")
# model = AutoModelForSeq2SeqLM.from_pretrained("digit82/kobart-summarization")

# summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# def summarize_text(text):
#     input_len = len(text.split())

#     # 너무 짧은 본문 방지
#     if input_len < 10:
#         return "[요약 생략] 본문이 너무 짧습니다."

#     # 너무 긴 본문은 앞부분만 사용
#     text = text[:1000]
#     max_len = min(200, int(input_len * 1.2))

#     try:
#         result = summarizer(text, max_length=max_len, min_length=20, do_sample=False)

#         if not result or "summary_text" not in result[0]:
#             return "[요약 실패] 요약 결과가 없습니다."

#         return result[0]["summary_text"]

#     except IndexError:
#         return "[요약 실패] 요약 결과가 비어 있습니다."
#     except Exception as e:
#         return f"[요약 실패] {str(e)}"


import os
import requests
from dotenv import load_dotenv

load_dotenv() 

# 🤗 Hugging Face Inference API URL (KoBART 요약 모델)
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/eenzeenee/t5-base-korean-summarization"

# 환경변수에서 API 토큰 가져오기 (.env 또는 Render 환경 설정에서 설정)
HUGGINGFACE_API_TOKEN = os.getenv("HF_API_TOKEN")

# 요청 헤더 설정
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

def summarize_text(text: str) -> str:
    input_len = len(text.strip().split())

    if input_len < 10:
        return "[요약 생략] 본문이 너무 짧습니다."

    text = text[:1000]

    try:
        response = requests.post(
            HUGGINGFACE_API_URL,
            headers=headers,
            json={"inputs": text},
            timeout=10 
        )

        response.raise_for_status()  # 4xx, 5xx 에러 자동 발생

        result = response.json()

        if isinstance(result, list) and len(result) > 0:
            summary = result[0].get("summary_text")
            if summary:
                return summary
            else:
                return "[요약 실패] 요약 결과에 summary_text가 없습니다."
        else:
            return "[요약 실패] 모델 응답 형식이 예기치 않습니다."

    except requests.exceptions.Timeout:
        return "[요약 실패] 요청 시간이 초과되었습니다."
    except requests.exceptions.RequestException as e:
        return f"[요약 실패] 요청 오류: {e}"
    except Exception as e:
        return f"[요약 실패] 예외 발생: {e}"
