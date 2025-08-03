import datetime
from datetime import datetime, timezone


class URLStorage:
    def __init__(self):
        self.db = {}

    def save(self, short_code, url):
        self.db[short_code] = {
            'url': url,
            'clicks': 0,
            'created_at': datetime.now(timezone.utc).isoformat()
        }

    def get(self, short_code):
        return self.db.get(short_code)

    def increment_click(self, short_code):
        if short_code in self.db:
            self.db[short_code]['clicks'] += 1
