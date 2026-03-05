# FreshCart Entry Page

## Setup
1. Install [Node.js](https://nodejs.org/) (v18+)
2. Run `npm install` in the project root
3. Run `npm run build` to generate the `dist/` folder
4. Serve the `dist/` folder from your Python backend as static files

## Python Integration (Flask example)
```python
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='dist', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('dist', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('dist', path)
```

## Python Integration (Django example)
In `urls.py`:
```python
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
]
```
Copy `dist/` contents into your Django static/templates folders.

## Files Overview
- `index.html` — Entry HTML
- `src/pages/Index.tsx` — Main animated page component
- `src/index.css` — Theme & design tokens
- `src/assets/hero-groceries.jpg` — Background image
- `tailwind.config.ts` — Tailwind configuration
- `src/App.tsx` — App router
- `src/main.tsx` — React entry point

## Customization
- Change store name in `src/pages/Index.tsx` (line ~102)
- Update CTA link `href="/store"` to your store URL
- Modify colors in `src/index.css` `:root` block
