import os
from typing import List

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://catan:secretpassword@db:5432/catan_db')

def get_cors_origins() -> List[str]:
    raw = os.environ.get('CORS_ORIGINS')
    if not raw:
        return ["*"]
    return [o.strip() for o in raw.split(',') if o.strip()]
