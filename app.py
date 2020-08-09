from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Config Elasticsearch
es = Elasticsearch('http://140.128.102.112:9200')

# Config MySQL
app.config['MYSQL_HOST'] = '140.128.102.106'
app.config['MYSQL_USER'] = 'moris'
app.config['MYSQL_PASSWORD'] = 'moris123'
app.config['MYSQL_DB'] = 'ptt_data'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MySQL
mysql = MySQL(app)
CORS(app, support_credentials=True)

# Get certain amount of latest articles (MySQL)
@app.route('/api/articles', methods=['GET'])
def getAllArticles():
    limit = request.args.get('limit', type=int)
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM ptt_data.ptt_content ORDER BY tp DESC LIMIT %s', [limit])
    result = cur.fetchall()
    return jsonify(result)

# Get a single article (MySQL)
@app.route('/api/article', methods=['GET'])
def getArticleById():
    articleId = request.args.get('articleId')
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM ptt_data.ptt_content WHERE url = %s', [articleId])
    result = cur.fetchone()
    return jsonify(result)

# Keyword search for correlated articles (Elasticsearch)
@app.route('/api/keyword-search', methods=['GET'])
def keywordSearch():
    keyword = request.args.get('keyword')
    doc = {
        'query': {
            'multi_match': {
                'query': keyword,
                'fields': ['title', 'content']
            }
        }
    }
    result = es.search(index='ptt', body=doc)
    return jsonify(result['hits']['hits'])

# Article/long-text search for correlated articles (Elasticsearch)
@app.route('/api/text-search', methods=['GET'])
def textSearch():
    text = request.args.get('text')
    doc = {
        'query': {
            'match': {
                'content': text
            }
        }
    }
    result = es.search(index='ptt', body=doc)
    return jsonify(result['hits']['hits'])


if __name__ == '__main__':
    app.run(debug=True)
