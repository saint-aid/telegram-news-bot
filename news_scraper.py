import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_headlines(limit=3, category_sid1="101", keywords=None):
    url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={category_sid1}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select("a[href*='/article/']")

    articles = []
    seen = set()

    # print(f"[DEBUG] category_sid1={category_sid1}, keywords={keywords}")
    # print(f"[DEBUG] Found {len(links)} raw links on page")
    # print(f"[DEBUG] Collected {len(articles)} articles after filtering")

    for link_tag in links:
        title = link_tag.get_text(strip=True)
        link = link_tag["href"]

        if link in seen or not title or not link:
            continue
        seen.add(link)

        content = get_article_content(link)

        # 🎯 키워드 필터링
        if keywords and not any(k in content for k in keywords):
            continue

        if len(content.split()) < 30:
            continue

        articles.append({
            "title": title,
            "link": link,
            "content": content
        })

        if len(articles) >= limit:
            break

    return articles


def get_article_content(url):
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # 뉴스 본문 파싱
        article_tag = soup.select_one("article")
        if article_tag:
            return article_tag.get_text(separator=" ", strip=True)

        # 만약 <article> 태그가 없으면 예외적으로 다른 방법 시도
        div_tag = soup.select_one("div#newsct_article")  # 모바일 네이버 뉴스
        if div_tag:
            return div_tag.get_text(separator=" ", strip=True)

        return "[본문 없음]"
    except Exception as e:
        return f"[본문 로딩 실패: {e}]"
