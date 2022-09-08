class BasedView(Resource):
    def get(self):
        director_key = request.args.get("director_id")
        genre_key = request.args.get("genre_id")
        if not director_key and not genre_key:
            all_movies = db.session.query(Movie).all()
            return movies_schema.dump(all_movies), 200
        elif not genre_key:
            result = db.session.query(Movie).filter(Movie.director_id == int(director_key)).all()
            if result:
                return movies_schema.dump(result), 200
            else:
                return '', 404

        elif not director_key:
            result = db.session.query(Movie).filter(Movie.genre_id == int(genre_key)).all()
            if result:
                return movies_schema.dump(result), 200
            else:
                return '', 404