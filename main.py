from flask import Flask, request, jsonify
from flask_restx import Api, Resource
import os

from models_db import *
from schemas import MovieSchema

DATABASE = os.path.join("data/database.db")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

api = Api(app)
movie_ns = api.namespace("movies")


@movie_ns.route("/")
class MoviesView(Resource):
    """
    Класс для обработки запросов в базу.
    """
    def get(self) -> list:
        """
        Функция для вывода всех фильмов в базе.
        :return: list
        """
        movies_genre_and_director = db.session.query(Movie.id, Movie.title, Movie.year, Movie.description, Movie.rating,
                                                     Movie.trailer, Genre.name.label("genre"),
                                                     Director.name.label("director")).join(Genre).join(Director)

        if "director_id" in request.args:
            did = request.args.get("director_id")
            movies_genre_and_director = movies_genre_and_director.filter(Movie.director_id == did)

        if "genre_id" in request.args:
            did = request.args.get("genre_id")
            movies_genre_and_director = movies_genre_and_director.filter(Movie.director_id == did)

        movies_all = movies_genre_and_director.all()
        return jsonify(movies_schema.dump(movies_all))

    def post(self) -> str:
        """
        Функция для добавления фильма в базу.
        :return: str
        """
        request_json = request.json
        movie_new = Movie(**request_json)
        with db.session.begin():
            db.session.add(movie_new)

        return f"Объект с id {movie_new.id} добавлен в базу!", 201


@movie_ns.route("/<int:movie_id>")
class MovieView(Resource):
    """
    Класс для обработки запросов в базу.
    """
    def get(self, movie_id: int):
        """
        Функция принимает значение movie_id, целое число и возращает фильм с указанным id.
        Если такого фильма нет сообщает об этом.
        :param movie_id: int
        :return: list or str
        """
        movie = db.session.query(Movie).get(movie_id)
        if movie:
            return jsonify(movie_schema.dump(movie))
        return "Нет фильма с таким id", 404

    def put(self, movie_id) -> str:
        """
        Функция принимает значение movie_id, целое число и обновляет фильм с указанным id.
        Если такого фильма нет сообщает об этом.
        :param movie_id: int
        :return: str
        """
        movie = db.session.query(Movie).get(movie_id)
        if not movie:
            return "Нет фильма с таким id", 404

        request_json = request.json
        movie.title = request_json["title"]
        movie.description = request_json["description"]
        movie.trailer = request_json["trailer"]
        movie.year = request_json["year"]
        movie.rating = request_json["rating"]
        movie.genre_id = request_json["genre_id"]
        movie.director_id = request_json["director_id"]
        db.session.add(movie)
        db.session.commit()
        return f"Фильм с id {movie_id} обновлен в базе!", 204

    def delete(self, movie_id) -> str:
        """
        Функция принимает значение movie_id, целое число и удаляет фильм с указанным id.
        Если такого фильма нет сообщает об этом.
        :param movie_id: int
        :return: str
        """
        movie = db.session.query(Movie).get(movie_id)
        if not movie:
            return "Нет фильма с таким id", 404
        db.session.delete(movie)
        db.session.commit()
        return f"Фильм с id {movie_id} удален из базы!", 204


if __name__ == "__main__":
    app.run(port=2060)
