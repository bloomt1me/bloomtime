import requests
from datetime import datetime

# ===================== Configuration =====================
API_KEY = "bc2d19470c084033a1ac0e9e26fc0030"
BASE_URL = "https://newsapi.org/v2/everything"
QUERY = "technology"
# =========================================================

def get_news():
    """Fetch news data from NewsAPI"""
    params = {
        "q": QUERY,
        "apiKey": API_KEY,
        "language": "en",
        "pageSize": 8,
        "sortBy": "publishedAt"
    }
    
    try:
        print("🌐 Connecting to NewsAPI...")
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "ok":
            print(f"❌ API Error: {data.get('message', 'Unknown error')}")
            return None
        return data
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def show_news(data):
    """Display news articles"""
    if not data or "articles" not in data:
        print("No news data available")
        return
    
    articles = data["articles"]
    total = data.get("totalResults", 0)
    
    print("\n" + "=" * 70)
    print(f"🔍 Keyword: {QUERY}")
    print(f"📊 Found {total} articles (showing top {len(articles)})")
    print("=" * 70)
    
    for i, news in enumerate(articles, 1):
        print(f"\n📰 【News {i}】")
        print("-" * 50)
        
        # 1. Title
        print(f"Title: {news.get('title', 'N/A')}")
        
        # 2. Source
        source = news.get('source', {})
        print(f"Source: {source.get('name', 'Unknown')}")
        
        # 3. Author
        if news.get('author'):
            print(f"Author: {news.get('author')}")
        
        # 4. Time
        time_str = news.get('publishedAt', '')
        if time_str:
            time_str = time_str.replace('T', ' ').replace('Z', '')[:16]
            print(f"Time: {time_str}")
        
        # 5. Description
        desc = news.get('description', '')
        if desc:
            if len(desc) > 60:
                desc = desc[:60] + '...'
            print(f"Description: {desc}")
        
        # 6. Content
        content = news.get('content', '')
        if content:
            if len(content) > 50:
                content = content[:50] + '...'
            print(f"Content: {content}")
        
        # 7. URL
        print(f"URL: {news.get('url', 'N/A')}")

def main():
    print("=" * 70)
    print("  Lab Work №7 — NewsAPI News Query")
    print("=" * 70)
    
    news_data = get_news()
    show_news(news_data)
    
    print("\n" + "=" * 70)
    print("✅ Program completed")

if __name__ == "__main__":
    main()