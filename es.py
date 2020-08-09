from elasticsearch import Elasticsearch

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
es.search(
    index='ptt_board_test',
    body=doc
)

# FLASK MYSQL LIKE QUERY
# cur = mysql.connection.cursor()
# cur.execute(
#     'SELECT * FROM ptt_data.ptt_content WHERE content LIKE %s LIMIT 10', ("%{}%".format(
#         keyword),))
# result = cur.fetchall()
