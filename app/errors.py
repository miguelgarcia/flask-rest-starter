from flask import current_app, jsonify, request


class ApiException(Exception):
    def __init__(self, message='Internal error', status_code=400, code="INTERNAL_ERROR"):
        self.message = message
        self.code = code
        self.status_code = status_code

    def __repr__(self):
        return 'ApiException: %s %s' % (self.code, self.message)

    def __str__(self):
        return 'ApiException: %s %s' % (self.code, self.message)


class NotFoundException(ApiException):
    def __init__(self, message='Not found', code="NOT_FOUND"):
        super().__init__(message, 404, code)


def api_exception_handler(e):
    current_app.logger.error([request.url, e, request.args, request.data])
    return jsonify(dict(
        code=e.code,
        message=e.message
    )), e.status_code
