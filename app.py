import os
import asyncio
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
from summarizer import summarize_text
from news_scraper import get_headlines # /today 명령어로 실시간 뉴스 요약

# .env 환경변수 불러오기
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask 앱
app = Flask(__name__)

# Telegram Application (비동기 처리용)
application = Application.builder().token(BOT_TOKEN).build()

# 카테고리 이름과 sid1 코드 매핑
CATEGORY_MAP = {
    "정치": "100",
    "경제": "101",
    "부동산": "101", 
    "주식": "101", 
    "코인": "101",   
    "사회": "102",
    "문화": "103",
    "세계": "104",
    "it": "105",
    "IT": "105",
    "ai": "105", 
    "AI": "105"
}
KEYWORD_MAP = {
    "부동산": ["부동산", "아파트", "전세", "매매"],
    "코인": ["코인", "비트코인", "가상화폐", "암호화폐", "이더리움", "블록체인"],
    "주식": ["주식", "코스피", "코스닥", "증시", "상장", "개미", "삼성전자"],
    "ai": ["AI", "인공지능", "생성형", "챗봇", "GPT", "LLM", "클로드", "바드", "오픈AI", "챗GPT"]
}

# /start 명령어
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "안녕하세요! 👋\n\n"
        "이 챗봇은 뉴스 기사를 크롤링해서 AI가 요약해주는 서비스예요.\n"
        "🧠 *Hugging Face Transformers* 모델을 사용해 자연스러운 한국어 요약을 제공합니다.\n\n"
        "원하시는 뉴스 카테고리를 `/category`로 골라보세요!"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# 자유 텍스트 요약 및 카테고리 버튼 처리
async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message:
        return

    text = message.text.strip()

    # 🎯 버튼 눌러서 들어온 경우 → /today 명령처럼 처리
    if text in CATEGORY_MAP:
        sid1 = CATEGORY_MAP[text]
        await message.reply_text(f"📰 [{text}] 뉴스 요약 중입니다...")

        articles = get_headlines(limit=3, category_sid1=sid1)
        if not articles:
            await message.reply_text("❌ 뉴스 기사를 찾을 수 없어요.")
            return

        for article in articles:
            title = article["title"]
            link = article["link"]
            content = article["content"]

            summary = summarize_text(content)
            msg = (
                f"🗞 *{title}*\n{link}\n\n"
                f"📌 *요약 결과*\n{summary}\n\n"
                f"[🤗 Powered by Hugging Face](https://huggingface.co/)"
            )
            await message.reply_text(msg, parse_mode="Markdown", disable_web_page_preview=True)

        return  # 🎯 여기서 끝!

    # 📝 일반 요약 처리
    summary = summarize_text(text)
    await message.reply_text(f"📌 *AI 요약 결과*\n\n{summary}", parse_mode="Markdown")


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message:
        return

    user_input = context.args[0] if context.args else "경제"
    category_sid = CATEGORY_MAP.get(user_input.lower(), "101")
    keywords = KEYWORD_MAP.get(user_input.lower(), None)

    await message.reply_text(f"📰 [{user_input}] 관련 뉴스 요약 중입니다...")

    try:
        articles = get_headlines(limit=3, category_sid1=category_sid, keywords=keywords)

        if not articles:
            await message.reply_text("❌ 관련된 뉴스 기사를 찾을 수 없어요.")
            return

        for article in articles:
            title = article["title"]
            link = article["link"]
            content = article["content"]
            summary = summarize_text(content)

            msg = f"🗞 *{title}*\n{link}\n\n📌 *요약 결과*\n{summary}\n\n🤗 _Powered by Hugging Face_"
            await message.reply_text(msg, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        await message.reply_text(f"❌ 오류 발생: {e}")


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["정치", "경제", "사회"],
        ["문화", "세계", "IT"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "📰 보고 싶은 뉴스 카테고리를 선택하세요:",
        reply_markup=reply_markup
    )


# /donate 후원 안내
async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🙏 챗봇이 도움이 되셨나요?\n\n"
        "💝 아래 QR코드를 스캔하여 토스로 후원해주실 수 있습니다!\n\n"
        "_커피 한 잔의 응원이 큰 힘이 됩니다._"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

     # 이미지 전송
    if os.path.exists("toss_qr.png"):
        with open("toss_qr.png", "rb") as photo:
            await update.message.reply_photo(photo=photo, caption="📱 토스 송금 QR코드")
    else:
        await update.message.reply_text("❌ QR 코드 이미지가 아직 등록되지 않았습니다.")

# 핸들러 등록
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("today", today))
application.add_handler(CommandHandler("donate", donate))
application.add_handler(CommandHandler("category", category))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, summarize))

# Flask용 Webhook 처리
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)

    async def process():
        await application.initialize()
        await application.process_update(update)
        await application.shutdown()

    asyncio.run(process())
    return "ok"


# 확인용 루트
@app.route("/")
def index():
    return "Bot is running"



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)