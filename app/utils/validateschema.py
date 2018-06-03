from flask import request
from functools import wraps

class SchemaViolationException(Exception):
    def __init__(self, error, status_code=400):
        self.error = error
        self.status_code = status_code

    def __repr__(self):
        return 'SchemaViolationException: %s' % self.error

    def __str__(self):
        return '%s' % (self.error)


def output(schema_class, *args_ma, **kw_ma):
    """ Checks that request.get_json() satisfies marshmallow schema: schema_class()
        On error SchemaViolationException is raised.
        On success the decorated function is called with the kword argument
        `data` containing the loaded schema_class
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            out = f(*args, **kw)
            schema = schema_class(*args_ma, **kw_ma)
            if isinstance(out, tuple):
                val = out[0]
                code = 200
                headers = dict()
                if len(out) > 1:
                    code = out[1]
                if len(out) > 2:
                    headers = out[2]
                return schema.dump(val).data, code, headers
            else:
                return schema.dump(out).data
        return wrapper
    return decorator

def inputbody(schema_class, *args_ma, **kw_ma):
    """ Checks that request.get_json() satisfies marshmallow schema: schema_class()
        On error SchemaViolationException is raised.
        On success the decorated function is called with the kword argument
        `data` containing the loaded schema_class
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            data, errors = schema_class(*args_ma, **kw_ma).load(request.get_json())
            if(len(errors) > 0):
                msg = ''
                for x in errors:
                    msg += x + ":"
                    for d in errors[x]:
                        msg += " " + str(d)
                    msg += '\n'
                raise SchemaViolationException('Schema violation:' + msg.strip())
            return f(*args, data=data, **kw)
        return wrapper
    return decorator

def qsargs(schema_class, *args_ma, **kw_ma):
    """ Checks that request.args satisfies marshmallow schema: schema_class()
        On error SchemaViolationException is raised.
        On success the decorated function is called with the kword argument
        `data` containing the loaded schema_class
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            data, errors = schema_class(*args_ma, **kw_ma).load(request.args)
            if(len(errors) > 0):
                msg = ''
                for x in errors:
                    msg += x + ":"
                    for d in errors[x]:
                        msg += " " + str(d)
                    msg += '\n'
                raise SchemaViolationException('Schema violation:' + msg.strip())
            return f(*args, data, **kw)
        return wrapper
    return decorator

def load_and_validate_schema(schema_class, instance):
    data, errors = schema_class().load(request.get_json(), instance=instance)
    if(len(errors) > 0):
        msg = ''
        for x in errors:
            msg += x + ":"
            for d in errors[x]:
                msg += " " + str(d)
            msg += '\n'
        raise SchemaViolationException('Schema violation:' + msg.strip())
    return data
