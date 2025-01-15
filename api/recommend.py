from flask import Flask, send_file, Blueprint
import os
from operator import itemgetter
from .search import items

app = Flask(__name__)

# Insert where items are collected
def grab_rec(value):
    lst = sorted(value, key=lambda x: itemgetter('all')(x['tags']))
    result = []
    for i in range(len(lst)):
        result.append(lst[i])
    return result

# Sample items data (replace with actual data)
ritems = grab_rec(items)

markdown_data = f"""
# Recommended Items

- **[{ritems[1]['name']}]({ritems[1]['link']})**:
"""

print(markdown_data)

@app.route('/tri2/socialmedia_frontend/navigation/recommended.md')
def recommended_md():
    return markdown_data

@app.route('/templates/index.html')
def index_html():
    return send_file(os.path.join(os.path.dirname(__file__), 'index.html'))

@app.route('/api/search.py')
def search_py():
    return send_file(os.path.join(os.path.dirname(__file__), 'search.py'))

recommend_api = Blueprint('recommend_api', __name__)

if __name__ == '__main__':
    PORT = 8887
    app.run(host='0.0.0.0', port=PORT)
    print(f"Server is running at http://localhost:{PORT}")
