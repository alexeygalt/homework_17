from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from create_data import Movie, Director, Genre
from serializations import movies_schema, movie_schema, director_schema, directors_schema, genres_schema, genre_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}
db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_key = request.args.get("director_id")
        genre_key = request.args.get("genre_id")
        if director_key and genre_key:
            result = db.session.query(Movie).filter(Movie.director_id == int(director_key) and
                                                    Movie.genre_id == int(genre_key)).all()
        elif director_key:
            result = db.session.query(Movie).filter(Movie.director_id == int(director_key)).all()

        elif genre_key:
            result = db.session.query(Movie).filter(Movie.genre_id == int(genre_key)).all()

        else:
            result = db.session.query(Movie).all()
        if result:
            return movies_schema.dump(result), 200
        else:
            return jsonify({"ValueError": "id not found"})

    def post(self):
        upload_date = request.get_json()
        new_movie = Movie(**upload_date)
        db.session.add(new_movie)
        db.session.commit()
        return movie_schema.dump(new_movie)


@movie_ns.route('/<int:mid>')
class MoviesView(Resource):
    def get(self, mid):

        movie = db.session.query(Movie).get(mid)
        if not movie:
            return jsonify({"ValueError": 'Movie_id not found'})
        return movie_schema.dump(movie)

    def put(self, mid):
        movie = db.session.query(Movie).get(mid)
        if not movie:
            return jsonify({"ValueError": 'Movie_id not found'})
        update_date = request.get_json()
        movie.title = update_date.get('title')
        movie.description = update_date.get('description')
        movie.trailer = update_date.get('trailer')
        movie.year = update_date.get('year')
        movie.rating = update_date.get('rating')
        movie.genre_id = update_date.get('genre_id')
        movie.director_id = update_date.get('director_id')
        db.session.add(movie)
        db.session.commit()
        return movie_schema.dump(movie)

    def delete(self, mid):
        movie = db.session.query(Movie).get(mid)
        if not movie:
            return jsonify({"ValueError": 'Movie_id not found'})

        db.session.delete(movie)
        db.session.commit()
        return "", 204


@directors_ns.route('/')
class DirectorView(Resource):
    def get(self):
        all_directors = db.session.query(Director).all()
        return directors_schema.dump(all_directors), 200

    def post(self):
        upload_date = request.get_json()
        new_director = Director(
            name=upload_date.get('name')
        )
        db.session.add(new_director)
        db.session.commit()
        return director_schema.dump(new_director)


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        director = db.session.query(Director).get(did)
        if not director:
            return jsonify({"ValueError": 'Director_id not found'})
        return director_schema.dump(director)

    def put(self, did):
        director = db.session.query(Director).get(did)
        if not director:
            return jsonify({"ValueError": 'Director_id not found'})
        upload_date = request.get_json()
        director.name = upload_date.get('name')
        db.session.add(director)
        db.session.commit()
        return director_schema.dump(director)

    def delete(self, did):
        director = db.session.query(Director).get(did)
        if not director:
            return jsonify({"ValueError": 'Director_id not found'})
        db.session.delete(director)
        db.session.commit()
        return "", 204


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = db.session.query(Genre).all()
        return genres_schema.dump(all_genres), 200

    def post(self):
        update_date = request.get_json()
        new_genre = Genre(name=update_date.get('name'))
        db.session.add(new_genre)
        db.session.commit()
        return genre_schema.dump(new_genre), 200


@genres_ns.route('/<int:gid>')
class GenresView(Resource):
    def get(self, gid):
        genre = db.session.query(Genre).get(gid)
        if not genre:
            return jsonify({"ValueError": 'Genre_id not found'})
        return genre_schema.dump(genre), 200

    def put(self, gid):
        genre = db.session.query(Genre).get(gid)
        if not genre:
            return jsonify({"ValueError": 'Genre_id not found'})
        upload_date = request.get_json()
        genre.name = upload_date.get('name')
        db.session.add(genre)
        db.session.commit()
        return genre_schema.dump(genre)

    def delete(self, gid):
        genre = db.session.query(Genre).get(gid)
        if not genre:
            return jsonify({"ValueError": 'Genre_id not found'})
        db.session.delete(genre)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
