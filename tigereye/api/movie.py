# coding=utf-8

from flask import request
from tigereye.api import ApiView
from tigereye.models.movie import Movie
from tigereye.extensions.validator import Validator


class MovieView(ApiView):

    def all(self):
        movies = list(Movie.query.all())
        return movies

    @Validator(mid=int)
    def get(self):
        mid = request.params['mid']
        movie = Movie.get(mid)
        return movie
