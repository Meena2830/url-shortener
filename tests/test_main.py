import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test 1: Shorten a valid URL
def test_shorten_url(client):
    res = client.post('/api/shorten', json={'url': 'https://example.com'})
    assert res.status_code == 201
    data = res.get_json()
    assert 'short_code' in data
    assert data['short_code']
    assert 'short_url' in data

# Test 2: Redirect using the short code
def test_redirect_url(client):
    res = client.post('/api/shorten', json={'url': 'https://example.com'})
    short_code = res.get_json()['short_code']
    res = client.get(f'/{short_code}', follow_redirects=False)
    assert res.status_code == 302
    assert res.headers['Location'] == 'https://example.com'

# Test 3: Fetch stats after redirection
def test_stats(client):
    res = client.post('/api/shorten', json={'url': 'https://www.wikipedia.org'})
    short_code = res.get_json()['short_code']
    client.get(f'/{short_code}')  # simulate click
    res = client.get(f'/api/stats/{short_code}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['url'] == 'https://www.wikipedia.org'
    assert data['clicks'] >= 1
    assert 'created_at' in data

# Test 4: Invalid URL should return 400
def test_invalid_url(client):
    res = client.post('/api/shorten', json={'url': 'not-a-url'})
    assert res.status_code == 400
    data = res.get_json()
    assert 'error' in data

# Test 5: Accessing non-existent short code should return 404
def test_404_redirect(client):
    res = client.get('/nonexistent123')
    assert res.status_code == 404
    data = res.get_json()
    assert 'error' in data
