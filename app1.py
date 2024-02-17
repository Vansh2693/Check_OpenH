import requests
from flask import Flask, jsonify
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

def search_articles(query, num_results=10):

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

            sum_url = "https://meaningcloud-summarization-v1.p.rapidapi.com/summarization-1.0"

            querystring = {"sentences":"5","url":{article_url}}

            headers = {
                "Accept": "application/json",
                "X-RapidAPI-Key": "c592668a06msh43c05340d9a7e86p140c20jsn98013aebf9f8",
                "X-RapidAPI-Host": "meaningcloud-summarization-v1.p.rapidapi.com"
            }

            respons = requests.get(sum_url, headers=headers, params=querystring)
            
            articles.append({'title': article_title, 'url': article_url, 'summary':respons.json()})  # Append each article to the list
            




        return articles  # Return the list of articles
    else:
        return None  # Return None if request failed

@app.route('/api/<string:param>', methods=['GET'])
def get_request(param):
    articles = search_articles(param)
    if articles:
        response = {
            'articles': articles
        }
    else:
        response = {
            'message': 'Failed to fetch search results.'
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
