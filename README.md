# 🔗 URL Shortener API

A simple Flask-based URL Shortener that allows users to shorten long URLs, redirect using short codes, and view click statistics.

## 🚀 Features

- Shorten long URLs to short codes.
- Redirect to the original URL using the short code.
- Track number of times a short URL has been accessed.
- View metadata like creation date and click count.

---

## 📦 API Endpoints

| Purpose          | Method | Endpoint                      | Description                                    |
|------------------|--------|-------------------------------|------------------------------------------------|
| Welcome          | GET    | `/`                           | API welcome message and route info             |
| Shorten URL      | POST   | `/api/shorten`                | Submit a long URL and receive a short code     |
| Redirect URL     | GET    | `/<short_code>`               | Redirects to the original long URL             |
| Get Stats        | GET    | `/api/stats/<short_code>`     | View click count and creation time             |

---

## 📥 Request/Response Examples

### POST `/api/shorten`

**Request:**
```json
{
  "url": "https://www.wikipedia.org"
}
