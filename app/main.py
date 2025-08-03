from flask import Flask, request, jsonify, redirect
from app.storage import URLStorage
from app.shortener import generate_short_code, is_valid_url

app = Flask(__name__)
storage = URLStorage()

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the URL Shortener API",
        "endpoints": {
            "shorten": "POST /api/shorten",
            "redirect": "GET /<short_code>",
            "stats": "GET /api/stats/<short_code>"
        }
    })

@app.route('/api/shorten', methods=['GET', 'POST'])
def shorten_url():
    if request.method == 'GET':
        return jsonify({
            'message': 'This endpoint only accepts POST requests with a JSON body: {"url": "<your-url>"}'
        }), 405

    data = request.get_json()
    url = data.get('url')

    if not url or not is_valid_url(url):
        return jsonify({'error': 'Invalid URL'}), 400

    short_code = generate_short_code()
    storage.save(short_code, url)

    return jsonify({
        'short_code': short_code,
        'short_url': f"http://localhost:5000/{short_code}"
    }), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    entry = storage.get(short_code)
    if not entry:
        return jsonify({'error': 'Short URL not found'}), 404

    storage.increment_click(short_code)
    return redirect(entry['url'])

@app.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    entry = storage.get(short_code)
    if not entry:
        return jsonify({'error': 'Short URL not found'}), 404

    return jsonify({
        'url': entry['url'],
        'clicks': entry['clicks'],
        'created_at': entry['created_at']
    })

if __name__ == '__main__':
    app.run(debug=True)
