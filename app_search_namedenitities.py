import spacy
import requests
from flask import Flask, jsonify
from newspaper import Article, ArticleException

nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

def extract_named_entities(text):
    doc = nlp(text)
    return list(set(ent.text for ent in doc.ents))

def search_articles_by_entities(entities, num_results=10):
    # Combine named entities into a single query string
    query = ' '.join(entities)

    api_key = "AIzaSyDdgsglrtocaYOcA8V1s4Ad0Te9bsAwIYs"
    search_engine_id = "d5e0315085b194afb"

    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&num={num_results}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])

        articles = []  # Store articles in a list
        for item in items:
            article_title = item.get('title')
            article_url = item.get('link')
            try:
                article = Article(article_url)
                article.download()
                article.parse()
                article.nlp()

                articles.append({
                    'title': article_title,
                    'url': article_url,
                    'summary': article.summary.replace("\n", "")
                })
            except ArticleException as e:
                print(f"Failed to process article: {article_url}. Error: {e}")
                continue

        return articles  # Return the list of articles
    else:
        return None  # Return None if request failed

@app.route('/api/<string:param>', methods=['GET'])
def get_request(param):
    named_entities = extract_named_entities(param)
    
    if named_entities:
        articles = search_articles_by_entities(named_entities)
        if articles:
            response = {
                'articles': articles
            }
        else:
            response = {
                'message': 'Failed to fetch search results.'
            }
    else:
        response = {
            'message': 'No named entities found in the input.'
        }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
