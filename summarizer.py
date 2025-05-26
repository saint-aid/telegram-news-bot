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

# 🤗 Hugging Face Inference API URL (KoBART 요약 모델)
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/digit82/kobart-summarization"

# 환경변수에서 API 토큰 가져오기 (.env 또는 Render 환경 설정에서 설정)
HUGGINGFACE_API_TOKEN = os.getenv("HF_API_TOKEN")

# 요청 헤더 설정
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

def summarize_text(text):
    """
    한국어 뉴스 본문을 Hugging Face Inference API를 통해 요약하는 함수

    Args:
        text (str): 뉴스 기사 본문 텍스트

    Returns:
        str: 요약 결과 문자열 (또는 오류 메시지)
    """

    # 본문이 너무 짧을 경우 요약 생략
    input_len = len(text.split())
    if input_len < 10:
        return "[요약 생략] 본문이 너무 짧습니다."

    # 너무 긴 입력은 앞부분만 자름 (1000자 제한)
    text = text[:1000]

    try:
        # API 요청
        response = requests.post(
            HUGGINGFACE_API_URL,
            headers=headers,
            json={"inputs": text},
            timeout=30
        )

        # 응답 성공 시 결과 추출
        if response.status_code == 200:
            result = response.json()
            if result and isinstance(result, list) and "summary_text" in result[0]:
                return result[0]["summary_text"]
            else:
                return "[요약 실패] 요약 결과가 없습니다."
        else:
            return f"[요약 실패] {response.status_code} - {response.text}"

    except Exception as e:
        return f"[요약 실패] {str(e)}"
