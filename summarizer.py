from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

tokenizer = AutoTokenizer.from_pretrained("digit82/kobart-summarization")
model = AutoModelForSeq2SeqLM.from_pretrained("digit82/kobart-summarization")

summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

def summarize_text(text):
    input_len = len(text.split())

    # 너무 짧은 본문 방지
    if input_len < 10:
        return "[요약 생략] 본문이 너무 짧습니다."

    # 너무 긴 본문은 앞부분만 사용
    text = text[:1000]
    max_len = min(200, int(input_len * 1.2))

    try:
        result = summarizer(text, max_length=max_len, min_length=20, do_sample=False)

        if not result or "summary_text" not in result[0]:
            return "[요약 실패] 요약 결과가 없습니다."

        return result[0]["summary_text"]

    except IndexError:
        return "[요약 실패] 요약 결과가 비어 있습니다."
    except Exception as e:
        return f"[요약 실패] {str(e)}"
