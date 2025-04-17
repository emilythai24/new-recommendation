# News Recommender

This project is a Flask-based web application that provides users with relevant, diverse, and trustworthy news articles. It uses the NewsAPI to fetch real-time news and incorporates a ranking algorithm based on Maximal Marginal Relevance (MMR) to ensure a balanced selection of content.

## Features

- Search for news articles by keyword or interest
- Ranks articles using a combination of relevance and diversity (MMR)
- Displays political bias (left, center, right) of each source
- Displays trustworthiness scores from precomputed mappings
- Clean and responsive frontend with color-coded trust indicators
- Loading animation with status message

## Technology Stack

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Data Source: NewsAPI.org
- Ranking: scikit-learn TF-IDF + cosine similarity

## Directory Structure

news_recommendation/ ├── app.py ├── templates/ │ └── index.html ├── static/ │ ├── script.js │ └── styles.css (optional) ├── bias_labels.json ├── trust_scores.json ├── .gitignore ├── README.md └── requirements.txt

## Inspiration

This project was inspired by the goals and principles of [DiversiNews](https://dl.acm.org/doi/abs/10.14778/3685800.3685854), a research-driven platform that aimed to promote diverse perspectives in news consumption. DiversiNews introduced the idea of enhancing traditional news search with diversity-aware ranking, allowing users to explore multiple viewpoints and reduce exposure to bias and filter bubbles. 

The News Recommender app builds on this concept by incorporating a Maximal Marginal Relevance (MMR) algorithm to balance relevance with source diversity, while also labeling each article with a political bias and trust score to empower more informed and critical news reading.


