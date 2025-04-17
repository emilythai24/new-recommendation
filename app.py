from flask import Flask, render_template, request, jsonify
import requests
import json
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from urllib.parse import urlparse, urlunparse


def clean_url(raw_url):
    parsed = urlparse(raw_url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))  # no query or fragment


app = Flask(__name__)

NEWS_API_KEY = "65494528a6a54a618f13dd2865a1034e"
NEWS_API_URL = "https://newsapi.org/v2/everything"
BIAS_MAP = json.load(open("bias_labels.json"))
TRUST_MAP = json.load(open("trust_scores.json"))


def classify_bias(url):
    domain = urlparse(url).netloc.replace("www.", "")
    return BIAS_MAP.get(domain, "unknown")


def get_trust_score(url):
    domain = urlparse(url).netloc.replace("www.", "")
    return TRUST_MAP.get(domain, 0.5)


def fetch_articles(query):
    params = {
        "q": query,
        "pageSize": 30,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "relevancy"
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code != 200:
        return []
    return response.json().get("articles", [])


def mmr_ranking(articles, query, lambda_diversity=0.5, top_n=5):
    texts = [a["title"] + " " + a["description"] for a in articles]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([query] + texts)

    sim_query = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    sim_items = cosine_similarity(tfidf[1:])

    selected = []
    candidates = list(range(len(articles)))

    while len(selected) < min(top_n, len(candidates)):
        if not selected:
            idx = sim_query.argmax()
        else:
            diversity_penalty = max(cosine_similarity(tfidf[selected[-1] + 1], tfidf[i + 1])[0][0] for i in candidates)
            idx = max(
                candidates,
                key=lambda i: lambda_diversity * sim_query[i] - (1 - lambda_diversity) * diversity_penalty
            )
        selected.append(idx)
        candidates.remove(idx)

    return [articles[i] for i in selected]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    interest = request.json.get("interest", "").lower()
    raw_articles = fetch_articles(interest)

    seen_urls = set()
    articles = []

    for a in raw_articles:
        if not a["title"] or not a["description"] or not a["url"]:
            continue

        url = clean_url(a["url"])
        if url in seen_urls:
            continue  # Skip duplicate

        seen_urls.add(url)
        domain = urlparse(url).netloc.replace("www.", "")

        articles.append({
            "title": a["title"],
            "description": a["description"],
            "url": a["url"],  # keep original URL to show on frontend
            "bias": BIAS_MAP.get(domain, "unknown"),
            "trust_score": round(TRUST_MAP.get(domain, 0.5), 2)
        })

    # Rank using Maximal Marginal Relevance (MMR)
    ranked = mmr_ranking(articles, interest)
    return jsonify(ranked)


if __name__ == "__main__":
    app.run(debug=True)
