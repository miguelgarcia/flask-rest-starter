from marshmallow import Schema as _Schema, fields, validate

class Schema(_Schema):
    @staticmethod
    def toObject(data, object):
        for k in data:
            object.__setattr__(k, data[k])