
from app.database.database import get_connection

class MovieService:

    @staticmethod
    def add_movie(title, genre, rating, watched):
        conn = get_connection()
        conn.execute(
            'INSERT INTO movies(title, genre, rating, watched) VALUES(?,?,?,?)',
            (title, genre, rating, int(watched))
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_movies(search=''):
        conn = get_connection()
        rows = conn.execute(
            'SELECT * FROM movies WHERE title LIKE ? ORDER BY rating DESC',
            (f'%{search}%',)
        ).fetchall()
        conn.close()
        return rows

    @staticmethod
    def delete_movie(movie_id):
        conn = get_connection()
        conn.execute('DELETE FROM movies WHERE id=?', (movie_id,))
        conn.commit()
        conn.close()
