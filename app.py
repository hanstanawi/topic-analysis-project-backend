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

# Get latest articles
@app.route('/api/articles', methods=['GET'])
def getAllArticles():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM ptt_data.ptt_content ORDER BY tp DESC LIMIT 5')
    result = cur.fetchall()
    return jsonify(result)

# Get single article
@app.route('/api/article', methods=['GET'])
@cross_origin()
def getArticleById():
    articleId = request.args.get('articleId')
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM ptt_data.ptt_content WHERE url = %s', [articleId])
    result = cur.fetchone()
    return jsonify(result)

# Search for correlated articles
@app.route('/api/search', methods=['GET'])
def searchTopics():
    keyword = request.args.get('keyword')
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM ptt_data.ptt_content WHERE content LIKE %s LIMIT 10', ("%{}%".format(
            keyword),))
    result = cur.fetchall()
    return jsonify(result)


doc = {
    'query': {
        'bool': {
            'must': {
                'match': {
                    'board': 'Gossiping'
                }
            },
            'must_not': {
                'match': {
                    'board': 'Nba'
                }
            }
        }
    }
}
# Elasticsearch search index
print(es.search(
    index='ptt_board_test',
    body=doc
)
)
if __name__ == '__main__':
    app.run(debug=True)
