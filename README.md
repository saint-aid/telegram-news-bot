# 🤖 텔레그램 뉴스 요약 챗봇

AI 기반으로 네이버 뉴스를 실시간 요약해주는 **한국어 요약 챗봇**입니다.  
Hugging Face의 KoBART 모델을 활용하여 텔레그램에서 카테고리별 뉴스 요약을 제공합니다.

---

## 🚀 기능 소개

- `/today` : 오늘의 주요 경제 뉴스를 요약
- `/today 부동산`, `/today 코인`, `/today 주식`, `/today AI` :
  각 주제에 해당하는 경제/IT 뉴스만 필터링하여 요약
- `/category` : 카테고리 버튼 선택으로 뉴스 요청 가능
- 일반 문장을 보내면 자동으로 요약 처리
- 요약 모델: 🤗 `digit82/kobart-summarization`

---

## 🧠 사용 기술

- Python + Flask
- python-telegram-bot v20+
- Hugging Face Transformers + KoBART
- BeautifulSoup (네이버 뉴스 본문 크롤링)
- Render 배포

---

## 📦 설치 및 실행

1. `.env` 파일 준비
```
BOT_TOKEN=your_telegram_token_here
```

2. 패키지 설치
```
pip install -r requirements.txt
```

3. 실행
```
python app.py
```

4. ngrok 사용 시
```
ngrok http 5000
```
Webhook 등록:
```
https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://<your-ngrok>.ngrok.io/webhook
```

---

## 🌍 Render 배포 가이드

이 프로젝트는 [Render.com](https://render.com)을 통해 무료로 배포했습니다.

### 🚀 배포 단계

1. [Render.com](https://render.com) 접속 → 로그인
2. "New → Web Service" 클릭
3. GitHub 저장소 선택
4. 아래와 같이 설정

| 항목 | 값 |
|------|-----|
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python app.py` |
| Environment Variables | `BOT_TOKEN=...` 입력 |
| Branch | main |

5. 배포 완료 후 주소 예: `https://news-telegram-bot.onrender.com`

### 🔗 Webhook 등록

브라우저 주소창에 입력:

```
https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=<YOUR_RENDER_URL>/webhook
```

### ☕ 슬립 방지 설정 (선택: 안해도 15분 후에는 5초 딜레이 연결됨)

- [UptimeRobot](https://uptimerobot.com)에서 5분 간격으로 ping 설정
- 혹은 GitHub Actions로 주기적 ping

---

## ⚠️ 내가 겪은 주요 시행착오와 해결법

| 문제 상황 | 해결 방법 |
|-----------|-----------|
| 뉴스 기사가 요약되지 않음 | 네이버 뉴스 구조 변경 → `soup.select("a[href*='/article/']")` 로 수정 |
| 요약 결과가 영어로 출력됨 | `facebook/bart-large-cnn` → `digit82/kobart-summarization` 교체 |
| `/today 부동산` 같은 필터링이 안 됨 | 본문 키워드 기반 필터링 추가 (`"부동산", "전세", ...`) |
| `update.message`가 None | `update.effective_message` 사용으로 해결 |
| `IndexError` 요약 실패 | `if not result:` 체크로 방어 코드 추가 |
| Webhook 작동 안 함 | Flask 서버 실행 + ngrok 주소 정확히 등록 확인 필요 |
| API 호출 작동 안 함 | 모델별로 API 방식이 되는 조건 값이 있음(pipeline_tag:summarization) |

---

## 📄 참고

- [KoBART Summarization 모델](https://huggingface.co/digit82/kobart-summarization)
- [python-telegram-bot docs](https://docs.python-telegram-bot.org/)

---

## 🙋‍♀️ 앞으로 확장 아이디어

- 뉴스 요약에 감정 분석 추가
- 사용자에게 요약 저장 기능
- 뉴스 추천 기능 연동
- DB 저장 및 즐겨찾기

---

## 🪟시연화면
![텔레그램 봇](https://github.com/user-attachments/assets/1299d99b-a7bb-4377-a8ba-d8ca00a96072)

---

## 👏 제작자

이 프로젝트는 실제 사용자가 직접 겪은 시행착오를 바탕으로 만든 실전형 챗봇입니다.
더 나은 개선을 위해 PR과 Issue를 환영합니다!
