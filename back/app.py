from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

db_config = {
    'host': '10.32.176.36',
    'user': 'site',
    'password': '123456',
    'database': 'movie_db',
    'charset': 'utf8mb4'
}


def get_db_connection():
    return pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)


@app.route('/api/movies')
def get_movies():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    search = request.args.get('search', '')
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute("SELECT * FROM movies WHERE title LIKE %s LIMIT %s OFFSET %s",
                       ('%' + search + '%', per_page, offset))
        cursor_total = conn.cursor()
        cursor_total.execute("SELECT COUNT(*) AS total FROM movies WHERE title LIKE %s", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM movies LIMIT %s OFFSET %s", (per_page, offset))
        cursor_total = conn.cursor()
        cursor_total.execute("SELECT COUNT(*) AS total FROM movies")

    movies = cursor.fetchall()
    total = cursor_total.fetchone()['total']
    conn.close()
    return jsonify({'movies': movies, 'total': total})


@app.route('/api/movie/<title>')
def get_movie(title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE title = %s", (title,))
    movie = cursor.fetchone()
    conn.close()
    if not movie:
        return jsonify({'message': 'Movie not found'}), 404
    return jsonify(movie)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
