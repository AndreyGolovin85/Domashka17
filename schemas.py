from marshmallow import Schema, fields


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Str()
    director = fields.Str()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()
