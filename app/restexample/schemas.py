from app.utils.schema import Schema, fields, validate


class ListArgsSchema(Schema):
    limit = fields.Integer(required=False, validate=[
                           validate.Range(1, 100)], missing=100)
    offset = fields.Integer(required=False, validate=[
                            validate.Range(0)], missing=0)


class CountrySchema(Schema):
    code = fields.String(required=True, validate=[validate.Length(max=255)])
    name = fields.String(required=True, validate=[validate.Length(max=255)])

