from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'topic_analysis'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MySQL
mysql = MySQL(app)
CORS(app)

# Get all the articles
@app.route('/api/articles', methods=['GET'])
def getAllArticles():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM topic_analysis.articles')
    result = cur.fetchall()
    return jsonify(result)

# Get single article
@app.route('/api/article', methods=['GET'])
def getArticleById():
    articleId = request.args.get('articleId')
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM topic_analysis.articles WHERE id = %s', articleId)
    result = cur.fetchone()
    return jsonify(result)

# Search for correlated articles
@app.route('/api/search', methods=['GET'])
def searchTopics():
    keyword = request.args.get('keyword')
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM topic_analysis.articles WHERE content LIKE %s', ("%{}%".format(
            keyword),))
    result = cur.fetchall()
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
